import logging
from peewee import *
from datetime import datetime
from playhouse.postgres_ext import JSONField
from .base_model import BaseModel

class LinksBacklog(BaseModel):
    id = BigAutoField()
    url = CharField(null=True)
    domain = CharField(null=True)
    error = TextField(null=True)
    scraped = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    last_scraped_on = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'links_backlogs'

    @classmethod
    def get_link(cls, **params):
        try:
            return cls.get(**params)
        except DoesNotExist as e:
            logging.debug(e)
            return None

    @classmethod
    def create_link(cls, **params):
        try:
            cls.create(**params)
        except IntegrityError as e:
            # link with given url already exists in db
            return str(e)
        except Exception as e:
            logging.debug(e)
            raise(e)

    @classmethod
    def get_links_to_scrape(cls, domain, page=1, limit=25):
        return cls.select() \
        .where(cls.domain==domain, cls.scraped==False) \
        .order_by(cls.id.asc()) \
        .paginate(page, limit)

    @classmethod
    def mark_link_as_scraped(cls, id):
        q = (
            cls.update({
                'scraped': True,
                'last_scraped_on': datetime.now()
                })
                .where(cls.id==id)
            )
        q.execute()
