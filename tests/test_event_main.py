import unittest

from modules.event_main import *
from modules.settings import Settings


class TestEventMain(unittest.TestCase):
    def test_empty_playlist_error(self):
        settings = Settings(
                    update_rate=30,
                    sfx_enabled=True,
                    music_enabled=True,
                    sfx_volume=0.5,
                    music_preset='grasswalk',
                    backup_name='JohnLeague#NA1',
                    music_volume_list=[0.9, 0.9, 0.9],
                    kda_threshold_list=[1, 3],
                    music_folder_name='empty_grasswalk'
                    )
        program = LeagueEventSoundsProgram(None, settings, 'testing_files')
        with self.assertRaises(dep_music.EmptyMusicPlaylistError):
            program.initialize_all_pygame_resources()

    def test_incorrect_song_type_error(self):
        settings = Settings(
            update_rate=30,
            sfx_enabled=True,
            music_enabled=True,
            sfx_volume=0.5,
            music_preset='grasswalk',
            backup_name='JohnLeague#NA1',
            music_volume_list=[0.9, 0.9, 0.9],
            kda_threshold_list=[1, 3],
            music_folder_name='invalid_grasswalk'
        )
        program = LeagueEventSoundsProgram(None, settings, 'testing_files')
        with self.assertRaises(dep_music.NonMusicFileType):
            program.initialize_all_pygame_resources()

    def test_no_music_errors_if_music_disabled(self):
        settings = Settings(
            update_rate=30,
            sfx_enabled=True,
            music_enabled=False,
            sfx_volume=0.5,
            music_preset='grasswalk',
            backup_name='JohnLeague#NA1',
            music_volume_list=[0.9, 0.9, 0.9],
            kda_threshold_list=[1, 3],
            music_folder_name='invalid_grasswalk'
        )
        program = LeagueEventSoundsProgram(None, settings, 'testing_files')
        program.initialize_all_pygame_resources()
        settings.music_folder_name = 'empty_grasswalk'
        program.initialize_all_pygame_resources()



if __name__ == '__main__':
    unittest.main()
