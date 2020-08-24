from bottle import HTTPResponse, static_file, run, request
from lib import *


@route("/")
def main_page():
    return template(
        "main",
        template_title="title tag",
        template_description="description tag"
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
