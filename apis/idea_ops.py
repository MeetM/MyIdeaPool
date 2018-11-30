from flask_restplus import Namespace, fields, Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)
from flask import request
from models import db
from models.idea import Idea
from utils.validation_checker import is_password_invalid, is_email_invalid

api = Namespace('ideas', description="Create and update ideas")

# Swagger params
_idea_create_request = api.model('create-idea', {
    'content': fields.String(required=True, description='Content'),
    'impact': fields.Integer(required=True, description='Impact score between 1 to 10'),
    'ease': fields.Integer(required=True, description='Ease score between 1 to 10'),
    'confidence': fields.Integer(required=True, description='Confidence score between 1 to 10')
})

_idea_create_response = api.model('new-idea', {
    'id': fields.Integer(required=True, description='Id'),
    'content': fields.String(required=True, description='Content'),
    'impact': fields.Integer(required=True, description='Impact score between 1 to 10'),
    'ease': fields.Integer(required=True, description='Ease score between 1 to 10'),
    'confidence': fields.Integer(required=True, description='Confidence score between 1 to 10'),
    'average_score': fields.Float(required=True, description='Average score'),
    'created_at': fields.Integer(required=True, description='Timestamp of Idea creation')
})

_idea_delete_request = api.model('delete-idea', {
    'id': fields.Integer(required=True, description='Idea Id')
})

_header_parser = api.parser()
_header_parser.add_argument('X-Access-Token', location='headers')


@api.route('')
class CreateIdea(Resource):

    @api.expect(_idea_create_request, _header_parser, validate=True)
    @api.response(code=201, model=_idea_create_response, description="Idea created successfully")
    @jwt_required
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        # TODO idea params validation
        idea = Idea(user_id=user_id, **data)
        db.session.add(idea)
        db.session.commit()
        # TODO implement a object level get idea method
        return Idea.get_idea_json(idea.idea_id), 201


@api.route('/<string:idea_id>')
class DeleteIdea(Resource):
    @api.expect(_header_parser, validate=True)
    @api.response(code=204, description="Idea deleted Successfully")
    @jwt_required
    def delete(self, idea_id):
        user_id = get_jwt_identity()
        idea = Idea.get_idea(int(idea_id))
        if idea.user_id == user_id:
            db.session.delete(idea)
            db.session.commit()
            return None, 204
        return {"error": "User not authorized to delete the idea"}, 400
