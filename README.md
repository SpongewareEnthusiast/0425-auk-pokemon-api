# Run locally
- clone the repo
- python -m venv .venv
- source ./.venv/bin/activate
- pip install -r ./requirements.txt 
- cd app/pokeSPI
- fastapi run main.py
# 0425-auk-pokemon-api
For the interview
Random Pokémon Endpoint
You should implement an API endpoint that allows the user to get the details of a random Pokémon.
The API should respond with the following information:
- The Pokémon ID.
- The silhouette image of the Pokémon.
- A list of four Pokémon names (the correct name and three decoy names)
For simplicity, you may restrict the available Pokémon to the first 50 listed by PokéAPI.
Verify Pokémon Endpoint
You should implement an API endpoint that allows the user to verify their guess about the random
Pokémon.
The API should accept the following inputs:
- The ID of a Pokémon.
- The name that the player guessed.
The API should then respond with the following data:
- The true name of the Pokémon.
- The URL of the full image.
- An indication of whether the guess was correct.
