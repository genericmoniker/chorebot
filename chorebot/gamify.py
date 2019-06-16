# -*- coding: utf-8 -*-
from chorebot.trello import TrelloClient


def update_game(todo_lists, now):
    for list_ in todo_lists:
        create_report_card(list_, now)


def create_report_card(list_, now):
    card = _get_report_card(list_)
    overdue = len(get_overdue_cards(list_, now))
    name = "Reputation: {} overdue chore{}".format(
        overdue, "" if overdue == 1 else "s"
    )
    TrelloClient.instance.rename_card(card, name)
    TrelloClient.instance.reposition_card(card, "top")


def _get_report_card(list_):
    for card in list_.cards:
        if card.name.startswith("Reputation:"):
            return card
    return TrelloClient.instance.add_card("Reputation:", list_)


def get_overdue_cards(list_, now):
    overdue = []
    for card in list_.cards:
        if card.due and card.due < now:
            overdue.append(card)
    return overdue
