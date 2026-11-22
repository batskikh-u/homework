
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "src")
)

from lexer import tokenize
from parser import parse
from toml_generator import generate_toml


TEST_DIR = Path(__file__).resolve().parent


def translate_file(filename):
    source = (TEST_DIR / filename).read_text(encoding="utf-8")
    return generate_toml(parse(tokenize(source)))


class TestTranslator(unittest.TestCase):

    def test_server_config(self):
        result = translate_file("server.conf")
        print(result)

    def test_game_config(self):
        result = translate_file("game.conf")
        print(result)

