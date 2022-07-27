from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from ring import db
# from ring.models import User

bp = Blueprint('shop', __name__, url_prefix='/shop')

@bp.route('/details/')
def detail():
    return render_template('shop/product-details.html')

@bp.route('/shop/')
def shop():
    return render_template('shop/shop-page.html')