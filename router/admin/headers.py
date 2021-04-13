import bottle

from lib import *

BASE_URL = Path('headers')
ADMIN_BASE_URL = ADMIN_ROUTE / BASE_URL


@admin_route(BASE_URL, GET_POST)
def admin_headers():
    name = None
    url = None
    if request.POST:
        name = request.params.get('name')
        url = request.params.get('url')

    elif request.query.get('name'):
        name = request.query.get('name')
        url = request.query.get('url')

    if name:
        c = Header(
            name=name,
            url=url,
        )
        print(c)
        redirect(
            ADMIN_BASE_URL,
            alert=Alert("Вы успешно создали ссылку в шапке!")
        )

    return admin_temp(
        "headers",
        data=get_json_list(Header),
    )


@admin_route(BASE_URL / "del" / ID)
def admin_del_header(id: int):
    Header[id].delete()
    commit()
    redirect(ADMIN_BASE_URL, alert=Alert("Ссылка успешно удалена из шапки!"))


@admin_route(BASE_URL / "edit" / ID, POST)
def admin_new_header(id: int):
    c = Header[id]
    c.set(
        name=request.params.get('name'),
        url=request.params.get('url'),
    )
    print(c)
    redirect(
        ADMIN_BASE_URL,
        alert=Alert("Вы успешно отредактировали ссылку!")
    )
