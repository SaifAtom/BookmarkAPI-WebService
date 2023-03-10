# BookMark API for WebService
By: Saif Eddine Essghaier | Major: IT Minor: BA

Using Flask to build a BookMark Restful API Server with Swagger document.

Integration with Flask, Swagger, Flask-SQLalchemy, Flask-jwt-extended, werkzeug and validators extensions.

### Extension:
- Restful: [Flask](https://flask.palletsprojects.com/en/2.2.x/api/)

- SQL ORM: [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

- Swagger: [Swagger](https://swagger.io/solutions/api-documentation/)

- Flask-jwt-extended: [Flask-OAuth](https://flask-jwt-extended.readthedocs.io/en/stable/)

- werkzeug: [werkzeug](https://werkzeug.palletsprojects.com/en/2.2.x/)


## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
|──────src/
| |──────config/
| | |────swagger.py
| |──────constants/
| | |────http_status_codes.py
| |──────docs/
| | |────login.yaml
| | |────register.yaml
| | |────short_url.yaml
| | |────stats.yaml
| |──────__init__.py
| |──────auth.py
| |──────bookmarks.py
| |──────database.py
|──────venv/
|──────instance/
| |──────bookmarks.db
|──────.flaskenv
|──────.gitignore
|──────.env
|──────README.md
|──────requirements.txt

```


## Flask Configuration

#### Configure ENVIRONMENT variables in .flashenv and .env

```
export FLASK_ENV=development
export FLASK_APP=src
export SQLALCHEMY_DB_URI=sqlite:///bookmarks.db
export JWT_SECRET_KEY='JWT_SECRET_KEY'
SECRET_KEY=dev

```

## Run Flask
### Run flask for develop
```
$ flask run
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/api`

### Run flask for production

** Run with gunicorn **

In  webapp/

```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```

* -w : number of worker
* -b : Socket to bind




## Reference

Offical Website

- Restful: [Flask](https://flask.palletsprojects.com/en/2.2.x/api/)
- SQL ORM: [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- Swagger: [Swagger](https://swagger.io/solutions/api-documentation/)
- Flask-jwt-extended: [Flask-OAuth](https://flask-jwt-extended.readthedocs.io/en/stable/)
- werkzeug: [werkzeug](https://werkzeug.palletsprojects.com/en/2.2.x/)
