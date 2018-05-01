from constants import *
import Hand

"""
Generic Player class
	has to implement the following methods:
		startHand(self, card1, card2)
	
	has to have the following attributes:
		name
"""

class Player:

	def __init__(self, name = "Player"):
		self.name = name
		self.hands = []
		self.cash = 10

	def startHand(self, card1, card2):
		self.hands.append(Hand.Hand([card1, card2]))
