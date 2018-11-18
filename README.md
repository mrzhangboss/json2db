# Json2DB

> Python3.6+


Just need defined a json object, then you can save it in to a relational DB like MySQL PostgreSQL or other DB.

## Reason To Write This FrameWork


## Example
    
    
    from json2db import JFactory
    d = {"aa": 1, "bb": 2, "brother": {"name": "jack", "namess": [{"other": "jack"}]}, 'sons': [{"son_name": "aa"}]}

    factory = JFactory()
    model = factory.from_json(data=d, root_name="data")
    model.create_tables_in_db()
    model.store(data=d)
    model.search(search_args=[("aa", 1)], limit=2)
    