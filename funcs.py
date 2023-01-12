import json
from .data.dicts import recipes
import Levenshtein as Lev


def find_closest_str(word: str, word_list: list[str]):
    min_distance = float('inf')
    closest_str = None
    for item in word_list:
        distance = Lev.distance(word, item)
        if distance < min_distance:
            min_distance = distance
            closest_str = item
    return closest_str


def query_recipe_by_name(name: str) -> list:
    result = []
    for recipe in recipes:
        if recipe.result.name == name:
            result.append(recipe)
    return result

