from datetime import datetime, timedelta
import random
import pytz
from chorebot.cache import BoardCache
from chorebot.config import create_client
from chorebot.gamify import update_game
from chorebot.log import get_logger

logger = get_logger(__name__)


def daily_update():
    logger.info('Caching board...')
    chores_board = BoardCache(get_chores_board(create_client()))
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    logger.info('Updating game...')
    update_game(get_todo_lists(chores_board), now)
    logger.info('Updating chores...')
    update_chores(chores_board, now)


def update_chores(chores_board, now):
    daily_chores = []
    bi_weekly_chores = []
    weekly_chores = []
    for card in chores_board.cards:
        card.fetch(False)
        if has_label(card, 'Daily'):
            set_due_today(card, now)
            daily_chores.append(card)
        elif has_label(card, 'Twice weekly') and now.weekday() in [0, 3]:
            set_due_in(card, now, 2)
            bi_weekly_chores.append(card)
        elif has_label(card, 'Weekly') and now.weekday() == 0:
            set_due_in(card, now, 5)
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
        card.change_list(new_list.id)
        list_i += 1


def set_due_today(card, now):
    set_due_in(card, now, 0)


def set_due_in(card, now, days):
    # The dates in the library and API are unclear (probably UTC, but the
    # library isn't setting a time); hack by adding a day, which seems to
    # produce the desired results.
    card.set_due(now + timedelta(days=days + 1))


def has_label(card, label_name):
    """Check if a card has a label with the given name."""
    label_name = label_name.lower()
    for label in card.labels:
        if label.name.lower() == label_name:
            return True
    return False


def get_chores_board(client):
    """Find and return the chores board."""
    boards = client.list_boards()
    for board in boards:
        if 'chores' in board.name.lower():
            return board
    raise Exception('Chores board not found.')


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
