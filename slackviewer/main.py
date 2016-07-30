import argparse
from slackviewer.app import app


def _configure_app():
    parser = argparse.ArgumentParser(usage='Public slack team viewer')
    parser.add_argument('-d', '--debug', action='store_false', help='enable flask debugging')
    args = parser.parse_args()

    if args.debug:
        print("WARNING: DEBUG MODE IS ENABLED!")
    app.config["PROPAGATE_EXCEPTIONS"] = True
    return args.debug


def main():
    debug = _configure_app()
    app.run(debug=debug)
