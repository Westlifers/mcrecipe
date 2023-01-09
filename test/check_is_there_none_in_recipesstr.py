from funcs import translate_recipestr_into_chinese, turn_recipe_into_Recipe
from data.dicts import recipes

none = 0
wrong = 0
for recipe in recipes:
    try:
        r = translate_recipestr_into_chinese(str(turn_recipe_into_Recipe(recipe)))
        if r is None:
            none += 1
    except Exception as e:
        print(recipe)
        print(e)
        wrong += 1

print(f'发现None：{none}个')
print(f'发现错误：{wrong}个')
