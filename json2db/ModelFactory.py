# -*- coding:utf-8 -*-
import warnings
import json
import re
from datetime import datetime
from typing import Optional, Union, List, Dict, Any, Tuple
from sqlalchemy import (String, Text, Integer, BigInteger, Float,
                        DECIMAL, SmallInteger, DateTime, Boolean, Column,
                        ForeignKey, create_engine)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.types import TypeEngine
from sqlalchemy.sql.visitors import VisitableType
from sqlalchemy.ext.declarative import declarative_base

from .core import JModel, Factory, ColumnFormat, FrameworkNotSupport, ParseDataError
from . import config
from .types import NAME_TYPE, TYPE_NAME, PYTHON_TYPE_NAME, DBType
from .converter import converter
import attr


@attr.s(auto_attribs=True)
class NodeField:
    name: str = attr.ib()
    column: str = attr.ib()
    alias: Optional[str] = None
    real_type: Optional[str] = None
    db_type: Optional[str] = None
    comment: Optional[str] = None
    nullable: bool = True
    default: Optional[Any] = None
    unique: Optional[bool] = None


@attr.s(auto_attribs=True)
class RootModel:
    name: str = attr.ib()
    alias: Optional[str] = None
    table_name: Optional[str] = None
    comment: Optional[str] = None
    fields: Dict[str, NodeField] = attr.Factory(dict)
    brothers: Dict[str, Any] = attr.Factory(dict)
    sons: Dict[str, Any] = attr.Factory(dict)


class CommonModelFactory(Factory):
    def __init__(self, *args, default_db_url: Optional[str] = None,
                 database: str = 'default',
                 primary_key: str = 'id',
                 primary_type: Union[TypeEngine, VisitableType] = Integer,
                 column_fmt: str = ColumnFormat.DEFAULT,
                 foreignkey_suffix: str = 'id',
                 use_foreign_key: bool = False,
                 ignore_head: str = ':',
                 add_time_col: bool = True,
                 time_col_name: str = 'gmt_create',
                 table_args: Optional[Dict] = None,
                 is_echo: bool = False,
                 str2col: Union[TypeEngine, VisitableType, str] = 'Text',
                 int2col: Union[TypeEngine, VisitableType, str] = 'Integer',
                 float2col: Union[TypeEngine, VisitableType, str] = 'Float',
                 bool2col: Union[TypeEngine, VisitableType, str] = 'Boolean',
                 date2col: Union[TypeEngine, VisitableType, str] = 'DateTime', **kwargs):
        """

        :param args:
        :param kwargs: See more in  CommonModel
        """
        self.default_db_url = config.DEFAULT_DB_URL if default_db_url is None else default_db_url
        self.fmt = ColumnFormat(column_fmt)
        self.primary_key = primary_key
        self.primary_type = primary_type
        self.foreignkey_suffix = foreignkey_suffix
        self.add_time_col = add_time_col
        self.time_col_name = self.fmt.rename(time_col_name)
        self.table_args = {} if table_args is None else table_args
        self.use_foreign_key = use_foreign_key
        self.is_echo = is_echo
        self.type_map = {
            str: str2col,
            int: int2col,
            bool: bool2col,
            float: float2col,
            datetime: date2col

        }
        self.ignore_head = ignore_head
        self.args = args
        self.kwargs = kwargs
        self.type_helper = DBType(database)

    def _build_models(self, root: RootModel) -> JModel:
        if self.add_time_col and self.time_col_name in root.fields:
            warnings.warn(
                f"In table {root.name} field {self.time_col_name} is same as the default timestamp key,"
                f" please delete it or use other key as time_col_name")

        return CommonModel(*self.args, model=root, factory=self, **self.kwargs)

    ALIAS_PATTERN = re.compile(r"<<([\w_.]+)")

    def get_alias(self, s: str) -> Optional[str]:
        """If something like `<<some`
        this field  alias is some

        :param s:
        :return:
        """
        alias = self.ALIAS_PATTERN.findall(s)
        if alias:
            return alias[0]

    def add_field(self, k: str, v: Any, comment: Optional[str] = None) -> NodeField:
        node = NodeField(name=k, column=self.fmt.rename(k))
        if comment:
            node.comment = comment
            alias = self.get_alias(comment)
            if alias:
                node.alias = alias
        else:
            # add value as part of comment
            node.comment = f"eg: {v}"

        node.real_type = TYPE_NAME[type(v)]
        convert_type = self.type_map[type(v)]
        if isinstance(convert_type, str):
            # Do a test
            if convert_type == 'Boolean':
                print(convert_type)
            self.type_helper.get_column(convert_type)
            node.db_type = convert_type
        elif isinstance(convert_type, VisitableType):
            node.db_type = self.type_helper.get_name(convert_type)
        else:
            assert isinstance(convert_type, TypeEngine)
            node.db_type = str(convert_type)
        return node

    def build_root(self, template: dict, name: str, max_depth: int, suffix: Optional[str] = None,
                   current_depth: int = 0) -> RootModel:
        root = RootModel(name=name)
        root.table_name = self.fmt.rename(name, suffix)
        for k, v in template.items():
            if isinstance(v, dict):
                v_keys = list(v.keys())
                if len(v_keys) == 1 and v_keys[0].startswith(self.ignore_head):
                    # if ignore this, must not a array or dict
                    v_key = v_keys[0]
                    assert not isinstance(v[v_key], dict) or not isinstance(v[v_key], list)
                    root.fields[k] = self.add_field(k, v[v_key], v_key[len(self.ignore_head):])
                elif 0 <= max_depth <= current_depth:
                    root.fields[k] = self.add_field(k, "json object", "auto compressed")
                else:
                    root.brothers[k] = self.build_root(template=v, name=k, max_depth=max_depth, suffix=suffix,
                                                       current_depth=current_depth + 1)
            elif isinstance(v, list):
                if len(v) == 0:
                    raise FrameworkNotSupport(f"Not Support No Value in Array of field:{k}")
                elif isinstance(v[0], dict):
                    if 0 <= max_depth <= current_depth:
                        root.fields[k] = self.add_field(k, "json object", "auto compressed")
                    else:
                        root.sons[k] = self.build_root(template=v[0], name=k, max_depth=max_depth, suffix=suffix,
                                                       current_depth=current_depth + 1)
                else:
                    root.fields[k] = self.add_field(k, "json array", "auto compressed")
            else:
                root.fields[k] = self.add_field(k, v)
        if self.primary_key in root.fields:
            raise FrameworkNotSupport(
                f"In table {name} field {self.primary_key} is same as the primary key,"
                f" please delete it or use other key as primary key")

        return root

    def from_json(self, *args, data: dict, root_name: str, suffix: Optional[str] = None, max_depth: int = -1,
                  **kwargs) -> JModel:

        root = self.build_root(data, root_name, max_depth, suffix=suffix)

        return self._build_models(root)

    @staticmethod
    def rebuild(data: dict) -> RootModel:
        root = RootModel(**{k: v for k, v in data.items() if k not in ('fields', 'brothers', 'sons')})

        if data['fields']:
            root.fields = {k: NodeField(**v) for k, v in data['fields'].items()}

        if data['brothers']:
            root.brothers.update({k: CommonModelFactory.rebuild(v) for k, v in data['brothers'].items()})

        if data['sons']:
            root.sons.update({k: CommonModelFactory.rebuild(v) for k, v in data['sons'].items()})

        return root

    def from_cache(self, *args, data: Union[dict, str], root_name: str, suffix: Optional[str] = None,
                   **kwargs) -> JModel:
        if isinstance(data, str):
            data = json.loads(data)
        return self._build_models(self.rebuild(data))


class CommonModel(JModel):
    def __init__(self, *args, model: RootModel,
                 factory: CommonModelFactory,
                 **kwargs):
        self.model = model
        self._model = {}
        self.factory = factory
        self._db_models = None
        self.Base = declarative_base()
        self.pk = self.factory.primary_key
        self.type_helper = self.factory.type_helper

    @property
    def engine(self):
        if hasattr(self, '_engine'):
            return self._engine
        else:
            self._engine = create_engine(self.factory.default_db_url, echo=self.factory.is_echo)
            return self._engine

    def tostring(self) -> str:
        pass

    def to_cache(self) -> str:
        return json.dumps(attr.asdict(self.model))

    def save_to_file(self, file_name: str, mode: str = 'w'):
        print(self.tostring(), file=open(file_name, mode=mode))

    NOT_STARTS = "--"
    SCOPE_NAME = NOT_STARTS + 'SCOPE_NAME'
    FATHER_NAME = NOT_STARTS + 'FATHER_NAME'

    def init_scope(self, table_name: str, father: Optional[dict]) -> dict:
        return {self.SCOPE_NAME: table_name, self.FATHER_NAME: father}

    def is_in(self, name: str, scope: dict) -> bool:
        def _rename(old):
            new_name = scope[self.SCOPE_NAME] + '.' + name
            if isinstance(old[name], tuple):
                new_value = tuple(list(old[name]) + [new_name])
            else:
                new_value = tuple([old[self.SCOPE_NAME] + '.' + name, new_name])
            scope[name] = new_value

        if name in scope:
            _rename(scope)
            return True

        _scope = scope[self.FATHER_NAME]
        while _scope:
            if name in _scope:
                _rename(_scope)
                return True
            else:
                _scope = _scope[self.FATHER_NAME]
        return False

    def brother_scope(self, root: dict, table_name: str, scope: dict) -> List:
        sons = []

        for k, v in root.items():
            if isinstance(v, dict):
                sons.extend(self.brother_scope(v, k, scope))
            elif isinstance(v, list):
                if len(v) == 0:
                    scope[k] = []
                else:
                    if isinstance(v[0], dict):
                        sons.append((k, v))
                    else:
                        scope[k] = json.dumps(v)
            else:
                full_name = table_name + '.' + k
                assert not self.is_in(full_name, scope)
                scope[full_name] = v
                if self.is_in(k, scope):
                    pass
                else:
                    scope[k] = v

        return sons

    def dict2scope(self, root: dict, table_name: str, father: Optional[dict] = None) -> dict:
        scope = self.init_scope(table_name, father)
        sons = []
        for k, v in root.items():
            if isinstance(v, dict):
                sons.extend(self.brother_scope(v, k, scope))
            elif isinstance(v, list):
                if len(v) == 0:
                    scope[k] = []
                else:
                    if isinstance(v[0], dict):
                        sons.append((k, v))
                    else:
                        scope[k] = json.dumps(v)
            else:
                full_name = table_name + '.' + k
                assert not self.is_in(full_name, scope)
                scope[full_name] = v
                if self.is_in(k, scope):
                    pass
                else:
                    scope[k] = v

        for k, v in sons:
            scope[k] = [self.dict2scope(x, k, scope) for x in v]
        return scope

    def set_field(self, obj: Any, name: str, value: Any, field: NodeField):
        # TODO: add type convert
        if value is None and field.nullable:
            if field.default is not None:
                setattr(obj, name, field.default)
            return
        fct = self.factory
        if fct.fmt.rename(field.name) == fct.add_time_col and not isinstance(value, datetime):
            # Not add datetime it will create by default
            return
        # Add Type Convert
        current_type = type(value)
        db_type = self.type_helper.get_column(field.db_type)
        if isinstance(db_type, TypeEngine):
            # some type like VARCHAR(1000)
            db_type = type(db_type)
        db_type_name = self.type_helper.get_name(db_type)
        need_type = PYTHON_TYPE_NAME[db_type_name]
        if current_type == need_type:
            new_value = value
        else:
            new_value = converter(current_type, need_type, value)
        setattr(obj, name, new_value)

    def init_root(self, model: RootModel, scope: dict,
                  debug: bool = False,
                  scope_is_pressed=False) -> Any:
        obj = self.db_models[model.name]()
        for k, v in model.brothers.items():
            # foreign has same scope with brother
            path = k if v.alias is None else v.alias
            new_scope = scope if scope_is_pressed else scope[path]

            setattr(obj, k, self.init_root(v, new_scope, debug=debug, scope_is_pressed=scope_is_pressed))

        for k, v in model.fields.items():
            if scope_is_pressed:
                path = k if v.alias is None else v.alias
                is_set = False
                _scope = scope
                while _scope:
                    if path in _scope:

                        if isinstance(_scope[path], tuple):
                            if debug:
                                raise ParseDataError(f"Columns Name {path} in {model.name} Conflict in {_scope[path]}")
                            else:
                                print(f"Columns Name {path} in {model.name} Conflict in {_scope[path]}")
                                full_name = model.name + '.' + path
                                if full_name in _scope:
                                    is_set = True
                                    self.set_field(obj, k, _scope[full_name], v)
                                    break
                                else:
                                    raise ParseDataError(f"Columns Name not find in {model.name} {full_name}")

                        else:
                            is_set = True
                            self.set_field(obj, k, _scope[path], v)
                            break
                    else:
                        _scope = _scope[self.FATHER_NAME]
                if not is_set:
                    self.set_field(obj, k, None, v)

            else:
                self.set_field(obj, k, scope.get(k), v)

        for k, v in model.sons.items():
            if scope_is_pressed:
                real_scope_name = v.name if v.alias is None else v.alias

                assert real_scope_name in scope
                assert isinstance(scope[real_scope_name], list)
                for o in scope[real_scope_name]:
                    n_v = self.init_root(v, o, debug=debug, scope_is_pressed=scope_is_pressed)
                    getattr(obj, k).append(n_v)
            else:
                sons = scope[k]
                for sc in sons:
                    n_v = self.init_root(v, sc, debug=debug, scope_is_pressed=scope_is_pressed)
                    getattr(obj, k).append(n_v)

        return obj

    def store(self, *args, data: dict, is_press: bool = False,
              engine: Optional[object] = None, **kwargs):
        if not is_press:
            root = self.init_root(self.model, scope=data, scope_is_pressed=is_press)
        else:
            scope = self.dict2scope(root=data, table_name=self.model.name)
            root = self.init_root(self.model, scope=scope, scope_is_pressed=is_press)
        if engine is None:
            engine = self.engine
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(root)
        session.commit()

    def convert(self, *args, data: dict, is_press: bool = False, **kwargs) -> Dict:
        if not is_press:
            root = self.init_root(self.model, scope=data, scope_is_pressed=is_press)
        else:
            scope = self.dict2scope(root=data, table_name=self.model.name)
            root = self.init_root(self.model, scope=scope, scope_is_pressed=is_press)
        return self.obj2json(root, self.model)

    def obj2json(self, obj, model: RootModel) -> dict:
        d = {}
        for k in model.fields:
            v = getattr(obj, k)
            d[k] = v

        for k, v in model.sons.items():
            r = []
            for x in getattr(obj, k):
                r.append(self.obj2json(x, v))
            d[k] = r
        for k, v in model.brothers.items():
            d[k] = self.obj2json(getattr(obj, k), v)

        return d

    def get_search_table(self, name: str) -> str:
        if name in self._model:
            return name
        for k, v in self._model.items():
            if v.alias == name:
                return k
        raise ParseDataError(f"Search args Error, table {name} not find")

    def get_search_field(self, model_name: str, field_name: str) -> str:
        fields = self._model[model_name].fields
        if field_name in fields:
            return field_name
        for k, v in fields.items():
            if v.alias == field_name:
                return k
        raise ParseDataError(f"Search args Error, table {model_name} {field_name} not find")

    def search(self, *args, search_args: List[Tuple[str, Any]], limit: int = 1, engine: Optional[object] = None,
               **kwargs) -> List:
        engine = self.engine if engine is None else engine
        session = sessionmaker(bind=engine)()
        table_name = self.model.name
        query = session.query(self.db_models[table_name])
        for k, v in search_args:
            s = k.split('.')
            tb_name = table_name if len(s) == 1 else self.get_search_table(s[-2])
            tb_attr = self.get_search_field(tb_name, s[-1])
            query = query.filter(getattr(self.db_models[tb_name], tb_attr) == v)
        # print("total query", query.count())
        query = query.order_by(getattr(self.db_models[table_name], self.factory.primary_key).desc()).limit(limit)
        rlt = []
        for d in query.all():
            rlt.append(self.obj2json(d, self.model))
        return rlt

    def get_primary_row(self):
        return Column(
            name=self.factory.primary_key,
            type_=self.factory.primary_type,
            autoincrement=True,
            primary_key=True
        )

    @staticmethod
    def _get_column(name: str, type_: type,
                    default: Optional[Any] = None,
                    nullable: bool = True,
                    unique: Optional[bool] = None):
        return Column(name=name, type_=type_,
                      default=default,
                      nullable=nullable,
                      unique=unique
                      )

    def get_column(self, field: NodeField) -> Column:
        if field.name == self.factory.time_col_name:
            # if field name is same as time_col_name set this field default is Now
            return self._get_column(self.factory.time_col_name, DateTime, datetime.now)
        type_ = self.factory.type_helper.get_column(field.db_type)
        return self._get_column(
            name=field.column,
            type_=type_,
            default=field.default,
            nullable=field.nullable,
            unique=field.unique
        )

    def foreign_column_name(self, name: str) -> str:
        f = self.factory

        return f.fmt.rename(name, f.foreignkey_suffix)

    def get_foreign_column(self, name: str, table_name: str, use_foreign_key: bool):
        f = self.factory
        args = [self.foreign_column_name(name), self.factory.primary_type]
        if use_foreign_key:
            fn, pk = f.fmt.rename(name), f.primary_key
            args.append(ForeignKey(f"{fn}.{pk}"))

        return Column(*args)

    def add_relationship(self, target: str, me: str, user_foreign_key: bool,
                         owed: bool = False):
        if not user_foreign_key:
            if owed:
                f_id = self.foreign_column_name(target)
                join = f'foreign({me}.{f_id})=={target}.{self.pk}'
            else:
                f_id = self.foreign_column_name(me)
                join = f'foreign({target}.{f_id})=={me}.{self.pk}'
            return relationship(target, primaryjoin=join)
        else:
            return relationship(target)

    def init_one_model(self, model: RootModel, use_foreign_key: bool, add_foreign: Optional[RootModel] = None,
                       add_time_col: bool = False):

        if model.table_name in self.Base.metadata.tables:
            raise FrameworkNotSupport(f"Same table {model.name} in one json object, please check")

        factory = self.factory
        cols = dict()
        cols['__tablename__'] = model.table_name
        cols['__table_args__'] = factory.table_args
        cols[factory.primary_key] = self.get_primary_row()

        for k, v in model.fields.items():
            cols[k] = self.get_column(v)

        for k, v in model.brothers.items():
            self.init_one_model(v, use_foreign_key)
            cols[self.foreign_column_name(k)] = self.get_foreign_column(v.name, v.table_name, use_foreign_key)
            cols[k] = self.add_relationship(k, model.name, user_foreign_key=use_foreign_key, owed=True)

        if add_foreign:
            cols[self.foreign_column_name(add_foreign.name)] = self.get_foreign_column(add_foreign.name,
                                                                                       add_foreign.table_name,
                                                                                       use_foreign_key)

        if add_time_col:
            cols[factory.time_col_name] = self._get_column(factory.time_col_name, DateTime, datetime.now)

        for k, v in model.sons.items():
            self.init_one_model(v, use_foreign_key, add_foreign=model)
            cols[k] = self.add_relationship(k, model.name, user_foreign_key=use_foreign_key, owed=False)

        table = type(model.name, (self.Base,), cols)
        if model.comment:
            tab = self.Base.metadata.tables[model.table_name]
            tab.comment = model.comment
        self._db_models[model.name] = table
        self._model[model.name] = model

    def init_all_models(self):
        if self._db_models is None:
            self._db_models = {}

            self.init_one_model(self.model, self.factory.use_foreign_key, add_time_col=self.factory.add_time_col)

    @property
    def db_models(self):
        if self._db_models is None:
            self.init_all_models()
        return self._db_models

    def create_tables_in_db(self, engine: Optional[object] = None):
        self.init_all_models()
        engine = self.engine if engine is None else engine
        self.Base.metadata.create_all(bind=engine)

    def delete_tables_in_db(self, engine: Optional[object] = None):
        self.init_all_models()
        engine = self.engine if engine is None else engine
        self.Base.metadata.drop_all(bind=engine)
