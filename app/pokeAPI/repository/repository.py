from httpx import AsyncClient
from fastapi import HTTPException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

async def fetch_pokemon(id: int):
    service_url = POKEAPI_URL + str(id)
    async with AsyncClient() as client:
        response = await client.get(service_url)
        if response.status_code != 200:
            raise HTTPException(status_code = 500, detail = "Something went wrong")
        data = response.json()
        return data

async def fetch_pokemon_names():
    service_url = POKEAPI_URL + "/?limit=50&offset=0"
    async with AsyncClient() as client:
        response = await client.get(service_url)
        if response.status_code != 200:
            raise HTTPException(status_code = 500, detail = "Something went wrong")
        data = response.json()
        return data