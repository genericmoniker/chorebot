import os
from configparser import ConfigParser, Error, NoSectionError, NoOptionError
from chorebot.trello import TrelloClient


def create_client():
    """Create a TrelloClient instance.

    Uses auth properties from config.ini.
    """
    config = _read_config()
    return TrelloClient(
        config.get("Auth", "api_key"), token=config.get("Auth", "token")
    )


def get_chore_board_name():
    config = _read_config()
    try:
        board_name = config.get("App", "chore_board")
    except (NoSectionError, NoOptionError):
        board_name = "chores"
    return board_name or "chores"


def _read_config():
    global _config
    if not _config:
        try:
            # Try Docker container location
            config_file = "/config/config.ini"
            if not os.path.exists(config_file):
                # Otherwise use local config
                config_dir = os.path.dirname(os.path.dirname(__file__))
                config_file = os.path.join(config_dir, "config.ini")
            _config = ConfigParser()
            _config.read(config_file)
            return _config
        except Error as e:
            raise Exception("Unable to read config.ini. " + str(e))
    return _config


_config = None
