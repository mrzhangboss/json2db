# -*- coding:utf-8 -*-
from .core import FrameworkNotSupport

TYPE_NAME = {str: 'str',
             int: 'int',
             float: 'float',
             bool: 'bool',
             bytes: 'bytes'}

NAME_TYPE = {v: k for k, v in TYPE_NAME.items()}

import sqlalchemy

DEFAULT_DB_TYPE_SCOPE = {"ARRAY": sqlalchemy.ARRAY, "BIGINT": sqlalchemy.BIGINT, "BINARY": sqlalchemy.BINARY,
                         "BLOB": sqlalchemy.BLOB, "BOOLEAN": sqlalchemy.BOOLEAN, "BigInteger": sqlalchemy.BigInteger,
                         "Binary": sqlalchemy.Binary, "Boolean": sqlalchemy.Boolean, "CHAR": sqlalchemy.CHAR,
                         "CLOB": sqlalchemy.CLOB, "DATE": sqlalchemy.DATE, "DATETIME": sqlalchemy.DATETIME,
                         "DECIMAL": sqlalchemy.DECIMAL, "Date": sqlalchemy.Date, "DateTime": sqlalchemy.DateTime,
                         "Enum": sqlalchemy.Enum, "FLOAT": sqlalchemy.FLOAT, "Float": sqlalchemy.Float,
                         "INT": sqlalchemy.INT, "INTEGER": sqlalchemy.INTEGER, "Integer": sqlalchemy.Integer,
                         "Interval": sqlalchemy.Interval, "JSON": sqlalchemy.JSON,
                         "LargeBinary": sqlalchemy.LargeBinary, "NCHAR": sqlalchemy.NCHAR,
                         "NVARCHAR": sqlalchemy.NVARCHAR, "NUMERIC": sqlalchemy.NUMERIC, "Numeric": sqlalchemy.Numeric,
                         "PickleType": sqlalchemy.PickleType, "REAL": sqlalchemy.REAL, "SMALLINT": sqlalchemy.SMALLINT,
                         "SmallInteger": sqlalchemy.SmallInteger, "String": sqlalchemy.String, "TEXT": sqlalchemy.TEXT,
                         "TIME": sqlalchemy.TIME, "TIMESTAMP": sqlalchemy.TIMESTAMP, "Text": sqlalchemy.Text,
                         "Time": sqlalchemy.Time, "Unicode": sqlalchemy.Unicode, "UnicodeText": sqlalchemy.UnicodeText,
                         "VARBINARY": sqlalchemy.VARBINARY, "VARCHAR": sqlalchemy.VARCHAR}

from sqlalchemy.dialects import mysql

MYSQL_DB_TYPE_SCOPE = {"BIGINT": mysql.BIGINT, "BINARY": mysql.BINARY, "BIT": mysql.BIT, "BLOB": mysql.BLOB,
                       "BOOLEAN": mysql.BOOLEAN, "CHAR": mysql.CHAR, "DATE": mysql.DATE, "DATETIME": mysql.DATETIME,
                       "DOUBLE": mysql.DOUBLE, "ENUM": mysql.ENUM, "DECIMAL": mysql.DECIMAL,
                       "FLOAT": mysql.FLOAT, "INTEGER": mysql.INTEGER, "JSON": mysql.JSON,
                       "LONGBLOB": mysql.LONGBLOB, "LONGTEXT": mysql.LONGTEXT, "MEDIUMBLOB": mysql.MEDIUMBLOB,
                       "MEDIUMINT": mysql.MEDIUMINT, "MEDIUMTEXT": mysql.MEDIUMTEXT, "NCHAR": mysql.NCHAR,
                       "NVARCHAR": mysql.NVARCHAR, "NUMERIC": mysql.NUMERIC, "SET": mysql.SET,
                       "SMALLINT": mysql.SMALLINT, "REAL": mysql.REAL, "TEXT": mysql.TEXT, "TIME": mysql.TIME,
                       "TIMESTAMP": mysql.TIMESTAMP, "TINYBLOB": mysql.TINYBLOB, "TINYINT": mysql.TINYINT,
                       "TINYTEXT": mysql.TINYTEXT, "VARBINARY": mysql.VARBINARY, "VARCHAR": mysql.VARCHAR,
                       "YEAR": mysql.YEAR,
                       # Alias
                       "INT": mysql.INTEGER
                       }

from sqlalchemy.dialects import oracle

ORACLE_DB_TYPE_SCOPE = {"VARCHAR": oracle.VARCHAR, "NVARCHAR": oracle.NVARCHAR, "CHAR": oracle.CHAR,
                        "DATE": oracle.DATE, "NUMBER": oracle.NUMBER, "BLOB": oracle.BLOB, "BFILE": oracle.BFILE,
                        "BINARY_FLOAT": oracle.BINARY_FLOAT, "BINARY_DOUBLE": oracle.BINARY_DOUBLE, "CLOB": oracle.CLOB,
                        "NCLOB": oracle.NCLOB, "TIMESTAMP": oracle.TIMESTAMP, "RAW": oracle.RAW, "FLOAT": oracle.FLOAT,
                        "DOUBLE_PRECISION": oracle.DOUBLE_PRECISION, "LONG": oracle.LONG, "INTERVAL": oracle.INTERVAL,
                        "VARCHAR2": oracle.VARCHAR2, "NVARCHAR2": oracle.NVARCHAR2, "ROWID": oracle.ROWID}

from sqlalchemy.dialects import mssql

MSSQL_DB_TYPE_SCOPE = {"INTEGER": mssql.INTEGER, "BIGINT": mssql.BIGINT, "SMALLINT": mssql.SMALLINT,
                       "TINYINT": mssql.TINYINT, "VARCHAR": mssql.VARCHAR, "NVARCHAR": mssql.NVARCHAR,
                       "CHAR": mssql.CHAR, "NCHAR": mssql.NCHAR, "TEXT": mssql.TEXT, "NTEXT": mssql.NTEXT,
                       "DECIMAL": mssql.DECIMAL, "NUMERIC": mssql.NUMERIC, "FLOAT": mssql.FLOAT,
                       "DATETIME": mssql.DATETIME, "DATETIME2": mssql.DATETIME2, "DATETIMEOFFSET": mssql.DATETIMEOFFSET,
                       "DATE": mssql.DATE, "TIME": mssql.TIME, "SMALLDATETIME": mssql.SMALLDATETIME,
                       "BINARY": mssql.BINARY, "VARBINARY": mssql.VARBINARY, "BIT": mssql.BIT, "REAL": mssql.REAL,
                       "IMAGE": mssql.IMAGE, "TIMESTAMP": mssql.TIMESTAMP, "ROWVERSION": mssql.ROWVERSION,
                       "MONEY": mssql.MONEY, "SMALLMONEY": mssql.SMALLMONEY, "UNIQUEIDENTIFIER": mssql.UNIQUEIDENTIFIER,
                       "SQL_VARIANT": mssql.SQL_VARIANT, "XML": mssql.XML
                       }

from sqlalchemy.dialects import sqlite

SQLITE_DB_TYPE_SCOPE = {"BLOB": sqlite.BLOB, "BOOLEAN": sqlite.BOOLEAN, "CHAR": sqlite.CHAR, "DATE": sqlite.DATE,
                        "DATETIME": sqlite.DATETIME, "DECIMAL": sqlite.DECIMAL, "FLOAT": sqlite.FLOAT,
                        "INTEGER": sqlite.INTEGER, "REAL": sqlite.REAL, "NUMERIC": sqlite.NUMERIC,
                        "SMALLINT": sqlite.SMALLINT, "TEXT": sqlite.TEXT, "TIME": sqlite.TIME,
                        "TIMESTAMP": sqlite.TIMESTAMP, "VARCHAR": sqlite.VARCHAR
                        }

from sqlalchemy.dialects import postgresql

POSTGRESQL_DB_TYPE_SCOPE = {"INTEGER": postgresql.INTEGER, "BIGINT": postgresql.BIGINT, "SMALLINT": postgresql.SMALLINT,
                            "VARCHAR": postgresql.VARCHAR, "CHAR": postgresql.CHAR, "TEXT": postgresql.TEXT,
                            "NUMERIC": postgresql.NUMERIC, "FLOAT": postgresql.FLOAT, "REAL": postgresql.REAL,
                            "INET": postgresql.INET, "CIDR": postgresql.CIDR, "UUID": postgresql.UUID,
                            "BIT": postgresql.BIT, "MACADDR": postgresql.MACADDR, "MONEY": postgresql.MONEY,
                            "OID": postgresql.OID, "REGCLASS": postgresql.REGCLASS,
                            "DOUBLE_PRECISION": postgresql.DOUBLE_PRECISION, "TIMESTAMP": postgresql.TIMESTAMP,
                            "TIME": postgresql.TIME, "DATE": postgresql.DATE, "BYTEA": postgresql.BYTEA,
                            "BOOLEAN": postgresql.BOOLEAN, "INTERVAL": postgresql.INTERVAL, "ENUM": postgresql.ENUM,
                            "TSVECTOR": postgresql.TSVECTOR, "DropEnumType": postgresql.DropEnumType,
                            "CreateEnumType": postgresql.CreateEnumType, "HSTORE": postgresql.HSTORE,
                            "JSON": postgresql.JSON, "JSONB": postgresql.JSONB, "ARRAY": postgresql.ARRAY
                            }

from sqlalchemy.dialects import firebird

FIREBIRD_DB_TYPE_SCOPE = {"SMALLINT": firebird.SMALLINT, "BIGINT": firebird.BIGINT, "FLOAT": firebird.FLOAT,
                          "DATE": firebird.DATE, "TIME": firebird.TIME, "TEXT": firebird.TEXT,
                          "NUMERIC": firebird.NUMERIC, "TIMESTAMP": firebird.TIMESTAMP, "VARCHAR": firebird.VARCHAR,
                          "CHAR": firebird.CHAR, "BLOB": firebird.BLOB
                          }

from sqlalchemy.dialects import sybase

SYBASE_DB_TYPE_SCOPE = {"CHAR": sybase.CHAR, "VARCHAR": sybase.VARCHAR, "TIME": sybase.TIME, "NCHAR": sybase.NCHAR,
                        "NVARCHAR": sybase.NVARCHAR, "TEXT": sybase.TEXT, "DATE": sybase.DATE,
                        "DATETIME": sybase.DATETIME, "FLOAT": sybase.FLOAT, "NUMERIC": sybase.NUMERIC,
                        "BIGINT": sybase.BIGINT, "INT": sybase.INT, "INTEGER": sybase.INTEGER,
                        "SMALLINT": sybase.SMALLINT, "BINARY": sybase.BINARY, "VARBINARY": sybase.VARBINARY,
                        "UNITEXT": sybase.UNITEXT, "UNICHAR": sybase.UNICHAR, "UNIVARCHAR": sybase.UNIVARCHAR,
                        "IMAGE": sybase.IMAGE, "BIT": sybase.BIT, "MONEY": sybase.MONEY,
                        "SMALLMONEY": sybase.SMALLMONEY, "TINYINT": sybase.TINYINT
                        }

_SUPPORT_DBS = {'firebird': FIREBIRD_DB_TYPE_SCOPE, 'mssql': MSSQL_DB_TYPE_SCOPE, 'mysql': MYSQL_DB_TYPE_SCOPE,
                'oracle': ORACLE_DB_TYPE_SCOPE, 'postgresql': POSTGRESQL_DB_TYPE_SCOPE, 'sqlite': SQLITE_DB_TYPE_SCOPE,
                'sybase': SYBASE_DB_TYPE_SCOPE, 'default': DEFAULT_DB_TYPE_SCOPE}

for k, v in _SUPPORT_DBS.items():
    # if not add __builtins__ ,  `eval` can use builtin functions
    v['__builtins__'] = "NULL"

from typing import Union, Optional
from sqlalchemy.types import TypeEngine
from sqlalchemy.sql.visitors import VisitableType


class DBType:
    def __init__(self, name: str = 'default'):
        if name not in _SUPPORT_DBS:
            raise FrameworkNotSupport("{} database not support "
                                      "All supported DB are {}".format(name, str(_SUPPORT_DBS.keys())))
        self.name = name
        self.type_names = _SUPPORT_DBS[name]
        self.types = {v: k for k, v in _SUPPORT_DBS[name].items()}

    def get_column(self, type_name: str) -> Union[TypeEngine, VisitableType]:
        # Do Some check when user choose their own database
        real_type = type_name.split('(', 1)[0].strip()
        if real_type not in self.type_names:
            if real_type.upper() not in self.type_names:
                raise FrameworkNotSupport(f"{type_name} not support in {self.name} database"
                                          f"Please defined your choose databae xxx2col fields")
            else:
                # Try upper all type name
                type_name = type_name.upper()
        try:
            return eval(type_name, _SUPPORT_DBS[self.name])
        except NameError as e:
            raise FrameworkNotSupport(f"{type_name} not support in {self.name} database")

    def get_name(self, typ: VisitableType) -> str:
        if typ not in self.types:
            raise FrameworkNotSupport(f"This Type {typ} not from {self.name} database, please check")
        return self.types[typ]


from datetime import datetime, date

PYTHON_TYPE_NAME = {
    "DOUBLE": float, "BIT": bool, "NVARCHAR": str, "SET": set, "SMALLDATETIME": datetime, "JSON": dict,
    "ROWVERSION": None,
    "SQL_VARIANT": None, "CLOB": bytes, "UNITEXT": str, "MEDIUMINT": int, "UnicodeText": str, "TIMESTAMP": datetime,
    "TEXT": str, "DATETIMEOFFSET": None, "NTEXT": str, "LONGBLOB": bytes, "FLOAT": float, "NCHAR": str,
    "DECIMAL": float, "JSONB": dict, "CreateEnumType": None, "SmallInteger": int, "String": str, "DATETIME2": datetime,
    "Enum": None, "Date": date, "BOOLEAN": bool, "YEAR": date, "Boolean": bool, "XML": str, "UNICHAR": str,
    "CIDR": None, "REGCLASS": None, "Interval": None, "TIME": datetime, "ENUM": None, "DOUBLE_PRECISION": None,
    "BINARY": bytes, "INT": int, "TINYINT": int, "REAL": None, "Numeric": None, "BINARY_FLOAT": None, "INTERVAL": None,
    "CHAR": chr, "NVARCHAR2": str, "BINARY_DOUBLE": float, "MONEY": float, "LONG": float, "DateTime": datetime,
    "BFILE": None, "LargeBinary": bytes, "Unicode": str, "MEDIUMTEXT": str, "PickleType": bytes, "DATE": date,
    "Text": str, "RAW": None, "MACADDR": None, "TINYBLOB": bytes, "ROWID": int, "OID": None, "HSTORE": None,
    "Float": float, "NCLOB": None, "UNIQUEIDENTIFIER": None, "INET": None, "UNIVARCHAR": str, "BYTEA": None,
    "BIGINT": int, "NUMERIC": None, "TSVECTOR": None, "UUID": str, "SMALLINT": int, "MEDIUMBLOB": str,
    "ARRAY": list, "INTEGER": int, "DATETIME": datetime, "Binary": bytes, "SMALLMONEY": float, "DropEnumType": None,
    "TINYTEXT": str, "VARCHAR2": str, "BigInteger": int, "VARBINARY": bytes, "Time": datetime, "BLOB": bytes,
    "LONGTEXT": str, "VARCHAR": str, "Integer": int, "IMAGE": bytes, "NUMBER": None

}

__all__ = ("TYPE_NAME", "NAME_TYPE", "PYTHON_TYPE_NAME", "DBType")
