import random
from datetime import datetime, timedelta

import pytz
from tzlocal import get_localzone

from chorebot.config import get_chore_board_name
from chorebot.log import get_logger
from chorebot.trello import TrelloClient

logger = get_logger(__name__)


def update_chores(chores_board, now):
    daily_chores = []
    bi_weekly_chores = []
    weekly_chores = []
    for card in chores_board.cards:
        if has_label(card, 'Daily'):
            set_due_today(card, now)
            daily_chores.append(card)
        elif has_label(card, 'Twice weekly') and now.weekday() in (0, 3):
            set_due_in(card, now, 2)
            bi_weekly_chores.append(card)
        elif has_label(card, 'Weekly') and now.weekday() == 0:
            set_due_in(card, now, 6)
            weekly_chores.append(card)
    assign(chores_board, daily_chores)
    assign(chores_board, bi_weekly_chores)
    assign(chores_board, weekly_chores)


def assign(chores_board, cards):
    """Assign cards by members or by random shuffle."""
    member_cards = [c for c in cards if c.member_ids]
    for card in member_cards:
        member_lists = get_todo_lists_by_card_members(chores_board, card)
        deal([card], member_lists)

    other_cards = [c for c in cards if c not in set(member_cards)]
    to_do_lists = get_todo_lists(chores_board)
    deal(other_cards, to_do_lists)


def deal(cards, lists):
    """Shuffle and deal cards to lists."""
    list_i = 0
    random.shuffle(cards)
    random.shuffle(lists)
    while cards:
        card = cards.pop()
        new_list = lists[list_i % len(lists)]
        logger.info('{} => {}'.format(card.name, new_list.name))
        TrelloClient.instance.move_card(card, new_list)
        list_i += 1


def set_due_today(card, now):
    set_due_in(card, now, 0)


def set_due_in(card, now, days):
    tz = get_localzone()
    due_hour = 23  # 11 PM
    due = tz.localize(
        datetime(
            now.year,
            now.month,
            now.day,
            due_hour
        ) + timedelta(days=days)
    )
    due_utc = due.astimezone(pytz.utc)
    TrelloClient.instance.reschedule_card(card, due_utc)


def has_label(card, label_name):
    """Check if a card has a label with the given name."""
    label_name = label_name.lower()
    for label in card.labels:
        if label.name.lower() == label_name:
            return True
    return False


def get_todo_lists(board):
    """Get all the 'to do' lists from a board.

    :return: list of to-do lists.
    """
    todo_lists = []
    for list_ in board.lists:
        if _is_todo_list(list_):
            todo_lists.append(list_)
    return todo_lists


def get_todo_lists_by_card_members(board, card):
    """Find the 'to do' lists for a chore card according to its members.

    :return: list of to-do lists.
    """
    todo_lists = []
    for member_id in card.member_ids:
        member = board.get_member(member_id)
        first_name = member.full_name.split(' ')[0].lower()
        for list_ in board.lists:
            if first_name in list_.name.lower():
                todo_lists.append(list_)
    return todo_lists


def _is_todo_list(list_):
    name = list_.name.lower()
    return 'todo' in name or 'to do' in name


def chore_board_matcher(name):
    chore_board_name = get_chore_board_name()
    return chore_board_name.lower() in name.lower()
