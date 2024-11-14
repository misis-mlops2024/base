import pytest 
import os


@pytest.fixture()
def config_path():
    curdir = os.path.dirname(__file__)
    return os.path.join(curdir, "test_params.yaml")
