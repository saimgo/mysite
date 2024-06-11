# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Tech', 'টেক'), ('Python', 'পাইথন'), ('C++', 'সি++'), ('Problem Solving', 'প্রবলেম সল্ভিং'), ('Math', 'গণিত'), ('C', 'সি'), ('PDFs', 'পিডিএফ')], validators=[DataRequired()])
    submit = SubmitField('Submit')
