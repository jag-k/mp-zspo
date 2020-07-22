# /usr/bin/python3
from functools import wraps
from os.path import join
from hashlib import pbkdf2_hmac
from sys import stderr
import binascii
from typing import Dict, List

import bottle
from bottle import response, request

try:
    from ujson import load, dump, loads, dumps
except ImportError:
    print("Please, install ujson module (pip3 install ujson)", file=stderr)
    from json import load, dump, loads, dumps

GET, POST, DELETE, PATCH = "GET", "POST", "DELETE", "PATCH"
app = bottle.Bottle()
bottle.ERROR_PAGE_TEMPLATE = open("view/error.html").read()


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
        return {
            "content": self.content,
            "type": self.alert_type
        }

    def __str__(self):
        return 'Alert(%s): "%s"' % (self.alert_type.capitalize(), self.content)

    def __repr__(self):
        return "<Alert(%s) %.10s>" % (self.alert_type.capitalize(), self.content)


ADMIN_COOKIE_KEY = "user"
ADMIN_COOKIE_SECRET = "o6fIcd0dcWSiV8BJYpdF"
# https://www.random.org/strings/?num=1&len=20&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new


# #   MAIN   # #
def template(source, template_title="", template_description="", extension=".html", including_page=None,
             alert: Alert = None, self_stationary_page=False,  *args, **kwargs):
    d = loads(request.get_cookie("kwargs", "{}", ADMIN_COOKIE_SECRET))
    if alert:
        alert = alert.conv
    if d:
        response.delete_cookie("kwargs", path='/')
        if 'alert' in d:
            alert = loads(d['alert'])
        kwargs.update(d)

    k = {
        "title": template_title,
        "description": template_description,
        "args": args,
        "alert": alert,
        "path": request.path,
        "kwargs": kwargs
    }

    if self_stationary_page:
        return bottle.template(join("view", source + extension), **k)
    return bottle.template("view/layout/skeleton.html",
                           including_page=including_page or join("view", source + extension),
                           **k
                           )


@wraps(bottle.redirect)
def redirect(url, code=None, alert: Alert = None, **kwargs):
    if kwargs or alert:
        if alert:
            kwargs['alert'] = dumps(alert.conv)
        response.set_cookie("kwargs", dumps(kwargs), ADMIN_COOKIE_SECRET, path='/')
    return bottle.redirect(url, code)


@wraps(bottle.Bottle.route)
def route(p=None, method='GET', callback=None, name=None,
          apply=None, skip=None, **config):

    def _(func):
        app.route(p, method, callback, name,
                  apply, skip, **config)(func)

        path = (p + '/').replace('//', '/')
        app.route(path, method, callback, name,
                  apply, skip, **config)(func)
        return func
    return _

