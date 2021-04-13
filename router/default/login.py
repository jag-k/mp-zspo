from lib import *


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

