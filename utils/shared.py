from flask import g
from flask import current_app
import redis


def get_redis_revoke_list():
    if 'db' not in g:
        redis_url = current_app.config['REDIS_URL']
        g.db = redis.StrictRedis(host=redis_url, port=6379, db=0)
    return g.db
