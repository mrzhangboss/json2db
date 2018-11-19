# -*- coding:utf-8 -*-
TYPE_NAME = {str: 'str',
             int: 'int',
             float: 'float',
             bool: 'bool'}

NAME_TYPE = {v: k for k, v in TYPE_NAME.items()}
from sqlalchemy import (ARRAY,
                        BIGINT,
                        BINARY,
                        BLOB,
                        BOOLEAN,
                        BigInteger,
                        Binary,
                        Boolean,
                        CHAR,
                        CLOB,
                        DATE,
                        DATETIME,
                        DECIMAL,
                        Date,
                        DateTime,
                        Enum,
                        FLOAT,
                        Float,
                        INT,
                        INTEGER,
                        Integer,
                        Interval,
                        JSON,
                        LargeBinary,
                        NCHAR,
                        NVARCHAR,
                        NUMERIC,
                        Numeric,
                        PickleType,
                        REAL,
                        SMALLINT,
                        SmallInteger,
                        String,
                        TEXT,
                        TIME,
                        TIMESTAMP,
                        Text,
                        Time,
                        Unicode,
                        UnicodeText,
                        VARBINARY,
                        VARCHAR)

DB_TYPE_NAME = {
    "INT": INT, "CHAR": CHAR, "VARCHAR": VARCHAR, "NCHAR": NCHAR, "NVARCHAR": NVARCHAR, "TEXT": TEXT, "Text": Text,
    "FLOAT": FLOAT, "NUMERIC": NUMERIC, "REAL": REAL, "DECIMAL": DECIMAL, "TIMESTAMP": TIMESTAMP, "DATETIME": DATETIME,
    "CLOB": CLOB, "BLOB": BLOB, "BINARY": BINARY, "VARBINARY": VARBINARY, "BOOLEAN": BOOLEAN, "BIGINT": BIGINT,
    "SMALLINT": SMALLINT, "INTEGER": INTEGER, "DATE": DATE, "TIME": TIME, "String": String, "Integer": Integer,
    "SmallInteger": SmallInteger, "BigInteger": BigInteger, "Numeric": Numeric, "Float": Float, "DateTime": DateTime,
    "Date": Date, "Time": Time, "LargeBinary": LargeBinary, "Binary": Binary, "Boolean": Boolean, "Unicode": Unicode,
    "UnicodeText": UnicodeText, "PickleType": PickleType, "Interval": Interval,
    "Enum": Enum, "ARRAY": ARRAY, "JSON": JSON

}
from datetime import datetime, date

PYTHON_TYPE_NAME = {
    "INT": int, "CHAR": chr, "VARCHAR": str, "NCHAR": str, "NVARCHAR": str, "TEXT": str, "Text": str,
    "FLOAT": float, "NUMERIC": float, "REAL": None, "DECIMAL": float, "TIMESTAMP": datetime, "DATETIME": datetime,
    "CLOB": None, "BLOB": bytes, "BINARY": bytes, "VARBINARY": bytes, "BOOLEAN": bool, "Boolean": bool, "BIGINT": int,
    "SMALLINT": int, "INTEGER": int, "DATE": date, "TIME": datetime, "String": str, "Integer": int,
    "SmallInteger": int, "BigInteger": int,
    "LargeBinary": int, "Binary": bytes, "Unicode": str,
    "UnicodeText": str, "PickleType": None, "Interval": None,
    "Enum": None, "ARRAY": None, "JSON": None

}

DB_NAME_TYPE = {v: k for k, v in DB_TYPE_NAME.items()}

__all__ = ("DB_NAME_TYPE", "DB_TYPE_NAME", "TYPE_NAME", "NAME_TYPE")
