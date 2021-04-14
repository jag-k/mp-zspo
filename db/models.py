"""
docs: https://docs.ponyorm.org/
"""
import os
from datetime import date
from pony.orm import *
from pony.orm.migrations.cli import migrate

# CREATE_DB = True
os.environ["MIGRATIONS_DIR"] = os.path.abspath(os.path.join(__file__, '../migrations'))

db = Database(provider='sqlite', filename='db.sqlite3', create_db=True)


# ===== MODELS =====

class Admin(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    name = Optional(str)
    hash = Required(str, unique=True)


class Settings(db.Entity):
    key = PrimaryKey(str)
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
    header = Optional("Header", cascade_delete=True)


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
    post = Optional(Post)


# ===== END MODELS =====

# def migration():
#     db.migrate(
#         command="make",
#         create_tables=True,
#         allow_auto_upgrade=True,
#         migration_dir=migration_dir,
#         **DATABASE
#     )
#
#
# migration_dir = MIGRATION_DIR if __name__ == "__main__" else join('db', MIGRATION_DIR)
# migration()

# db.bind(provider='sqlite', filename='db.sqlite', create_db=True)

db.generate_mapping(check_tables=False)
migrate(db, 'make')
migrate(db, 'apply')

if __name__ == '__main__':
    from pprint import pprint

    pprint(db.entities)
