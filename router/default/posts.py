from lib import *

BASE_URL = Path('/pages')


@route(BASE_URL / ID)
def news_post_page(id: int):
    if exists(n for n in Post if n.id == id):
        n = Post[id]
        # category = n["category"]["id"]
        return template(
            "pages_post",
            template_title=n.title,
            template_description=n.description,
            post=get_json(n),
        )
    redirect(BASE_URL, alert=Alert("Пост не найден."))

