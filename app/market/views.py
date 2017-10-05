from functools import wraps

from flask import render_template
from . import market
from ..models import Category, Object

def menu_wrapper(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        template, params = func(*args, **kwargs)
        categories = Category.query.all()
        params.update({'categories':categories})
        return render_template(template, **params)

    return wrapped

@market.route('/')
@menu_wrapper
def index():
    objects = Object.query.all()
    return 'market/index.html', {'objects':objects}


@market.route('/category/<int:category_id>')
@menu_wrapper
def category(category_id):
    category = Category.query.get(category_id)
    objects = Object.query.filter_by(category=category)
    return 'market/category.html', {'objects':objects, 'cat':category}

@market.route('/object/<int:object_id>')
@menu_wrapper
def object(object_id):
    object = Object.query.get(object_id)
    return 'market/object.html', {'object':object}