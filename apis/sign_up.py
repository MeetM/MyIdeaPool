from flask_restplus import Namespace, fields, Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask import request
from models import db
from models.user import User

api = Namespace('users', description="User sign up")

# Swagger params
_signup_request = api.model('signup', {
    'email': fields.String(required=True, description='Email Address'),
    'name': fields.String(required=True, description='Name'),
    'password': fields.String(required=True, description='Password'),
})

_signup_response = api.model('signup-response', {
    'access_token': fields.String(required=True, description='Access token for the user'),
    'refresh_token': fields.String(required=True, description='Refresh token for the user')
})


@api.route('')
class SignUp(Resource):

    @api.expect(_signup_request, validate=True)
    @api.response(code=201, model=_signup_response, description="Sign-up successful")
    def post(self):
        data = request.get_json()
        # TODO Check for valid email and password
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.email, fresh=True)
        refresh_token = create_refresh_token(user.email)
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token
               }, 201
