from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class ProductInputForm(FlaskForm):
    prod_name = StringField('제품명', validators=[Length(min=3, max=25)])
    prod_image = TextAreaField('제품 사진', validators=None)
    prod_price = StringField('제품 가격', validators=[Length(min=3, max=25)])
    prod_quantity = StringField('제품 수량', validators=None)
    prod_expand = StringField('제품 소개', validators=[Length(min=3, max=300)])




# https://wtforms.readthedocs.io/en/2.3.x/fields/#basic-fields 참고  FileField 혹은 MultipleFileField 확인