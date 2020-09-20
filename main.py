from bottle import HTTPResponse, static_file, run, request
from lib import *
import html
from pony.converting import str2datetime


@route("/")
def main_page():
    return template(
        "main",
        template_title="title tag",
        template_description="description tag",

        blog=get_json_list(Blog),
        categories=get_json_list(Category),
        faq=get_json_list(FAQ),
        
        main_settings = get_settings("main"),

        active_header=Header.MAIN,
    )


@route("/bookform")
def main_page():
    return template(
        "bookform",
        template_title="title tag",
        template_description="description tag",

        active_header=Header.TIME,
    )


@route("/blog")
def blog_page():
    return template(
        "blog",
        template_title="title tag",
        template_description="description tag",
        categories=get_json_list(Category),
        blog=get_json_list(Blog),

        active_header=Header.BLOG,
    )


@route("/directions")
def directions_page():
    return template(
        "directions",
        template_title="title tag",
        template_description="description tag",

        active_header=Header.DIRECTION,
    )


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
def admin_pages_meta():
    if request.method == POST:
        update_settings("main", dict(request.params))
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
            update_settings("socials", dict(request.params))
        return redirect("/admin/socials", alert=Alert("Социалки успешно сохранены!"))

    with db_session:
        data = get_settings("socials")

    return admin_temp(
        "socials",
        socials=data
    )


@admin_route("/about_me", GET_POST)
def admin_pages_meta():
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
        params["title"] = html.unescape(params["title"])
        params["description"] = html.unescape(params["description"])
        params["category"] = params.get("category")
        params["content"] = html.unescape(params["content"])
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
def admin_new_news(id: int):
    n = Blog[id]
    if request.method == POST:
        params = dict(request.params)
        print("params", params)
        n.set(
            title=html.unescape(params["title"]),
            description=html.unescape(params["description"]),
            category=params.get("category"),
            content=html.unescape(params["content"]),
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


@admin_route("/faq", GET_POST)
def admin_new_news():
    if request.POST:
        c = FAQ(
            question=request.params.get('question'),
            answer=request.params.get('answer'),
        )
        print(c)
        redirect(
            "/admin/faq",
            alert=Alert("Вы успешно создали вопрос-ответ!")
        )

    return admin_temp(
        "faq",
        data=get_json_list(FAQ),
    )


@admin_route("/faq/del/<id:int>")
def admin_new_news(id: int):
    FAQ[id].delete()
    commit()
    redirect('/admin/faq', alert=Alert("Вопрос-ответ успешно удалён!"))


@admin_route("/faq/edit/<id:int>", POST)
def admin_new_news(id: int):
    c = FAQ[id]
    c.set(
            question=request.params.get('question'),
            answer=request.params.get('answer'),
        )
    print(c)
    redirect(
        "/admin/faq",
        alert=Alert("Вы успешно отредактировали вопрос-ответ!")
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
    run(app=app, host="0.0.0.0", port=8080, quiet=False, reloader=True)
