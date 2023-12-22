import os


def expand_var_and_user(path) -> str:
    return os.path.expanduser(os.path.expandvars(path))


def flatten(t):
    return [item for sublist in t for item in sublist]

