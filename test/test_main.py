import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.pokeAPI.main import app

client = TestClient(app)

@pytest.fixture
def setup_pokemon_names():
    with patch("app.pokeAPI.main.POKEMON_NAMES", ["bulbasaur", "charmander", "squirtle", "bulbasaur", "charmander", "squirtle","bulbasaur", "charmander", "squirtle", "a"]):
        yield
# @pytest.fixture
# def setup_lifespan():
#     async def mock_lifespan(app):
#         global pokemon_names
#         pokemon_names = ["bulbasaur", "charmander", "squirtle"]  # Populate array here
#         yield

#     with patch("app.pokeAPI.main.lifespan", mock_lifespan):
#         yield

@pytest.fixture
def mock_max_pokemon_id():
    with patch("app.pokeAPI.main.MAX_POKEMON_ID", 9):
        yield

@pytest.fixture
def mock_fetch_pokemon():
    with patch("app.pokeAPI.repository.repository.fetch_pokemon", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "id": 1,
            "sprites": {
                "other": {
                    "dream_world": {
                        "front_default": "https://example.com/bulbasaur.png"
                    }
                }
            },
            "name": "bulbasaur"
        }
        yield mock

@pytest.fixture
def mock_create_answers():
    with patch("app.pokeAPI.helpers.helpers.create_answers") as mock:
        mock.return_value = ["bulbasaur", "charmander", "squirtle", "pikachu"]
        yield mock

@pytest.fixture
def mock_random_int():
    with patch("app.pokeAPI.helpers.helpers.random_int") as mock:
        mock.return_value = 1
        yield mock

def test_random_pokemon(setup_pokemon_names,mock_max_pokemon_id, mock_fetch_pokemon, mock_create_answers, mock_random_int):
    response = client.get("/random-pokemon")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "id": 1,
        "image": "https://example.com/bulbasaur.png",
        "guesses": ['squirtle', 'squirtle', 'bulbasaur', 'squirtle']
    }


# Test /validate-answer endpoint (correct answer)
def test_validate_answer_correct(mock_fetch_pokemon, mock_max_pokemon_id):
    response = client.get("/validate-answer", params={"id": 1, "name": "bulbasaur"})
    assert response.status_code == 200
    assert response.json() == {
        "is_correct": True,
        "image": "https://example.com/bulbasaur.png",
        "correct_name": "bulbasaur"
    }

# Test /validate-answer endpoint (incorrect answer)
def test_validate_answer_incorrect(mock_fetch_pokemon, mock_max_pokemon_id):
    response = client.get("/validate-answer", params={"id": 1, "name": "pikachu"})
    assert response.status_code == 200
    assert response.json() == {
        "is_correct": False,
        "image": "https://example.com/bulbasaur.png",
        "correct_name": "bulbasaur"
    }

# Test /validate-answer endpoint (missing parameters)
def test_validate_answer_missing_parameters():
    response = client.get("/validate-answer")
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Id or name not supplied"
    }
