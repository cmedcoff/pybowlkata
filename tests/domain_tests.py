from bowl import *
from random import randint
import unittest 
from unittest import mock

class Non10thFrameTests(unittest.TestCase):

    def setUp(self):
        next_frame_number = randint(2, 10)
        self.next_frame = Frame(next_frame_number, None)
        self.frame = Frame(next_frame_number - 1 , self.next_frame)

    def test_non_strike_or_spare(self):
        self.frame.pins1 = randint(0,5)
        self.frame.pins2 = randint(0,4)
        self.assertFalse(self.frame.is_strike())
        self.assertFalse(self.frame.is_spare())
        expected = str(self.frame.pins1 + self.frame.pins2)
        actual = self.frame.calc_score()
        self.assertEqual(expected, actual)

    def test_spare_score(self):
        self.frame.pins1 = 5
        self.frame.pins2 = 5
        self.assertTrue(self.frame.is_spare())

        # validate score cannot be determined without the next throw
        self.assertEqual("?", self.frame.calc_score())

        # validate score with next throw
        self.next_frame.pins1 = 1
        self.assertEqual(str(11), self.frame.calc_score()) 

    def test_strike_score(self):
        self.frame.pins1 = 10
        self.assertEqual(True, self.frame.is_strike())

        # validate score cannot be determine without the next two throws
        self.assertEqual("?", self.frame.calc_score())

        # validate score with next two throws
        self.next_frame.pins1 = 3
        self.next_frame.pins2 = 2
        self.assertEqual(str(15), self.frame.calc_score())

  
class _10thFrameTests(unittest.TestCase):

    def setUp(self):
        self.f10 = Frame(10, None)

    def test_10th_frame_non_strike_or_spare_score(self):
        # there should only be two throws, then the game is over
        # the score for the frame is the sum of the two throws
        self.f10.pins1 = randint(0,4)
        self.f10.pins2 = randint(0,4)
        expected = str(self.f10.pins1 + self.f10.pins2)
        actual = self.f10.calc_score()
        self.assertEqual(expected, actual)

#    def test_strike_score(self):
#        pass
#
#    def test_spare_score(self):
#        pass

class TestPlayerTurnNon10thFrame(unittest.TestCase):

    def setUp(self):
        self.mockBall = mock.Mock()
        self.player = Player("Chuck", self.mockBall)
        self.player.current_frame_index = randint(0,8) 

    def test_turn_over_after_one_throw_for_strike(self):
        self.mockBall.throw.side_effect = [10]
        frame_index = self.player.current_frame_index
        self.player.take_turn()
        self.assertTrue(self.player.frames[frame_index].has_thrown_1())
        self.assertFalse(self.player.frames[frame_index].has_thrown_2())
        self.assertFalse(self.player.frames[frame_index].has_thrown_3())

    def test_turn_over_after_two_throw_for_spare(self):
        self.mockBall.throw.side_effect = [9, 1]
        frame_index = self.player.current_frame_index
        self.player.take_turn()
        self.assertTrue(self.player.frames[frame_index].has_thrown_1())
        self.assertTrue(self.player.frames[frame_index].has_thrown_2())
        self.assertFalse(self.player.frames[frame_index].has_thrown_3())


class TestPlayerTurn10thFrame(unittest.TestCase):

    def setUp(self):
        self.mockBall = mock.Mock()
        self.player = Player("Chuck", self.mockBall)
        self.player.current_frame_index = 9

    def test_turn_over_after_two_throws_for_non_strike(self):
        self.mockBall.throw.side_effect = [5, 1]
        frame_index = self.player.current_frame_index
        self.player.take_turn()
        self.assertTrue(self.player.frames[frame_index].has_thrown_1())
        self.assertTrue(self.player.frames[frame_index].has_thrown_2())
        self.assertFalse(self.player.frames[frame_index].has_thrown_3())

    def test_turn_over_after_three_throws_for_spare(self):
        self.mockBall.throw.side_effect = [5, 5, 5]
        frame_index = self.player.current_frame_index
        self.player.take_turn()
        self.assertTrue(self.player.frames[frame_index].has_thrown_1())
        self.assertTrue(self.player.frames[frame_index].has_thrown_2())
        self.assertTrue(self.player.frames[frame_index].has_thrown_3())

    def test_turn_over_after_three_throws_for_strike(self):
        self.mockBall.throw.side_effect = [10, 1, 1]
        frame_index = self.player.current_frame_index
        self.player.take_turn()
        self.assertTrue(self.player.frames[frame_index].has_thrown_1())
        self.assertTrue(self.player.frames[frame_index].has_thrown_2())
        self.assertTrue(self.player.frames[frame_index].has_thrown_3())

class miscTests(unittest.TestCase):

    def setUp(self):
        self.mockBall = mock.Mock()
        self.player = Player("Chuck", self.mockBall)
        self.player.current_frame_index = 0

    def test_some(self):
        self.mockBall.throw.side_effect = [10, 10, 9, 0, ]

        self.player.take_turn()
        print(self.player)

        self.player.take_turn()
        print(self.player)

        self.player.take_turn()
        print(self.player)



