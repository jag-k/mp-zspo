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


class Blog(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    description = Required(str)
    category = Optional("Category")
    date = Required(date)
    draft = Optional(bool, default=True)
    content = Required(str)
    image = Optional(str)
    custom_link = Optional(str)


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    link = Required(str)
    posts = Set(Blog)


class Feature(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    description = Required(str)
    icon = Optional(str)
    sub_features = Set("SubFeature", cascade_delete=True)


class SubFeature(db.Entity):
    id = PrimaryKey(int, auto=True)
    feature = Required(Feature)
    title = Required(str)
    date = Required(date)
    content = Required(str)
    image = Optional(str)
    link = Optional(str)


# ===== END MODELS =====
db.generate_mapping(
    create_tables=True
)

if __name__ == '__main__':
    from pprint import pprint
    pprint(db.entities)
