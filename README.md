# A minimal example of a load test using Locust on Flask-SQLAlchemy + Flask-RESTPlus CRUD App.


## Introduction

Locust is an open source load testing tool which allows you to define load testing scenarions under a locustfile.py file.
Very handy to hook up python integration tests with load testing.

Flask SQLAlchemy simplifies the setup of the SQLAlchemy ORM into a Flask application.

Flask RESTPLus automatically adds swagger docs to your Flask REST api.

This project is a TODO CRUD from Flask RESTplus website using Flask SQLAlchemy to store the TODOs. It is then load tested with Locust.

## Quick start

```
pip install -r requirements.txt  # Install dependencies
python init_db.py  # Creates the database.
python backend.py  # Starts the backend.
locust --host=http://localhost:5000
```

Open http://127.0.0.1:5000 to check you TODO list REST API!
Open http://127.0.0.1:8089 and start your load test!

## More

http://docs.locust.io/en/latest/quickstart.html
https://flask-restplus.readthedocs.io/en/stable/
http://flask-sqlalchemy.pocoo.org/2.1/
