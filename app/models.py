import string

import os
import os.path as op
import random
from flask import url_for

from flask_admin import form
from jinja2 import Markup
from sqlalchemy.event import listens_for
from werkzeug.utils import secure_filename

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView

IMAGE_PATH = op.join(op.dirname(__file__), 'static/images')
IMAGE_URL = '/static/images/'
#thumb_path = op.join(op.dirname(__file__), 'thumbs')

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

    def __str__(self):
        return self.title

class Object(db.Model):
    __tablename__ = 'object'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    category_id = db.Column(db.ForeignKey(Category.id))
    category = db.relationship(Category, backref='objects')
    colors = db.relationship('Colors', secondary=association_table)
    price = db.Column(db.Integer())

    def __str__(self):
        return self.title

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    object_id = db.Column(db.ForeignKey(Object.id))
    object = db.relationship(Object, backref='images')
    image = db.Column(db.String(64), nullable=True)
    alt = db.Column(db.String(64), nullable=True)

    @property
    def url(self):
        return IMAGE_URL + self.image


# @listens_for(Image, 'after_insert')
# def add_thumb(mapper, connection, target):
#     if target.image:
#         img = target.image
#         splited_img = img.split('.')
#         extension = splited_img[-1:][0]
#         file = splited_img[:-1][0]
#         thumbnail = file + '_thumb' + '.' + extension
#         sql = "UPDATE image SET thumbnail='"+thumbnail+"' WHERE id="+str(target.id)
#         db.engine.execute(sql)

class Param(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return self.title

class ObjectParam(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    param_id = db.Column(db.ForeignKey(Param.id))
    param = db.relationship(Param, backref='objectparams')
    object_id = db.Column(db.ForeignKey(Object.id))
    object = db.relationship(Object, backref='params')
    value = db.Column(db.String(200), nullable=True)

@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.image:
        # Delete image
        try:
            os.remove(op.join(IMAGE_PATH, target.image))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(IMAGE_PATH,
                              form.thumbgen_filename(target.image)))
        except OSError:
            pass

class Colors(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    html_code = db.Column(db.String(10), nullable=False, unique=True)

    def __str__(self):
        return self.title

class UserAdmin(ModelView):
    column_display_pk = True
    form_columns = ['email', 'is_admin', 'password_hash', 'firstname', 'lastname']

class CategoryAdmin(ModelView):
    column_display_pk = True
    form_columns = ['title']

class ColorsAdmin(ModelView):
    column_display_pk = True
    form_columns = ['title', 'html_code']

class ObjectAdmin(ModelView):
    column_display_pk = True
    form_columns = ['title', 'colors', 'category', 'price']

class ParamAdmin(ModelView):
    column_display_pk = True
    form_columns = ['title']

class ObjectParamAdmin(ModelView):
    column_display_pk = True
    form_columns = ['object', 'param', 'value']

class ImageView(ModelView):

    def prefix_name(obj, file_data):
        suffix = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
        parts = op.splitext(file_data.filename)
        return secure_filename('{}_{}{}'.format(parts[:-1], suffix, parts[-1]))

    form_extra_fields = {
        'image': form.ImageUploadField('Image',
                                      base_path=IMAGE_PATH,
                                      namegen=prefix_name,
                                      allowed_extensions=['jpg', 'png'],
                                      thumbnail_size=(100, 100, True)),
}
