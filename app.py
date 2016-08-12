#!/usr/bin/env python
import logging
from logging.handlers import TimedRotatingFileHandler

from app import create_app, socketio
from app.libs.slack import slack

app, _args = create_app()


@app.before_first_request
def _spawn_other_threads():
    slack.start()


def _configure_logging(app):
    # System wide logging
    logger = logging.getLogger()

    log_fh = TimedRotatingFileHandler('logs/log', when='midnight', backupCount=30)
    log_fh.suffix = '%Y_%m_%d'
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)"')
    log_fh.setFormatter(formatter)

    stderr_fh = logging.StreamHandler()

    logger.addHandler(log_fh)
    logger.addHandler(stderr_fh)
    logger.setLevel(logging.DEBUG)

    # Flask app logging
    app.logger

if __name__ == '__main__':
    _configure_logging(app)
    logging.info('Starting server')
    socketio.run(app, **_args)
