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

    def __init__(self, user_id, content, impact, ease, confidence):
        self.user_id = user_id
        self.content = content
        self.impact = impact
        self.ease = ease
        self.confidence = confidence

    @classmethod
    def get_idea_json(cls, idea_id):
        idea = cls.query.filter_by(idea_id=idea_id).first()
        avg = (idea.confidence + idea.ease + idea.impact)/3.0
        return {
          "id": idea.idea_id,
          "content": idea.content,
          "impact": idea.impact,
          "ease": idea.ease,
          "confidence": idea.confidence,
          "average_score": avg,
          "created_at": int(idea.created_at.timestamp())
        }

    @classmethod
    def get_idea(cls, idea_id):
        return cls.query.filter_by(idea_id=idea_id).first()

