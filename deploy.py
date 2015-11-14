from project.application import create_app
from project.config import DeploymentConfig

app = create_app(DeploymentConfig)