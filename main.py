from typing import Optional
from fastapi import FastAPI, HTTPException
from random import randint, shuffle
from httpx import AsyncClient


POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"
MAX_POKEMON_ID = 50
pokemon_names = []

async def lifespan(app: FastAPI):
    global pokemon_names
    service_url = POKEAPI_URL + "/?limit=50&offset=0"
    async with AsyncClient() as client:
        response = await client.get(service_url)
        if response.status_code != 200:
            raise HTTPException(status_code = 500, detail = "Something went wrong")
        data = response.json()
        pokemon_names = [p["name"] for p in data["results"]]
    yield
    print("APP SHUTTING DOWN")

app = FastAPI(lifespan=lifespan)


def random_int():
    return randint(1,MAX_POKEMON_ID)

def create_wrong_answers(answer_id):
    # convert to 0 based index
    new_ind = answer_id - 1
    answer_array = [pokemon_names[(new_ind + random_int()) % len(pokemon_names)],
            pokemon_names[(new_ind + random_int()) % len(pokemon_names)], 
            pokemon_names[(new_ind + random_int()) % len(pokemon_names)],
            pokemon_names[new_ind]]
    shuffle(answer_array)
    return answer_array


async def fetch_pokemon(id: int):
    service_url = POKEAPI_URL + str(id)
    async with AsyncClient() as client:
        response = await client.get(service_url)
        if response.status_code != 200:
            raise HTTPException(status_code = 500, detail = "Something went wrong")
        data = response.json()
        return data

@app.get("/random-pokemon")
async def random_pokemon():
    generated_id = random_int()
    random_pokemon_data = await fetch_pokemon(generated_id)
    random_pokemon_obj = {
            "name": random_pokemon_data["name"],
            "id": random_pokemon_data["id"],
            "image": random_pokemon_data["sprites"]["other"]["dream_world"]["front_default"],
            "guesses": create_wrong_answers(generated_id)
        }  
    return random_pokemon_obj


@app.get("/validate-answer")
async def validate_answer(id: Optional[int] = None, name: Optional[str] = None):
    if (id == None or name == None):
        raise HTTPException(status_code = 422, detail = "Id or name not supplied")
    pokemon_to_check_against = await fetch_pokemon(id)
    is_correct = False
    if (pokemon_to_check_against["name"] == name):
        is_correct: True
    return  { 
            "is_correct": is_correct,
            "image": pokemon_to_check_against["sprites"]["other"]["dream_world"]["front_default"] ,
            "correct_name": pokemon_to_check_against["name"]
            }