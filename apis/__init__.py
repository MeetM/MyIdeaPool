from flask_restplus import Api

from .sign_up import api as sign_up_api

api = Api(
    title='My Idea Pool API',
    version='1.0',
    description='For CodeMentorX',
)

api.add_namespace(sign_up_api)
