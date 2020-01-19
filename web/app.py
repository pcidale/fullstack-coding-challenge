import argparse
from flask import Flask
from flask_migrate import Migrate
from routes import (unbabel_app, bad_request, page_not_found,
                    method_not_allowed, unprocessable, internal_server_error)
from models import db

migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(unbabel_app, url_prefix="/en-es")
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(422, unprocessable)
    app.register_error_handler(500, internal_server_error)

    db.init_app(app)
    migrate.init_app(app, db)

    return app, migrate


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unbabel Web App')
    parser.add_argument(
        '-e',
        '--env',
        choices=['dev', 'test', 'prod'],
        default='dev',
        dest='env',
        required=False,
        help='mode of run  (default: dev)'
    )
    parser.add_argument(
        '-p',
        '--port',
        default=8000,
        dest='port',
        type=int,
        required=False,
        help='app port  (default: 8000)'
    )
    args = parser.parse_args()

    config = {
        'dev': 'config.DevelopmentConfig',
        'test': 'config.TestingConfig',
        'prod': 'config.ProductionConfig'
    }.get(args.env)

    app, _ = create_app(config)
    app.run(host='0.0.0.0', port=args.port)
