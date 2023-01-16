
import os
import sys 
sys.path.append('/Users/aaronl/eclipse-workspace/radio-detox/RadioDetox/src/python/enferno')
from code.app import create_app
from code.settings import DevConfig, ProdConfig
from flask_security.utils import login_user
from flask import g
import sys
from code.public import *
#This is what runs the application
CONFIG = ProdConfig if os.environ.get('FLASK_DEBUG') == '0' else DevConfig
if __name__ == "__main__":
    
    app = create_app(CONFIG)
    app.config['UPLOAD_FOLDER'] 
    app.run(debug=True)
    