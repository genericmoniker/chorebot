from datetime import datetime
import unittest
from chorebot.chores import get_todo_lists, get_todo_lists_by_card_members, \
    has_label, deal, update_chores


class UpdateChoresTest(unittest.TestCase):

    def setUp(self):
        daily = FakeLabel('Daily')
        bi_weekly = FakeLabel('Twice Weekly')
        weekly = FakeLabel('Weekly')
        inigo = FakeMember('Inigo Montoya')
        wesley = FakeMember('Wesley')
        buttercup = FakeMember('Buttercup')
        members = [inigo, wesley, buttercup]
        list_inigo = FakeList('Inigo - To Do')
        list_wesley = FakeList('Wesley - To Do')
        list_buttercup = FakeList('Buttercup - To Do')
        list_done = FakeList('Done')
        lists = [list_inigo, list_wesley, list_buttercup, list_done]
        cards = [
            FakeCard(labels=[daily]),
            FakeCard(labels=[daily]),
            FakeCard(labels=[daily]),
            FakeCard(labels=[weekly]),
            FakeCard(labels=[weekly]),
            FakeCard([inigo.id], [daily], 'Inigo\'s'),
            FakeCard([wesley.id], [daily]),
            FakeCard([inigo.id, wesley.id], [bi_weekly], 'Shared')
        ]
        for card in cards:
            card.change_list(list_done.id)
        left_over = FakeCard(labels=[weekly])
        left_over.change_list(list_inigo.id)
        cards.append(left_over)
        self.board = FakeBoard(lists, cards, members)

    def test_daily_assigned(self):
        now = datetime(2015, 7, 21, 3)  # a Tuesday

        update_chores(self.board, now)

        list_done = self.board.obj_by_name('lists', 'Done')
        for card in self.board.cards:
            if has_label(card, 'Daily'):
                self.assertNotEqual(card.list_id, list_done.id)
                self.assertEqual(card.due.day, 22)  # UTC issue

    def test_bi_weekly_assigned(self):
        now = datetime(2015, 7, 23, 3)  # a Thursday

        update_chores(self.board, now)

        list_done = self.board.obj_by_name('lists', 'Done')
        for card in self.board.cards:
            if has_label(card, 'Twice Weekly'):
                self.assertNotEqual(card.list_id, list_done.id)
                self.assertEqual(card.due.day, 26)  # UTC issue

    def test_weekly_assigned(self):
        now = datetime(2015, 7, 20, 3)  # a Monday

        update_chores(self.board, now)

        list_done = self.board.obj_by_name('lists', 'Done')
        for card in self.board.cards:
            if has_label(card, 'Weekly'):
                self.assertNotEqual(card.list_id, list_done.id)
                self.assertEqual(card.due.day, 26)  # UTC issue

    def test_single_member_assigned(self):
        now = datetime(2015, 7, 20, 3)  # a Monday

        update_chores(self.board, now)

        card = self.board.obj_by_name('cards', 'Inigo\'s')
        list_inigo = self.board.obj_by_name('lists', 'Inigo - To Do')
        self.assertEqual(card.list_id, list_inigo.id)

    def test_multi_member_assigned(self):
        now = datetime(2015, 7, 20, 3)  # a Monday

        update_chores(self.board, now)

        card = self.board.obj_by_name('cards', 'Shared')
        list_inigo = self.board.obj_by_name('lists', 'Inigo - To Do')
        list_wesley = self.board.obj_by_name('lists', 'Wesley - To Do')
        self.assertIn(card.list_id, [list_inigo.id, list_wesley.id])


class ChoresHelperTest(unittest.TestCase):

    def test_deal(self):
        cards = [FakeCard(), FakeCard(), FakeCard(), FakeCard()]
        lists = [FakeList('1'), FakeList('2')]
        deal(cards, lists)
        count0 = count1 = 0
        for card in cards:
            if card.list_id == lists[0].id:
                count0 += 1
            elif card.list_id == lists[1].id:
                count1 += 1
        self.assertEqual(count0, len(cards) / 2)
        self.assertEqual(count1, len(cards) / 2)

    def test_has_label(self):
        card = FakeCard(labels=[
            FakeLabel('Princess'),
            FakeLabel('Farm Boy'),
        ])

        self.assertTrue(has_label(card, 'Princess'))
        self.assertTrue(has_label(card, 'farm boy'))
        self.assertFalse(has_label(card, 'Pirate'))

    def test_get_todo_lists(self):
        todo_lists = [
            FakeList('todo'),
            FakeList('to do'),
            FakeList('ToDo'),
            FakeList('To Do'),
            FakeList('Inigo - todo'),
            FakeList('to do - Wesley'),
        ]
        other_lists = [
            FakeList('done'),
            FakeList('Buttercup'),
        ]
        board = FakeBoard(lists=todo_lists + other_lists)

        result = get_todo_lists(board)

        self.assertListEqual(result, todo_lists)

    def test_get_todo_lists_by_card_members(self):
        inigo = FakeMember('Inigo Montoya')
        wesley = FakeMember('Wesley')
        buttercup = FakeMember('Buttercup')
        members = [inigo, wesley, buttercup]
        list_inigo = FakeList('Inigo - todo')
        list_wesley = FakeList('to do - Wesley')
        lists = [list_inigo, list_wesley, FakeList('done')]
        cards = [
            FakeCard([inigo.id]),
            FakeCard([wesley.id]),
            FakeCard([inigo.id, wesley.id])
        ]
        board = FakeBoard(lists, cards, members)

        result = get_todo_lists_by_card_members(board, cards[0])
        self.assertEqual(result, [list_inigo])

        result = get_todo_lists_by_card_members(board, cards[1])
        self.assertEqual(result, [list_wesley])

        result = get_todo_lists_by_card_members(board, cards[2])
        self.assertEqual(result, [list_inigo, list_wesley])


class FakeTrelloObject(object):
    _next_id = 1

    @classmethod
    def next_id(cls):
        id_ = cls._next_id
        cls._next_id += 1
        return id_

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)


class FakeBoard(FakeTrelloObject):
    def __init__(self, lists=None, cards=None, members=None):
        self.id = self.next_id()
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


class FakeList(FakeTrelloObject):
    def __init__(self, name):
        self.id = self.next_id()
        self.name = name


class FakeCard(FakeTrelloObject):
    def __init__(self, member_ids=None, labels=None, name=None):
        self.id = self.next_id()
        self.member_ids = member_ids or []
        self.labels = labels or []
        self.name = name
        self.due = None
        self.list_id = None

    def fetch(self, eager=True):
        pass

    def set_due(self, due):
        self.due = due

    def change_list(self, list_id):
        self.list_id = list_id


class FakeLabel(FakeTrelloObject):
    def __init__(self, name):
        self.id = self.next_id()
        self.name = name


class FakeMember(FakeTrelloObject):
    def __init__(self, full_name):
        self.id = self.next_id()
        self.full_name = full_name
