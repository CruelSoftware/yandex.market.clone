from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

association_table = db.Table('association', db.Model.metadata,
     db.Column('object_id', db.Integer, db.ForeignKey('object.id')),
     db.Column('colors_id', db.Integer, db.ForeignKey('colors.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow())
    avatar_hash = db.Column(db.String(32))

    @property
    def password(self):
        raise AttributeError('password is not readable atribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False, unique=True)

class Object(db.Model):
    __tablename__ = 'object'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    colors = db.relationship('Colors', secondary=association_table)

class Colors(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    html_code = db.Column(db.String(10), nullable=False, unique=True)