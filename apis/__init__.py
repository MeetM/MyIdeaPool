from flask_restplus import Api

from .sign_up import api as sign_up_api
from .user_auth import api as user_auth_api

api = Api(
    title='My Idea Pool API',
    version='1.0',
    description='For CodeMentorX',
)

api.add_namespace(sign_up_api)
api.add_namespace(user_auth_api)