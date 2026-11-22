def expect(tokens, position, token_type):
    if position >= len(tokens):
        raise SyntaxError(f"Ожидался токен {token_type}")

    if tokens[position]["type"] != token_type:
        raise SyntaxError(f"Ожидался токен {token_type}")

    return tokens[position]


def parse(tokens):
    result = {}
    position = 0

    while position < len(tokens):
        name = expect(tokens, position, "NAME")
        position += 1

        expect(tokens, position, "COLON")
        position += 1

        value = tokens[position] if position < len(tokens) else None

        if value is None or value["type"] not in (
            "NUMBER", "STRING"
        ):
            raise SyntaxError("Ожидалось число или строка")

        result[name["value"]] = value["value"]
        position += 1

        expect(tokens, position, "SEMICOLON")
        position += 1

    return result