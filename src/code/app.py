# -*- coding: utf-8 -*-

from flask import Flask, render_template, has_app_context,g
from code.settings import ProdConfig
from flask_security import Security, SQLAlchemyUserDatastore,login_user, current_user,LoginForm, url_for_security
from code.user.models import User, Role
from code.user.forms import ExtendedRegisterForm
from code.extensions import   cache,  db, debug_toolbar, migrate, serversession
from code.public.views import bp_public
from code.user.views import bp_user
import code.commands as commands
from flask_session import SqlAlchemySessionInterface
import flask_bcrypt as Bcrypt
from flask_login import LoginManager
from code.user.database import db_session
def create_app(config_object=ProdConfig):
    
    app = Flask(__name__)
    additional_config(app)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    
    return app

def additional_config(app):


    
    return
def register_extensions(app):
    cache.init_app(app)
    db.init_app(app)
    
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore,register_form=ExtendedRegisterForm)
    #mail.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app,db)
    serversession.init_app(app)
    import flask_wtf
    flask_wtf.CSRFProtect(app)
    #login_manager = LoginManager(app)
    #login_manager.login_view = "security.login"
    #@login_manager.user_loader
    #def load_user(id):
        #return User.query.get(int(id)

    #login_manager.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(bp_public)
    app.register_blueprint(bp_user)  
    #with app.app_context():
        #login_user(current_user)
    
    return None
        
        

def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': User,
            'Role': Role
        }

    app.shell_context_processor(shell_context)



def register_commands(app):
    """Register Click commands."""

    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.create_db)
    app.cli.add_command(commands.install)
    app.cli.add_command(commands.create)
    app.cli.add_command(commands.add_role)
    app.cli.add_command(commands.reset)

