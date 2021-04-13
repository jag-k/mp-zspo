from html import unescape

from lib import *

BASE_URL = Path('pages')
ADMIN_BASE_URL = ADMIN_ROUTE / BASE_URL


@admin_route(BASE_URL)
def admin_new_news():
    return admin_temp(
        BASE_URL / "index",
        data=Post.select(),
    )


@admin_route(BASE_URL / "new", GET_POST)
def admin_new_news():
    if request.method == POST:
        params = dict(request.params)
        p = Post(
            title=unescape(params["title"]),
            description=unescape(params["description"]),
            content=unescape(params["content"]),
            date=date.today().isoformat(),
            hidden=bool(params.pop("published", False)),
        )
        commit()
        if params.get('header'):
            h = Header(
                name=p.title,
                url=str(BASE_URL / str(p.id)).lstrip('/')
            )
            commit()
            p.header = h
            commit()
            redirect(ADMIN_BASE_URL, alert=Alert("Вы создали новую страницу и ссылку в шапке!"))

        redirect(ADMIN_BASE_URL, alert=Alert("Вы создали новую страницу!"))

    return admin_temp(
        BASE_URL / "new",
        data={},
    )


@admin_route(BASE_URL / "edit" / ID, GET_POST)
def admin_edit_news(id: int):
    p = Post[id]
    if request.method == POST:
        params = dict(request.params)
        name = unescape(params["title"])
        p.set(
            title=name,
            description=unescape(params["description"]),
            content=unescape(params["content"]),
            hidden=bool(params.pop("published", False)),
        )
        if not params.get('header'):
            p.header.delete()
            p.header = None
        elif p.header:
            p.header.name = name
        else:
            p.header = Header(
                name=name,
                url=str(BASE_URL / str(p.id)).lstrip('/')
            )
        commit()
        redirect(ADMIN_BASE_URL, alert=Alert("Вы отредактировали страницу!"))

    return admin_temp(
        BASE_URL / "new",
        date=date.today().isoformat(),
        data=get_json(p),
    )


@admin_route(BASE_URL / "del" / ID)
def admin_new_news(id: int):
    Post[id].delete()
    commit()
    redirect(ADMIN_BASE_URL, alert=Alert("Страница успешно удалена!"))
