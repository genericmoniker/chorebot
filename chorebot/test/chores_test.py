from datetime import datetime
import unittest

import mock

from chorebot import chores
from chorebot.chores import get_todo_lists, get_todo_lists_by_card_members, \
    has_label, deal, update_chores
from chorebot.trello import Member, List, Card, Board, TrelloClient, Label


class UpdateChoresTest(unittest.TestCase):

    def setUp(self):
        chores.client = TrelloClient(None, None, mock.MagicMock())
        inigo = Member('Inigo Montoya')
        wesley = Member('Wesley')
        buttercup = Member('Buttercup')
        members = [inigo, wesley, buttercup]
        list_inigo = List('Inigo - To Do')
        list_wesley = List('Wesley - To Do')
        list_buttercup = List('Buttercup - To Do')
        list_done = List('Done')
        lists = [list_inigo, list_wesley, list_buttercup, list_done]
        cards = [
            Card(labels=[Label('Daily')]),
            Card(labels=[Label('Daily')]),
            Card(labels=[Label('Daily')]),
            Card(labels=[Label('Weekly')]),
            Card(labels=[Label('Weekly')]),
            Card([inigo.id], [Label('Daily')], 'Inigo\'s'),
            Card([wesley.id], [Label('Daily')]),
            Card([inigo.id, wesley.id], [Label('Twice Weekly')], 'Shared')
        ]
        for card in cards:
            card.list_id = list_done.id
        left_over = Card(labels=[Label('Weekly')])
        left_over.list_id = list_inigo.id
        cards.append(left_over)
        self.board = Board(lists, cards, members)

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
        cards = [Card(), Card(), Card(), Card()]
        lists = [List('1'), List('2')]
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
        card = Card(labels=[Label('Princess'), Label('Farm Boy')])

        self.assertTrue(has_label(card, 'Princess'))
        self.assertTrue(has_label(card, 'farm boy'))
        self.assertFalse(has_label(card, 'Pirate'))

    def test_get_todo_lists(self):
        todo_lists = [
            List('todo'),
            List('to do'),
            List('ToDo'),
            List('To Do'),
            List('Inigo - todo'),
            List('to do - Wesley'),
        ]
        other_lists = [
            List('done'),
            List('Buttercup'),
        ]
        board = Board(lists=todo_lists + other_lists)

        result = get_todo_lists(board)

        self.assertListEqual(result, todo_lists)

    def test_get_todo_lists_by_card_members(self):
        inigo = Member('Inigo Montoya')
        wesley = Member('Wesley')
        buttercup = Member('Buttercup')
        members = [inigo, wesley, buttercup]
        list_inigo = List('Inigo - todo')
        list_wesley = List('to do - Wesley')
        lists = [list_inigo, list_wesley, List('done')]
        cards = [
            Card([inigo.id]),
            Card([wesley.id]),
            Card([inigo.id, wesley.id])
        ]
        board = Board(lists, cards, members)

        result = get_todo_lists_by_card_members(board, cards[0])
        self.assertEqual(result, [list_inigo])

        result = get_todo_lists_by_card_members(board, cards[1])
        self.assertEqual(result, [list_wesley])

        result = get_todo_lists_by_card_members(board, cards[2])
        self.assertEqual(result, [list_inigo, list_wesley])
