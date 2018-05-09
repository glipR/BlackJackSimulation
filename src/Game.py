from constants import *
import Deck
import Player
import GameState

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

		self.gameState = GameState.gameState()

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
				print("{} received the\n\t{} and the\n\t{} {}".format(player.name, cardDescription(card1), cardDescription(card2), player.getScores()))

	def dealingRound(self):
		"""
		Simulates the dealing round of all players
		:return: none
		"""
		removing_players = []
		for player in self.playing_players:
			while True:
				self.updateGameState()
				response = player.hitResponse(self.gameState)
				if response == HIT:
					card = self.deck.pick_card()
					card[VIS] = True
					hit_response = player.hit(card)
					if self.verbose:
						print("{} hit and recieved the\n\t{}".format(player.name, cardDescription(card)))
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
						for hand in player.hands:
							print("\t{}".format(hand.knownHand()))
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
			self.updateGameState()
			player = self.playing_players[player_ind]
			response = player.betResponse(self.gameState)
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
		:return: an array containing all winning players
		"""
		hands = []
		for player in players:
			for hand in player.hands:
				hands.append((hand, player))
		### Rule 1 - Blackjack
		winners = []
		for hand in hands:
			if hand[0].isBlackjack():
				winners.append(hand)
		if winners != []:
			return winners

		### Rule 2 - 21
		for hand in hands:
			if hand[0].score() == 21:
				winners.append(hand)
		if winners != []:
			return winners

		### Rule 3 - 5 Card
		for hand in hands:
			if len(hand[0]) >= 5:
				winners.append(hand)
		if winners != []:
			return winners

		### Rule 4 - Score
		max_score = max(hands, key = lambda x: x[0].score())[0].score()
		for hand in hands:
			if hand[0].score() == max_score:
				winners.append(hand)
		# Winners is definitely non zero
		return winners

	def playGame(self):
		self.dealTwoCards()
		self.initialBet()
		self.dealingRound()
		self.bettingRound()
		if self.verbose:
			if len(self.playing_players) == 0:
				print("The dealer wins!")
			else:
				winning_players = self.comparePlayers(self.playing_players)
				if len(winning_players) == 1:
					player = winning_players[0][1]
					print("{} won the pool of ${}".format(player.name, self.pool))
					player.giveMoney(self.pool)
				elif len(set([x[1] for x in winning_players])) == 1:
					player = winning_players[0][1]
					print("{} won the pool of ${}".format(player.name, self.pool))
					player.giveMoney(self.pool)
				else:
					player_dict = {}
					for hand in winning_players:
						if hand[1] not in player_dict.keys():
							player_dict[hand[1]] = 0
						player_dict[hand[1]] += 1
					for key in player_dict.keys():
						print("{} won {}/{} of the pool of ${}".format(key.name, player_dict[key], len(winning_players), self.pool))
						key.giveMoney(self.pool * player_dict[key] // len(winning_players))

	def updateGameState(self):
		self.gameState.reset()
		for player in self.players:
			self.gameState.addPlayer(player)


test = Game()
test.playGame()
