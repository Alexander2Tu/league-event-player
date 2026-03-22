# league_eventsounds.py

# Same-directory modules
import dep_music

# Standard library modules
import json
from pathlib import Path
import random
import ssl
import time
import traceback
import urllib.request

# Custom-installed modules
import pygame

# This name will be used for spectator, when the API cannot return the currentPlayer details
BACKUP_NAME = 'YourUsernameHere#Tag'


class LeagueEvent:
    def __init__(self):

        # Available checks: 'kills', 'deaths', 'assists', 'creepScore', 'wardScore'
        # Note: creepScore only updates every 10 CS! wardScore updates seemingly randomly...
        self._score_check_list = ['kills', 'deaths', 'assists', 'creepScore']
        
        self._data_dict = None
        self._old_dict = None
        
        self._user_dict = None
        self._old_user_dict = None
        
        self._stats_dict = dict()
        self._old_stats_dict = dict()

        self._current_name = None
        
        self._current_kda = 0
        self._current_phase = 0
        
        self._running = True
        self._connected = True
        
        self._counter = 0
        self._seconds = 0
        self._error_count = 0

        self._setup_all_settings()
        # Creates the following:
        # self._update_rate
        # self._volume
        # self._volume_list
        # self._music_folder_name
        # self._kda_thresholds

        print('Initialized all settings!')


    def run(self) -> None:
        '''Runs the LeagueEvent Client'''
        self._initialize_prerun_resources()

        print('Running application!')
        try:
            self._loop()
        finally:
            print(self._data_dict)


    def _initialize_prerun_resources(self):
        self._setup_player()
        print('Set up music player!')

        pygame.init()
        self._clock = pygame.time.Clock()
        pygame.mixer.init()
        print('Set up pygame!')

        self._test_run_player()


    def _loop(self) -> None:
        '''Runs the loop for the LeagueEvent Client'''
        while self._running:
            self._clock.tick(self._update_rate)
            
            self._handle_events()
            self._tick()
            self._tick_events(0)
            
            self._update_stats()
            self._check_stats()

            self._music_player.update_all()


    def _handle_events(self) -> None:
        '''When run, checks for any events and handles them appropriately'''
        'There are no events or inputs yet...'


    def _tick(self) -> None:
        '''When run, increases self._counter by one, reseting to 0 once self._update_rate is reached'''
        self._counter += 1

        if self._counter > self._update_rate:
            self._counter = 0

            if self._music_player.get_duration() != 0:
                self._music_player.tick()


    def _tick_events(self, interval: int) -> None:
        '''When run, checks the League API every integer time interval specified'''
        if interval < 1:
            self._check_api()
            
        else:
            if self._counter >= self._update_rate:
                self._seconds += 1

            if self._seconds >= interval:
                self._check_api()
                self._seconds = 0




    def _update_stats(self) -> None:
        '''When run, updates the self._stats_dict and self._old_stats_dict
        in accordance with current data'''
        if self._data_dict != None:
            info_dict = self._data_dict
            if 'summonerName' in info_dict['activePlayer']:
                self._current_name = info_dict['activePlayer']['summonerName']

            else:
                self._current_name = BACKUP_NAME
                
            self._user_dict = self._find_user(self._data_dict)

            if self._old_dict != None:
                self._old_user_dict = self._find_user(self._old_dict)


            # Updates all stats in user scores
            for keyword in self._user_dict['scores']:

                if self._old_user_dict != None:
                    self._old_stats_dict[keyword] = self._old_user_dict['scores'][keyword]

                self._stats_dict[keyword] = self._user_dict['scores'][keyword]


            # Updates all other stats that aren't in scores or dictionaries
            for keyword in self._user_dict:
                keyword_type = type(keyword)
                forbidden_types = [list, dict]

                if keyword_type not in forbidden_types:
                    if self._old_user_dict != None:
                        self._old_stats_dict[keyword] = self._old_user_dict[keyword]

                    self._stats_dict[keyword] = self._user_dict[keyword]


        self._update_kda()



    def _update_kda(self) -> None:
        '''When run, uses the info stored in self._stats_dict to calculate
        Kill-Death-Assist ratio'''
        if len(self._stats_dict) != 0:
            kills = self._stats_dict['kills']
            deaths = self._stats_dict['deaths']
            assists = self._stats_dict['assists']

            if deaths == 0:
                deaths = 0.5

            self._current_kda = (kills + assists) / deaths

            #print(f'Current KDA: {self._current_kda}')

            self._update_phase()
                

    def _update_phase(self) -> None:
        '''When run, checks the current kda to update the phase value
        (temporary phases are not included)'''
        self._current_phase = 0

        phase_value = 1
        for threshold_value in self._kda_thresholds:
            if self._current_kda >= threshold_value:
                self._current_phase = phase_value

            phase_value += 1

        #print(f'Current Phase: {self._current_phase}')
        


    def _check_stats(self) -> None:
        '''When run, checks the stats to see if they match up with old stats; performs an event if not'''
        if self._user_dict != None:
            for keyword in self._user_dict['scores']:
            
                if keyword in self._old_stats_dict:
                
                    if self._stats_dict[keyword] > self._old_stats_dict[keyword]:

                        if keyword == 'kills' or keyword == 'assists':
                            self._music_player.set_duration(10)

                        if keyword in self._score_check_list:
                            print(f'|{keyword}| values changed from {self._old_stats_dict[keyword]} to {self._stats_dict[keyword]};\nPLAYING random {keyword} SOUND')
                            self._play_event(keyword)

        if len(self._stats_dict) != 0:
            self._play_phase()


    def _play_phase(self) -> None:
        '''When called, unmutes music appropriate to the current phase
        and player status (recent kills or death timer)'''
        solo_phase = self._current_phase

        if self._music_player.get_duration() != 0:
            solo_phase += 1

        if self._stats_dict['isDead'] == True:
            solo_phase = 0

        # Boundaries; if less than phase 0, turn 0, more than max,
        #  turn max phase
        if solo_phase < 0:
            solo_phase = 0

        if solo_phase > len(self._music_player.get_channels()) - 1:
            solo_phase = len(self._music_player.get_channels()) - 1

        self._music_player.solo(solo_phase)




    def _play_event(self, event: str) -> None:
        '''Given an event keyword, plays the sound associated with it'''
        event_sounds = []
        path_string = 'sounds//'
        path_string += event

        for file_path in Path(path_string).iterdir():
                event_sounds.append(file_path)
                
        chosen_sound = random.choice(event_sounds)
        self._play_sound(chosen_sound)


    def _play_sound(self, path: Path) -> None:
        '''When given a Path, plays the sound at that path'''
        sound_file = pygame.mixer.Sound(path.open('r'))
        sound_file.set_volume(self._volume)
        sound_file.play(0)
        

    def _find_user(self, data_dict: dict) -> 'Player Dict' or None:
        '''When run, finds the player in the self._data_dict and returns that subdictionary'''
        for champ_dict in data_dict['allPlayers']:
            if champ_dict['summonerName'] == self._current_name:
                return champ_dict

        print('FAILED TO FIND PLAYER')
        


    def _check_api(self):
        '''When ran, consults the League API and assigns the data dictionary to self._data_dict'''
        text_data = self._api_send_receive('https://127.0.0.1:2999/liveclientdata/allgamedata', [])

        if text_data != None:
            if self._connected == False:
                print('Connection reestablished!')
                self._connected = True
                self._error_count = 0

            
            self._run_player()
                
            dict_data = text_to_json(text_data)

            if self._data_dict != None:
                self._old_dict = self._data_dict
            
            self._data_dict = dict_data

            #print(f'DEBUG: {self._data_dict}')
        




    def _api_send_receive(self, url: str, header_list: list[tuple[str]]) -> str:
        '''Given a url and header list, returns the text data at the url'''
        try:
            ctx = ssl.create_default_context()

            # CERTIFICATION IS DISABLED; CHECK LATER
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            request = urllib.request.Request(url)
            for header in header_list:
                request.add_header(header)
            
            response = urllib.request.urlopen(request, context = ctx)

            text_response = response.read().decode(encoding = 'utf-8')

            return text_response


        # urllib.error.URLError
        except:
            self._error_count += 1
            print(f'\rError Connecting ({self._error_count}); trying again in 5 seconds...', end='')

            if self._music_player != None:
                self._stop_player()

            self._connected = False
            time.sleep(5)



    def _setup_player(self) -> None:
        '''When called, sets up the music player for the client, pulling
        all files from ./music/kda and loading them'''
        # directory is 'music/kda'
        music_list = []
        for path in Path('music//kda//' + self._music_folder_name).iterdir():
            if path.is_file():
                music_list.append(path)

        self._music_player = dep_music.MusicPlayer(music_list)



    def _test_run_player(self) -> None:
        '''When called, tests to see if player can run successfully;
        may raise a NonMusicFileType exception'''
        self._run_player()
        self._stop_player()


    def _run_player(self) -> None:
        '''When called, runs the music player'''
        if self._music_player.get_running() == False:
            self._music_player.run(True)
            self._adjust_volume(self._volume_list)
            self._music_player.solo(0)


    def _stop_player(self) -> None:
        '''When called, stops the music player'''
        self._music_player.stop_all()


    def _adjust_volume(self, volume_list: list[float]) -> None:
        '''Given a list for volumes, changes the volume'''
        index = 0
        for volume in volume_list:
            try:
                self._music_player.set_volume(index, volume)
                
            except IndexError:
                print(f'Invalid index {index} for volume of music')
            
            index += 1


    def _setup_all_settings(self) -> None:
        '''When called, sets up all user settings from the file settings.txt'''
        settings_list = None

        try:
            settings_list = path_to_list('settings.txt')

        except FileNotFoundError:
            print('\nERROR: settings.txt file was NOT FOUND')
            print('Please create a settings.txt file in the same directory as the executable file and add arguments:')
            print('UPDATE_RATE, VOLUME, VOLUME_LIST, and MUSIC_FOLDER_NAME')
            print('and their values (int, int, list[int], str) respectively')
            self._running = False

        if settings_list != None:
            settings_list = filter_list(settings_list)

            try:
                self._process_settings(settings_list)

            except IndexError:
                print('settings.txt exists, but is malformed in format.')
                print('Please follow the example_settings.txt for correct formatting of settings.')
                self._running = False


    def _process_settings(self, settings_list: list[str]) -> None:
        '''Given a list of setting strings, define the correct attributes
        with the correct values'''
        for setting_str in settings_list:
            if setting_str.startswith('UPDATE_RATE'):
                number_str = setting_str.split('=')[-1].strip()
                self._update_rate = int(number_str)
                #print(f'Update Rate is now: {self._update_rate}')


            elif setting_str.startswith('VOLUME_LIST'):
                list_str = setting_str.split('=')[-1].strip()
                self._volume_list = str_to_list(list_str, float)
                #print(f'Volume List is now: {self._volume_list}')


            elif setting_str.startswith('VOLUME'):
                number_str = setting_str.split('=')[-1].strip()
                self._volume = float(number_str)
                #print(f'Volume is now: {self._volume}')


            elif setting_str.startswith('MUSIC_FOLDER_NAME'):
                string = setting_str.split('=')[-1].strip()

                if "'" in string:
                    string = string.strip("'")
                
                self._music_folder_name = string
                #print(f'Folder Name is now: {self._music_folder_name}')


            elif setting_str.startswith('KDA_THRESHOLDS'):
                list_str = setting_str.split('=')[-1].strip()
                self._kda_thresholds = str_to_list(list_str, float)
                self._kda_thresholds.sort()
                #print(f'KDA thresholds are now: {self._kda_thresholds}')


def str_to_list(list_str: str, correct_type: type) -> list:
    '''Given a string in list format, returns it in list form'''
    # [0.7, 0.5, 0.3]

    real_list = []

    if list_str.startswith('[') and list_str.endswith(']'):
        list_str = list_str[1:-1]

        string_list = list_str.split(',')
        for item in string_list:
            item = correct_type(item.strip())
            real_list.append(item)

        return real_list

    else:
        print('INVALID FORMAT FOR STR TO LIST CONVERSION:')
        print(f'{list_str} IS NOT VALID')




def path_to_list(path_str: str) -> list[str]:
    '''Given a string, returns the list of strings at that path file'''
    file = None

    try:
        file = Path(path_str).open('r')
        text = file.readlines()

        return text

    finally:
        if file != None:
            file.close()


def filter_list(raw_list: list[str]) -> list[str]:
    '''Given a raw list of strings, which include \n and blank lines,
    give back a filtered list without those elements'''
    final_list = []
    for line in raw_list:
        line = line.strip()
        
        if line.startswith('#') or line == '':
            pass
        
        else:
            final_list.append(line)

    return final_list



def text_to_json(text: str) -> 'list or dict':
    '''Given text data, converts and returns it in dictionary or list format'''
    return json.loads(text)    



def run():
    try:
        LeagueEvent().run()
    except Exception as error:
        print(f'The program has crashed unexpectedly; the program will now print the exception and its traceback.')
        print(error)
        traceback.print_exc()
        input()
        input()



if __name__ == '__main__':
    run()

