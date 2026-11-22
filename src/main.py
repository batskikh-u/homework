import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent / "src")
)

from lexer import tokenize
from parser import parse
from toml_generator import generate_toml


EXIT_FAILURE = 1


def main():
    try:
        if len(sys.argv) > 1:
            source = Path(sys.argv[1]).read_text(encoding="utf-8")
        else:
            source = sys.stdin.read()

        tokens = tokenize(source)
        data = parse(tokens)
        print(generate_toml(data))

    except (SyntaxError, ValueError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()
