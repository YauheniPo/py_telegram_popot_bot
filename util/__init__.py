from os import path


def get_project_dirpath():
    return path.split(path.dirname(path.abspath(__file__)))[0]
