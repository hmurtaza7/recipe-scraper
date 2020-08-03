from peewee import *
from datetime import datetime
from playhouse.postgres_ext import *
from .base_model import BaseModel

class Recipe(BaseModel):
    id = BigAutoField()
    title = CharField(null=True)
    ingredients = JSONField(null=True)
    instructions = TextField(null=True)
    total_time = IntegerField(null=True)
    yields = CharField(null=True)
    external_url = CharField(null=True)
    host = CharField(null=True)
    host_author = CharField(null=True)
    host_image_url = CharField(null=True)
    host_ratings = DoubleField(null=True)
    language = CharField(null=True)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'recipes'
