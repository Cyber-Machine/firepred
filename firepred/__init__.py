from flask import Flask

from firepred.routes.home import home_bp
from firepred.routes.predict import predict_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(predict_bp)

    return app
