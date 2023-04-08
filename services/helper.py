import logging


def save_as_file(text: str, name: str):
    with open(f'tmp/{name}', 'w+') as file:
        file.write(text)


def prepare_logging():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s: [%(levelname)s] %(message)s', datefmt='%d %b %H:%M:%S')
    logging.addLevelName(logging.ERROR, f"\x1b[31;1m{logging.getLevelName(logging.ERROR)}\x1b[0m")
    logging.addLevelName(logging.WARNING, f"\x1b[33;20m{logging.getLevelName(logging.WARNING)}\x1b[0m")
