from random import randint, shuffle
def random_int(upper_limit: int):
    return randint(1,upper_limit)

def random_int_exclude_current_id(curent_id: int, upper_limit: int):
    new_random = random_int(upper_limit)
    if (new_random == curent_id):
        new_random += 1
    return new_random

def create_answers(pokemon_names: list[str], answer_id: int, upper_limit: int):
    # convert to 0 based index
    print(pokemon_names)
    print(answer_id)
    print(upper_limit)
    new_ind = answer_id - 1
    answer_array = [pokemon_names[(new_ind + random_int_exclude_current_id(answer_id, upper_limit)) % len(pokemon_names)],
            pokemon_names[(new_ind + random_int_exclude_current_id(answer_id, upper_limit)) % len(pokemon_names)], 
            pokemon_names[(new_ind + random_int_exclude_current_id(answer_id, upper_limit)) % len(pokemon_names)],
            pokemon_names[new_ind]]
    shuffle(answer_array)
    return answer_array