import os
import sys

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

if not os.getenv('UNITTESTING', None):
    print('No UNITTESTING env variable set, exitting')  # noqa print alert
    sys.exit(1)


@pytest.fixture(scope='session', autouse=True)
def server():
    client = TestClient(app)
    yield client
