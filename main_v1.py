"""
A sample flask application on Cloud Run. Version 1
Articles Link
https://blog.devgenius.io/deploy-a-flask-app-with-docker-google-cloud-run-and-cloud-sql-for-postgresql-6dc9e7f4c434

"""
import os

from flask import Flask

from webargs import fields
from webargs.flaskparser import use_args

# Initialise flask app
app = Flask(__name__)

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