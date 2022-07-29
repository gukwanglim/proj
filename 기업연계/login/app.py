from datetime import datetime
 
from flask import Flask, render_template, session, g, request, url_for, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from forms import UserCreateForm, UserLoginForm

# bp = Blueprint('main', __name__, url_prefix='/main')

app = Flask(__name__)
 
app.config['SECRET_KEY'] = 'this is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template('main/main.html')

@app.route('/register', methods=['GET','POST'])
def register():
	form = UserCreateForm()
	if request.method == 'POST' and form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user:
			user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('main'))	
		else:
			flash('이미 존재하는 사용자입니다.')
	return render_template('auth/signup.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main'))
        flash(error)
    return render_template('auth/login.html', form=form)

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')   # 여기서 user_id는 위 login 함수에서 seccion에 저장한 정보이다
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.get(user_id)

@app.route('/logout/')
def logout():
    session.clear()                        # clear를 사용하여 user_id를 제거
    return redirect(url_for('main'))

@app.route('/my-account')
def account():
    return render_template('auth/my-account.html')

# 사용자 모델 추가
class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email, password):
      self.username = username
      self.email = email
 
      self.set_password(password)

    def __repr__(self):
        return f"<User('{self.id}', '{self.username}', '{self.email}')>"

    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

    