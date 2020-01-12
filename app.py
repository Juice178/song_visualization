from flaskr import create_app
import os

env = os.getenv('env', 'prod')
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True)