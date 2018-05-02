from constants import *
import random

"""
Basic Deck implementation
	52 Cards, each with a suit and face
	Able to pick with replacement, or without replacement
"""

class Deck:

	def __init__(self):

		self.current_deck = [None]*(len(SUITS)*len(FACES))
		for x in range(len(SUITS)):
			for y in range(len(FACES)):
				self.current_deck[x*len(FACES) + y] = [SUITS[x], FACES[y], False]


	def pick_card(self, replacement = False):
		if len(self.current_deck) == 0:
			raise ValueError("Deck is empty")
		index = random.randint(0, len(self.current_deck)-1)

		returning_card =  self.current_deck[index]

		if not replacement:
			self.current_deck = self.current_deck[:index] + self.current_deck[index+1:]

		return returning_card

	def reset(self):
		self.current_deck = [None] * (len(SUITS) * len(FACES))
		for x in range(len(SUITS)):
			for y in range(len(FACES)):
				self.current_deck[x * len(FACES) + y] = [SUITS[x], FACES[y]]
