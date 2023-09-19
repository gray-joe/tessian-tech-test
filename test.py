import pytest
from flask.testing import FlaskClient
import bot


@pytest.fixture
def client() -> FlaskClient:
    """Returns a client which can be used to test the HTTP API."""
    bot.app.config["TESTING"] = True

    with bot.app.test_client() as client:
        yield client


def test_retrieve_history(client: FlaskClient):
    client.post("/user/test_retrieve/message", json={"text": "Hello"})

    response = client.get("/user/test_retrieve/message")
    assert response.status_code == 200
    history = response.json

    assert len(history) == 3

    assert history[0] == {"message": "Hello", "type": "user"}
    assert history[1] == {"message": "Welcome! Let me tell you a joke.", "type": "bot"}
    assert history[2]["type"] == "bot"
