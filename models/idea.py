from models import db
from datetime import datetime


class Idea(db.Model):

    __tablename__ = "ideas"
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    idea_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    impact = db.Column(db.Integer, nullable=False, default=1)
    ease = db.Column(db.Integer, nullable=False, default=1)
    confidence = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    average_score = db.Column(db.Float, default=1)

    def __init__(self, user_id, content, impact, ease, confidence):
        self.user_id = user_id
        self.content = content
        self.impact = impact
        self.ease = ease
        self.confidence = confidence
        self.average_score = (confidence + ease + impact)/3.0

    @classmethod
    def get_idea_json(cls, idea_id):
        idea = cls.query.filter_by(idea_id=idea_id).first()
        return {
          "id": idea.idea_id,
          "content": idea.content,
          "impact": idea.impact,
          "ease": idea.ease,
          "confidence": idea.confidence,
          "average_score": idea.average_score,
          "created_at": int(idea.created_at.timestamp())
        }

    @classmethod
    def get_idea(cls, idea_id):
        return cls.query.filter_by(idea_id=idea_id).first()

    @classmethod
    def update_idea(cls, idea_id, content, impact, ease, confidence):
        idea = cls.query.filter_by(idea_id=idea_id).first()
        idea.content = content
        idea.impact = impact
        idea.ease = ease
        idea.confidence = confidence
        idea.average_score = (confidence + ease + impact) / 3.0
        db.session.commit()

    @classmethod
    def get_idea_page(cls, user_id, page):
        ideas = cls.query.filter_by(user_id=user_id).order_by(Idea.average_score.desc()).paginate(page=page, max_per_page=10)
        response = []
        for idea in ideas.items:
            response.append(
                {
                    "id": idea.idea_id,
                    "content": idea.content,
                    "impact": idea.impact,
                    "ease": idea.ease,
                    "confidence": idea.confidence,
                    "average_score": idea.average_score,
                    "created_at": int(idea.created_at.timestamp())
                }
            )
        return response
