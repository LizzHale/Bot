To read about this project, please [visit the site!](http://mysterious-brushlands-7144.herokuapp.com/about)


Setup with an existing database:
* clone the repo
* cd into the repo
* Create a new virtual environment and active `virtualenv env & source env/bin/activate`
* Create and source the .env with the following environment variables:
DATABASE_URL
PORT
SECRET_KEY
HOST
BOT_PORT
NICK
IDENT
REALNAME
CHANNEL
PATH:<path/to/postgres/pg_config:$PATH
* Install requirements `pip install -r requirements.txt`
* start the web and worker processes `foreman start`

Setup a new database:
* Install postgres
* Create a new database and set the DATABASE_URL environment variable
* Create the tables by running `python tables.py`
* Seed the database (This takes approximately 3 hours) `pyton setupdata.py`


