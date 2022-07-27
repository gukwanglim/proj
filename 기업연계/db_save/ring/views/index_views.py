from flask import Blueprint, render_template

bp = Blueprint('index', __name__, url_prefix='/index')


@bp.route('/main/')
def main_page():
    return render_template('main/main.html')