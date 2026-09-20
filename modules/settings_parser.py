# settings_parser.py
# Contains main function that parses the main settings file and
# the preset settings file, returning a Settings object.
import ast
from modules.settings import Settings, MissingSettingsException


def parse_all_settings(main_settings_path: str, music_preset_folder_path: str) -> Settings:
    """
    Given a path to the main settings file, returns a Settings
    object of all arguments. Raises MissingSettingsException
    if missing any settings.
    """
    argument_dict = dict()
    parse_main_settings(argument_dict, main_settings_path)
    parse_music_preset_settings(argument_dict, music_preset_folder_path)
    return construct_settings_object(argument_dict)


def parse_main_settings(argument_dict: dict, main_settings_path: str) -> None:
    """
    Parses the main settings.txt file, adding all arguments into
    the passed-in argument_dict. Raises MissingSettingsException
    if missing any settings.
    """
    _parse_argument_file(main_settings_path, argument_dict)

    main_type_dict = {'UPDATE_RATE': int,
                      'SFX_ENABLED': bool,
                      'MUSIC_ENABLED': bool,
                      'SFX_VOLUME': float,
                      'MUSIC_PRESET': str,
                      'BACKUP_NAME': str}
    verify_arguments(argument_dict, main_type_dict, 'Main')


def _parse_argument_file(file_path: str, output_dict: dict) -> None:
    """
    Given a file path, extracts all variables and values into the given
    output dictionary.
    """
    with open(file_path, 'r') as argument_file:
        for line in argument_file:
            if line.strip().startswith('#') or line.count('=') != 1:
                continue
            else:
                # Valid non-comment line with one = sign
                variable, value = line.split('=')
                output_dict[variable.strip()] = _parse_argument_value(variable, value)


def _parse_argument_value(variable_name: str, value: str) -> 'MysteryType':
    """
    Given a variable name and value, returns the value corrected to the
    correct type. If not found, keeps it a string.
    """
    variable_name = variable_name.strip()
    value = value.strip()
    type_dict = {'UPDATE_RATE': int,
                 'SFX_ENABLED': bool,
                 'MUSIC_ENABLED': bool,
                 'SFX_VOLUME': float,
                 'MUSIC_PRESET': str,
                 'BACKUP_NAME': str,
                 'VOLUME_LIST': list,
                 'MUSIC_FOLDER_NAME': str,
                 'KDA_THRESHOLDS': list}

    if variable_name in type_dict and type_dict[variable_name] is not str:
        return ast.literal_eval(value)
    else:
        return value


def verify_arguments(argument_dict: dict, settings_key_dict: dict,
                     settings_type: str = '') -> None:
    """
    Given the argument dictionary for all arguments in settings,
    raises MissingSettingsException if any arguments are missing.
    Raises TypeError if settings type mismatches with the provided
    settings_key_dict.
    """
    for key, expected_type in settings_key_dict.items():
        if key not in argument_dict:
            raise MissingSettingsException(f'{settings_type} settings is missing the argument: |{key}| with '
                                           f'type |{expected_type}|; '
                                           f'please add that argument back and restart the program.')
        elif type(argument_dict[key]) is not expected_type:
            raise TypeError(f'{settings_type} settings has argument: |{key}| with type |{type(argument_dict[key])}|,'
                            f' when expected type was |{expected_type}|; please correct the type.')



def parse_music_preset_settings(argument_dict: dict, music_preset_folder_path: str):
    """
    Parses the music preset settings file, finding the path
    inside the provided argument_dict, and adding the new data into it.
    """
    preset_path = f'{music_preset_folder_path}\\{argument_dict['MUSIC_PRESET']}.txt'
    _parse_argument_file(preset_path, argument_dict)

    preset_type_dict = {'VOLUME_LIST': list,
                        'MUSIC_FOLDER_NAME': str,
                        'KDA_THRESHOLDS': list}
    verify_arguments(argument_dict, preset_type_dict, 'Preset')


def construct_settings_object(argument_dict) -> Settings:
    return Settings(
                    update_rate=argument_dict['UPDATE_RATE'],
                    sfx_enabled=argument_dict['SFX_ENABLED'],
                    music_enabled=argument_dict['MUSIC_ENABLED'],
                    sfx_volume=argument_dict['SFX_VOLUME'],
                    music_preset=argument_dict['MUSIC_PRESET'],
                    backup_name=argument_dict['BACKUP_NAME'],
                    music_volume_list=argument_dict['VOLUME_LIST'],
                    kda_threshold_list=argument_dict['KDA_THRESHOLDS'],
                    music_folder_name=argument_dict['MUSIC_FOLDER_NAME']
                    )

