#!/usr/bin/env python
from chorebot.chores import daily_update
from chorebot.log import setup_logging


def main():
    setup_logging()
    daily_update()
