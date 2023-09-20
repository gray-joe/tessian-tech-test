import pytest
from flask.testing import FlaskClient
import bot


@pytest.fixture
def client() -> FlaskClient:
    """Returns a client which can be used to test the HTTP API."""
    bot.app.config["TESTING"] = True

    with bot.app.test_client() as client:
        yield client


def test_retrieve_history_for_single_message(client: FlaskClient):
    client.post("/user/test_retrieve/message", json={"text": "Hello"})

    response = client.get("/user/test_retrieve/message")
    assert response.status_code == 200
    history = response.json

    assert len(history) == 3

    assert history[0] == {"message": "Hello", "type": "user"}
    assert history[1] == {"message": "Welcome! Let me tell you a joke.", "type": "bot"}
    assert history[2]["type"] == "bot"


def test_retrieve_empty_history(client: FlaskClient):
    response = client.get("/user/test_empty_retrieve/message")
    assert response.status_code == 404

    # Ensure an empty conversation history is returned
    history = response.json
    assert len(history) == 0


def test_retrieve_history_for_multiple_messages(client: FlaskClient):
    client.post("/user/test_multiple_retrieve/message", json={"text": "Hello there"})
    client.post("/user/test_multiple_retrieve/message", json={"text": "Tell another joke!"})

    response = client.get("/user/test_multiple_retrieve/message")
    assert response.status_code == 200

    # Ensure the conversation history includes the user and bot messages
    # Ensure the bot only sends the welcome message on the first message
    history = response.json
    assert len(history) == 5
    assert history[0] == {"message": "Hello there", "type": "user"}
    assert history[1] == {"message": "Welcome! Let me tell you a joke.", "type": "bot"}
    assert history[2]["type"] == "bot"
    assert history[3]["type"] == "user"
    assert history[4]["type"] == "bot"
    assert history[4] != {"message": "Welcome! Let me tell you a joke.", "type": "bot"}


def test_retrieve_nonexistent_conversation_history(client: FlaskClient):
    response = client.get("/user/nonexistent_user/message")
    assert response.status_code == 404


def test_handle_user_message(client: FlaskClient):
    response = client.post("/user/test_user_message/message", json={"text": "Hello there"})
    assert response.status_code == 200

    # Ensure the bot responds with a joke
    bot_responses = response.json
    assert len(bot_responses) == 2
    assert "joke" in bot_responses[0]


def test_handle_user_message_with_special_characters(client: FlaskClient):
    response = client.post("/user/test_user_message_with_special/message", json={"text": "Ærøskøb!£#~`3東賢蔵❤️👩"})
    assert response.status_code == 200

    # Ensure the bot responds with a joke
    bot_responses = response.json
    assert len(bot_responses) == 2
    assert bot_responses[0] == "Welcome! Let me tell you a joke."


def test_handle_empty_user_message(client: FlaskClient):
    response = client.post("/user/test_empty_user_message/message", json={"text": ""})
    assert response.status_code == 200

    # Ensure the bot responds with a joke
    bot_responses = response.json
    assert len(bot_responses) == 2
    assert bot_responses[0] == "Welcome! Let me tell you a joke."


def test_handle_long_user_message(client: FlaskClient):
    response = client.post("/user/test_long_user_message/message", json={"text": "123" * 1000000})
    assert response.status_code == 200

    # Ensure the bot responds with a joke
    bot_responses = response.json
    assert len(bot_responses) == 2
    assert bot_responses[0] == "Welcome! Let me tell you a joke."


def test_invalid_json_post(client: FlaskClient):
    response = client.post("/user/test_invalid_user_message/message", data="Invalid JSON Data")
    assert response.status_code == 415