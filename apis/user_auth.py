from flask_restplus import Namespace, fields, Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_raw_jwt,
    get_jti,
    jwt_refresh_token_required,
    get_jwt_identity
)
from auth.token_ops import revoke_tokens
from models.user import User


# Swagger parameters
api = Namespace('access-tokens', description="Manage user log-in and log-out")

_user_login = api.model('User-Login', {
    'email': fields.String(required=True, description='user email address'),
    'password':  fields.String(required=True, description='user password')
})

_login_response = api.model('login-response', {
    'access_token': fields.String(required=True, description='Refresh token for the user'),
    'refresh_token': fields.String(required=True, description='Refresh token for the user')
})

_refresh_token_request = api.model('refresh-token', {
    'refresh_token': fields.String(required=True, description='Refresh token for the existing user')
})

_refresh_response = api.model('refresh-response', {
    'access_token': fields.String(required=True, description='Refresh token for the user')
})

_header_parser = api.parser()
_header_parser.add_argument('X-Access-Token', location='headers')


@api.route('')
class UserAuth(Resource):

    @api.doc("User login - Returns JWT Access and Refresh tokens")
    @api.expect(_user_login, validate=True)
    @api.response(code=201, model=_login_response, description="Login Successful")
    def post(self):
        data = request.get_json()
        user = User.authenticate(**data)

        if not user:
            return {'message': 'Invalid credentials', 'authenticated': False}, 401

        access_token = create_access_token(identity=user.email, fresh=True)
        refresh_token = create_refresh_token(user.email)
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token
               }, 201

    @api.doc("User logout")
    @api.expect(_refresh_token_request, _header_parser, validate=True)
    @api.response(code=204, description="Logout Successful")
    @jwt_required
    def delete(self):
        data = request.get_json()
        refresh_token = data["refresh_token"]
        access_token_jti = get_raw_jwt()['jti']
        refresh_token_jti = get_jti(refresh_token)
        revoke_tokens(access_token_jti, refresh_token_jti)
        return None, 204


@api.route('/refresh')
class RefreshToken(Resource):
    @api.doc("Refresh Access token")
    @api.expect(_refresh_token_request, validate=True)
    @api.response(code=200, model=_refresh_response, description="Refresh Successful")
    @jwt_refresh_token_required
    def post(self):
        email = get_jwt_identity()
        access_token = create_access_token(identity=email, fresh=False)
        return {'access_token': access_token}, 201
