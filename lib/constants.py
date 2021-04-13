import os
import re
from pathlib import Path

import bottle
from pony.orm.integration.bottle_plugin import PonyPlugin

from db.controller import SALT
from misc import BASE_DIR, PUBLIC_PATH

try:
    from ujson import load, dump, loads, dumps
except ImportError:
    from json import load, dump, loads, dumps

GET, POST, DELETE, PATCH = "GET", "POST", "DELETE", "PATCH"
GET_POST = GET, POST
ID = "<id:int>"

app = application = bottle.Bottle()
app.install(PonyPlugin())
bottle.Jinja2Template.settings = {
    # 'autoescape': True,
}

bottle.TEMPLATE_PATH.insert(0, BASE_DIR / 'view')
images_path = PUBLIC_PATH / 'img'
paths = [p[len(str(images_path)):] or "/" for p, d, f in os.walk(images_path)]
images = [
    {
        "path": "/" + p[len(str(images_path)):] + '/' + i,
        "name": i
    } for p, d, f in os.walk(images_path)
    for i in filter(lambda x: x != '__init__.py', f)]

# language=PythonRegExp
PHONE_RE = re.compile(r'^(?:\+7|7|8)?[\s\-]?\(?([489][0-9]{2})\)?[\s\-]?([0-9]{3})[\s\-]?([0-9]{2})[\s\-]?([0-9]{2})$')


class Alert:
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"

    def __init__(self, content: str, alert_type=SUCCESS):
        self.content = content
        self.alert_type = alert_type

    @property
    def conv(self):
        return {
            "content": self.content,
            "type": self.alert_type
        }

    def __dir__(self):
        return self.conv

    def __str__(self):
        return 'Alert(%s): "%s"' % (self.alert_type.capitalize(), self.content)

    def __repr__(self):
        return "<Alert(%s) %.10s>" % (self.alert_type.capitalize(), self.content)


# ==============================================================================
# ADMINS

ADMIN_LOGIN_ROUTE = "/login"
ADMIN_LOGOUT_ROUTE = "/logout"
ADMIN_COOKIE_KEY = "user"
ADMIN_COOKIE_SECRET = SALT
ADMIN_ROUTE = Path('/admin')

try:
    from typing import Union

    PathLike = Union[str, Path]
except ImportError:
    PathLike = None
