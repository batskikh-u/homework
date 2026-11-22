import json


def format_value(value):
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)

    if isinstance(value, list):
        items = [format_value(item) for item in value]
        return "[" + ", ".join(items) + "]"

    return str(value)


def generate_toml(data):
    lines = []

    for name, value in data.items():
        lines.append(f"{name} = {format_value(value)}")

    return "\n".join(lines)