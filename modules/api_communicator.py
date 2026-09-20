# api_communicator.py
# Contains APICommunicator class, which handles
# communicating with the League API and creating
# APICommunication objects on success; None on failure.
import json
from modules.api_communication import APICommunication
import ssl
import urllib.request


class APICommunicator:
    LEAGUE_API_URL = 'https://127.0.0.1:2999/liveclientdata/allgamedata'

    def __init__(self, backup_name: str):
        self._backup_name = backup_name

    def request_api(self, custom_response: str = None) -> APICommunication:
        """
        When ran, consults the League API and constructs
        APICommunication object; returns None if invalid format.
        """
        if custom_response is None:
            text_data = self._api_send_receive(APICommunicator.LEAGUE_API_URL, [])
        else:
            text_data = custom_response

        try:
            game_data = json.loads(text_data)
            player_name = self._find_name(game_data)
            if player_name is None:
                player_name = self._backup_name

            player_data = self._find_player(player_name, game_data)
            return self._construct_communication_object(player_data)
        except TypeError:
            # If API response was an error
            return None
        except KeyError:
            # If API response is malformed
            return None
        except CannotFindPlayerException:
            return None


    def _api_send_receive(self, url: str, header_list: list[tuple[str]]) -> str:
        """Given a url and header list, returns the text data at the url"""
        try:
            ctx = ssl.create_default_context()

            # CERTIFICATION IS DISABLED; CHECK LATER
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            request = urllib.request.Request(url)
            for header in header_list:
                request.add_header(header)

            response = urllib.request.urlopen(request, context=ctx)
            text_response = response.read().decode(encoding='utf-8')

            return text_response

        except urllib.error.URLError:
            return None
        except Exception as unknown_error:
            print(type(unknown_error))
            return None

    def _find_name(self, data_dict: dict) -> str:
        try:
            return data_dict['activePlayer']['riotId']
        except KeyError:
            return None

    def _find_player(self, player_name: str, game_data: dict) -> dict:
        for player_data in game_data['allPlayers']:
            if player_data['riotId'] == player_name:
                return player_data

        raise CannotFindPlayerException

    def _construct_communication_object(self, player_data: dict) -> APICommunication:
        scores = player_data['scores']
        return APICommunication(kills=scores['kills'],
                                deaths=scores['deaths'],
                                assists=scores['assists'],
                                is_dead=player_data['isDead'],
                                name=player_data['riotId'])


class CannotFindPlayerException(Exception):
    pass