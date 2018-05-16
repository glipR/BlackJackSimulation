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
		self.removing = []

	def startHand(self, card1, card2):
		self.hands.append(Hand.Hand([card1, card2]))

	def newRound(self):
		self.cur_bet = 0

	def hitResponse(self, hand, state):
		#Implemented by each individual
		return

	def betResponse(self, hand, state):
		#Implemented by each individual
		return

	def surrenderResponse(self, state):
		#Implemented by each individual
		return

	def splitResponse(self, state):
		#Implemented by each individual
		return

	def setSplit(self, card1, card2):
		self.hands[0].cards[0][VIS] = True
		self.hands[0].cards[1][VIS] = True
		hand1 = Hand.Hand([self.hands[0].cards[0], card1])
		hand2 = Hand.Hand([self.hands[0].cards[1], card2])
		self.hands = [hand1, hand2]

	def hit(self, card, hand):
		self.hands[self.hands.index(hand)].addCard(card)
		if not self.hands[self.hands.index(hand)].isValid():
			self.removing.append(self.hands.index(hand))

	def update(self):
		for index in self.removing[::-1]:
			del self.hands[index]
		self.removing = []

	def getScores(self):
		return [hand.score() for hand in self.hands]

	def takeMoney(self, amount, hand):
		self.cash -= amount
		self.hands[self.hands.index(hand)].cur_bet += amount

	def giveMoney(self, amount):
		self.cash += amount
