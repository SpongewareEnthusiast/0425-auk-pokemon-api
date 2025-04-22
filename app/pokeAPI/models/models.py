from pydantic import BaseModel

class ValidatedAnswer(BaseModel):
    is_correct: bool
    image: str 
    correct_name: str

class RandomPokemon(BaseModel):
    id: int 
    image: str
    guesses: list[str]