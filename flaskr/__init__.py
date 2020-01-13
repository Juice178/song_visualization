import os 
from flask import Flask
import logging

def create_app(env="stg"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.logger.setLevel(logging.ERROR)

    if env == 'stg':
        app.config.from_pyfile("stg.cfg", silent=False)
    else:
        app.config.from_pyfile("prod.cfg", silent=False)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass 

    from . import visualize
    app.register_blueprint(visualize.bp)
    app.add_url_rule('/', endpoint="index")

    return app