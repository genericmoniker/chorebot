from datetime import datetime, timedelta
import random
from chorebot.config import create_client
from chorebot.log import get_logger

logger = get_logger(__name__)


def daily_update():
    client = create_client()
    chores_board = get_chores_board(client)
    to_do_lists = get_to_do_lists(chores_board)
    daily_chores = []
    cards = chores_board.get_cards()
    for card in cards:
        card.fetch(False)
        if has_label(card, 'Personal Daily'):
            update_personal_daily_chore(card)
        elif has_label(card, 'Daily'):
            set_due_today(card)
            daily_chores.append(card)
    deal(daily_chores, to_do_lists)


def update_personal_daily_chore(card):
    set_due_today(card)
    todo_list = find_todo_list_by_member(card)
    if todo_list and card.list_id != todo_list.id:
        card.change_list(todo_list.id)


def deal(cards, lists):
    """Shuffle and deal cards to lists."""
    list_i = 0
    random.shuffle(cards)
    while cards:
        cards.pop().change_list(lists[list_i % len(lists)].id)
        list_i += 1


def set_due_today(card):
    # The dates in the library and API are unclear; hack by adding a day, which
    # seems to produce the desired results.
    card.set_due(datetime.now() + timedelta(days=1))


def has_label(card, label_name):
    for label in card.labels:
        if label.name == label_name:
            return True
    return False


def get_chores_board(client):
    boards = client.list_boards()
    for board in boards:
        if 'Chores' in board.name:
            return board
    raise Exception('Chores board not found.')


def get_to_do_lists(board):
    """Get all the 'to do' lists from a board."""
    todo = []
    lists = board.get_lists(None)
    for list_ in lists:
        name = list_.name.lower()
        if 'todo' in name or 'to do' in name:
            todo.append(list_)
    return todo


def find_todo_list_by_member(card):
    """Find the todo list for a chore card according to the assigned member."""
    # Figure out who the chore is assigned to and find that to do list.
    if not card.member_ids:
        return None
    member = card.client.get_member(card.member_ids[0])
    first_name = member.full_name.split(' ')[0]
    lists = card.board.get_lists(None)
    for list_ in lists:
        if first_name in list_.name:
            return list_
    return None
