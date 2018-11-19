# -*- coding:utf-8 -*-
import json
from typing import Optional, Any
from datetime import datetime
from .core import ParseDataError

NOT_STARTS = "--"


def int2datetime(v: int) -> datetime:
    s = str(v)
    N = len(s)
    if N == 13 or N == 10:
        if N == 13:
            v = v / 1000
        return datetime.fromtimestamp(v)
    raise ParseDataError(f"int2datetime error this can't convert {v} to datetime")


def float2datetime(v: float) -> datetime:
    s = str(int(v))
    N = len(s)
    if N == 13 or N == 10:
        if N == 13:
            v = v / 1000
        return datetime.fromtimestamp(v)
    raise ParseDataError(f"float2datetime error this can't convert {v} to datetime")


def delete_scope_info(value: dict) -> dict:
    return {k: (delete_scope_info(v) if isinstance(v, dict) else (
        [delete_scope_info(x) for x in v] if isinstance(v, list) else v)) for k, v in value.items() if
            not k.startswith(NOT_STARTS)}


def dict2str(v: dict) -> str:
    return json.dumps(delete_scope_info(v))


def list2str(v: list) -> str:
    if len(v) == 0:
        return "[]"
    if isinstance(v[0], dict):
        return json.dumps([delete_scope_info(x) for x in v])
    return json.dumps(v)


from dateutil.parser import parse as s2date


def str2datetime(v: str) -> datetime:
    N = len(v)
    if v.isnumeric() and (N == 13 or N == 10):
        # it's maybe timestampe
        value = int(v)
        if N == 13:
            value = value / 1000
        return datetime.fromtimestamp(value)
    return s2date(v)


converter_support = {
    (int, datetime): int2datetime,
    (str, datetime): str2datetime,
    (float, datetime): float2datetime,

    (str, int): int,
    (float, int): int,
    (bool, int): int,

    (str, float): float,
    (bool, float): float,

    (int, str): str,
    (float, str): str,
    (datetime, str): str,

    (dict, str): dict2str,
    (list, str): list2str

}


def converter(current_type: type, need_type: type, value: Any) -> Any:
    if need_type == current_type:
        return value
    if (current_type, need_type) in converter_support:
        try:
            return converter_support[(current_type, need_type)](value)
        except Exception as e:
            print(e)
            return None
    raise ParseDataError(f"Current convert not support from {current_type} to {need_type}")


