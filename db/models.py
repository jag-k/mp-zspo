"""
docs: https://docs.ponyorm.org/
"""
from datetime import date
from sys import argv

from pony.orm import *

from config import DATABASE

CREATE_DB = True

db = Database()


# ===== MODELS =====

class Admin(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    name = Optional(str)
    hash = Required(str, unique=True)


class Settings(db.Entity):
    key = PrimaryKey(str, auto=True)
    value = Required(Json)


class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    link = Optional(str)
    description = Optional(str)
    category = Optional("Category")
    date = Required(date)
    hidden = Optional(bool, default=False)
    content = Required(str)


class News(Post):
    image = Optional(str)


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    link = Optional(str)
    block = Optional("Block")
    hidden = Optional(bool, default=False)
    posts = Set(Post, cascade_delete=True)


class Block(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    link = Optional(str)
    categories = Set(Category, cascade_delete=True)


class Header(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    url = Optional(str)


# ===== END MODELS =====

db.migrate(
    command="make",
    create_tables=True,
    allow_auto_upgrade=True,
    migration_dir='migration',
    **DATABASE
)

if __name__ == '__main__':
    from pprint import pprint

    pprint(db.entities)
