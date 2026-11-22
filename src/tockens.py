def create_token(token_type, value, line, column):
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }
