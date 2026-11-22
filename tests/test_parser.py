import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from lexer import tokenize
from parser import parse


source = '''
count: 0b101;
name: @"Alex";
'''

tokens = tokenize(source)
result = parse(tokens)

print("Результат разбора:")
for name, value in result.items():
    print(f"{name} = {value}")