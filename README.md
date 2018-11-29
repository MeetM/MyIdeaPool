# My Idea Pool
Prod API Endpoint - http://ideapool.meetm.co

## To run in prod
* pip install -r requirements.txt
* Initialize secret env variables
* python -m flask db init (only once)
* python -m flask db migrate (on any change in model)
* python -m flask db upgrade (on any change in model)
* python -m flask run --host=0.0.0.0

