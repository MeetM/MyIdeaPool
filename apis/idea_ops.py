from flask_restplus import Namespace, fields, Resource
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from flask import request
from models import db
from models.idea import Idea
from utils.validation_checker import are_idea_params

api = Namespace('ideas', description="Create, update and delete ideas")

create_idea_model = api.model('create-idea', {
        'content': fields.String(required=True, description='Content'),
        'impact': fields.Integer(required=True, description='Impact score between 1 to 10'),
        'ease': fields.Integer(required=True, description='Ease score between 1 to 10'),
        'confidence': fields.Integer(required=True, description='Confidence score between 1 to 10')
    })

detail_idea_model = api.model('new-idea', model={
    'id': fields.Integer(required=True, description='Id'),
    'content': fields.String(required=True, description='Content'),
    'impact': fields.Integer(required=True, description='Impact score between 1 to 10'),
    'ease': fields.Integer(required=True, description='Ease score between 1 to 10'),
    'confidence': fields.Integer(required=True, description='Confidence score between 1 to 10'),
    'average_score': fields.Float(required=True, description='Average score'),
    'created_at': fields.Integer(required=True, description='Timestamp of Idea creation')
})

idea_page_model = api.model('idea-page', model={'ideas': fields.List(fields.Nested(detail_idea_model))})

idea_page_req_parser = api.parser()
idea_page_req_parser.add_argument('page', type=int, location='args')
idea_page_req_parser.add_argument('X-Access-Token', location='headers')

access_token_header_parser = api.parser()
access_token_header_parser.add_argument('X-Access-Token', location='headers')


@api.route('')
class CreateIdeaGetIdeaPage(Resource):

    @api.doc("Create Idea")
    @api.expect(create_idea_model, access_token_header_parser, validate=True)
    @api.response(code=201, model=detail_idea_model, description="Idea created successfully")
    @jwt_required
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        if not are_idea_params(**data):
            return {"error": "Input parameters not valid. Scores should be between 1 and 10"}, 400
        idea = Idea(user_id=user_id, **data)
        db.session.add(idea)
        db.session.commit()
        return Idea.get_idea_json(idea.idea_id), 201

    @api.doc("Get Ideas Page")
    @api.expect(idea_page_req_parser, validate=True)
    @api.response(code=200, model=idea_page_model, description="Ideas Page")
    @jwt_required
    def get(self):
        data = request.args
        page = 1
        if data and "page" in data:
            page = data["page"]
        user_id = get_jwt_identity()
        return Idea.get_idea_page(user_id=user_id, page=int(page)), 200


@api.route('/<int:idea_id>')
class UpdateDeleteIdea(Resource):

    @api.doc("Delete idea")
    @api.expect(access_token_header_parser, validate=True)
    @api.response(code=204, description="Idea deleted Successfully")
    @jwt_required
    def delete(self, idea_id):
        user_id = get_jwt_identity()
        idea = Idea.get_idea(idea_id)
        if idea.user_id == user_id:
            db.session.delete(idea)
            db.session.commit()
            return None, 204
        return {"error": "User not authorized to delete the idea"}, 400

    @api.doc("Update idea")
    @api.expect(access_token_header_parser, validate=True)
    @api.response(code=200, model=detail_idea_model, description="Idea updated successfully")
    @jwt_required
    def put(self, idea_id):
        data = request.get_json()
        Idea.update_idea(int(idea_id), **data)

        return Idea.get_idea_json(idea_id), 200
