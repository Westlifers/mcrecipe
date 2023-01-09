import json
from os import path
import re

target_file = path.join(path.dirname(__file__), '..', 'data', 'namespace.json')
namespace = {}
with open(path.join(path.dirname(__file__), '..', 'rawdata', 'zh-cn.json')) as f:
    raw_data = json.loads(f.read())
pattern = re.compile(r'(minecraft.*)')
for namespaceid, chinese in raw_data.items():
    if 'minecraft' in namespaceid:
        name = pattern.findall(namespaceid)[0]
        name = name.replace('.', ':', 1).replace('.', '_')
        namespace[chinese] = name


with open(target_file, 'w+', encoding='utf-8') as f:
    f.write(json.dumps(namespace))
