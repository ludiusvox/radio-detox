from flask_security.forms import RegisterForm,LoginForm
from wtforms import StringField



class ExtendedRegisterForm(RegisterForm):
    name = StringField('Full Name')





class UserInfoForm():
    pass

class ExtendedLoginForm(LoginForm):
    pass