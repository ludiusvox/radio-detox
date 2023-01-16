# -*- coding: utf-8 -*-
import bleach
import os
#import redis

os_env = os.environ


class Config(object):

    def uia_username_mapper(identity):
        # we allow pretty much anything - but we bleach it.
        return bleach.clean(identity, strip=True)
    SECURITY_EMAIL_VALIDATOR_ARGS = { "check_deliverability" : False }
    SECRET_KEY = os.environ.get('SECRET_KEY', '3nF3Rn0')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_ENABLED = True # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///enferno.db'
    # for postgres
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql:///enferno')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/10')
    #CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/11')
    SQLALCHEMY_RECORD_QUERIES = True
    TESTING = False
    DEBUG = True
    SECURITY_REGISTERABLE = True
    import os
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    import secrets
    #app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = 'username'
    LOGIN_DISABLED = False
    #SECURITY_POST_LOGIN_VIEW = "login_user.html"
    secret = secrets.token_urlsafe(32)
    #app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', '12531253')
    #app.config.from_object('config.email')
    secret_key = secret
    CACHE_NO_NULL_WARNING = True
    WTF_CSRF_CHECK_DEFAULT = False
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = False
    SECURITY_CSRF_COOKIE_NAME = "XSRF-TOKEN"
   # have session and remember cookie be samesite (flask/flask_login)
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    
    import logging, sys
    logging.basicConfig(stream=sys.stderr)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_TYPE = 'filesystem'
    #app.config['SECURITY_EMAIL_SENDER'] = 'ludiusvox@gmail.com'
    
    
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    }

    # Mail Config
    SEND_REGISTEREMAIL = False
    # security
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CONFIRMABLE = False
    
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', '3nF3Rn0')
    SECURITY_USER_IDENTITY_ATTRIBUTES = [{"email": {"mapper": uia_username_mapper, "case_insensitive": True}}]
    
    
    SECURITY_POST_CONFIRM_VIEW = '/dashboard'
    POST_LOGIN_VIEW = '/login'
    #SESSION_TYPE = 'redis'
    #SESSION_REDIS = redis.from_url(os.environ.get('SESSION_REDIS', 'redis://localhost:6379/1'))
    PERMANENT_SESSION_LIFETIME = 3600
    

    

class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/enferno'
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
