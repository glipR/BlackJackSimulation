from constants import *
import Deck
import DummyPlayer
import HumanPlayer
import GameState
import Bots

"""
Game Implementation
	The main file for simulation, encapsulates the Blackjack hitting and betting rounds
	for 1 round
"""

class Game:

	def __init__(self):
		self.players = [Bots.SimpleBully(name= "Simple Bully"),
						Bots.LuckyDisciple(name= "Lucky Disciple"),
						Bots.UnluckyDisciple(name= "Unlucky Disciple"),
						Bots.OpenMindedBully(name= "Open Minded Bully"),
						Bots.Calculator(name= "Calculator")]

		#self.players = [DummyPlayer.DummyPlayer(name = "AI 1"),
		#				DummyPlayer.DummyPlayer(name = "AI 2"),
		#				DummyPlayer.DummyPlayer(name = "AI 3")]

		self.playing_players = [player for player in self.players]

		self.deck = Deck.Deck()

		self.verbose = True

		self.pool = 0

		self.gameState = GameState.gameState()

		self.winning_players = []

	def dealTwoCards(self):
		"""
		Deals two cards to all players
		"""
		for player in self.playing_players:
			card1, card2 = self.deck.pick_card(), self.deck.pick_card()
			card2[VIS] = True
			player.startHand(card1, card2)
			if self.verbose:
				print("{} received the\n\t{} and the\n\t{} {}".format(player.name, cardDescription(card1), cardDescription(card2), player.getScores()))

	def offerSurrender(self):
		"""
		Offers each player to surrender, and removes them should this be the case
		"""
		keep = []
		for player in self.playing_players:
			self.updateGameState()
			if player.surrenderResponse(self.gameState):
				player.giveMoney(self.gameState.cur_bet()/2)
				player.removeHand(player.hands[0])
				player.dead = True
				self.pool -= self.gameState.cur_bet()/2
				if self.verbose:
					print("{} Surrendered and recieved ${} back".format(player.name, self.gameState.cur_bet()/2))
			else:
				keep.append(player)
		self.playing_players = keep

	def offerSplit(self):
		"""
		Offers each player to split their cards, also checks that a split is possible
		"""
		for player in self.players:
			self.updateGameState()
			if player.splitResponse(self.gameState):
				card1, card2 = self.deck.pick_card(), self.deck.pick_card()
				player.giveMoney(self.gameState.cur_bet())
				player.setSplit(card1, card2)
				player.takeMoney(self.gameState.cur_bet(), player.hands[0])
				player.takeMoney(self.gameState.cur_bet(), player.hands[1])
				self.pool += self.gameState.cur_bet()
				if self.verbose:
					print("{} Split their hand, and recieved 2 new cards".format(player.name))

	def simRound(self):
		"""
		Simulates a round of blackjack
		:return whether to finish the game after this round
		"""
		#Create an array which can be used to find the correct hand, player
		hands_arr = []
		for player in self.playing_players:
			for hand in player.hands:
				hands_arr.append([hand, player])
		#First, prompt for betting, then dealing

		#If everyone stands, with no hits, then stop
		all_stand = True

		for hand, player in hands_arr:

			self.updateGameState()

			if self.gameState.players_alive() == 1:
				return True

			if self.verbose:
				print("Player {}, Hand {}".format(player.name, player.hands.index(hand)))

				print([hand.allHand() for hand in player.hands])
				print(player.removing)


			## Betting

			if player.cash > 0:
				betResponse = player.betResponse(hand, self.gameState)
			else:
				if player.cur_bet < self.gameState.cur_bet():
					betResponse = FOLD
				else:
					betResponse = STAND
			if betResponse == RAISE:
				all_stand = False
				if self.verbose:
					print("\tRaises")
				self.cur_bet += 1
				player.takeMoney(1, hand)
				self.pool += 1
			elif betResponse == FOLLOW:
				all_stand = False
				if self.verbose:
					print("\tFollows")
				player.takeMoney(1, hand)
				self.pool += 1
			elif betResponse == STAND:
				if self.verbose:
					print("\tStands")
			elif betResponse == FOLD:
				player.removeHand(hand)
				all_stand = False
				if self.verbose:
					print("\tFolds")
			else:
				raise ValueError("I don't understand betting response {}".format(betResponse))

			## Dealing

			all_done = True

			if betResponse != FOLD and not hand.done:
				if self.verbose:
					print("\tThen")

				hitResponse = player.hitResponse(hand, self.gameState)
				if hitResponse == HIT:
					all_done = False
					card = self.deck.pick_card()
					card[VIS] = True
					player.hit(card, hand)
					if self.verbose:
						print("\tHit and recieved the {}".format(cardDescription(card)))
				elif hitResponse == DONE:
					player.hands[player.hands.index(hand)].done = True
					if self.verbose:
						print("\tDoes not hit")
				else:
					raise ValueError("I don't understand hitting response {}".format(hitResponse))

		# Remove any hands / players that busted

		to_remove = []
		for x in range(len(self.playing_players)):
			self.playing_players[x].update()
			if len(self.playing_players[x].hands) == 0:
				self.playing_players[x].dead = True
				to_remove.append(x)
		for y in sorted(to_remove)[::-1]:
			if self.verbose:
				print("{} is out of valid hands!".format(self.playing_players[y].name))
			del self.playing_players[y]

		# Return whether every stood / held

		return (all_stand and all_done)

	def initialBet(self):
		for player in self.playing_players:
			player.takeMoney(1, player.hands[0])
			self.pool += 1
			self.cur_bet = 1

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
		self.offerSurrender()
		self.offerSplit()
		res = False
		while not res and len(self.playing_players) > 1:
			res = self.simRound()
		if len(self.playing_players) == 0:
			if self.verbose:
				print("The dealer wins!")
		else:
			for player in self.players:
				player.update()
			if self.verbose:
				print("The remaining hands are:")
				for player in self.playing_players:
					for hand in player.hands:
						print("{} Hand {}: {}".format(player.name, player.hands.index(hand), hand.allHand()))
			self.winning_players = self.comparePlayers(self.playing_players)
			for player in self.playing_players:
				for hand in player.hands:
					if (hand, player) not in self.winning_players:
						player.removeHand(hand)
			if len(self.winning_players) == 1:
				player = self.winning_players[0][1]
				player.giveMoney(self.pool)
				if self.verbose:
					print("{} won the pool of ${}".format(player.name, self.pool))
			elif len(set([x[1] for x in self.winning_players])) == 1:
				player = self.winning_players[0][1]
				player.giveMoney(self.pool)
				if self.verbose:
					print("{} won the pool of ${}".format(player.name, self.pool))
			else:
				player_dict = {}
				for hand in self.winning_players:
					if hand[1] not in player_dict.keys():
						player_dict[hand[1]] = 0
					player_dict[hand[1]] += 1
				for key in player_dict.keys():
					if self.verbose:
						print("{} won {}/{} of the pool of ${}".format(key.name, player_dict[key], len(self.winning_players), self.pool*player_dict[key]/len(self.winning_players)))
					key.giveMoney(self.pool * player_dict[key] / len(self.winning_players))

	def updateGameState(self):
		self.gameState.reset()
		for player in self.players:
			self.gameState.addPlayer(player)

