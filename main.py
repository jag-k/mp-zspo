from html import unescape

from bottle import HTTPResponse, static_file, run
from pony.converting import str2datetime

from lib import *


@route("/")
def main_page():
    headers = get_settings("headers")

    return template(
        "main",
        template_title=headers.get('main', "Молодёжный портал"),
        template_description=headers.get('description_main', ""),

        posts=get_json_list(Post),
        blocks=get_json_list(Block),
        categories=get_json_list(Category),
        news=get_json_list(News),

        about=get_settings("about"),
        main_settings=get_settings("main"),
    )


@route("/news")
def blog_page():
    headers = get_settings("headers")

    return template(
        "blog",
        template_title=headers.get('blog', "Блог"),
        template_description=headers.get('description_blog', ""),
        categories=get_json_list(Category),
        posts=get_json_list(Post),
    )


@route("/blog/<id:int>")
def blog_post_page(id: int):
    if exists(b for b in Blog if b.id == id):
        b = Blog[id]
        # category = b["category"]["id"]
        return template(
            "blog_post",
            template_title=b.title + " | Блог",
            template_description=b.description,
            post=get_json(b),
            categories=get_json_list(Category),
        )
    else:
        redirect("/blog", alert=Alert("Пост не найден."))


@route(ADMIN_LOGIN_ROUTE, method=GET_POST)
def login():
    alert = None
    if request.POST:
        h = hash_admin(request.forms.get("login"), request.forms.get("password"))
        if is_hash_admin(h):
            response.set_cookie(ADMIN_COOKIE_KEY, h, ADMIN_COOKIE_SECRET, max_age=604800, httponly=True)
            redirect_from = request.get_cookie("redirect", "/admin", ADMIN_COOKIE_SECRET)
            redirect(redirect_from)
        else:
            alert = Alert(
                "Вы ввели не правильный логин или пароль! Повторите снова",
                Alert.DANGER
            )
    if request.params.get("from"):
        response.set_cookie('redirect', request.params.get("from", ADMIN_LOGIN_ROUTE), ADMIN_COOKIE_SECRET)

    return template(join("admin", "login"),
                    template_title="Вход в админку",
                    alert=alert,
                    )


@admin_route("/")
def admin():
    return admin_temp(
        "create_user",
        description="None",
    )


@admin_route("/main_page", GET_POST)
def admin_pages_main():
    if request.method == POST:
        par = dict(request.params)
        for filename in request.files:
            par[filename] = save_img(filename, "main_page", filename)

        for key, value in list(par.items()):
            if isinstance(value, bytes):
                del par[key]

        update_settings("main", par)
        redirect("/admin/main_page", alert=Alert("Главная страница успешно обновлена!"))

    data = get_settings("main")

    return admin_temp(
        "main",
        data=data
    )


@admin_route("/meta", GET_POST)
def admin_pages_meta():
    if request.method == POST:
        update_settings("meta", dict(request.params))
        redirect("/admin/meta", alert=Alert("Метатеги успешно сохранены!"))

    data = get_settings("meta")

    return admin_temp(
        "meta",
        data=data
    )


@admin_route("/socials", GET_POST)
def admin_pages_socials():
    if request.POST:
        with db_session:
            par = dict(request.params)
            for (key, value) in par.items():
                if PHONE_RE.match(value):
                    par[key] = '7' + ''.join(PHONE_RE.match(value).groups())
            update_settings("socials", par)
        return redirect("/admin/socials", alert=Alert("Социалки успешно сохранены!"))

    data = get_settings("socials")

    return admin_temp(
        "socials",
        data=data
    )


@admin_route("/about_me", GET_POST)
def admin_about_me():
    if request.method == POST:
        update_settings("about", dict(request.params))
        redirect("/admin/about_me", alert=Alert('Блок "Обо мне" изменен!'))

    data = get_settings("about")

    return admin_temp(
        "about_me",
        data=data
    )


@admin_route("/blog/new", GET_POST)
def admin_new_news():
    if request.method == POST:
        params = dict(request.params)
        params["title"] = unescape(params["title"])
        params["description"] = unescape(params["description"])
        params["category"] = params.get("category")
        params["content"] = unescape(params["content"])
        params["custom_link"] = params.get("custom_link", "")
        params["date"] = str2datetime(params["date"])
        params["image"] = ""
        params["draft"] = "published" not in params
        if "published" in params:
            del params["published"]

        n = Blog(**params)
        commit()
        image = save_img("blog_" + str(n.id), "blog")
        n.image = image
        commit()

        redirect("/admin/blog", alert=Alert("Вы создали новый пост в блоге!"))

    categories = get_json_list(Category)
    if not categories:
        redirect('/admin/blog/category', alert=Alert("У вас ещё нет категорий", Alert.WARNING))
    return admin_temp(
        "blog/new",
        date=date.today().isoformat(),
        data={},
        categories=get_json_list(Category),
    )


@admin_route("/blog/edit/<id:int>", GET_POST)
def admin_edit_news(id: int):
    n = Blog[id]
    if request.method == POST:
        params = dict(request.params)
        print("params", params)
        n.set(
            title=unescape(params["title"]),
            description=unescape(params["description"]),
            category=params.get("category"),
            content=unescape(params["content"]),
            custom_link=params.get("custom_link", ""),
            date=str2datetime(params["date"]),
        )

        commit()
        print(n.category)
        if request.files.get('image'):
            image = save_img("blog_" + str(n.id), "blog")
            n.image = image
            commit()

        redirect("/admin/blog", alert=Alert("Вы отредактировали пост в блоге!"))

    categories = get_json_list(Category)
    if not categories:
        redirect('/admin/blog/category', alert=Alert("У вас ещё нет категорий", Alert.WARNING))

    return admin_temp(
        "blog/new",
        date=date.today().isoformat(),
        data=get_json(n),
        categories=get_json_list(Category),
    )


@admin_route("/blog/category", GET_POST)
def admin_new_news():
    if request.POST:
        c = Category(
            name=request.params.get('name'),
        )
        print(c)
        redirect(
            "/admin/blog/category",
            alert=Alert("Вы успешно создали категорию!")
        )

    return admin_temp(
        "blog/category",
        data=get_json_list(Category),
    )


@admin_route("/blog")
def admin_new_news():
    return admin_temp(
        "blog/index",
        data=get_json_list(Blog),
    )


@admin_route("/blog/del/<id:int>")
def admin_new_news(id: int):
    Blog[id].delete()
    commit()
    redirect('/admin/blog', alert=Alert("Пост успешно удалён!"))


@admin_route("/blog/category/del/<id:int>")
def admin_new_news(id: int):
    Category[id].delete()
    commit()
    redirect('/admin/blog/category', alert=Alert("Категория успешно удалена!"))


@admin_route("/blog/category/edit/<id:int>", POST)
def admin_new_news(id: int):
    c = Category[id]
    c.set(
        name=request.params.get('name'),
    )
    print(c)
    redirect(
        "/admin/blog/category",
        alert=Alert("Вы успешно отредактировали категорию!")
    )


@admin_route("/headers", GET_POST)
def admin_new_news():
    if request.POST:
        c = Header(
            name=request.params.get('name'),
            url=request.params.get('url'),
        )
        print(c)
        redirect(
            "/admin/headers",
            alert=Alert("Вы успешно создали ссылку в шапке!")
        )

    return admin_temp(
        "headers",
        data=get_json_list(Header),
    )


@admin_route("/headers/del/<id:int>")
def admin_new_news(id: int):
    Header[id].delete()
    commit()
    redirect('/admin/headers', alert=Alert("Ссылка успешно удалена из шапки!"))


@admin_route("/headers/edit/<id:int>", POST)
def admin_new_news(id: int):
    c = Header[id]
    c.set(
        name=request.params.get('name'),
        url=request.params.get('url'),
    )
    print(c)
    redirect(
        "/admin/headers",
        alert=Alert("Вы успешно отредактировали ссылку!")
    )


@admin_route("/toggle_public_blog/<id:int>")
def admin_edit_news(id):
    n = select(n for n in Blog if n.id == id).first()
    d = n.draft
    n.draft = not d
    redirect("/admin/blog", alert=Alert("Вы %s новость!" % ('опубликовали' if d else 'скрыли')))


if os.getenv("DEVELOP") == "True":
    @route("/create_admin", GET_POST)
    def create_admin_page():
        if request.POST:
            create_admin(
                request.forms.get("login"),
                request.forms.get("password"),
                request.forms.get("name", ""),
            )

            redirect("/")

        return template(
            join("admin", "create_user")
        )


@admin_route("/ckeditor/upload_photo/<path:path>", POST)
def upload_photo(path):
    try:
        file = save_img(path=path, name_in_form="upload", overwrite=False)
        return {
            "url": file
        }
    except OSError:
        return {
            "error": {
                "message": "Изображение с таким именем существует. "
                           "Пожалуйста, переименуйте изображение и попробуйте снова."
            }
        }
    except Exception as err:
        return {
            "error": {
                "message": "Ошибка во время загрузки!\n(%s: %s)" % (type(err).__name__, err)
            }
        }


@route("/<file:path>")
def static(file):
    f = static_file(file, "./public")
    if f.status_code == 404:
        return HTTPResponse(
            body=template(
                "error",
                template_title="404",
            ),
            status=404
        )
    return f


if __name__ == '__main__':
    run(app=app, host="0.0.0.0", port=8080, quiet=False, reloader=True, debug=True)
