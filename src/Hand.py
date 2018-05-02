from constants import *
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
		return self.score() <= 21

	def score(self):
		count_aces = 0
		card_sum = 0
		for card in self.cards:
			if card[FACE] == "A":
				count_aces += 1
			card_sum += MIN_VALUE[card[FACE]]
		for _ in range(count_aces):
			if card_sum < 12:
				card_sum += 10
		return card_sum

	def highCard(self):
		cur = self.cards[0]
		for x in range(1, len(self.cards)):
			if compareHighCard(cur, self.cards[x]) == 1:
				cur = self.cards[x]
		return cur