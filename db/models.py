"""
docs: https://docs.ponyorm.org/
"""
from sys import argv
from datetime import date

from pony.orm import *
CREATE_DB = True
db = Database("sqlite", "db.sqlite3", create_db=CREATE_DB or "-c" in argv or "--create-db" in argv)


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
    draft = Optional(bool, default=True)
    content = Required(str)


class News(Post):
    image = Optional(str)


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    link = Optional(str)
    block = Optional("Block")
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
db.generate_mapping(
    create_tables=True
)

if __name__ == '__main__':
    from pprint import pprint
    pprint(db.entities)
