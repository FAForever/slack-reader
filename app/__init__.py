import argparse
import flask
from flask_socketio import SocketIO
import eventlet

from app.libs.redis import host

socketio = SocketIO()
eventlet.monkey_patch()


def _register_blueprints(app):
    from app.routes.index import index
    app.register_blueprint(index, url_prefix='/api/v1')

    return app


def _parse_args():
    parser = argparse.ArgumentParser(usage='Public slack team viewer')
    parser.add_argument('-d', '--debug', action='store_true', help='enable flask debugging')
    return vars(parser.parse_args())


def _configure_app():
    app = flask.Flask(__name__, static_folder="static")
    return app


def _configure_socketio(app):
    socketio.init_app(app, message_queue='redis://{}'.format(host))


def create_app():
    app = _configure_app()
    app = _register_blueprints(app)

    args = _parse_args()
    _configure_socketio(app)

    return app, args
