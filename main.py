from bottle import HTTPResponse, static_file, run, request
from lib import *


@route("/")
def main_page():
    return template(
        "main",
        template_title="title tag",
        template_description="description tag"
    )


@route("/bookform")
def main_page():
    return template(
        "bookform",
        template_title="title tag",
        template_description="description tag"
    )


@route("/blog")
def blog_page():
    return template(
        "blog",
        template_title="title tag",
        template_description="description tag"
    )


@route("/directions")
def directions_page():
    return template(
        "directions",
        template_title="title tag",
        template_description="description tag"
    )


@route("/edit")
def main_page():
    return template(
        "admin/edit",
        template_title="title tag",
        template_description="description tag",
        data={}
    )


@route(ADMIN_LOGIN_ROUTE, method=GET_POST)
def login():
    alert = None
    if request.POST:
        h = hash_admin(request.forms.get("login"), request.forms.get("password"))
        if is_hash_admin(h):
            response.set_cookie(ADMIN_COOKIE_KEY, h, ADMIN_COOKIE_SECRET, max_age=604800, httponly=True)
            redirect_from = request.get_cookie("redirect", "/admin", ADMIN_COOKIE_SECRET)
            return redirect(redirect_from)
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
        "edit",
        description="None"
    )


@admin_route("/blog/new", GET_POST)
def admin_new_news():
    if request.method == POST:
        params = dict(request.params)
        params["title"] = html.unescape(params["title"])
        params["description"] = html.unescape(params["description"])
        params["direction"] = params.get("description", 0)
        params["content"] = html.unescape(params["content"])
        params["custom_link"] = html.unescape(params.get("custom_link", "")) or None
        params["date"] = str2datetime(params["date"])
        params["image"] = ""
        params["draft"] = "published" not in params
        if "published" in params:
            del params["published"]

        with db_session:
            n = Blog(**params)
            commit()
            image = save_img("blog_" + str(n.id), "blog")
            n.image = image
            commit()

        return redirect("/admin/blog", alert=Alert("Вы создали новый пост в блоге!"))

    return admin_temp(
        "new/blog",
        date=date.today().isoformat(),
    )


@admin_route("/blog/edit/<id:int>", GET_POST)
def admin_edit_news(id):
    with db_session:
        n = select(n for n in Blog if n.id == id).first().to_dict(with_collections=True, related_objects=True)

    n["date"] = n["date"].isoformat()
    pprint(n)

    if request.method == POST:
        params = dict(request.params)
        with db_session:
            n = Blog[id]
            params["title"] = html.unescape(params["title"])
            params["content"] = html.unescape(params["content"])
            params["date"] = str2datetime(params["date"])
            params["draft"] = "published" not in params
            if "published" in params:
                del params["published"]
            if request.files.get("image"):
                image = save_img("blog_" + str(n.id), "blog")
                params["image"] = image
            elif "image" in params:
                del params['image']
            n = n.set(**params)

        return redirect("/admin/blog", alert=Alert("Вы отредактировали новость!"))

    return admin_temp(
        "edit/blog",
        data=n
    )


@admin_route("/toggle_public_blog/<id:int>")
def admin_edit_news(id):
    with db_session:
        n = select(n for n in Blog if n.id == id).first()
        d = n.draft
        n.draft = not d
    return redirect("/admin/blog", alert=Alert("Вы %s новость!" % ('опубликовали' if d else 'скрыли')))


if os.getenv("DEVELOP") == "True":
    @route("/create_admin", GET_POST)
    def create_admin_page():
        if request.POST:
            create_admin(
                request.forms.get("login"),
                request.forms.get("password"),
                request.forms.get("name", ""),
            )

            return redirect("/")

        return template(
            "create_user"
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
