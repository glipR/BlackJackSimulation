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

	def startHand(self, card1, card2):
		self.hands.append(Hand.Hand([card1, card2]))
		self.cur_hand = 0

	def response(self):
		#Placeholder for testing
		if self.hits > 0:
			self.hits -= 1
			return HIT
		else:
			self.hits = 3
			return DONE

	def hit(self, card):
		self.hands[self.cur_hand].addCard(card)
		if not self.hands[self.cur_hand].isValid():
			#Remove the hand
			pass