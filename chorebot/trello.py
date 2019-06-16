# -*- coding: utf-8 -*-
"""Simple Trello client."""

# See here for details about the API:
# https://developers.trello.com
import logging

import dateutil.parser
import requests


class TrelloClient(object):
    BASE_URL = "https://api.trello.com/1/"
    instance = None

    def __init__(self, key, token, session=None):
        TrelloClient.instance = self
        logging.getLogger("requests").setLevel(logging.WARN)
        self._s = session or requests.session()
        self._s.params = dict(key=key, token=token)

    def load_board(self, name_matcher):
        boards_data = self._get_boards()
        board_data = self._find_board(boards_data, name_matcher)
        board_id = board_data["id"]
        lists = [List.from_data(d) for d in self._get_lists(board_id)]
        cards = [Card.from_data(d) for d in self._get_cards(board_id)]
        members = [Member.from_data(d) for d in self._get_members(board_id)]
        for list_ in lists:
            list_.cards = [c for c in cards if c.list_id == list_.id]
        return Board(lists, cards, members, board_id)

    def add_card(self, name, to_list):
        url = self.BASE_URL + "cards"
        data = dict(name=name, idList=to_list.id, due=None)
        card_id = self._post(url, data)
        data["id"] = card_id
        return Card.from_data(data)

    def rename_card(self, card, new_name):
        card.name = new_name
        url = self.BASE_URL + "cards/{}/name".format(card.id)
        self._put(url, dict(value=new_name))

    def move_card(self, card, to_list):
        card.list_id = to_list.id
        url = self.BASE_URL + "cards/{}/idList".format(card.id)
        self._put(url, dict(value=to_list.id))

    def reschedule_card(self, card, due):
        card.due = due
        url = self.BASE_URL + "cards/{}/due".format(card.id)
        self._put(url, dict(value=due.isoformat()))

    def reposition_card(self, card, pos):
        url = self.BASE_URL + "cards/{}/pos".format(card.id)
        self._put(url, dict(value=pos))

    def _get(self, url):
        r = self._s.get(url)
        r.raise_for_status()
        return r.json()

    def _put(self, url, data):
        r = self._s.put(url, data)
        r.raise_for_status()

    def _post(self, url, data):
        r = self._s.post(url, data)
        r.raise_for_status()
        return r.json().get("id")

    def _get_boards(self):
        # https://developers.trello.com/advanced-reference/member#get-1-members-idmember-or-username-boards
        url = self.BASE_URL + "members/me/boards"
        return self._get(url)

    def _get_lists(self, board_id):
        # https://developers.trello.com/advanced-reference/board#get-1-boards-board-id-lists-filter
        url = self.BASE_URL + "boards/{}/lists".format(board_id)
        return self._get(url)

    def _get_cards(self, board_id):
        # https://developers.trello.com/advanced-reference/board#get-1-boards-board-id-lists-filter
        url = self.BASE_URL + "boards/{}/cards".format(board_id)
        return self._get(url)

    def _get_members(self, board_id):
        # https://developers.trello.com/advanced-reference/board#get-1-boards-board-id-members
        url = self.BASE_URL + "boards/{}/members".format(board_id)
        return self._get(url)

    @staticmethod
    def _find_board(boards_data, name_matcher):
        for board_data in boards_data:
            if name_matcher(board_data["name"]):
                return board_data
        else:
            raise Exception("Board not found.")


class TrelloObject(object):
    _next_id = 1

    @classmethod
    def next_id(cls):
        id_ = cls._next_id
        cls._next_id += 1
        return id_

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)


class Board(TrelloObject):
    def __init__(self, lists=None, cards=None, members=None, id_=None):
        self.id = id_ or self.next_id()
        self.lists = lists
        self.cards = cards
        self.members = members

    def get_member(self, member_id):
        for member in self.members:
            if member.id == member_id:
                return member
        return None

    def obj_by_name(self, attr, name):
        objs = self.__getattribute__(attr)
        for obj in objs:
            if obj.name == name:
                return obj


class List(TrelloObject):
    def __init__(self, name, id_=None):
        self.id = id_ or self.next_id()
        self.name = name
        self.cards = []

    @classmethod
    def from_data(cls, data):
        return cls(data["name"], data["id"])


class Card(TrelloObject):
    def __init__(
        self,
        member_ids=None,
        labels=None,
        name=None,
        due=None,
        list_id=None,
        id_=None,
    ):
        self.id = id_ or self.next_id()
        self.member_ids = member_ids or []
        self.labels = labels or []
        self.name = name
        self.due = self.to_datetime(due)
        self.list_id = list_id

    @classmethod
    def from_data(cls, data):
        return cls(
            data.get("idMembers", []),
            [Label.from_data(d) for d in data.get("labels", [])],
            data["name"],
            data["due"],
            data["idList"],
            data.get("id", None),
        )

    @staticmethod
    def to_datetime(dt):
        if dt:
            return dateutil.parser.parse(dt)
        return None


class Member(TrelloObject):
    def __init__(self, full_name, id_=None):
        self.id = id_ or self.next_id()
        self.full_name = full_name

    @classmethod
    def from_data(cls, data):
        return cls(data["fullName"], data["id"])


class Label(TrelloObject):
    def __init__(self, name, id_=None):
        self.id = id_ or self.next_id()
        self.name = name

    @classmethod
    def from_data(cls, data):
        return cls(data["name"], data["id"])
