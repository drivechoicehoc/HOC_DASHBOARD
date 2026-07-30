import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database", "hoc_dashboard.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False