from lib import *

if os.getenv("DEVELOP") == "True":
    @route("/create_admin", GET_POST, True)
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
