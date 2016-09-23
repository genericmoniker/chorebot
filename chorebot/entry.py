#!/usr/bin/env python
from datetime import datetime

import pytz

from chorebot.chores import logger, chore_board_matcher, get_todo_lists, \
    update_chores
from chorebot.config import create_client
from chorebot.gamify import update_game
from chorebot.log import setup_logging


def main():
    setup_logging()
    daily_update()


def daily_update():
    client = create_client()
    logger.info('Loading board...')
    chores_board = client.load_board(chore_board_matcher)
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    logger.info('Updating game...')
    update_game(get_todo_lists(chores_board), now)
    logger.info('Updating chores...')
    update_chores(chores_board, now)
