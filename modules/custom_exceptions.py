# custom_exceptions.py
# Contains all custom exceptions used in the
# LeagueEventPlayer.


class NonSoundFileType(Exception):
    def __init__(self, path_of_error: str):
        self.path_of_error = path_of_error


class EmptySoundFolder(Exception):
    def __init__(self, path_of_error: str):
        self.path_of_error = path_of_error
