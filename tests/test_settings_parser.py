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


    def test_settings_parser_parses_preset_correctly(self):
        argument_dict = {'UPDATE_RATE': 30,
                         'SFX_VOLUME': 0.5,
                         'MUSIC_PRESET': 'grasswalk_preset'}
        parse_music_preset_settings(argument_dict, '.\\testing_files')
        self.assertEqual(argument_dict['VOLUME_LIST'], [1.0, 0.9, 0.8])
        self.assertEqual(argument_dict['MUSIC_FOLDER_NAME'], 'grasswalk')
        self.assertEqual(argument_dict['KDA_THRESHOLDS'], [1, 3])


    def test_construct_settings_object(self):
        argument_dict = {'UPDATE_RATE': 30,
                         'SFX_VOLUME': 0.5,
                         'MUSIC_PRESET': 'grasswalk_preset',
                         'VOLUME_LIST': [1.0, 0.9, 0.8],
                         'MUSIC_FOLDER_NAME': 'grasswalk',
                         'KDA_THRESHOLDS': [1, 3]}
        settings_obj = construct_settings_object(argument_dict)
        self.assertEqual(type(settings_obj), Settings)
        self.assertEqual(argument_dict['UPDATE_RATE'], settings_obj.update_rate)
        self.assertEqual(argument_dict['SFX_VOLUME'], settings_obj.sfx_volume)
        self.assertEqual(argument_dict['MUSIC_PRESET'], settings_obj.music_preset)
        self.assertEqual(argument_dict['VOLUME_LIST'], settings_obj.music_volume_list)
        self.assertEqual(argument_dict['MUSIC_FOLDER_NAME'], settings_obj.music_folder_name)
        self.assertEqual(argument_dict['KDA_THRESHOLDS'], settings_obj.kda_threshold_list)


    def test_full_parsing(self):
        settings_obj = parse_all_settings('.\\testing_files\\settings2.txt', '.\\testing_files')
        argument_dict = {'UPDATE_RATE': 30,
                         'SFX_VOLUME': 0.5,
                         'MUSIC_PRESET': 'grasswalk_preset',
                         'VOLUME_LIST': [1.0, 0.9, 0.8],
                         'MUSIC_FOLDER_NAME': 'grasswalk',
                         'KDA_THRESHOLDS': [1, 3]}
        self.assertEqual(type(settings_obj), Settings)
        self.assertEqual(argument_dict['UPDATE_RATE'], settings_obj.update_rate)
        self.assertEqual(argument_dict['SFX_VOLUME'], settings_obj.sfx_volume)
        self.assertEqual(argument_dict['MUSIC_PRESET'], settings_obj.music_preset)
        self.assertEqual(argument_dict['VOLUME_LIST'], settings_obj.music_volume_list)
        self.assertEqual(argument_dict['MUSIC_FOLDER_NAME'], settings_obj.music_folder_name)
        self.assertEqual(argument_dict['KDA_THRESHOLDS'], settings_obj.kda_threshold_list)


if __name__ == '__main__':
    unittest.main()
