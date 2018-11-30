from flask_restplus import Namespace, fields, Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from models.user import User


# Swagger parameters
api = Namespace('me', description="User profile")

_user_profile_response = api.model('user-profile-response', {
    'email': fields.String(required=True, description='User email address'),
    'name': fields.String(required=True, description='Name'),
    'avatar_url': fields.String(required=True, description='Avatar URL'),
})

_header_parser = api.parser()
_header_parser.add_argument('X-Access-Token', location='headers')


@api.route('')
class UserProfile(Resource):

    @api.expect(_header_parser, validate=True)
    @api.response(code=200, model=_user_profile_response, description="User Profile Info")
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        profile_info = User.get_profile_json(email)
        return profile_info, 200
