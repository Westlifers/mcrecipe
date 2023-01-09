import json
from os import path

with open(path.join(path.dirname(__file__), '..', 'all_recipes.json'), 'r', encoding='utf-8') as f:
    recipes = json.loads(f.read())

flag = True
for recipe in recipes:
    if 'crafting_special_' not in recipe['recipe']['type'] and '_from_' not in recipe['item']:
        if type(recipe['recipe']['result']) == dict:
            if 'minecraft:' + recipe['item'] != recipe['recipe']['result']['item']:
                flag = False
                print(recipe)
        elif type(recipe['recipe']['result']) == str:
            if 'minecraft:' + recipe['item'] != recipe['recipe']['result']:
                flag = False
                print(recipe)

print(flag)
