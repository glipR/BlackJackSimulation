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

class GenericPlayer:

	def __init__(self, name = "Dummy"):
		self.name = name
		self.hands = []
		self.cash = 10
		self.cur_bet = 0

	def startHand(self, card1, card2):
		self.hands.append(Hand.Hand([card1, card2]))
		self.cur_hand = 0

	def newRound(self):
		self.cur_bet = 0

	def hitResponse(self, state):
		#Implemented by each individual
		return

	def betResponse(self, state):
		#Implemented by each individual
		return

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

	def giveMoney(self, amount):
		self.cash += amount
