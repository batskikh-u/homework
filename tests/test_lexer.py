import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from lexer import tokenize


source = 'count: 0b101;'
tokens = tokenize(source)

for token in tokens:
    print(token)