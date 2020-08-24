from bottle import HTTPResponse, static_file, run, request
from lib import *


@route("/")
def main_page():
    return template(
        "main",
        template_title="title tag",
        template_description="description tag"
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
