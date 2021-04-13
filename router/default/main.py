from lib import *


@route("/")
def main_page():
    headers = get_settings("headers")

    return template(
        "main",
        template_title=headers.get('main', "Молодёжный Парламент"),
        template_description=headers.get('description_main', ""),

        posts=get_json_list(Post),
        blocks=get_json_list(Block),
        categories=get_json_list(Category),
        news=get_json_list(News),

        about=get_settings("about"),
        main_settings=get_settings("main"),
    )

