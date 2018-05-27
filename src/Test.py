from constants import *
from Game import *

class Test(Game):

	def __init__(self):
		self.iter = 3

	def simulateReset(self):
		results = []
		for x in range(self.iter):
			Game.__init__(self)
			self.verbose = False
			self.playGame()
			results.append([self.winning_players,self.players])
		return results

test = Test()
res = test.simulateReset()
i = 0
for game in res:
	i += 1
	print(f"Game: {i}")
	for player in game[1]:
		print(f"\tPlayer: {player.name}")
		for hand in player.hands + player.dead_hands:
			print(f"\t\tHand: {hand.allHand()} {'X' if hand in [y[0] for y in game[0]] else ''}")

