# from data.dicts import namespace, tags
"""注意，item是指Item类，或者{'item': 'minecraft:xxx'}这样的一个字典，而tag是指Tag类，或者{'tag': 'minecraft:xxx'}这样的一个字典"""
from PIL import Image
from os import path
import json
# 为了避免与dicts形成互引用，直接把这段代码搬过来了......
# 定义全局变量namespace，tags以及全配方recipes
namespace_path = path.join(path.dirname(__file__), 'data', 'namespace.json')
tags_path = path.join(path.dirname(__file__), 'data', 'all_tags.json')
with open(namespace_path, 'r', encoding='utf-8') as f:
    namespace = json.loads(f.read())
with open(tags_path, 'r', encoding='utf-8') as f:
    tags = json.loads(f.read())


class Item:
    def __init__(self, item: dict[str, str]):
        self.id = item['item']
        for name, id in namespace.items():
            if id == self.id:
                self.name = name
                return
        self.name = None


class Tag:
    def __init__(self, tag: dict[str, list]):
        # 先来考虑item列表形成的自定义tag
        if tag['tag'] == 'minecraft:diy':
            self.tag = 'minecraft:diy'
            self.val = [Item(x) for x in tag['val']]
            return
        # 然后才是正常情况
        self.tag = tag['tag']
        val = []

        # 把self.val转换成真正的Name的列表，需要递归，因为tmd tags里面的值可能还包含了tags
        def standardize_val(tag_, sign: bool = False):
            # sign用来标记是否是由同名tag递归而入
            for ob in tags:
                if ob['tag'] == tag_:
                    for tag_or_item in ob['val']:
                        # 先判断是否是tag
                        # 但如果是同名tag递归而入，就跳过属于自己的那次循环
                        if sign and tag_or_item == tag_:
                            continue
                        flag = False  # 是否是tag
                        for ob_ in tags:
                            if ob_['tag'] == tag_or_item:
                                flag = True
                                # 接下来就要递归了，但在递归前需要规避一个bug：tag有同名item，会导致无限递归
                                # 解决方法：此时立即判断自己是否在自己的val中时，若是，直接将自己添加进结果，并标记sign为True，函数会在下次递归判断是否递归时判断tag时跳过自己
                                if tag_or_item in ob_['val']:
                                    # 进入bug区域
                                    val.append(Item({'item': tag_or_item}))
                                    sign = True
                        # 若是，递归
                        if flag:
                            standardize_val(tag_or_item, sign)
                            sign = False
                        # 若否，加入val
                        else:
                            val.append(Item({'item': tag_or_item}))
        standardize_val(tag['tag'])
        self.val = val


def get_image_by_Item(item: Item) -> Image:
    """通过Item对象返回对应的图片"""
    filename = item.id.replace('minecraft:', '')
    images_path = path.join(path.dirname(__file__), 'data', 'images', filename + '.png')
    return Image.open(images_path)


# 配方通用类
class Recipe:
    def __init__(self, type_: str, group: str):
        self.type = type_  # 配方种类
        self.group = group  # 配方分组


# 烧炼配方通用类
class Burning(Recipe):
    def __init__(self, type_: str, group: str, ingredient: Item or Tag or list[Item], result: Item, experience: float, cookingtime: int):
        Recipe.__init__(self, type_, group)
        self.ingredient = ingredient
        self.result = result
        self.experience = experience
        self.cookingtime = cookingtime

    def __str__(self):
        d = {'minecraft:blasting': '高炉', 'minecraft:campfire_cooking': '营火', 'minecraft:smelting': '熔炉', 'minecraft:smoking': '烟熏炉'}
        cache = {}
        if type(self.ingredient) == list:
            ingredient = self.ingredient[0]
            ingredient.name += '等'
            cache[ingredient] = self.ingredient[1:]
        elif type(self.ingredient) == Tag:
            ingredient = self.ingredient.val[0]
            ingredient.name += '等'
            cache[ingredient] = self.ingredient.val[1:]
        else:
            ingredient = self.ingredient
        rep = f'''烧炼配方（{d[self.type]}）
{ingredient.name}\t
🔥\t -> {self.result.name}
燃料
        '''
        if cache:
            rep += f'\n其中，{list(cache.keys())[0].name}可以替换成{[x.name for x in list(cache.values())[0]]}'
        rep += f'\n烧炼时间：{self.cookingtime}秒'
        return rep

    def image(self) -> Image:
        background = Image.open(path.join(path.dirname(__file__), 'data', 'images', 'burning.png'))
        if type(self.ingredient) == list:
            ingredient = self.ingredient[0]
        elif type(self.ingredient) == Tag:
            ingredient = self.ingredient.val[0]
        else:
            ingredient = self.ingredient
        ingredient_pos, fuel_pos, result_pos = (17, 17), (17, 107), (162, 57)
        ingredient = get_image_by_Item(ingredient).resize((30, 30))
        fuel = Image.open(path.join(path.dirname(__file__), 'data', 'images', 'coal.png')).resize((30, 30))
        result = get_image_by_Item(self.result).resize((40, 40))
        background.paste(ingredient, (ingredient_pos[0], ingredient_pos[1], ingredient_pos[0] + ingredient.width, ingredient_pos[1] + ingredient.height), ingredient)
        background.paste(fuel, (fuel_pos[0], fuel_pos[1], fuel_pos[0] + fuel.width, fuel_pos[1] + fuel.height), fuel)
        background.paste(result, (result_pos[0], result_pos[1], result_pos[0] + result.width, result_pos[1] + result.height), result)
        return background


# 高炉配方
class Blasting(Burning):
    def __init__(self, group: str, ingredient: Item or Tag or list[Item], result: Item, experience: float, cookingtime: int = 5):
        Burning.__init__(self, 'minecraft:blasting', group, ingredient, result, experience, cookingtime)


# 营火配方
class Campfire_cooking(Burning):
    def __init__(self, group: str, ingredient: Item or Tag or list[Item], result: Item, experience: float, cookingtime: int = 5):
        Burning.__init__(self, 'minecraft:campfire_cooking', group, ingredient, result, experience, cookingtime)


# 熔炉配方
class Smelting(Burning):
    def __init__(self, group: str, ingredient: Item or Tag or list[Item], result: Item, experience: float, cookingtime: int = 5):
        Burning.__init__(self, 'minecraft:smelting', group, ingredient, result, experience, cookingtime)


# 烟熏炉配方
class Smoking(Burning):
    def __init__(self, group: str, ingredient: Item or Tag or list[Item], result: Item, experience: float, cookingtime: int = 5):
        Burning.__init__(self, 'minecraft:smoking', group, ingredient, result, experience, cookingtime)


# 有序配方
class Crafting_shaped(Recipe):
    def __init__(self, group: str, pattern: list[str], key: dict[str, Item or Tag or list[Item]], result: Item, count: int = 1):
        Recipe.__init__(self, 'minecraft:crafting_shaped', group)
        self.pattern = [list(x) for x in pattern]  # 将'## '形式转换为['#', '#', ' ']形式
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[0])):
                if self.pattern[i][j] == ' ':
                    self.pattern[i][j] = '/'  # 将['#', '#', ' ']形式转换为['#', '#', '/']形式
        self.key = key
        self.result = result
        self.count = count

    def __str__(self):
        rep = '有序配方：\n'
        rep += f'按以下规则摆放物品以生成 {self.result.name}{(" * " + str(self.count)) if self.count > 1 else ""}\n'
        for row in self.pattern:
            row_str = '\t'.join(row)
            rep += row_str + '\n'
        rep += '其中：\n'
        for item, value in self.key.items():
            if type(value) == Item:
                rep += f'{item} 是 {value.name}\n'
            elif type(value) == Tag:
                rep += f'{item} 可以是 {[x.name for x in value.val]}\n'
            else:
                rep += f'{item} 可以是 {[x.name for x in value]}\n'
        return rep
    
    def image(self) -> Image:
        background = Image.open(path.join(path.dirname(__file__), 'data', 'images', 'crafting_shaped.png'))
        pattern_pos = [
            [(17, 17), (62, 17), (107, 17)],
            [(17, 62), (62, 62), (107, 62)],
            [(17, 107), (62, 107), (107, 107)]
        ]
        result_pos = (210, 60)
        pattern = []
        for i in range(len(self.pattern)):
            row = []
            for j in range(len(self.pattern[i])):
                if self.pattern[i][j] == '/':
                    row.append(None)
                else:
                    if type(self.key[self.pattern[i][j]]) == list:
                        item = self.key[self.pattern[i][j]][0]
                    elif type(self.key[self.pattern[i][j]]) == Tag:
                        item = self.key[self.pattern[i][j]].val[0]
                    else:
                        item = self.key[self.pattern[i][j]]
                    img = get_image_by_Item(item).resize((30, 30))
                    row.append(img)
            pattern.append(row)
        result = get_image_by_Item(self.result).resize((38, 38))
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                if pattern[i][j] is None:
                    continue
                background.paste(pattern[i][j], (pattern_pos[i][j][0], pattern_pos[i][j][1], pattern[i][j].width + pattern_pos[i][j][0], pattern[i][j].height + pattern_pos[i][j][1]), pattern[i][j])
        background.paste(result, (result_pos[0], result_pos[1], result_pos[0] + result.width, result_pos[1] + result.height), result)
        return background


# 无序配方
class Crafting_shapeless(Recipe):
    def __init__(self, group: str, ingredients: list[Item or Tag], result: Item, count: int = 1):
        # ingredients会出现列表套列表，但转换成了自定义tag
        Recipe.__init__(self, 'minecraft:crafting_shapeless', group)
        self.ingredients = ingredients
        self.result = result
        self.count = count

    def __str__(self):
        rep = '无序配方：\n'
        cache = {}
        result = []
        for x in self.ingredients:
            if type(x) == Item:
                result.append(x.name)
            else:
                result.append(x.val[0].name + '等')
                cache[x.val[0].name] = x.val[1:]
        rep += f'将下列物品任意摆放以生成 {self.result.name}{(" * " + str(self.count)) if self.count > 1 else ""}\n{result}'
        if cache:
            rep += '\n其中：\n'
            for key, value in cache.items():
                rep += f'{key} 还可以是 {[x.name for x in value]}\n'
        return rep
    
    def image(self) -> Image:
        background = Image.open(path.join(path.dirname(__file__), 'data', 'images', 'crafting_shapeless.png'))
        ingredients_pos = [
            [(17, 17), (62, 17), (107, 17)],
            [(17, 62), (62, 62), (107, 62)],
            [(17, 107), (62, 107), (107, 107)]
        ]
        result_pos = (205, 60)
        ingredients = []
        for item in self.ingredients:
            if type(item) == Tag:
                item = item.val[0]
            ingredients.append(get_image_by_Item(item).resize((30, 30)))
        result = get_image_by_Item(self.result).resize((38, 38))
        for n in range(len(ingredients)):
            i = n // 3
            j = n % 3
            background.paste(ingredients[n], (ingredients_pos[i][j][0], ingredients_pos[i][j][1], ingredients[n].width + ingredients_pos[i][j][0], ingredients[n].height + ingredients_pos[i][j][1]), ingredients[n])
        background.paste(result, (result_pos[0], result_pos[1], result_pos[0] + result.width, result_pos[1] + result.height), result)
        return background


# 锻造台配方
class Smithing(Recipe):
    def __init__(self, group: str, base: Item or Tag, addition: Item or Tag, result: Item):
        # 据wiki，base有可能包含tag，但实际上没看到tag。为保险起见，还是在init中考虑一下tag的情况。addition也是这样。
        # wiki也没指定result一定是一个item，但实际上只有一个item
        Recipe.__init__(self, 'minecraft:smithing', group)
        self.base = base
        self.addition = addition
        self.result = result

    def __str__(self):
        rep = '锻造台配方：\n'
        rep += f'{self.base.name} 🔨 {self.addition.name} -> {self.result.name}'
        return rep


# 切石机配方
class Stonecutting(Recipe):
    def __init__(self, group: str, ingredient: Item or Tag, result: Item, count: int):
        # 同理，据wiki，ingredient也可能是tag，但实际上没看到tag
        Recipe.__init__(self, 'minecraft:stonecutting', group)
        self.ingredient = ingredient
        self.result = result
        self.count = count

    def __str__(self):
        rep = '切石机配方：\n'
        rep += f'{self.ingredient.name} ⚙️-> {self.result.name}{(" * " + str(self.count)) if self.count > 1 else ""}'
        return rep

