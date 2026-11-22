import json
import re

from tokens import create_token


SYMBOLS = {
    ":": "COLON",
    ";": "SEMICOLON",
    ",": "COMMA",
    ")": "RPAREN",
    "(": "LPAREN",
    "+": "PLUS",
    "-": "MINUS",
    "?": "EXPR_MARK",
    "{": "LBRACE",
    "}": "RBRACE"
}

ONE = 1
TWO = 2


def read_name(text, pos, line, column):
    match = re.match(r"[a-zA-Z][a-zA-Z0-9]*", text[pos:])

    if not match:
        raise SyntaxError("Некорректное имя")

    value = match.group()
    token = create_token("NAME", value, line, column)

    return token, pos + len(value), column + len(value)


def read_number(text, pos, line, column):
    match = re.match(r"0[bB][01]+", text[pos:])

    if not match:
        raise SyntaxError(f"Некорректное число: строка {line}")

    value = match.group()
    end = pos + len(value)

    if end < len(text) and text[end].isalnum():
        raise SyntaxError(f"Некорректное число: строка {line}")

    token = create_token("NUMBER", value, line, column)
    return token, end, column + len(value)


def read_string(text, pos, line, column):
    end = pos + TWO
    escaped = False

    while end < len(text):
        char = text[end]

        if char == "\n":
            break

        if char == '"' and not escaped:
            raw = text[pos + ONE:end + ONE]

            try:
                value = json.loads(raw)
            except json.JSONDecodeError as error:
                raise SyntaxError(
                    f"Некорректная строка: строка {line}"
                ) from error

            length = end + ONE - pos
            token = create_token("STRING", value, line, column)
            return token, end + ONE, column + length

        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False

        end += ONE

    raise SyntaxError(f"Незакрытая строка: строка {line}")


def read_symbol(text, pos, line, column):
    if text[pos:pos + TWO] == "#(":
        token = create_token("ARRAY_START", "#(", line, column)
        return token, pos + TWO, column + TWO

    char = text[pos]

    if char not in SYMBOLS:
        raise SyntaxError(
            f"Неизвестный символ {char!r}: "
            f"строка {line}, столбец {column}"
        )

    token = create_token(SYMBOLS[char], char, line, column)
    return token, pos + ONE, column + ONE


def skip_comment(text, pos, column):
    while pos < len(text) and text[pos] != "\n":
        pos += ONE
        column += ONE

    return pos, column


def tokenize(text):
    tokens = []
    pos = 0
    line = ONE
    column = ONE

    while pos < len(text):
        char = text[pos]

        if char in " \t\r":
            pos += ONE
            column += ONE
            continue

        if char == "\n":
            pos += ONE
            line += ONE
            column = ONE
            continue

        if text[pos:pos + TWO] == "||":
            pos, column = skip_comment(text, pos, column)
            continue

        if text[pos:pos + TWO] == '@"':
            result = read_string(text, pos, line, column)
        elif char.isascii() and char.isalpha():
            result = read_name(text, pos, line, column)
        elif char == "0":
            result = read_number(text, pos, line, column)
        else:
            result = read_symbol(text, pos, line, column)

        token, pos, column = result
        tokens.append(token)

    return tokens