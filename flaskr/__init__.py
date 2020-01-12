import os 
from flask import Flask 

def create_app(env="stg"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if env == 'stg':
        app.config.from_pyfile("stg.cfg", silent=False)
    else:
        app.config.from_pyfile("prod.cfg", silent=False)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass 

    @app.route("/hello")
    def hello():
        return 'Hello, World!'

    # from . import db
    # db.init_app(app)
    # from . import auth
    # app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint="index")

    return app