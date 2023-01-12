import os
import json


def write_tags():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'all_tags.json')
    tags = []
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '..', 'rawdata', 'tags')):
        # 遍历文件列表
        # 如果当前文件夹的路径中包含 worldgen，跳过这次遍历，因为这个文件夹下面的tag太tm烦了
        if 'worldgen' in root:
            continue
        for file in files:
            # 检查文件是否为 JSON 文件
            if file.endswith('.json'):
                # 获取文件的完整路径
                file_path = os.path.join(root, file)
                # 获取文件名（不包含 .json 后缀）
                file_name = file[:-5]
                # 读取 JSON 文件
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # 去掉values字段中的’#‘符号
                    for i in range(len(data['values'])):
                        data['values'][i] = data['values'][i].replace('#', '')
                    # 组装新的对象
                    obj = {
                        'tag': 'minecraft:' + file_name,
                        'val': data['values']
                    }
                    # 将新的对象添加到结果列表中
                    tags.append(obj)

    with open(path, 'w+', encoding='utf-8') as f:
        f.write((json.dumps(tags)))
