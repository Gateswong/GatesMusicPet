def trim_quote(text):
    if len(text) > 2 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    return text

