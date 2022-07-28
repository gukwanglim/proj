from flask import Blueprint, url_for, render_template, flash, request, session, g

bp = Blueprint('pages', __name__, url_prefix='/pages')

@bp.route('/cart/')
def shopping_cart():
    return render_template('page/cart.html')

@bp.route('/checkout/')
def check():
    return render_template('page/checkout.html')

@bp.route('/about_us/')
def about():
    return render_template('page/about-us.html')