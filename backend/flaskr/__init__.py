import os
from flask import Flask, redirect, request

from flaskr.db import db, ma

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, static_folder='app', static_url_path='/app')
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "zakroma.sqlite"),
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, "zakroma.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    #from flaskr import db
    db.init_app(app)
    
    # apply the blueprints to the app
    from .routes import bloh, afonarizms, humor_pump, horoscope, about

    app.register_blueprint(bloh.bp, url_prefix='/api/v1')
    app.register_blueprint(afonarizms.bp, url_prefix='/api/v1')
    app.register_blueprint(humor_pump.bp, url_prefix='/api/v1')
    app.register_blueprint(horoscope.bp, url_prefix='/api/v1')
    app.register_blueprint(about.bp, url_prefix='/api/v1')


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        secure_connection = request.base_url[:5] != 'http:'

        if secure_connection:   #development
        # if not secure_connection: #production
            return redirect(request.base_url.replace('http', 'https'))
        
        return  app.send_static_file("index.html")

    return app
