# -*- coding:utf-8 -*-
import pytest
from json2db.core import ColumnFormat, FrameworkNotSupport


def test_not_support():
    with pytest.raises(FrameworkNotSupport):
        ColumnFormat.to_column("test", "NotSupportFormat")


def test_to_camel():
    assert "abcAbc" == ColumnFormat.to_column("abc_abc", ColumnFormat.CAMEL)
    assert "abcAbcId" == ColumnFormat.to_column("abc_abc", ColumnFormat.CAMEL, "id")
    assert "abcAbcEfg" == ColumnFormat.to_column("abc_abc_efg", ColumnFormat.CAMEL, "")
    assert "abcAbcEfgId" == ColumnFormat.to_column("abc_abc_efg", ColumnFormat.CAMEL, "id")
    assert "AbcAbc" == ColumnFormat.to_column("AbcAbc", ColumnFormat.CAMEL)

    assert "AbcAbcFakeId" == ColumnFormat.to_column("AbcAbc", ColumnFormat.CAMEL, "fake_id")


def test_to_underline():
    assert "abc_abc" == ColumnFormat.to_column("abcAbc", ColumnFormat.UNDERLINE)
    assert "abc_abc_id" == ColumnFormat.to_column("abcAbc", ColumnFormat.UNDERLINE, 'id')
    assert "abc_Abc_id" == ColumnFormat.to_column("abc_Abc", ColumnFormat.UNDERLINE, 'id')


def test_to_default():
    assert "abcAbc" == ColumnFormat.to_column("abcAbc", ColumnFormat.DEFAULT)
    assert "abcAbcid" == ColumnFormat.to_column("abcAbc", ColumnFormat.DEFAULT, 'id')


