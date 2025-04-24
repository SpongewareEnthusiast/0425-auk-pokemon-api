from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.pokeAPI.repository.repository import fetch_pokemon, fetch_pokemon_names
from app.pokeAPI.helpers.helpers import random_int, create_answers
from app.pokeAPI.models.models import ValidatedAnswer, RandomPokemon



MAX_POKEMON_ID = 50
async def lifespan(app: FastAPI):
    global pokemon_names
    data = await fetch_pokemon_names()
    pokemon_names = [p["name"] for p in data["results"]]
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/random-pokemon", response_model=RandomPokemon)
async def random_pokemon() -> RandomPokemon:
    generated_id = random_int(MAX_POKEMON_ID)
    print(MAX_POKEMON_ID)
    random_pokemon_data = await fetch_pokemon(generated_id)
    random_pokemon_obj = {
            "id": random_pokemon_data["id"],
            "image": random_pokemon_data["sprites"]["other"]["dream_world"]["front_default"],
            "guesses": create_answers(pokemon_names, generated_id, MAX_POKEMON_ID)
        }  
    return random_pokemon_obj

@app.get("/validate-answer", response_model=ValidatedAnswer)
async def validate_answer(id: Optional[int] = None, name: Optional[str] = None) -> ValidatedAnswer:
    if (id == None or name == None):
        raise HTTPException(status_code = 422, detail = "Id or name not supplied")
    pokemon_to_check_against = await fetch_pokemon(id)
    is_correct = False
    if (pokemon_to_check_against["name"] == name):
        is_correct = True
    return  { 
            "is_correct": is_correct,
            "image": pokemon_to_check_against["sprites"]["other"]["dream_world"]["front_default"] ,
            "correct_name": pokemon_to_check_against["name"]
            }