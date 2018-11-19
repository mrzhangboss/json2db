# -*- coding:utf-8 -*-
import time
import pytest
from json2db.ModelFactory import CommonModelFactory


class TestCommonModelFactory:

    def test_load_from_json(self):
        d = {"aa": 1, "bb": 2}
        factory = CommonModelFactory()
        models = factory.from_json(data=d, root_name='data')
        assert len(models.model.sons) == 0

    def test_load_son(self):
        d = {"aa": 1, "bb": 2, "sons": [{"name": "jack"}]}
        assert len(CommonModelFactory().from_json(data=d, root_name='data').model.sons) == 1

    def test_load_brother(self):
        d = {"aa": 1, "bb": 2, "brother": {"name": "jack"}}
        assert len(CommonModelFactory().from_json(data=d, root_name='data').model.brothers) == 1

    def test_load_describe(self):
        d = {"aa": 1, "bb": 2, "brother": {":name": "jack"}}
        assert len(CommonModelFactory(ignore_head=':').from_json(data=d, root_name='data').model.brothers) == 0

    def test_load_from_cache(self):
        d = {"aa": 1, "bb": 2, "brother": {"name": "jack"}}
        factory = CommonModelFactory()
        models = factory.from_json(data=d, root_name='data')
        cache = models.to_cache()
        new_model = factory.from_cache(data=cache, root_name='data')
        assert len(models.model.brothers) == 1

    @pytest.mark.skip
    def test_create_all_table(self):
        d = {"aa": 1, "bb": 2, "brother": {"name": "jack"}}
        factory = CommonModelFactory(is_echo=True)
        model = factory.from_json(data=d, root_name="data")
        model.create_tables_in_db()

    @pytest.mark.skip
    def test_create_all_table_with_foreign_key(self):
        d = {"aa": 1, "bb": 2, "brother": {"name": "jack"}}
        factory = CommonModelFactory(is_echo=True, use_foreign_key=True)
        model = factory.from_json(data=d, root_name="data")
        model.create_tables_in_db()
        model.delete_tables_in_db()

    @pytest.mark.skip
    def test_drop_all_table_with_foreign_key(self):
        d = {"aa": 1, "bb": 2, "brother": {"name": "jack"}}
        factory = CommonModelFactory(is_echo=True, use_foreign_key=True)
        model = factory.from_json(data=d, root_name="data")
        model.delete_tables_in_db()

    # @pytest.mark.skip

    def test_store_data_search(self):
        d = {"aa": 1, "bb": 2, "brother": {"name": "jack", "namess": [{"other": "jack"}]}, 'sons': [{"son_name": "aa"}]}
        factory = CommonModelFactory(is_echo=True, use_foreign_key=False)
        model = factory.from_json(data=d, root_name="data")
        model.create_tables_in_db()
        time.sleep(1)
        model.store(data=d)
        new_d = {"aa": 1, "name": "jack", "namess": [{"other": "jack"}], 'sons': [{"son_name": "aa"}]}
        model.store(data=new_d, is_press=True)

        assert len(model.search(search_args=[], limit=2)) == 2
        assert len(model.search(search_args=[("aa", 1)], limit=2)) == 2
        assert len(model.search(search_args=[("bb", None)], limit=2)) == 1
