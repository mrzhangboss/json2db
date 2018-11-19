# Json2DB

> Python3.6+


Just need defined a json object, then you can save it in to a relational DB like MySQL PostgreSQL or other DB.

## Reason To Write This FrameWork

Although NoSQL Database like MongoDB is popular, we still need SQL DataBase for analyze data,
so this module is helping us store json to database, and help us build them in  db.


## Feture

- Support Different Style of database column

If you want your db column like `some_thing` style
    
    from json2db import JFactory, ColumnFormat
    JFactory(column_fmt=ColumnFormat.UNDERLINE)
   
If you want your db column to be `someThing` style, use `ColumnFormat.CAMEL`

Default we do nothing as the json format.

- Support Control the Table Column, just set `int2col` `float2col` `str2col` ... from `sqlalchemy sql type`


- Support Add a TimeStamp for your first table

- Support set table args for your each table init

- Support add comment to your field

Just Use `{"field": {":my comment": "real value"}}`, it can take the `my comment` to this `field`

- Support Control the max_depth of your table

PS: min is `0` which meaning it only one table for all json

- Support Restore your data to anther table

if your data like `d = {"father_id": 1, "father_name": "father", "brother": {"brother_name": "jack"}, 'sons': [{"son_name": "aa"}}`, You can save it to a 
new table like `father - son ` framework like `{"father_id": 1, "brother_name": "jack", 'sons': [{"son_name": "aa", "father_name": "father"}]}`

PS: you move `brother` field to `father` table, and move `father` field to `son` table,you can use 

    model.store(data=new_d, is_press=True)
    
See more sample please see [tests](tests)


## A Simple Example 

> For create_table ,store data and search data 
    
    
    from json2db import JFactory, ColumnFormat
    d = {"aa": 1, "bb": 2, "brother": {"name": "jack", "namess": [{"other": "jack"}]}, 'sons': [{"son_name": "aa"}]}

    factory = JFactory()
    model = factory.from_json(data=d, root_name="data")
    model.create_tables_in_db()
    model.store(data=d)
    model.search(search_args=[("aa", 1)], limit=2)
  
 You can save your data to any `sqlalchemy` support database like MySQL, PostgreSQL,Oracle,SQLite(Default stored if you not set `db_url`) and so on.
 The `db_url` format please see more detail see [https://docs.sqlalchemy.org/en/latest/core/engines.html](https://docs.sqlalchemy.org/en/latest/core/engines.html)
 
 
# TODO:

- add model migration
