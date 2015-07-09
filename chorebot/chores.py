from datetime import datetime
from chorebot.config import create_client
from chorebot.log import get_logger

logger = get_logger(__name__)


def daily_update():
    client = create_client()
    chores_board = get_chores_board(client)
    cards = chores_board.get_cards()
    reset_personal_daily_chores(client, cards)


def reset_personal_daily_chores(client, cards):
    for card in cards:
        if has_label(card, 'Personal Daily'):
            card.set_due(datetime.utcnow())
            move_to_correct_list(client, card)


def move_to_correct_list(client, card):
    list_ = find_todo_list_for_chore(client, card)
    if list_ and card.list_id != list_.id:
        card.change_list(list_.id)
        logger.info(
            'Card "{}" moved to list "{}".'.format(
                card.name,
                list_.name
            )
        )

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


def find_todo_list_for_chore(client, card):
    """Find the todo list for a chore card."""
    # Figure out who the chore is assigned to and find that to do list.
    if not card.member_ids:
        return None
    member = client.get_member(card.member_ids[0])
    first_name = member.full_name.split(' ')[0]
    lists = card.board.get_lists(None)
    for list_ in lists:
        if first_name in list_.name:
            return list_
    return None
