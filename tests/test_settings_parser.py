import unittest
from modules.settings import *
from modules.settings_parser import *
import os



class TestSettingsParser(unittest.TestCase):
    def test_settings_obj_holds_attributes(self):
        update_rate = 30
        volume = 0.5
        music_preset = 'grasswalk'
        volume_list = [0.99, 0.99, 0.99]
        kda_threshold_list = [1, 3]
        music_folder_name = 'grasswalk'

        obj = Settings(update_rate, volume, music_preset, volume_list, kda_threshold_list, music_folder_name)

        self.assertEqual(obj.update_rate, update_rate)
        self.assertEqual(obj.sfx_volume, volume)
        self.assertEqual(obj.music_preset, music_preset)
        self.assertEqual(obj.music_volume_list, volume_list)
        self.assertEqual(obj.kda_threshold_list, kda_threshold_list)
        self.assertEqual(obj.music_folder_name, music_folder_name)


    def test_settings_parser_parses_main_correctly(self):
        argument_dict = dict()
        test_path = '.\\testing_files\\settings1.txt'
        parse_main_settings(argument_dict, test_path)

        self.assertEqual(argument_dict['UPDATE_RATE'], 30)
        self.assertEqual(argument_dict['SFX_VOLUME'], 0.5)
        self.assertEqual(argument_dict['MUSIC_PRESET'], 'grasswalk')

    def test_verify_arguments_raises_correct_errors(self):
        expected_types = {'String': str,
                          'Integer': int}
        with self.assertRaises(TypeError):
            verify_arguments({'Integer': 'one',
                              'String': 1134}, expected_types)

        with self.assertRaises(MissingSettingsException):
            verify_arguments({'Float', 0.5}, expected_types)





if __name__ == '__main__':
    unittest.main()
