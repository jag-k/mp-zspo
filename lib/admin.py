from datetime import datetime

from bottle import request
from pony.orm.core import Query

from db.controller import get_admin_by_hash
from db.models import News, db
from lib.constants import *
from pony.orm import select

from lib.utility import pagination


def get_current_admin():
    return get_admin_by_hash(request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET))


def get_news(page_number=1, pagesize=10):
    n = pagination(list(select(n for n in News if not n.draft and n.date <= datetime.now()).sort_by(News.date))[::-1],
                   page_number, pagesize)
    return n


def get_json_select(query: Query):
    return [get_json(e) for e in list(query)]


def get_json_list(entity: db.Entity):
    return get_json_select(select(e for e in entity))


def get_json(entity: db.Entity, last_entity=False):
    d = entity.to_dict(with_collections=not last_entity, related_objects=not last_entity)
    for key in d:
        if issubclass(type(d[key]), db.Entity):
            d[key] = get_json(d[key], True)
    return d

