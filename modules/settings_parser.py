# settings_parser.py
# Contains main function that parses the main settings file and
# the preset settings file, returning a Settings object.
from modules.settings import Settings, MissingSettingsException


def parse_all_settings(main_settings_path: str) -> Settings:
    """
    Given a path to the main settings file, returns a Settings
    object of all arguments. Raises MissingSettingsException
    if missing any settings.
    """
    argument_dict = dict()
    parse_main_settings(argument_dict, main_settings_path)
    parse_music_preset_settings(argument_dict)
    return construct_settings_object(argument_dict)


def parse_main_settings(argument_dict: dict, main_settings_path: str) -> None:
    """
    Parses the main settings.txt file, adding all arguments into
    the passed-in argument_dict. Raises MissingSettingsException
    if missing any settings.
    """
    with open(main_settings_path, 'r') as main_settings_file:
        for line in main_settings_file:
            if line.strip().startswith('#') or line.count('=') != 1:
                continue
            else:
                # Valid non-comment line with one = sign
                variable, value = line.split('=')
                argument_dict[variable.strip()] = _parse_argument_value(variable, value)

    main_type_dict = {'UPDATE_RATE': int,
                      'SFX_VOLUME': float,
                      'MUSIC_PRESET': str}
    verify_arguments(argument_dict, main_type_dict, 'Main')


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



def parse_music_preset_settings(argument_dict: dict, music_preset_folder: str = 'music_presets'):
    """
    Parses the music preset settings file, finding the path
    inside the provided argument_dict, and adding the new data into it.
    """
    pass


def _parse_argument_value(variable_name: str, value: str) -> 'MysteryType':
    """
    Given a variable name and value, returns the value corrected to the
    correct type. If not found, keeps it a string.
    """
    variable_name = variable_name.strip()
    value = value.strip()
    type_dict = {'UPDATE_RATE': int,
                 'SFX_VOLUME': float,
                 'MUSIC_PRESET': str,
                 'VOLUME_LIST': list,
                 'MUSIC_FOLDER_NAME': str,
                 'KDA_THRESHOLDS': list}

    if variable_name in type_dict:
        return type_dict[variable_name](value)
    else:
        return value


def construct_settings_object(argument_dict) -> Settings:
    pass

