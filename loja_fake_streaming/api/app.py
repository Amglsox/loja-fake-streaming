import logging

from flask import Flask


logger = logging.getLogger()
logger.level = logging.DEBUG


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = True
    with app.app_context():
        from routes.resources import routes

        app.register_blueprint(routes)
    return app


app = create_app()
