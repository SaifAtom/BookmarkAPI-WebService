from flask import Flask, redirect, jsonify
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmark
from flask_jwt_extended import JWTManager
import src.constants.http_status_codes as error
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            SWAGGER={"title": "Bookmarks API WebService Project", "uiversion": 3},
        )

    else:
        app.config.from_mapping(test_config)

    # INTIATE APP WITH DATABASE
    db.app = app
    db.init_app(app)

    # INITIATE JWT WITH APP
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    # INTIALIZE SWAGGER
    Swagger(app, config=swagger_config, template=template)

    # REDIRECT SHORT_URL TO URL
    @app.get("/<short_url>")
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits + 1
            db.session.commit()
            return redirect(bookmark.url)

    # ERROR HANDLERS
    @app.errorhandler(error.HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not found"}), error.HTTP_404_NOT_FOUND

    @app.errorhandler(error.HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify({"error": "Something went wrong, we are working on it"}),
            error.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
