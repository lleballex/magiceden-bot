from misc import database

import json
from peewee import Model
from peewee import IntegerField, CharField, TextField


class User(Model):
    user_id = IntegerField(unique=True)

    class Meta:
        database = database
        db_table = 'users'


class Parser(Model):
    collection = CharField()
    filters = TextField()
 
    class Meta:
        database = database
        db_table = 'parsers'

    @classmethod
    def create(cls, **query):
        query['filters'] = json.dumps(query['filters'])
        return super().create(**query)

    def get_filters(self):
        return json.loads(self.filters)