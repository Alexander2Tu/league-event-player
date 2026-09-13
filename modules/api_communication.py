# api_communication.py
# Contains APICommunication class, used to contain info
# sent by API.

class APICommunication:
    def __init__(self, kills: int, deaths: int, assists: int,
                 is_dead: bool, name: bool = None):
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.is_dead = is_dead
        self.name = name
