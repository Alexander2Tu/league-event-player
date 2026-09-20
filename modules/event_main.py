# event_main.py
# Contains LeagueEventSoundsProgram, which runs the main program.
import traceback
from pathlib import Path

import dep_music
# Module Imports
from modules.api_communicator import APICommunicator
from modules.settings import Settings
import modules.settings_parser


# Library Imports
import pygame




class LeagueEventSoundsProgram:
    def __init__(self, api_communicator: APICommunicator,
                 settings: Settings,
                 base_directory: str = '.'):
        # Saved Arguments
        self.api_communicator = api_communicator
        self.settings = settings
        self.base_directory = base_directory    # Path to root of program

        # Main Variables
        self._previous_api_response = None
        self._clock = None


    def run(self) -> None:
        """
        Runs the League Event Sounds Program.
        """
        try:
            self.initialize_all_pygame_resources()
            self.main_loop()
        except Exception as e:
            if self._music_player is not None:
                self._stop_player()
            self._print_appropriate_error_message(e)


    def initialize_all_pygame_resources(self):
        """
        Initializes all pygame resources: music player, clock, and mixer.
        """
        if self.settings.music_enabled:
            self._setup_player()
        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.mixer.init()

        self._test_run_player()     # Test for NonMusicFileType Error


    def _setup_player(self):
        """
        Initializes the music player
        """
        music_list = []
        for path in sorted(Path(self.base_directory + '//music//kda//' + self.settings.music_folder_name).iterdir()):
            if path.is_file():
                music_list.append(path)

        self._music_player = dep_music.MusicPlayer(music_list)


    def _test_run_player(self):
        """
        Briefly runs all music tracks to test for invalid file types.
        Raises NonMusicFileType if unable to run any music track.
        """
        self._music_player.mute_all()





    def main_loop(self):
        pass


    def _print_appropriate_error_message(self, e: Exception):
        """
        Given an exception that occurred during running of program,
        prints expected or unexpected error messages to aid the user.
        """
        if type(e) is dep_music.EmptyMusicPlaylistError:
            print(f'ERROR: Music player failed to find music tracks in '
                  f'"music/kda/{self.settings.music_folder_name}", please check that '
                  f'the music folder is non-empty or disable music in the settings.')
        elif type(e) is dep_music.NonMusicFileType:
            print(f'ERROR: Music player failed to run on provided music tracks in '
                  f'"music/kda/{self.settings.music_folder_name}", please check that all '
                  f'tracks are valid music files.')
        else:
            print(f'Program ran into unexpected |{type(e)}| exception.')
            print(f'Error message: {e}')
            print(f'Full traceback: {traceback.format_exc()}')

        input('Press any key to exit program...')