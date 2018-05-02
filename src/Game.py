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
		"""
		Deals two cards to all players
		(Meant for game start, doesn't currently deal with Dealer hand)
		:return:
		"""
		for player in self.playing_players:
			card1, card2 = self.deck.pick_card(), self.deck.pick_card()
			player.startHand(card1, card2)
			if self.verbose:
				print("{} received the {} and the {}".format(player.name, cardDescription(card1), cardDescription(card2)))

	def playerState(self, player):
		"""
		Gets the card state of the game, excluding the player argument
		:param player: Player whose hands you will exclude
		:return: list of players, from which the player can surmise cards + bets
		"""

	def dealingRound(self):
		"""
		Simulates the dealing round of all players
		:return: none
		"""
		removing_players = []
		for player in self.playing_players:
			while True:
				response = player.hitResponse()
				if response == HIT:
					card = self.deck.pick_card()
					card[VIS] = True
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

	def comparePlayers(self, players):
		"""
		Compares the remaining players hands and returns the winner
		:param players: the list of remaining players
		:return: the final player
		"""
		hands = []
		for player in players:
			for hand in player.hands:
				hands.append((hand, player))
		maxScore = max(hands, key = lambda x: x[0].score())[0].score()
		x = 0
		while x < len(hands):
			if hands[x][0].score() < maxScore:
				del hands[x]
			else:
				x += 1
		if len(hands) == 1:
			return hands[0][1]
		if maxScore == 21 and len(min(hands, key = lambda x: len(x[0].cards))[0].cards) == 2:
			#Blackjack present
			x = 0
			while x < len(hands):
				if len(hands[x][0].cards) > 2:
					del hands[x]
				else:
					x += 1
			if len(hands) == 1:
				return hands[0][1]
			while len(hands) > 1:
				card1 = hands[0][0].highCard()
				card2 = hands[1][0].highCard()
				if compareHighCard(card1, card2) == 0:
					del hands[1]
				else:
					del hands[0]
			return hands[0][1]
		else:
			while len(hands) > 1:
				card1 = hands[0][0].highCard()
				card2 = hands[1][0].highCard()
				if compareHighCard(card1, card2) == 0:
					del hands[1]
				else:
					del hands[0]
			return hands[0][1]

	def playGame(self):
		self.dealTwoCards()
		self.initialBet()
		self.dealingRound()
		self.bettingRound()
		if self.verbose:
			if len(self.playing_players) == 0:
				print("The dealer wins!")
			else:
				winning_player = self.comparePlayers(self.playing_players)
				print("{} won the pool of ${}".format(winning_player.name, self.pool))


test = Game()
test.playGame()
