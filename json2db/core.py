# -*- coding:utf-8 -*-
import re
from typing import Optional, Union, List, Dict, Any, Tuple
from abc import abstractclassmethod


class JException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class FrameworkNotSupport(JException):
    pass


class ParseDataError(JException):
    pass


class ColumnFormat:
    DEFAULT = "DEFAULT"  # not change the name of json
    CAMEL = "CAMEL"  # convert it to camel
    UNDERLINE = "UNDERLINE"  # use python underline format

    __support = (DEFAULT, CAMEL, UNDERLINE)
    __UNDERLINE_PATTERN = re.compile("(?<=[a-z])([A-Z])")

    __CAMEL_PATTERN = re.compile("(?<=[a-z])(_[a-z])")

    @staticmethod
    def str2camel(v: str) -> str:
        return ColumnFormat.__CAMEL_PATTERN.sub(lambda x: x.group()[1].upper(), v)

    @staticmethod
    def str2underline(v: str) -> str:
        return v[0].lower() + ColumnFormat.__UNDERLINE_PATTERN.sub(lambda x: '_' + x.group().lower(), v[1:])

    @classmethod
    def to_column(cls, value: str, fmt: str = DEFAULT, suffix: Optional[str] = None) -> str:
        """suffix the first key must be all lower alpha like id , key .etc

        :param value:
        :param fmt:
        :param suffix:
        :return:
        """
        if fmt not in cls.__support:
            raise FrameworkNotSupport(f"{fmt} not ColumnFormat in {cls.__support}")
        if suffix:
            if fmt == cls.CAMEL:
                suffix = cls.str2camel(suffix)
                suffix = suffix[0].upper() + suffix[1:]
                return cls.str2camel(value + suffix)
            if fmt == cls.UNDERLINE:
                suffix = cls.str2underline(suffix)
                suffix = "_" + suffix
                return cls.str2underline(value + suffix)
            return value + suffix
        else:
            suffix = ""
            n_value = value + suffix
            if fmt == cls.CAMEL:
                return cls.str2camel(n_value)
            if fmt == cls.UNDERLINE:
                return cls.str2underline(n_value)
            return n_value

    def __init__(self, fmt: str = DEFAULT):
        self.fmt = fmt

    def rename(self, v: str, suffix: Optional[str] = None) -> str:
        return ColumnFormat.to_column(value=v, suffix=suffix, fmt=self.fmt)


class JModel:
    """Base Model of json object
    It can save data, search data, and create or delete  tables in db

    """

    @abstractclassmethod
    def to_cache(cls) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def tostring(cls) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def store(cls, *args, data: dict, is_press: bool = False, engine: Optional[object] = None, **kwargs):
        raise NotImplementedError

    @abstractclassmethod
    def search(cls, *args, search_args: List[Tuple[str, Any]], limit: int = 1, engine: Optional[object] = None,
               **kwargs):
        raise NotImplementedError

    @abstractclassmethod
    def create_tables_in_db(cls, engine: Optional[object] = None):
        raise NotImplementedError

    @abstractclassmethod
    def delete_tables_in_db(cls, engine: Optional[object] = None):
        raise NotImplementedError


class Factory:
    """Base Factory
    It can generate JModel from json or xml or cache


    """

    @abstractclassmethod
    def from_json(cls, *args, data: dict, root_name: str, suffix: Optional[str] = None, max_depth: int = -1,
                  **kwargs) -> JModel:
        raise NotImplementedError

    @abstractclassmethod
    def from_cache(cls, *args, data: Union[dict, str], root_name: str, suffix: Optional[str] = None,
                   **kwargs) -> JModel:
        raise NotImplementedError
