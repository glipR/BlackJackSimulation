from constants import *
import Deck
import Player

"""
Game Implementation
	The main file for simulation, encapsulates the Blackjack hitting and betting rounds
	for 1 round
"""

class Game:

	def __init__(self):

		self.players = [Player.Player(name= "Player 1"),
						Player.Player(name= "Player 2"),
						Player.Player(name= "Player 3")]

		self.playing_players = [player for player in self.players]

		self.deck = Deck.Deck()

	def dealTwoCards(self):
		for player in self.playing_players:
			card1, card2 = self.deck.pick_card(), self.deck.pick_card()
			player.startHand(card1, card2)
			print("{} received the {} and the {}".format(player.name, cardDescription(card1), cardDescription(card2)))


test = Game()
test.dealTwoCards()