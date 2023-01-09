import os
import json

path = os.path.join(os.path.dirname(__file__), '..', 'rawdata', 'recipes')
recipes = []
for filename in os.listdir(path):
    with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
        recipe = json.loads(f.read())
    if 'result' not in recipe:
        continue
    recipes.append(recipe)

with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'all_recipes.json'), 'w+', encoding='utf-8') as f:
    f.write((json.dumps(recipes)))
