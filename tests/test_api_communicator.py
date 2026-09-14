import unittest
from modules.api_communication import *
from modules.api_communicator import *


class TestAPICommunicator(unittest.TestCase):
    def setUp(self):
        self.communicator = APICommunicator('JohnLeague#NA1')

    def test_communication_obj_holds_attributes(self):
        kills, deaths, assists = 1, 2, 3
        is_dead = False
        name = 'JohnLeague#NA1'
        obj = APICommunication(kills, deaths, assists, is_dead, name)

        self.assertEqual(obj.kills, kills)
        self.assertEqual(obj.deaths, deaths)
        self.assertEqual(obj.assists, assists)
        self.assertEqual(obj.is_dead, is_dead)
        self.assertEqual(obj.name, name)


    def test_communication_obj_defaults_name(self):
        kills, deaths, assists = 1, 2, 3
        is_dead = False
        obj = APICommunication(kills, deaths, assists, is_dead)

        self.assertEqual(obj.name, None)


    def test_communicator_requires_backup_name(self):
        with self.assertRaises(TypeError):
            communicator = APICommunicator()


    def test_communicator_finds_player(self):
        name = 'JohnLeague#NA1'
        game_data = {'allPlayers': [
            {'riotId': 'JaneLeague#NA2'},
            {'riotId': 'JohnLeague#NA1'}
        ]}
        invalid_game_data = {}
        invalid_game_data2 = {'allPlayers': [
            {'riotId': 'JaneLeague#NA2'}
        ]}
        self.assertEqual(self.communicator._find_player(name, game_data), game_data['allPlayers'][1])
        with self.assertRaises(KeyError):
            self.communicator._find_player(name, invalid_game_data)
        with self.assertRaises(CannotFindPlayerException):
            self.communicator._find_player(name, invalid_game_data2)


    def test_communicator_returns_valid_response_on_situation(self):
        communicator = APICommunicator('JohnLeague#NA1')
        communication_data = communicator.request_api()
        self.assertTrue(communication_data is None or type(communication_data) is APICommunication)


    def test_communicator_returns_valid_information_on_active_game(self):
        # Only uncomment and run if game is active & no activity in kda yet
        pass
        # communicator = APICommunicator('JohnLeague#NA1')
        # communication_data = communicator.request_api()
        # self.assertEqual(communication_data.kills, 0)
        # self.assertEqual(communication_data.deaths, 0)
        # self.assertEqual(communication_data.assists, 0)
        # self.assertEqual(communication_data.is_dead, False)


if __name__ == '__main__':
    unittest.main()
