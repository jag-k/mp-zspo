from html import unescape

from pony.converting import str2datetime

from lib import *

BASE_URL = Path('/news')
ADMIN_BASE_URL = ADMIN_ROUTE / BASE_URL


@admin_route(BASE_URL)
def admin_new_news():
    return admin_temp(
        BASE_URL / "index",
        data=get_json_list(News),
    )


@admin_route(BASE_URL / "new", GET_POST)
def admin_new_news():
    if request.method == POST:
        params = dict(request.params)
        n = News(
            title=unescape(params["title"]),
            description=unescape(params["description"]),
            content=unescape(params["content"]),
            date=str2datetime(params["date"]),
            image="",
            hidden=bool(params.pop("published", False)),
        )
        commit()
        image = save_img("news_" + str(n.id), "news")
        n.image = image
        commit()

        redirect(ADMIN_BASE_URL, alert=Alert("Вы создали новый пост в блоге!"))

    return admin_temp(
        BASE_URL / "new",
        date=date.today().isoformat(),
        data={},
    )


@admin_route(BASE_URL / "edit" / ID, GET_POST)
def admin_edit_news(id: int):
    n = News[id]
    if request.method == POST:
        params = dict(request.params)
        print("params", params)
        n.set(
            title=unescape(params["title"]),
            description=unescape(params["description"]),
            category=params.get("category"),
            content=unescape(params["content"]),
            date=str2datetime(params["date"]),
            hidden=bool(params.pop("published", False)),
        )

        commit()
        print(n.category)
        if request.files.get('image'):
            image = save_img("news_" + str(n.id), "news")
            n.image = image
            commit()

        redirect(ADMIN_BASE_URL, alert=Alert("Вы отредактировали пост в блоге!"))

    return admin_temp(
        BASE_URL / "new",
        date=date.today().isoformat(),
        data=get_json(n),
    )


@admin_route(BASE_URL / "del" / ID)
def admin_new_news(id: int):
    News[id].delete()
    commit()
    redirect(ADMIN_BASE_URL, alert=Alert("Пост успешно удалён!"))


@admin_route(Path("/toggle_public_news") / ID)
def admin_edit_news(id):
    n = select(n for n in News if n.id == id).first()
    d = n.draft
    n.draft = not d
    redirect(BASE_URL, alert=Alert("Вы {} новость!".format('опубликовали' if d else 'скрыли')))
