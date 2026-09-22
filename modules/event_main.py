# event_main.py
# Contains LeagueEventSoundsProgram, which runs the main program.


# Module Imports
import dep_music
from modules.api_communication import APICommunication
from modules.api_communicator import APICommunicator
from modules.settings import Settings


# Library Imports
from pathlib import Path
import pygame
import traceback



class LeagueEventSoundsProgram:
    TIMER_TICK_EVENT = pygame.USEREVENT + 1

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

        # Used to manage connection failure text
        self._connected = False
        self._error_count = 0


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
        Also initializes the 1-second repeating event.
        """
        if self.settings.music_enabled:
            self._setup_player()

        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.mixer.init()

        pygame.time.set_timer(self.TIMER_TICK_EVENT, 1000)


    def _setup_player(self):
        """
        Initializes the music player, raises
        NonMusicFileType exception if any files selected
        are not music files.
        """
        music_list = []
        for path in sorted(Path(self.base_directory + '//music//kda//' + self.settings.music_folder_name).iterdir()):
            if path.is_file():
                music_list.append(path)

        self._music_player = dep_music.MusicPlayer(music_list)


    def main_loop(self, infinite_loop: bool = True) -> None:
        """
        Runs the loop for the League Event Sounds program.
        """
        while infinite_loop:
            self._clock.tick(self.settings.update_rate)  # Regulate loop time to update rate
            self._handle_events()

            communication_obj = self.api_communicator.request_api()
            if communication_obj:
                self._check_stats(communication_obj)
            else:
                self._print_failure_text()


    def _handle_events(self) -> None:
        """
        When run, checks for any events and handles them appropriately
        """
        for event in pygame.event.get():
            if event.type == self.TIMER_TICK_EVENT:
                # Updates the music player timer to tick down duration.
                self._music_player.tick()


    def _check_stats(self, communication_obj: APICommunication) -> None:
        if not self._connected:
            self._print_reconnect_text()
            self._run_player()

        if self.settings.music_enabled:
            self._handle_kda_music(communication_obj)

        if self.settings.sfx_enabled:
            self._handle_sfx(communication_obj)


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