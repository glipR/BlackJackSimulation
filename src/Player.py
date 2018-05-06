from constants import *
import Hand

"""
Generic Player class
	has to implement the following methods:
		startHand(self, card1, card2)
		response(self)
		hit(self, card)
		
	has to have the following attributes:
		name
"""

class Player:

	def __init__(self, name = "Player"):
		self.name = name
		self.hands = []
		self.cash = 10
		self.hits = 3
		self.verbose = True
		self.cur_bet = 0

	def startHand(self, card1, card2):
		self.hands.append(Hand.Hand([card1, card2]))
		self.cur_hand = 0

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

	def hit(self, card):
		self.hands[self.cur_hand].addCard(card)
		if not self.hands[self.cur_hand].isValid():
			del self.hands[self.cur_hand]
			return OVER
		return GOOD

	def getScores(self):
		return [hand.score() for hand in self.hands]

	def takeMoney(self, amount):
		self.cash -= amount
		self.cur_bet += amount
