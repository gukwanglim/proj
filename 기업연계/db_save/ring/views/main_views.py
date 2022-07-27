# 화면을 구성하는 파일

from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

# from pybo.models import Question


bp = Blueprint('main', __name__, url_prefix='/')                         
                                                                

@bp.route('/hello')
def hello_py():
    return 'Hello, py.'


@bp.route('/')
def index():
    return redirect(url_for('index.main_page'))

