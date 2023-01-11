import json
from .classes import *
from .data.dicts import namespace, tags, recipes


def query_recipe_by_name(name: str) -> list:
    result = []
    for recipe in recipes:
        if recipe.result.name == name:
            result.append(recipe)
    return result

