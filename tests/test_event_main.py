import unittest

from modules.event_main import *
from modules.settings import Settings


class TestEventMain(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(
                    update_rate=30,
                    sfx_enabled=True,
                    music_enabled=True,
                    sfx_volume=0.5,
                    music_preset='grasswalk',
                    sfx_folder='default',
                    backup_name='JohnLeague#NA1',
                    music_volume_list=[0.9, 0.9, 0.9],
                    kda_threshold_list=[1, 3],
                    music_folder_name='grasswalk'
                    )


    def test_empty_playlist_error(self):
        self.settings.music_folder_name = 'empty_grasswalk'
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        with self.assertRaises(dep_music.EmptyMusicPlaylistError):
            program.initialize_all_pygame_resources()

    def test_incorrect_song_type_error(self):
        self.settings.music_folder_name = 'invalid_grasswalk'
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        with self.assertRaises(dep_music.NonMusicFileType):
            program.initialize_all_pygame_resources()

    def test_no_music_errors_if_music_disabled(self):
        self.settings.music_enabled = False
        self.settings.music_folder_name = 'invalid_grasswalk'
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        program.initialize_all_pygame_resources()
        self.settings.music_folder_name = 'empty_grasswalk'
        program.initialize_all_pygame_resources()

    def test_process_kda_changes_returns_correct_boolean(self):
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        program.initialize_all_pygame_resources()
        communication_obj1 = APICommunication(0, 0, 0, False, 'JohnLeague#NA1')
        communication_obj2 = APICommunication(0, 0, 0, False, 'JohnLeague#NA1')
        communication_obj3 = APICommunication(1, 0, 0, False, 'JohnLeague#NA1')
        communication_obj4 = APICommunication(1, 0, 0, True, 'JohnLeague#NA1')
        self.assertEqual(program.process_kda_changes(communication_obj1), False)
        program._previous_api_response = communication_obj1
        self.assertEqual(program.process_kda_changes(communication_obj2), False)
        program._previous_api_response = communication_obj2
        self.assertEqual(program.process_kda_changes(communication_obj3), True)
        program._previous_api_response = communication_obj3
        self.assertEqual(program.process_kda_changes(communication_obj4), False)

    def test_non_sound_file_error(self):
        self.settings.sfx_folder = 'invalid'
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        with self.assertRaises(custom_exceptions.NonSoundFileType):
            program.initialize_all_pygame_resources()

    def test_empty_sound_folder_error(self):
        self.settings.sfx_folder = 'empty'
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        with self.assertRaises(custom_exceptions.EmptySoundFolder):
            program.initialize_all_pygame_resources()

    def test_no_sound_errors_if_sound_disabled(self):
        self.settings.sfx_enabled = False
        self.settings.sfx_folder = 'empty'
        program = LeagueEventSoundsProgram(None, self.settings, 'testing_files')
        program.initialize_all_pygame_resources()
        self.settings.sfx_folder = 'invalid'
        program.initialize_all_pygame_resources()


if __name__ == '__main__':
    unittest.main()
