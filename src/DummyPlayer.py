from GenericPlayer import *

class DummyPlayer(GenericPlayer):

	def hitResponse(self, hand, state):
		if hand.score() < 18:
			return HIT
		return DONE

	def betResponse(self, hand, state):
		board_bet = state.cur_bet()
		if board_bet > hand.cur_bet:
			if hand.score() > 15 + board_bet and self.cash > 0:
				return FOLLOW
			else:
				return FOLD
		elif hand.score() > 16 + board_bet and self.cash > 0:
			return RAISE
		else:
			return STAND

	def surrenderResponse(self, state):
		return False

	def splitResponse(self, state):
		if self.hands[0].canSplit():
			return True

