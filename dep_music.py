# dep_music.py

# This is a shortened version of multi-music-player.py, intended for use
# in another program

import pygame
from pathlib import Path
import time


# Change based on speed of the computer and file size; default is 0
# short .mp3 tends to load faster while long .ogg takes longer
DELAY = 0.01


class MusicPlayer:
    def __init__(self, song_list: list['Songs']):
        # Note: The list of songs should be in order
        
        self._song_list = song_list
        self._duration = 0
        self._running = False

        # These will be defined later in run()
        self._channel_list = None
        self._sound_list = None
        
        self._volume_list = None
        self._mute_list = None




    def run(self, loop_bool):
        self._init_all()
        self._create_all_attributes()

        self._loop_bool = loop_bool
        self.play_all()


    def get_running(self) -> bool:
        '''When called, returns the running state of the music player'''
        return self._running



    def play_all(self) -> None:
        '''When called, plays all songs; will override current songs
        playing in the process'''
        self._play_all_sounds(0)
        self._manage_delay()
        self._running = True



    def stop_all(self) -> None:
        '''When called, stops all songs'''
        for channel in self._channel_list:
            channel.stop()

        self._running = False


    def update_all(self) -> None:
        '''When called, checks and updates all automatic events'''
        self._update_volume()
        self._check_finished()


    def set_duration(self, duration: int) -> None:
        '''Given a duration, sets the _duration attribute to
        that value (module will not keep track of time on its own)'''
        self._duration = duration


    def get_duration(self) -> int:
        '''When called, returns the value of the attribute _duration'''
        return self._duration


    def tick(self) -> None:
        '''When called, decreases the duration attribute by 1 until it reaches
        0; raise an error if duration is already at 0 or below'''

        if self._duration > 0:
            self._duration += -1

        else:
            raise DurationAlreadyZeroError()


    def close_all_files(self) -> None:
        '''When called, closes all files in self._song_list'''
        for song in self._song_list:
            song.close()



    def solo(self, sound_num: int) -> None:
        '''Given a sound number, will unmute song at sound number, and
        mute the rest of the sounds in the list'''
        self.mute_all()
        self._mute_list[sound_num] = False


    def solo_fade(self, sound_num: int) -> None:
        '''Given a sound number, will unmute song at sound number, and
        mute the rest of the sounds in the list'''
        self.mute_all()
        self._mute_list[sound_num] = False



    def mute_all(self) -> None:
        '''When called, mutes all sounds (updates the mute list)'''
        for mute_index in range(0, len(self._mute_list)):
            self._mute_list[mute_index] = True



    def get_mute(self, sound_num: int) -> bool:
        '''Given a sound number, will return the mute status of the
        sound at that sound number'''
        
        try:
            return self._mute_list[sound_num]

        except IndexError:
            print(f'ERROR: INVALID INDEX FOR SOUND OBJECT (get_mute)')



    def mute(self, sound_num: int) -> None:
        '''Given a sound number, will mute the track at that index (0 included)'''
        try:
            self._mute_list[sound_num] = True

        except IndexError:
            print(f'ERROR: CANNOT MUTE THE TRACK AT {sound_num}; THERE ARE {len(self._channel_list)} channels, starting from 0!')



    def unmute(self, sound_num: int) -> None:
        '''Given a sound number, will unmute the track at that index
        (0 included)'''
        
        try:
            self._mute_list[sound_num] = False

        except IndexError:
            print(f'ERROR: CANNOT UNMUTE THE TRACK AT {sound_num}; THERE ARE {len(self._channel_list)} channels, starting from 0!')



    def get_volume(self, sound_num: int) -> None:
        '''Given a sound number, returns the volume float for it'''
        try:
            return self._volume_list[sound_num]

        except IndexError:
            print(f'ERROR: INVALID INDEX FOR SOUND OBJECT (get_volume)')


    def set_volume(self, sound_num: int, volume: float) -> None:
        '''Given a sound number and volume float, sets the volume
        at that sound channel to the volume amount'''
        self._volume_list[sound_num] = volume
        


    def get_channels(self) -> list['Channels']:
        '''When called, returns the list of all channels'''
        return self._channel_list
    

    def _manage_delay(self) -> None:
        '''When called, pauses and unpauses the channels based on
        global constant DELAY'''
        self._pause_all()
        self._unpause_all()


    def _pause_all(self) -> None:
        '''When called, pauses all songs based on the DELAY global constant'''
        delay_time = 0
        for channel in self._channel_list:
            time.sleep(delay_time)
            channel.pause()
            delay_time += DELAY


    def _unpause_all(self) -> None:
        '''When called, unpauses all songs with no delay'''
        for channel in self._channel_list:
            channel.unpause()


    def _check_finished(self) -> None:
        '''When called, checks whether the first song was done;
        if yes, then plays all songs again'''
        if self._channel_list[0].get_busy() == False and self._loop_bool and self._running:
            self.play_all()



    def _update_volume(self) -> None:
        '''When called, updates the volume for each song'''
        for sound_index in range(0, len(self._sound_list)):
            current_sound = self._sound_list[sound_index]
            current_volume = self._volume_list[sound_index]
            current_mute = self._mute_list[sound_index]

            if current_mute == False:
                current_sound.set_volume(current_volume)

            else:
                current_sound.set_volume(0.0)
            


    def _init_all(self) -> None:
        '''Initializes all pygame modules that this program needs'''
        pygame.init()
        pygame.mixer.init()
        self._clock = pygame.time.Clock()


    def _create_all_attributes(self) -> None:
        '''When called, creates all attributes'''
        self._create_channels()
        self._create_sounds()
        self._create_volume_list()
        self._create_mute_list()


    def _create_channels(self) -> None:
        '''When called, creates channels and assigns them to self._channel_list'''
        self._channel_list = self._make_channels(len(self._song_list), 3)

    
    def _create_sounds(self) -> None:
        '''When called, creates sound objects and assigns them to
        self._sound_list'''
        sound_list = []
        for song in self._song_list:
            sound_list.append(pygame.mixer.Sound(song))

        self._sound_list = sound_list


    def _create_volume_list(self) -> None:
        '''When called, creates an attribute to keep track of volumes
        in the form of self._volume_list'''
        self._volume_list = []

        for song in self._song_list:
            self._volume_list.append(1.0)


    def _create_mute_list(self) -> None:
        '''When called, creates an attribute to keep track of mute booleans
        in the form of self._mute_list'''
        self._mute_list = []

        for song in self._song_list:
            self._mute_list.append(False)



    def _play_all_sounds(self, loop_amount: int) -> None:
        '''Plays all sounds in the object sound_list once'''
        for sound_index in range(0, len(self._sound_list)):
            current_channel = self._channel_list[sound_index]
            current_sound = self._sound_list[sound_index]
            
            current_channel.play(current_sound, loop_amount)




    def _change_volume(self, sound_num: int) -> None:
        '''Given a sound number, will decrease the sound volume at the given
        sound number by the pre-defined sound interval'''

        try:
            current_volume = self._volume_list[sound_num - 1]
            proposed_volume = round(current_volume - self._volume_interval, 1)
            current_name = self._get_name(self._song_list[sound_num-1].name)

            if proposed_volume >= 0.0:
                print(f'Volume of {current_name} ({current_volume}) has been changed to {proposed_volume}!')
                self._volume_list[sound_num - 1] = proposed_volume

            else:
                print(f'Volume of {current_name} has been reset to 1.0!')
                self._volume_list[sound_num - 1] = 1.0

        except IndexError:
            print('Error: No music assigned to that key.')



    def _make_channels(self, channel_amount: int, extras: int) -> list['Channels']:
        '''Given an integer, returns a list of channels whose quantity is 
        equal to the number, while setting the channel amount including extras'''
        channel_list = []

        # Sets the max channel amount before making channels
        pygame.mixer.set_num_channels(channel_amount + extras)

        # Creating the channels
        for loop in range(0, channel_amount):
            channel_list.append(pygame.mixer.Channel(loop))

        return channel_list


    def _get_name(self, path_str: str) -> str:
        '''Given a string path, returns only the filename'''
        if '\\' in path_str:
            return path_str.split('\\')[-1]



def run() -> None:
    '''Gets file inputs, creates a MusicPlayer object and runs it'''
    song_list = get_file_input()
    loop_bool = get_loop()

    if len(song_list) != 0:
        MusicPlayer(song_list).run(loop_bool)



def get_file_input() -> list['Songs']:
    '''With no arguments, reads user input and returns a list of
    song files'''
    song_list = []
    while True:
        song_path = input('What is the song path (or Q to quit)? ')

        if song_path.upper() == 'Q':
            return song_list

        try:
            song_path = Path(song_path)

            if song_path.is_file():
                song = song_path.open('r')
                song_list.append(song)
                print(f'Added: {song_path}')

            elif song_path.is_dir():
                for file in song_path.iterdir():
                    if file.is_file():
                        song = file.open('r')
                        song_list.append(song)
                        print(f'Added: {file}')

                    else:
                        print(f'{file} is not a file, skipping...')


            elif song_path.exists() == False:
                print('Invalid path. Song not added.')

            else:
                print('Unknown error has occured; provided path is not a file or directory, yet still exists.')
                

        finally:
            print()



def get_loop() -> bool:
    '''Gets user input for whether or not the songs will loop indefinitely'''
    
    yes_list = ['YES', 'SURE', 'AFFIRMATIVE', 'TRUE', 'YEAH', 'PLEASE', 'HAI',
                'YEP', 'PERCHANCE']
    no_list = ['NO', 'NOPE', 'NAH', 'FALSE', 'NEGATIVE', 'IYA']

    while True:
        loop_input = input('Do you want loop? ')
        if loop_input.upper() in yes_list:
            return True
        elif loop_input.upper() in no_list:
            return False
        else:
            print('Input not recognized, please try again.')



def _list_in_str(str_list: list[str], term: str) -> bool:
        '''Given a list of strings, return True if one of the strings is
        in the term string, case-insensitive'''

        for search in str_list:
            if search.upper() in term.upper():
                return True

        return False

#
# Custom Errors
#

class DurationAlreadyZeroError(Exception):
    pass


if __name__ == '__main__':
    sample_song_list = [Path('..//Multi Music Player//music//moonlight//1moonlight_vocals.mp3')]
