import os
import logging
import pytest
import api
from api import config
from api.config import DataReadingError, DataValidationError

#####################################################################################
#                                 Testing logging
#####################################################################################
# _logger = config.get_logger(logger_name="test")

# def mock_debug():
#     _logger.warning("warning message")

# def mock_info():
#     _logger.info("warning message")

# def mock_warning():
#     _logger.warning("warning message")


# def test_logger_debug(caplog):
#     caplog.set_level(logging.DEBUG, logger="test")
#     mock_debug()
#     # print(caplog.text)
#     assert "warning message" in caplog.text


# def test_logger_info(caplog):
#     caplog.set_level(logging.INFO)
#     mock_info()
#     assert "warning message" in caplog.text


# def test_logger_warning(caplog):
#     caplog.set_level(logging.WARNING)
#     mock_warning()
#     assert "warning message" in caplog.text


#####################################################################################
#                                 Testing custom errors
#####################################################################################
def test_DataReadingError_without_message():
    with pytest.raises(DataReadingError) as excinfo:
        raise DataReadingError()
    assert "DataReadingError" == str(excinfo.value)


def test_DataReadingError_with_message():
    with pytest.raises(DataReadingError) as excinfo:
        raise DataReadingError("with message")
    assert "DataReadingError with message" == str(excinfo.value)


def test_DataValidationError_without_message():
    with pytest.raises(DataValidationError) as excinfo:
        raise DataValidationError()
    assert "DataValidationError" == str(excinfo.value)


def test_DataValidationError_with_message():
    with pytest.raises(DataValidationError) as excinfo:
        raise DataValidationError("with message")
    assert "DataValidationError with message" == str(excinfo.value)


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


def mock_config():
    """get config, used for testing default config"""
    _config = config.get_config()

    if _config is None:
        raise EnvironmentError("_config environment is not set.")

    return _config


def test_default_config_production(mock_staging_true):
    _config = mock_config()
    assert _config.__class__.__name__ == "ProductionConfig"


def test_default_config_development(mock_staging_false):
    _config = mock_config()
    assert _config.__class__.__name__ == "DevelopmentConfig"