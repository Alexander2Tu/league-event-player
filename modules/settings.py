# settings.py
# Contains Settings class, meant to hold all user settings to be processed
# by program.


class Settings:
    def __init__(self, update_rate: int,
                 sfx_volume: float, music_preset: str,
                 music_volume_list: list[float],
                 kda_threshold_list: list[int], music_folder_name: str):
        # Global Settings
        self.update_rate = update_rate
        self.sfx_volume = sfx_volume
        self.music_preset = music_preset

        # Preset Settings
        self.music_volume_list = music_volume_list
        self.kda_threshold_list = kda_threshold_list
        self.music_folder_name = music_folder_name


class MissingSettingsException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message
