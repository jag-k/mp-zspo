"""
docs: https://docs.ponyorm.org/
"""
from pprint import pprint
from sys import argv
from datetime import date

from pony.orm import *
CREATE_DB = True
db = Database("sqlite", "db.sqlite3", create_db=CREATE_DB or "-c" in argv or "--create-db" in argv)


# ===== MODELS =====

class Admin(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    name = Optional(str)
    hash = Required(str, unique=True)
    news_list = Set('News', cascade_delete=True)


class Settings(db.Entity):
    key = PrimaryKey(str, auto=True)
    value = Required(Json)


class News(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    date = Required(date)
    draft = Optional(bool, default=True)
    content = Required(str)
    image = Optional(str)
    old_link = Optional(str)
    admin = Required(Admin)


# ===== END MODELS =====
db.generate_mapping(
    create_tables=True
)

if __name__ == '__main__':
    pprint(db.entities)
