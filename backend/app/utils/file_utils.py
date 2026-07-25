from pathlib import Path


def file_exists(path: str) -> bool:
    return Path(path).exists()


def create_directory(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
