from datetime import datetime
from itertools import count
 
from flask import Flask, render_template, session, g, request, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from sqlalchemy import select

from forms import ProductInputForm, UserCreateForm, UserLoginForm

# bp = Blueprint('main', __name__, url_prefix='/main')

app = Flask(__name__)
 
app.config['SECRET_KEY'] = 'this is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

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
      self.password = password

    def __repr__(self):
        return f"<User('{self.id}', '{self.username}', '{self.email}')>"

# 제품 모델 추가
class Product(db.Model):
    __table_name__ = 'product'

    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(150), unique=False, nullable=True)
    prod_image = db.Column(db.Text(), unique=False, nullable=True)
    prod_price = db.Column(db.String(150), unique=False, nullable=True)
    prod_quantity = db.Column(db.String(150), unique=False, nullable=True)
    prod_expand = db.Column(db.String(300), unique=False, nullable=True)

    def __init__(self, prod_name, prod_image, prod_price, prod_quantity, prod_expand):
        self.prod_name = prod_name
        self.prod_image = prod_image
        self.prod_price = prod_price
        self.prod_quantity = prod_quantity
        self.prod_expand = prod_expand

    def __repr__(self):
        return f"<Product('{self.prod_id}', '{self.prod_name}', '{self.prod_image}', '{self.prod_price}', '{self.prod_quantity}', '{self.prod_expand}')>"


@app.route('/')
def main():
    prod = Product.query.all()
    image_names = []
    for file in prod:
        image_names.append(file.prod_image)
    print(image_names)


# flask는 len 사용 불가. {% for i in range(prod | length) %} 이런 식으로 사용 가능.
    # prod_list = []

    # for i in range(a):
        
    #     prod_list.append(prod[i].prod_image)
    #     return prod_list

    # print('여기에 출력 : ', len(prod))      


    # [<Product('1', '사과', 'http://kormedi.com/wp-content/uploads/2020/09/roman-samokhin-580x429.jpg', '1500', 'None', '달고 맛있습니다.')>, <Product('2', '아포카도', 'https://img.etoday.co.kr/pto_db/2021/06/600/20210602131530_1627835_1200_779.jpg', '9000', 'None', '잘 익은 아포카도.')>]


    # print('////////')
    # print('그 다음 출력 : ', prod[0])

    # [<Product('1', '사과', 'http://kormedi.com/wp-content/uploads/2020/09/roman-samokhin-580x429.jpg', '1500', 'None', '달고 맛있습니다.')>]


    # print('////////////')
    # print('제발 : ', prod[0].prod_name)


    # 사과

    return render_template('main/main.html', prod=prod)

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
    if request.method == 'POST' and form.validate_on_submit():                 # 점검
        error = None
        # print("비밀번호:%s" % form.password.data) 
        user = User.query.filter_by(username=form.username.data).first()
        # print("아이디:%s" % form.username.data) 
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            # print(session)
            session['user_name'] = form.username.data
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

@app.route('/upload')
def up():
    return render_template('page/upload.html')

@app.route('/product')
def prod():
    return render_template('shop/shop-page.html')

@app.route('/product-details')
def details():
    return render_template('shop/product-details.html')

@app.route('/cart')
def cart():
    return render_template('page/cart.html')

@app.route('/QnA')
def qna():
    return render_template('page/Q&A.html')

