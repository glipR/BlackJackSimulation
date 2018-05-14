from GenericPlayer import *

class DummyPlayer(GenericPlayer):

	def hitResponse(self, state):
		if len(self.hands) != 0:
			if self.hands[0].score() < 18:
				return HIT
		return DONE

	def betResponse(self, state):
		board_bet = state.cur_bet()
		if board_bet > self.cur_bet:
			if max([hand.score() for hand in self.hands]) > 15 + board_bet and self.cash > 0:
				return FOLLOW
			else:
				return FOLD
		elif max([hand.score() for hand in self.hands]) > 16 + board_bet and self.cash > 0:
			return RAISE
		else:
			return STAND

	def surrenderResponse(self, state):
		return False

	def splitResponse(self, state):
		if self.hands[0].canSplit():
			return True

