ONE = 1
MIN_ARGUMENTS = 2


def expect(tokens, pos, token_type):
    if pos >= len(tokens):
        raise SyntaxError(f"Ожидался токен {token_type}")

    token = tokens[pos]

    if token["type"] != token_type:
        raise SyntaxError(
            f"Ожидался {token_type}, получен {token['type']} "
            f"(строка {token['line']}, столбец {token['column']})"
        )

    return token


def parse(tokens):
    result = {}
    pos = 0

    while pos < len(tokens):
        name = expect(tokens, pos, "NAME")
        pos += ONE

        if name["value"] in result:
            raise SyntaxError(
                f"Повторное объявление: {name['value']}"
            )

        expect(tokens, pos, "COLON")
        pos += ONE

        value, pos = parse_value(tokens, pos, result)
        expect(tokens, pos, "SEMICOLON")
        pos += ONE

        result[name["value"]] = value

    return result


def parse_value(tokens, pos, variables):
    if pos >= len(tokens):
        raise SyntaxError("Ожидалось значение")

    token = tokens[pos]
    token_type = token["type"]

    if token_type == "NUMBER":
        return int(token["value"], 2), pos + ONE

    if token_type == "STRING":
        return token["value"], pos + ONE

    if token_type == "ARRAY_START":
        return parse_array(tokens, pos + ONE, variables)

    if token_type == "EXPR_MARK":
        return parse_expression(tokens, pos + ONE, variables)

    raise SyntaxError(f"Недопустимое значение: {token['value']}")


def require_number(value):
    if not isinstance(value, int) or isinstance(value, bool):
        raise SyntaxError("Операция требует числовые аргументы")

    return value


def parse_operand(tokens, pos, variables):
    if pos < len(tokens) and tokens[pos]["type"] == "NAME":
        name = tokens[pos]["value"]

        if name not in variables:
            raise SyntaxError(f"Неизвестная константа: {name}")

        return require_number(variables[name]), pos + ONE

    value, pos = parse_value(tokens, pos, variables)
    return require_number(value), pos


def parse_array(tokens, pos, variables):
    values = []

    if pos < len(tokens) and tokens[pos]["type"] == "RPAREN":
        return values, pos + ONE

    while True:
        value, pos = parse_value(tokens, pos, variables)
        values.append(value)

        if pos >= len(tokens):
            raise SyntaxError("Не закрыт массив")

        if tokens[pos]["type"] == "RPAREN":
            return values, pos + ONE

        expect(tokens, pos, "COMMA")
        pos += ONE


def parse_expression(tokens, pos, variables):
    expect(tokens, pos, "LBRACE")
    pos += ONE

    if pos >= len(tokens):
        raise SyntaxError("Не указана операция")

    operation = tokens[pos]
    pos += ONE

    if operation["type"] in ("PLUS", "MINUS"):
        result, pos = parse_binary(
            tokens, pos, variables, operation["type"]
        )
    elif operation["type"] == "NAME":
        if operation["value"] != "min":
            raise SyntaxError("Неизвестная операция")
        result, pos = parse_min(tokens, pos, variables)
    else:
        raise SyntaxError("Неизвестная операция")

    expect(tokens, pos, "RBRACE")
    return result, pos + ONE


def parse_binary(tokens, pos, variables, operation):
    left, pos = parse_operand(tokens, pos, variables)
    right, pos = parse_operand(tokens, pos, variables)

    if operation == "PLUS":
        return left + right, pos

    return left - right, pos


def parse_min(tokens, pos, variables):
    expect(tokens, pos, "LPAREN")
    pos += ONE
    values = []

    while True:
        value, pos = parse_operand(tokens, pos, variables)
        values.append(value)

        if pos >= len(tokens):
            raise SyntaxError("Не закрыта функция min")

        if tokens[pos]["type"] == "RPAREN":
            break

        expect(tokens, pos, "COMMA")
        pos += ONE

    if len(values) < MIN_ARGUMENTS:
        raise SyntaxError("min требует минимум два аргумента")

    return min(values), pos + ONE