from lib import *
from .news import BASE_URL as NEWS_URL

BASE_URL = NEWS_URL / "category"
ADMIN_BASE_URL = ADMIN_ROUTE / BASE_URL


@admin_route(BASE_URL, GET_POST)
def admin_new_news():
    if request.POST:
        c = Category(
            name=request.params.get('name'),
        )
        print(c)
        redirect(
            ADMIN_BASE_URL,
            alert=Alert("Вы успешно создали категорию!")
        )

    return admin_temp(
        BASE_URL,
        data=get_json_list(Category),
    )


@admin_route(BASE_URL / "del" / ID)
def admin_new_news(id: int):
    Category[id].delete()
    commit()
    redirect(ADMIN_BASE_URL, alert=Alert("Категория успешно удалена!"))


@admin_route(BASE_URL / "edit" / ID, POST)
def admin_new_news(id: int):
    c = Category[id]
    c.set(
        name=request.params.get('name'),
    )
    print(c)
    redirect(
        ADMIN_BASE_URL,
        alert=Alert("Вы успешно отредактировали категорию!")
    )
