# launch.py
import modules.api_communicator
import modules.event_main
import modules.settings_parser


def main():
    settings = modules.settings_parser.parse_all_settings('.//settings.txt', 'music_presets')
    api_communicator = modules.api_communicator.APICommunicator(settings.backup_name)
    program = modules.event_main.LeagueEventSoundsProgram(api_communicator, settings)
    program.run()


if __name__ == '__main__':
    main()

