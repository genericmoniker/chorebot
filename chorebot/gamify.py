# -*- coding: utf-8 -*-


def update_game(todo_lists, now):
    for list_ in todo_lists:
        create_report_card(list_, now)


def create_report_card(list_, now):
    card = _get_report_card(list_)
    overdue = len(get_overdue_cards(list_, now))
    name = 'Reputation: {} overdue chore{}'.format(
        overdue,
        '' if overdue == 1 else 's'
    )
    card.set_name(name)
    card.set_pos('top')


def _get_report_card(list_):
    cards = list_.list_cards()
    for card in cards:
        if card.name.startswith('Reputation:'):
            return card
    return list_.add_card('Reputation:')


def get_overdue_cards(list_, now):
    overdue = []
    for card in list_.list_cards():
        card.fetch()
        if card.due_date and card.due_date < now:
            overdue.append(card)
    return overdue
