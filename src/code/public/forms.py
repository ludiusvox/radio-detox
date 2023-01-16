from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length
from wtforms.widgets import TextInput


'''
class MyForm(Form):
    field = StringField('MyLabel',validators=[DataRequired,],widget=TextInput())
'''
class init_Register(FlaskForm):
    name = StringField('name', validators=[DataRequired(), length(min=1, max=30)])
    submit = SubmitField('Register')
