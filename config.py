import os

# Config file, put all your keys and passwords and whatnot in here
DB_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/bob")
SECRET_KEY = os.environ.get("SECRET_KEY")
HOST = os.environ.get("HOST")
BOT_PORT = os.environ.get("BOT_PORT")
NICK = os.environ.get("NICK")
IDENT = os.environ.get("IDENT")
REALNAME = os.environ.get("REALNAME")
CHANNEL = os.environ.get("CHANNEL")
