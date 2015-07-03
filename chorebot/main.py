from chorebot.config import create_client


def main():
    client = create_client()
    chores = get_chores_board(client)
    lists = chores.get_lists(None)
    print lists


def get_chores_board(client):
    boards = client.list_boards()
    for board in boards:
        if 'Chores' in board.name:
            return board
    raise Exception('Chores board not found.')


if __name__ == '__main__':
    main()
