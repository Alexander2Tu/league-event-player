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



if __name__ == '__main__':
    unittest.main()
