import os
from peewee import *

database = PostgresqlDatabase(
    os.environ.get('DATABASE_NAME', 'recipe_db'),
    host=os.environ['DATABASE_HOST'],
    port=os.environ['DATABASE_PORT'],
    user=os.environ['DATABASE_USER'],
    password=os.environ['DATABASE_PASSWORD'],
    autorollback=True
)

# class UnknownField(object):
#     def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

database.connect()
# db.close()
