import math
from os.path import join
from threading import Thread

from bottle import request, FileUpload

from db.controller import update_settings
from lib.constants import *

try:
    from typing import Callable
except ImportError:
    Callable = None


def paginator(data_len, sep):
    return {
        "pages": math.ceil(data_len / sep),
        "current": int(request.query.get("page", "1"))
    }


def save_img(filename="", path="", name_in_form="image", overwrite=True):
    file_path = os.path.join(images_path, path)
    file = request.files.get(name_in_form)  # type: bottle.FileUpload
    return save_file(file, filename, file_path, overwrite)


def save_file(file: FileUpload, filename="", file_path="", overwrite=True):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    extension = file.raw_filename.split(".", 1)[1]
    if not filename:
        filename = file.raw_filename.split(".", 1)[0]
    save_path = os.path.join(file_path, filename + "." + extension)
    file.save(save_path, overwrite=overwrite)
    return save_path[len(PUBLIC_PATH.rstrip('/')):]


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


def async_func(func):
    # type: (Callable) -> Callable
    def wrap(*args, **kwargs) -> Thread:
        task = Thread(target=func, name=func.__name__, args=args, kwargs=kwargs)
        # task.daemon = True
        task.start()
        return task

    return wrap


def pagination(obj, pagenum: int, pagesize: int):
    offset = (pagenum - 1) * pagesize
    return obj[offset:offset + pagesize]


def get_directories(path: str):
    return sorted(join(p, x)[len(images_path):] for p, d, _ in os.walk(path) for x in d)


def get_files(path: str):
    return sorted(filter(lambda x: x != '__init__.py', next(os.walk(join(images_path, path)))[2]))


def save_settings_from_form(settings_key: str):
    par = dict(request.params)
    for filename in request.files:
        par[filename] = save_img(filename, "", filename)

    for key, value in list(par.items()):
        if isinstance(value, bytes):
            del par[key]

    update_settings(settings_key, par)


def is_current_page(url: str) -> bool:
    if url == "":
        return request.path == '/'

    if url.startswith("/"):
        return request.path.startswith(url)

    return request.path.endswith(url)
