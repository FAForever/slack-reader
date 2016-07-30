import argparse
from slackviewer.app import app


def _configure_app():
    parser = argparse.ArgumentParser(usage='Public slack team viewer')
    parser.add_argument('-d', '--debug', action='store_true', help='enable flask debugging')
    args = parser.parse_args()
    return args.debug


def main():
    debug = _configure_app()
    app.run(host="0.0.0.0", debug=debug)
