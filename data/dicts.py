from classes import *
import json

# TODO 没写完
"""
经过我的观察（仅就1.19.2而言）
物品在配方文件中出现的位置有：
1. 各个配方的result
2. 烧炼配方的ingredient
3. 有序配方的key
4. 无序配方的ingredients
5. 锻造台配方的base和addition
6. 切石机配方的ingredient
物品在配方文件中出现的形式有：
1. {'item': 'minecraft:xxx'}和{'tag': 'minecraft:xxx'}，可能出现在上面所有6个地方
2. {'item': 'minecraft:xxx', 'count': int}，只可能出现在有序配方和无序配方的result中
3. [{'item': 'minecraft:xxx'}, {'item': 'minecraft:xxx'}, ...]，只可能出现在
4. [{'item': 'minecraft:xxx'}, [{'item': 'minecraft:xxx'}, ...]]，只可能出现在
"""


def transform(sth: dict or list[dict] or str):
    """接收item或tag或它们的列表，甚至要考虑到列表套列表，或者意外地，item的字符串，以及带count的item，返回对应的class形式"""
    if type(sth) == dict:
        if 'item' in sth:
            # 排除掉count字段
            return Item({'item': sth['item']})
        elif 'tag' in sth:
            return Tag(sth)
    elif type(sth) == list:
        for i in range(len(sth)):
            if type(sth[i]) == list:
                # 考虑列表套列表，将这个子列表转换成自定义tag
                sth[i] = {'tag': 'minecraft:diy', 'val': sth[i]}
        return [Item(x) if 'item' in x else Tag(x) for x in sth]
    elif type(sth) == str:
        return Item({"item": sth})


with open(path.join(path.dirname(__file__), 'all_recipes.json'), 'r', encoding='utf-8') as f:
    recipes_ = json.loads(f.read())
    recipes = []
    for recipe in recipes_:
        if 'group' not in recipe:
            recipe['group'] = ''
        match recipe['type']:
            case 'minecraft:blasting':
                if 'cookingtime' in recipe:
                    recipes.append(
                        Blasting(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                 recipe['experience'],
                                 cookingtime=recipe['cookingtime']))
                else:
                    recipes.append(
                        Blasting(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                 recipe['experience']))
            case 'minecraft:campfire_cooking':
                if 'cookingtime' in recipe:
                    recipes.append(
                        Campfire_cooking(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                         recipe['experience'],
                                         cookingtime=recipe['cookingtime']))
                else:
                    recipes.append(
                        Campfire_cooking(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                         recipe['experience']))
            case 'minecraft:smelting':
                if 'cookingtime' in recipe:
                    recipes.append(
                        Smelting(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                 recipe['experience'],
                                 cookingtime=recipe['cookingtime']))
                else:
                    recipes.append(
                        Smelting(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                 recipe['experience']))
            case 'minecraft:smoking':
                if 'cookingtime' in recipe:
                    recipes.append(
                        Smoking(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                recipe['experience'],
                                cookingtime=recipe['cookingtime']))
                else:
                    recipes.append(
                        Smoking(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                recipe['experience']))
            case 'minecraft:crafting_shaped':
                # 先把key里面的值转换成class形式
                for key, value in recipe['key'].items():
                    recipe['key'][key] = transform(recipe['key'][key])
                if 'count' in recipe['result']:
                    recipes.append(
                        Crafting_shaped(recipe['group'], recipe['pattern'], recipe['key'], transform(recipe['result']),
                                        recipe['result']['count']))
                else:
                    recipes.append(
                        Crafting_shaped(recipe['group'], recipe['pattern'], recipe['key'], transform(recipe['result'])))
            case 'minecraft:crafting_shapeless':
                if 'count' in recipe['result']:
                    recipes.append(Crafting_shapeless(recipe['group'], transform(recipe['ingredients']),
                                                      transform(recipe['result']), recipe['result']['count']))
                else:
                    recipes.append(Crafting_shapeless(recipe['group'], transform(recipe['ingredients']),
                                                      transform(recipe['result'])))
            case 'minecraft:smithing':
                recipes.append(Smithing(recipe['group'], transform(recipe['base']), transform(recipe['addition']),
                                        transform(recipe['result'])))
            case 'minecraft:stonecutting':
                recipes.append(
                    Stonecutting(recipe['group'], transform(recipe['ingredient']), transform(recipe['result']),
                                 recipe['count']))
