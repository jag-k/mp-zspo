from lib import *
from requests import post

# pylint: disable=no-member

@route("/", method=["get", "post"])
def main_page():

    if request.method == POST:

        message = "Имя:\n" + request.forms.name + "\n\nПочта:\n" + request.forms.email + "\n\nСообщение:\n" + request.forms.inputEmail1
        print(message)

        

    return template(
        "main",
        template_title="title tag",
        template_description="description tag"
    )



@route("/<file:path>")
def static(file):
    f = bottle.static_file(file, "./public")
    if f.status_code == 404:
        return template(
            "error",
            template_title="404",
        )
    return f


if __name__ == '__main__':
    bottle.run(app=app, host="0.0.0.0", port=8080, quiet=False, reloader=True)
