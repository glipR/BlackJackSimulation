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

		self.verbose = True

	def dealTwoCards(self):
		for player in self.playing_players:
			card1, card2 = self.deck.pick_card(), self.deck.pick_card()
			player.startHand(card1, card2)
			if self.verbose:
				print("{} received the {} and the {}".format(player.name, cardDescription(card1), cardDescription(card2)))

	def hittingRound(self):
		removing_players = []
		for player in self.playing_players:
			while True:
				response = player.response()
				if response == HIT:
					card = self.deck.pick_card()
					player.hit(card)
					if self.verbose:
						print("{} hit and recieved {}".format(player.name, cardDescription(card)))
				elif response == FOLD:
					removing_players.append(player)
					break
				elif response == DONE:
					break
		for player in removing_players:
			self.playing_players.remove(player)


test = Game()
test.dealTwoCards()
test.hittingRound()