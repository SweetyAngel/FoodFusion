from flask import Flask
from .models import create_table

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    create_table()

    from .routes import main
    app.register_blueprint(main)

    return app
