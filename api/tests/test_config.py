import os
import pytest
import api
from api import config


#####################################################################################
#                                 Testing logging
#####################################################################################
def test_get_console_handler():
    pass


def test_get_file_handler():
    pass


def test_get_logger():
    pass


#####################################################################################
#                                 Testing custom errors
#####################################################################################
def test_DataReadingError():
    pass


def test_DataParsingError():
    pass


#####################################################################################
#                                 Testing Configs
#####################################################################################
def test_production_config():
    _config = config.ProductionConfig
    assert _config.TESTING == False
    assert _config.DEBUG == False
    assert _config.DEVELOPMENT == False
    assert _config.DB_NAME == "covid"
    

def test_development_config():
    _config = config.DevelopmentConfig
    assert _config.TESTING == True
    assert _config.DEBUG == True
    assert _config.DEVELOPMENT == True
    assert _config.DB_NAME == "covid-staging"
    

@pytest.fixture
def mock_staging_true(monkeypatch):
    monkeypatch.setenv('STAGING', "True")

@pytest.fixture
def mock_staging_false(monkeypatch):
    monkeypatch.setenv('STAGING', "False")

def test_get_config():
    """get config, used for testing default config"""
    _config = config.get_config()

    if _config is None:
        raise EnvironmentError("USER environment is not set.")

    return _config

def test_default_config_production(mock_staging_true):
    _config = test_get_config()
    assert _config.__class__.__name__ == "ProductionConfig"

def test_default_config_development(mock_staging_false):
    _config = test_get_config()
    assert _config.__class__.__name__ == "DevelopmentConfig"