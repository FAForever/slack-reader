import flask
from slackviewer.archive import archive

app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


@app.route("/channel/<name>")
def channel_name(name):
    messages = archive.get_messages(name)
    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(archive.get_channel_ids_by_name()))


@app.route("/")
def index():
    return channel_name('general')
