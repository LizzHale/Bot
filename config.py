import os

# Config file, put all your keys and passwords and whatnot in here
DB_URL = os.environ.get("DATABASE_URL", "sqlite://bob.db")
SECRET_KEY = os.environ.get("SECRET_KEY")
