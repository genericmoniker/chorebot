
class BoardCache(object):
    """Cache of a Trello board."""

    def __init__(self, board):
        self.board = board
        self._lists = None
        self._cards = None
        self._members = None

    @property
    def lists(self):
        if not self._lists:
            self._lists = self.board.get_lists(None)
        return self._lists

    @property
    def cards(self):
        if not self._cards:
            self._cards = self.board.get_cards()
        return self._cards

    @property
    def members(self):
        if not self._members:
            # todo - get_members is broken in the library
            self._members = self.board.get_members()
        return self._members

    def get_member(self, member_id):
        return self.board.client.get_member(member_id)
        # for member in self.members:
        #     if member.id == member_id:
        #         return member
        # return None
