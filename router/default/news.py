from lib import *

BASE_URL = Path('/news')


@route(BASE_URL)
def news_page():
    headers = get_settings("headers")

    return template(
        "news",
        template_title=headers.get('news', "Блог"),
        template_description=headers.get('description_news', ""),
        data=get_json_list(News),
    )


@route(BASE_URL / ID)
def news_post_page(id: int):
    if exists(n for n in News if n.id == id):
        n = News[id]
        # category = n["category"]["id"]
        return template(
            "news_post",
            template_title=n.title + " | Блог",
            template_description=n.description,
            post=get_json(n),
            categories=get_json_list(Category),
        )
    redirect(BASE_URL, alert=Alert("Пост не найден."))

