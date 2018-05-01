

"""
Hand Class
	Stores the information concerning a single hand
"""

class Hand:

	def __init__(self, cards):
		self.cards = cards

	def addCard(self, card):
		self.cards.append(card)

	def isValid(self):
		return True