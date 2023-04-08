def save_as_file(text: str, name: str):
    with open(f'tmp/{name}', 'w+') as file:
        file.write(text)
