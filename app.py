from flaskr import create_app
import os

if __name__ == "__main__":
    env = os.getenv('env', 'prod')
    app = create_app()
    app.run()