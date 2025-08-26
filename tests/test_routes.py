import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from website import create_app

# def test_home_route():
#     app = create_app()
#     client = app.test_client()
#     response = client.get("/")
#     assert response.status_code == 200

@pytest.mark.parametrize("route, expected_status", [
    ("/", 200),
    ("/env", 200),
    ("/db-check", 200),
])
def test_route_response(route, expected_status):
    app = create_app({"TESTING": True})
    client = app.test_client()
    response = client.get(route)
    assert response.status_code == expected_status
