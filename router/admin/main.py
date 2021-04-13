from lib import *


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
        redirect(ADMIN_ROUTE / "main_page", alert=Alert("Главная страница успешно обновлена!"))

    data = get_settings("main")

    return admin_temp(
        "main",
        data=data
    )


@admin_route("/other", GET_POST)
def admin_pages_other_settings():
    if request.method == POST:
        par = dict(request.params)
        for filename in request.files:
            par[filename] = save_img(filename, '', filename)

        for key, value in list(par.items()):
            if isinstance(value, bytes):
                del par[key]

        update_settings("other", par)
        redirect(ADMIN_ROUTE / "other", alert=Alert("Настройки сохранены!"))

    data = get_settings("other")

    return admin_temp(
        "other",
        data=data
    )


@admin_route("/meta", GET_POST)
def admin_pages_meta():
    if request.method == POST:
        update_settings("meta", dict(request.params))
        redirect(ADMIN_ROUTE / "meta", alert=Alert("Метатеги успешно сохранены!"))

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
        return redirect(ADMIN_ROUTE / "socials", alert=Alert("Социалки успешно сохранены!"))

    data = get_settings("socials")

    return admin_temp(
        "socials",
        data=data
    )


@admin_route("/about_me", GET_POST, True)
def admin_about_me():
    if request.method == POST:
        update_settings("about", dict(request.params))
        redirect(ADMIN_ROUTE / "about_me", alert=Alert('Блок "Обо мне" изменен!'))

    data = get_settings("about")

    return admin_temp(
        "about_me",
        data=data
    )

