from functools import wraps

from bottle import request, response

from db.controller import *
from db.models import Admin, db
from lib.constants import *
from htmlmin.decorator import htmlmin

from lib.utility import is_current_page, paginator
from misc import ADMIN_TAB, config


def admin_route(url: PathLike, method="GET", disable=False):
    def wrap(func):
        if disable:
            return

        url_ = Path(str(url).strip("/"))

        @route(ADMIN_ROUTE / url_, method)
        def wrapped(*args, **kwargs):
            user = request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET)
            if is_hash_admin(user):
                return func(*args, **kwargs)
            bottle.redirect("{}?from={}".format(ADMIN_LOGIN_ROUTE, ADMIN_ROUTE / url_))

        return wrapped

    return wrap


def admin_temp(source, title="", extension=".html", *args, **kwargs):
    h = request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET)
    admins = list(Admin.select())
    user = get_admin_by_hash(h)
    if not user:
        redirect(ADMIN_LOGOUT_ROUTE)
    url = request.path[len(str(ADMIN_ROUTE)):].lstrip('/')
    with ADMIN_TAB(url):
        return template(
            ADMIN_ROUTE / str(source).strip('/'),
            title + " (Админка)" if title else "Админка",
            extension,

            admins=admins,
            user=user,
            request=request,
            url=url,
            tab=ADMIN_TAB,
            today=date.today().isoformat(),
            db_session=db_session,
            *args, **kwargs)


@htmlmin(remove_comments=True)
def template(source, template_title="", extension=".html", alert: Alert = None, **kwargs):
    d = loads(request.get_cookie("kwargs", "{}", ADMIN_COOKIE_SECRET))
    if alert:
        alert = alert.conv
    if d:
        response.delete_cookie("kwargs", path='/')
        if 'alert' in d:
            alert = loads(d['alert'])
        kwargs.update(d)

    headers = get_settings("headers")

    h = request.get_cookie(ADMIN_COOKIE_KEY, None, ADMIN_COOKIE_SECRET)
    user = get_admin_by_hash(h)
    kwargs.update(db.entities)
    kwargs['alert_data'] = alert
    return bottle.jinja2_template(
        str(source).lstrip('/') + extension,

        meta_title=template_title,
        settings=get_all_settings(),
        paginator=paginator,

        desc=desc,
        select=select,

        meta_description=get_settings("description", ""),

        favicon=headers.get('favicon', ''),
        logo=get_settings('other').get('logo', ''),

        admin_user=user,
        config=config,
        is_current_page=is_current_page,

        domain="%s://%s" % (request.urlparts.scheme, request.urlparts.netloc),
        # including_page=None if self_stationary_page
        # else (including_page or join("view", source + extension)),
        **kwargs
    )


@wraps(bottle.redirect)
def redirect(url: PathLike = None, code: int = None, alert: Alert = None, **kwargs):
    if url is None:
        url = request.url
    if kwargs or alert:
        if alert:
            kwargs['alert'] = dumps(alert.conv)
        response.set_cookie("kwargs", dumps(kwargs), ADMIN_COOKIE_SECRET, path="/")
    raise bottle.redirect(str(url), code)


@wraps(bottle.Bottle.route)
def route(p=None, method='GET', callback=None, name=None,
          apply=None, skip=None, disable=False, **config):
    def wrap(func):
        if disable:
            return

        def wrapped(*args, **kwargs):
            with db_session:
                res = func(*args, **kwargs)
            return res

        path = str(p)
        print(path)
        app.route(path, method, callback, name,
                  apply, skip, **config)(wrapped)

        path = (path + '/').replace('//', '/')
        app.route(path, method, callback, name,
                  apply, skip, **config)(wrapped)
        return wrapped

    return wrap
