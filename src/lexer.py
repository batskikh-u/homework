import re

from tockens import create_token


def token_name(text, position, line, column):
    cur_name = ""

    for i in range(position, len(text)):
        if re.fullmatch(r"[a-zA-Z0-9]", text[i]):
            cur_name += text[i]
        else:
            break

    if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", cur_name):
        return None

    token = create_token("NAME", cur_name, line, column)

    return token, position + len(cur_name), line, column + len(cur_name)


def token_number(text, position, line, column):
    cur_number = ""

    for i in range(position, len(text)):
        if re.fullmatch(r"[01bB]", text[i]):
            cur_number += text[i]
        else:
            break

    if not re.fullmatch(r"0[bB][01]+", cur_number):
        return None

    token = create_token("NUMBER", cur_number, line, column)

    return token, position + len(cur_number), line, column + len(cur_number)


def token_string(text, position, line, column):
    if text[position:position + 2] != '@"':
        return None

    cur_string = ""

    for i in range(position + 2, len(text)):
        if text[i] != '"':
            cur_string += text[i]
        else:
            break
    else:
        return None

    token = create_token("STRING", cur_string, line, column)

    end_position = i + 1
    end_column = column + end_position - position

    return token, end_position, line, end_column


def token_comment(text, position, line, column):
    if text[position:position + 2] != "||":
        return None

    start = position
    position += 2

    while position < len(text) and text[position] != "\n":
        position += 1

    new_column = column + position - start

    return None, position, line, new_column


def token_symbol(text, position, line, column):
    symbols = {
        ":": "COLON",
        ";": "SEMICOLON",
        ",": "COMMA",
        "#": "ARRAY_MARK",
        "(": "LPAREN",
        ")": "RPAREN",
        "+": "PLUS",
        "-": "MINUS",
        "?": "EXPR_MARK",
        "{": "LBRACE",
        "}": "RBRACE"
    }
    char = text[position]
    if char not in symbols:
        return None
    token = create_token(
        symbols[char],
        char,
        line,
        column
    )
    return token, position + 1, line, column + 1


def tokenize(text):
    tokens = []
    position = 0
    line = 1
    column = 1
    while position < len(text):
        char = text[position]
        if char in " \t\r":
            position += 1
            column += 1
            continue
        if char == "\n":
            position += 1
            line += 1
            column = 1
            continue
        result = None
        if text[position:position + 2] == "||":
            result = token_comment(text, position, line, column)
        elif char.isalpha():
            result = token_name(text, position, line, column)
        elif char == "0":
            result = token_number(text, position, line, column)
        elif char == "@":
            result = token_string(text, position, line, column)
        else:
            result = token_symbol(text, position, line, column)
        if result is None:
            raise SyntaxError(
                f"Неизвестный символ {char!r}, "
                f"строка {line}, столбец {column}")
        token, position, line, column = result
        if token is not None:
            tokens.append(token)
    return tokens
