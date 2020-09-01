# /usr/bin/python3
import math
import os
import sys
from threading import Thread
from types import FunctionType

from db.controller import *
from functools import wraps
from os.path import join
from sys import stderr
from pony.orm.core import Query
import bottle
from bottle import response, request

from htmlmin.decorator import htmlmin


try:
    from ujson import load, dump, loads, dumps
except ImportError:
    if os.getenv("IGNORE_UJSON") is None:
        print("Please, install ujson module (pip3 install ujson)", file=stderr)
    from json import load, dump, loads, dumps

GET, POST, DELETE, PATCH = "GET", "POST", "DELETE", "PATCH"
GET_POST = [GET, POST]
app = application = bottle.Bottle()


public_path = "./public"
images_path = join(public_path, 'img')
paths = [p[len(images_path):] or "/" for p, d, f in os.walk(images_path)]
images = [
    {
        "path": "/" + p[len(images_path):] + '/' + i,
        "name": i
    } for p, d, f in os.walk(images_path)
    for i in filter(lambda x: x != '__init__.py', f)]


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
ADMIN_COOKIE_KEY = "user"
ADMIN_COOKIE_SECRET = SALT
ADMIN_ROUTE = "/admin"


def admin_route(url, method="GET"):
    def wrap(func):
        @route(ADMIN_ROUTE + url.rstrip("/"), method)
        def wrapped(*args, **kwargs):
            user = request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET)
            if is_hash_admin(user):
                return func(*args, **kwargs)
            bottle.redirect(ADMIN_LOGIN_ROUTE + "?from=" + ADMIN_ROUTE + url.rstrip("/"))
        return wrapped
    return wrap


def admin_temp(source, title="", extension=".html", *args, **kwargs):
    h = request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET)
    with db_session:
        admins = list(Admin.select())
        user = get_admin_by_hash(h)
    if not user:
        return redirect("/logout")
    return template(
        join("admin", source),
        title + " (Админка)" if title else "Админка",
        extension,
        index="view/layout/admin.html",
        admins=admins,
        user=user,
        request=request,
        # url=request.urlparts.path.split(ADMIN_ROUTE + "/", 1)[1],
        db_session=db_session,
        *args, **kwargs)


# ==============================================================================
# MAIN

@htmlmin(remove_comments=True)
def template(source, template_title="", extension=".html", including_page=None,
             alert: Alert = None, self_stationary_page=False, index=join("view", "layout", "index.html"),
             *args, **kwargs):
    d = loads(request.get_cookie("kwargs", "{}", ADMIN_COOKIE_SECRET))
    if alert:
        alert = alert.conv
    if d:
        response.delete_cookie("kwargs", path='/')
        if 'alert' in d:
            alert = loads(d['alert'])
        kwargs.update(d)

    with db_session:
        return bottle.template(
            join("view", source + extension) if self_stationary_page else index,

            title=template_title,
            args=args,
            alert=alert,
            kwargs=kwargs,
            settings=get_all_settings(),
            paginator=paginator,

            desc=desc,
            select=select,

            description=get_settings("description", ""),

            including_page=None if self_stationary_page
            else (including_page or join("view", source + extension)),
            **db.entities
        )


@wraps(bottle.redirect)
def redirect(url: str = None, code: int = None, alert: Alert = None, **kwargs):
    if url is None:
        url = request.url
    if kwargs or alert:
        if alert:
            kwargs['alert'] = dumps(alert.conv)
        response.set_cookie("kwargs", dumps(kwargs), ADMIN_COOKIE_SECRET, path="/")
    return bottle.redirect(url, code)


@wraps(bottle.Bottle.route)
def route(p=None, method='GET', callback=None, name=None,
          apply=None, skip=None, **config):

    def wrap(func):
        app.route(p, method, callback, name,
                  apply, skip, **config)(func)

        path = (p + '/').replace('//', '/')
        app.route(path, method, callback, name,
                  apply, skip, **config)(func)
        return func
    return wrap


def paginator(data_len, sep):
    return {
        "pages": math.ceil(data_len / sep),
        "current": int(request.query.get("page", "1"))
    }


def save_img(filename="", path="", name_in_form="image", overwrite=True):
    file_path = os.path.join(images_path, path)
    file = request.files.get(name_in_form)   # type: bottle.FileUpload
    return save_file(file, filename, file_path, overwrite)


def save_file(file: bottle.FileUpload, filename="", file_path="", overwrite=True):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    extension = file.raw_filename.split(".", 1)[1]
    if not filename:
        filename = file.raw_filename.split(".", 1)[0]
    save_path = os.path.join(file_path, filename + "." + extension)
    file.save(save_path, overwrite=overwrite)
    return save_path[len(public_path.rstrip('/')):]


@db_session
def get_current_admin():
    return get_admin_by_hash(request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET))


def normal_news(content: str):
    r = ""
    add = True
    for i in content:
        if i == "<":
            add = False
            continue
        if i == ">":
            add = True
            continue
        if add:
            r += i
    return r.replace("&nbsp;", "").strip()


@db_session
def get_news(pagenum=1, pagesize=10):
    n = pagination(list(select(n for n in Blog if not n.draft and n.date <= datetime.now()).sort_by(Blog.date))[::-1],
                   pagenum, pagesize)
    return n


@db_session
def get_json_select(query: Query):
    return [get_json(e) for e in list(query)]


@db_session
def get_json_list(entity: db.Entity):
    return get_json_select(select(e for e in entity))


@db_session
def get_json(entity: db.Entity):
    d = entity.to_dict(with_collections=True, related_objects=True)
    for key in d:
        if issubclass(type(d[key]), db.Entity):
            d[key] = get_json(d[key])
    return d


def async_func(func):
    # type: (FunctionType) -> FunctionType
    def wrap(*args, **kwargs) -> Thread:
        task = Thread(target=func, name=func.__name__, args=args, kwargs=kwargs)
        # task.daemon = True
        task.start()
        return task
    return wrap


def pagination(obj, pagenum: int, pagesize: int):
    offset = (pagenum - 1) * pagesize
    return obj[offset:offset+pagesize]


def get_directories(path: str):
    return sorted(join(p, x)[len(images_path):] for p, d, _ in os.walk(path) for x in d)


def get_files(path: str):
    return sorted(filter(lambda x: x != '__init__.py', next(os.walk(join(images_path, path)))[2]))


if __name__ == '__main__':
    with db_session:
        pprint(get_json(Blog[1]))
