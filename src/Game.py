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

		self.pool = 0

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
				response = player.hitResponse()
				if response == HIT:
					card = self.deck.pick_card()
					hit_response = player.hit(card)
					if self.verbose:
						print("{} hit and recieved {}".format(player.name, cardDescription(card)))
						if hit_response == GOOD:
							print("{} still has a valid hand!".format(player.name))
						elif hit_response == OVER:
							print("{} busted their hand!".format(player.name))
					if len(player.hands) == 0:
						removing_players.append(player)
				elif response == FOLD:
					removing_players.append(player)
					break
				elif response == DONE:
					if self.verbose:
						print("{} ended the round with hands with scores {}".format(player.name, player.getScores()))
					break
		for player in removing_players:
			self.playing_players.remove(player)

	def initialBet(self):
		for player in self.playing_players:
			player.takeMoney(1)
			self.pool += 1
			self.cur_bet = 1

	def bettingRound(self):
		player_ind = 0
		self.same_bet = 0
		while len(self.playing_players) > 1 and self.same_bet < 2*len(self.playing_players):
			player = self.playing_players[player_ind]
			response = player.betResponse(self.cur_bet)
			if response == RAISE:
				if self.verbose:
					print("{} Raises the bet!".format(player.name))
				self.cur_bet += 1
				self.same_bet = 1
				player.takeMoney(1)
				self.pool += 1
			elif response == FOLLOW:
				if self.verbose:
					print("{} Follows the previous bet".format(player.name))
				self.same_bet += 1
				player.takeMoney(1)
				self.pool += 1
			elif response == STAND:
				if self.verbose:
					print("{} is happy to stand".format(player.name))
				self.same_bet += 1
			elif response == FOLD:
				if self.verbose:
					print("{} is out!".format(player.name))
				del self.playing_players[player_ind]
				player_ind -= 1
			else:
				raise ValueError("I don't understand betting response {}".format(response))
			player_ind = (player_ind + 1) % len(self.playing_players)



	def playGame(self):
		self.dealTwoCards()
		self.initialBet()
		self.hittingRound()
		self.bettingRound()
		if self.verbose:
			if len(self.playing_players) == 0:
				print("The dealer wins!")
			else:
				print("{} won the pool of ${}".format(self.playing_players[0].name, self.pool))


test = Game()
test.playGame()
