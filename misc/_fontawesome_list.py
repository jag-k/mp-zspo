from os import listdir
from re import compile

from misc import BASE_DIR

icon = compile(r'id="([a-z\-]+)"')

path = BASE_DIR / "src" / "sprites"

FILES = list(map(lambda x: path / x, listdir(path)))

for f in FILES:
    with open(f, 'r') as file:
        print(f)
        print('enum("' + '", "'.join(icon.findall(file.read())) + '")')
        print()
