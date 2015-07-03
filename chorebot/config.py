import os
from ConfigParser import ConfigParser, Error
from trello import TrelloClient


def create_client():
    """Create a TrelloClient instance.

    Uses auth properties from config.ini.
    """
    config = _read_config()
    return TrelloClient(
        api_key=config.get('Auth', 'api_key'),
        api_secret=config.get('Auth', 'api_secret'),
        token=config.get('Auth', 'token'),
        token_secret=config.get('Auth', 'token_secret')
    )


def _read_config():
    try:
        config_dir = os.path.dirname(os.path.dirname(__file__))
        config_file = os.path.join(config_dir, 'config.ini')
        parser = ConfigParser()
        parser.read(config_file)
        return parser
    except Error as e:
        raise Exception('Unable to read config.ini. ' + str(e))
