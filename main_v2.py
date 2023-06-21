"""
A sample flask application on Cloud Run. Version 1
Articles Link
https://blog.devgenius.io/deploy-a-flask-app-with-docker-google-cloud-run-and-cloud-sql-for-postgresql-6dc9e7f4c434

"""
import os
import sqlalchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from webargs import fields
from webargs.flaskparser import use_args

DATABASE_HOST = "10.115.225.3"
DATABASE_USER = "meusuario"
DATABASE_PASSWORD = "123456"
DATABASE_NAME = "cloud_test"
DATABASE_PORT = "3306"

# Helper Functions
def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    db_host = DATABASE_HOST
    db_user = DATABASE_USER
    db_pass = DATABASE_PASSWORD
    db_name = DATABASE_NAME
    db_port = DATABASE_PORT

    pool = sqlalchemy.crerate_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )

    return pool

def get_connect_url():
    db_host = DATABASE_HOST
    db_user = DATABASE_USER
    db_pass = DATABASE_PASSWORD
    db_name = DATABASE_NAME
    db_port = DATABASE_PORT
    
    return sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        )

# Initialise flask app
app = Flask(__name__)

# Cria uma instância do SQLAlchemy
app.config["SQLALCHEMY_DATABSE_URI"] = get_connect_url()

db = SQLAlchemy(app)


@app.route("/hello", methods=["GET"])
def hello():
    """Method 1: Return a simple hello"""
    return "Hello", 200


@app.route("/hello/<my_name>", methods=["GET"])
def hello_name(my_name):
    """Method 2: Return hello with name, given in url"""
    return f"Hello from url, {my_name}", 200


@app.route("/hello_body", methods=["POST"])
@use_args(argmap={"my_name": fields.Str(required=True)})
def hello_from_body(args):
    """Method 3: Return hello with name, given in body"""
    my_name = args.get("my_name", "")
    return f"Hello from body, {my_name}", 200


@app.route("/", methods=["GET"])
def top_page():
    """top_page"""
    return "Welcome to my application, version 1\n"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))