from project.application import create_app
from project.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run(port=81, host="0.0.0.0" ,threaded=True)