from models import db
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password, name):
        self.email = email.lower().strip()
        self.password = generate_password_hash(password, method='sha256')
        self.name = name

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @classmethod
    def get_profile_json(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        md5 = hashlib.md5()
        md5.update(user.email.encode('utf-8'))
        digest = md5.hexdigest()
        avatar_url = "https://www.gravatar.com/avatar/" + str(digest) + "?d=mm&s=200"
        return {
            'email': user.email,
            'name': user.name,
            'avatar_url': avatar_url
        }
