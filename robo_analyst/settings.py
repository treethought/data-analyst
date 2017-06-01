# -*- coding: utf-8 -*-
"""Application configuration.

See https://github.com/sloria/cookiecutter-flask for configuration options with other flask-extensions
"""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('ROBO_ANALYST_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0 # for refeshing static files

class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
