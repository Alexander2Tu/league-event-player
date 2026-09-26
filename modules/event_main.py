# event_main.py
# Contains LeagueEventSoundsProgram, which runs the main program.


# Module Imports
import dep_music
from modules import custom_exceptions
from modules.api_communication import APICommunication
from modules.api_communicator import APICommunicator
from modules.settings import Settings


# Library Imports
from pathlib import Path
import pygame
import random
import time
import traceback



class LeagueEventSoundsProgram:
    TIMER_TICK_EVENT = pygame.USEREVENT + 1

    def __init__(self, api_communicator: APICommunicator,
                 settings: Settings,
                 base_directory: str = '.',
                 print_log_path: str = ''):
        # Saved Arguments
        self.api_communicator = api_communicator
        self.settings = settings
        self.base_directory = base_directory    # Path to root of program
        self.print_log_path = print_log_path

        # For printing to file without closing
        self.print_file = None

        # Main Variables
        self._previous_api_response = None
        self._clock = None
        self._music_player = None
        self._sfx_sound_dict = dict()

        # Used to manage connection failure text
        self._connected = False
        self._error_count = 0


    def run(self) -> None:
        """
        Runs the League Event Sounds Program.
        """
        exception_exit = False
        try:
            self.initialize_all_pygame_resources()
            self.main_loop()
        except Exception as e:
            self._print_appropriate_error_message(e)
            exception_exit = True
        finally:
            self._close_all_resources()

        if exception_exit:
            input('Press any key to exit program...')


    def initialize_all_pygame_resources(self):
        """
        Initializes all pygame resources: music player, clock, and mixer.
        Also initializes the 1-second repeating event.
        """
        if self.settings.music_enabled:
            self._setup_player()
            self.log('Music player set up!')
        else:
            self.log('Music player disabled; skipping...')

        if self.settings.sfx_enabled:
            self._setup_sfx()
            self.log('Sound effects set up!')
        else:
            self.log('Sound effects disabled; skipping...')

        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.mixer.init()

        pygame.time.set_timer(self.TIMER_TICK_EVENT, 1000)
        self.log('Pygame finished setting up!')


    def _setup_player(self):
        """
        Initializes the music player, raises
        NonMusicFileType exception if any files selected
        are not music files.
        """
        music_list = []
        for path in sorted(Path(self.base_directory + '//music//' + self.settings.music_folder_name).iterdir()):
            if path.is_file():
                music_list.append(path)

        self._music_player = dep_music.MusicPlayer(music_list)


    def _setup_sfx(self):
        event_types = 'kills', 'deaths', 'assists'
        for event_type in event_types:
            sound_list = []
            for sound_file in (
                    Path(f'{self.base_directory}//sounds//{self.settings.sfx_folder}//{event_type}').iterdir()):
                if sound_file.is_file():
                    try:
                        sound = pygame.mixer.Sound(sound_file.open('r'))
                        sound.set_volume(self.settings.sfx_volume)
                        sound_list.append(sound)
                    except pygame.error:
                        raise custom_exceptions.NonSoundFileType(f'{self.base_directory}//sounds//{event_type}')
            if len(sound_list) == 0:
                raise custom_exceptions.EmptySoundFolder(f'{self.base_directory}//sounds//{event_type}')
            self._sfx_sound_dict[event_type] = sound_list


    def main_loop(self, infinite_loop: bool = True) -> None:
        """
        Runs the loop for the League Event Sounds program.
        """
        while infinite_loop:
            self._clock.tick(self.settings.update_rate)  # Regulate loop time to update rate
            self._handle_pygame_events()

            communication_obj = self.api_communicator.request_api()
            if communication_obj:
                self._check_stats(communication_obj)
            else:
                self._connected = False
                self._stop_player()
                self._print_failure_text()


    def _handle_pygame_events(self) -> None:
        """
        When run, checks for any events and handles them appropriately
        """
        for event in pygame.event.get():
            if event.type == self.TIMER_TICK_EVENT:
                # Updates the music player timer to tick down duration.
                if self._music_player.get_duration() > 0:
                    self._music_player.tick()


    def _check_stats(self, communication_obj: APICommunication) -> None:
        """
        Using the provided APICommunication, handles playing music
        and sound effects.
        """
        if not self._connected:
            self._print_reconnect_text()
            self._error_count = 0
            self._connected = True
            self._run_player()

        if self.process_kda_changes(communication_obj):
            if self.settings.sfx_enabled:
                self._handle_sfx(communication_obj)

            if self.settings.music_enabled:
                self._handle_kda_music(communication_obj)

        self._previous_api_response = communication_obj


    def _print_reconnect_text(self):
        """
        Prints message informing of reconnection.
        """
        self.log(f'Successfully connected!')


    def _run_player(self):
        """
        Runs the music player.
        """
        if not self._music_player.get_running():
            self._music_player.run(True)
            self._adjust_volume(self.settings.music_volume_list)
            self._music_player.solo(0)


    def _adjust_volume(self, volume_list: list[float]) -> None:
        """
        Given a list for volumes, changes the volume
        for each music track
        """
        for i in range(len(volume_list)):
            try:
                self._music_player.set_volume(i, volume_list[i])

            except IndexError:
                self.log(f'ERROR: Invalid music index {i} for volume of music')


    def process_kda_changes(self, communication_obj: APICommunication) -> bool:
        """
        Given an APICommunication, returns True if any of the KDA stats
        changed. Also sets music timer for recent kills.
        """
        if self._previous_api_response is None:
            return False

        if (communication_obj.kills > self._previous_api_response.kills or
                communication_obj.assists > self._previous_api_response.assists):
            self._music_player.set_duration(10)
            return True
        elif communication_obj.deaths > self._previous_api_response.deaths:
            return True
        else:
            return False


    def _handle_kda_music(self, communication_obj: APICommunication) -> None:
        """
        Given an APICommunication, handles the changing of music.
        """
        deaths = max(0.5, communication_obj.deaths)  # Prevent division by zero
        kda = (communication_obj.kills + communication_obj.assists) / deaths

        chosen_phase = 0

        # Determine music phase based on kda
        for i in range(len(self.settings.kda_threshold_list)):
            if kda >= self.settings.kda_threshold_list[i]:
                chosen_phase = i
                break

        # Increase phase if recently killed
        if self._music_player.get_duration() != 0:
            chosen_phase += 1

        # Zero out phase if dead
        if communication_obj.is_dead:
            chosen_phase = 0

        # Correct to music limits
        chosen_phase = min(chosen_phase, len(self._music_player.get_channels()) - 1)
        chosen_phase = max(0, chosen_phase)

        self._music_player.solo(chosen_phase)


    def _handle_sfx(self, communication_obj: APICommunication) -> None:
        """
        Given an APICommunication, handles the playing of sound effects.
        """
        if communication_obj.kills > self._previous_api_response.kills:
            random.choice(self._sfx_sound_dict['kills']).play(0)

        if communication_obj.deaths > self._previous_api_response.deaths:
            random.choice(self._sfx_sound_dict['deaths']).play(0)

        if communication_obj.assists > self._previous_api_response.assists:
            random.choice(self._sfx_sound_dict['assists']).play(0)


    def _stop_player(self) -> None:
        """
        When called, stops the music player.
        """
        if self._music_player:
            self._music_player.stop_all()


    def _print_failure_text(self):
        """
        When called, prints error connecting message.
        """
        self._error_count += 1
        for i in range(5, 0, -1):
            if i > 1:
                self.log(f'\rError connecting ({self._error_count}); trying again in {i} seconds...', end='')
            else:
                self.log(f'\rError connecting ({self._error_count}); trying again in {i} second...', end='')
            time.sleep(1)


    def _print_appropriate_error_message(self, e: Exception):
        """
        Given an exception that occurred during running of program,
        prints expected or unexpected error messages to aid the user.
        """
        if type(e) is dep_music.EmptyMusicPlaylistError:
            self.log(f'ERROR: Music player failed to find music tracks in '
                     f'"music/kda/{self.settings.music_folder_name}", please check that '
                     f'the music folder is non-empty or disable music in the settings.')
        elif type(e) is dep_music.NonMusicFileType:
            self.log(f'ERROR: Music player failed to run on provided music tracks in '
                     f'"music/kda/{self.settings.music_folder_name}", please check that all '
                     f'tracks are valid music files.')
        elif type(e) is custom_exceptions.NonSoundFileType:
            self.log(f'ERROR: Sound player failed to load provided sound files in '
                     f'"{e.path_to_error}", please check that all '
                     f'tracks are valid sound files.')
        elif type(e) is custom_exceptions.EmptySoundFolder:
            self.log(f'ERROR: Sound player found no sound files in '
                     f'"{e.path_to_error}", please add sound files in there '
                     f'or disable sound effects in the settings.')
        else:
            self.log(f'Program ran into unexpected |{type(e)}| exception.')
            self.log(f'Error message: {e}')
            self.log(f'Full traceback: {traceback.format_exc()}')


    def _close_all_resources(self):
        """
        When run, closes all resources (expected to happen at end of program)
        """
        if self._music_player is not None:
            self._stop_player()
            self._music_player = None
        if self.print_file is not None:
            self.print_file.close()
            self.print_file = None


    def log(self, print_message: str, end: str = '\n'):
        """
        Given a string, prints to the console or log file
        depending on initial construction input.
        """
        if self.print_log_path:
            if self.print_file:
                self.print_file.write(f'{print_message}{end}')
                self.print_file.flush()
            else:
                self.print_file = open(self.print_log_path, 'a')
        else:
            print(print_message, end=end)
