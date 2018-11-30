# My Idea Pool
Prod API Endpoint - http://ideapool.meetm.co

Swagger UI (via flask-restplus) enables API interaction directly from browser  

## To run in prod
* virtualenv -p /usr/bin/python3 mip
* pip install -r requirements.txt
* Initialize secret env variables
* python -m flask db init (only once)
* python -m flask db migrate (on any change in model)
* python -m flask db upgrade (on any change in model)
* python -m flask run --host=0.0.0.0

## Infrastructure Info

Currently running on EC2, using RDS MySQL DB to store users and ideas information.
Using Redis via Elastic cache to store JWT revocation info.

## Major frameworks and libraries used

- Flask
- Flask-Restplus
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended