import yaml

from utils.const import default_settings


def read_yaml(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        d = yaml.load(content, Loader=yaml.FullLoader)
    except FileNotFoundError:
        d = default_settings
    return d


def write_yaml(path: str, data: dict):
    with open(path, "w") as f:
        yaml.dump(data, f)
