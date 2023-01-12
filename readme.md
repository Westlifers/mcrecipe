## Mcrecipe: 关于Minecraft配方的小工具

### 功能
funcs.py提供了一些入口函数
1. `query_recipe_by_name`，通过物品中文名查询合成配方
2. `find_closest_str`，便于处理用户输入错误的情况

### 配方类的说明
`query_recipe_by_name`返回一个包含了查询到的配方之对象列表，每个对象的__str__方法会按预设的格式打印出配方。如果你对这方法不满意，可以修改。
每个对象还有一个image方法，返回一张示例图片(PIL的Image对象)，对多可能配方默认取每个位置的第一个物品。目前只有有序配方、无序配方和烧炼配方有image()方法。

### 数据提取
所有数据来源于游戏`Minecraft`，内容遵循Minecraft的使用许可协议（https://account.mojang.com/terms#license）

由于游戏特性，配方依赖于游戏版本，本项目默认使用`1.19.2`之数据。欲使用其它版本，需更改`data`目录下的数据

1. 在rawdata目录下添加你获取到的对应版本的配方文件夹(recipes)以及标签文件夹(tags)，获取方法见：[如何获取配方和tags](https://www.reddit.com/r/Minecraft/comments/dccl9j/crafting_recipe_json_files/)
2. 在rawdata目录下添加你获取到的对应版本的中文译名对照，获取方法见：[如何获取语言文件](https://www.bilibili.com/read/cv17737809/)
3. 在data目录下添加你获取到的对应版本的物品图片文件，获取方法见：[如何获取物品图片](https://mc.nerothe.com/) 。注：[来源](https://mc.nerothe.com/)
4. 运行dataprocess目录下的collect.py文件，程序会在data文件夹中生成`all_tags.json` `all_tags.json` `namespace.json`
