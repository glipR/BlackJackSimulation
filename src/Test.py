from constants import *
from Game import *

class Test(Game):

	def __init__(self):
		self.iter = 10000

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
win_dic = {}
cash_dic = {}
i = 0

first = True
for game in res:
	i += 1
	#print(f"Game: {i}")
	start = first
	for player in game[1]:
		if start:
			first = False
			win_dic[player.name] = []
			cash_dic[player.name] = []
		win_dic[player.name].append(True if len(player.hands) - len(player.removing) > 0 else False)
		cash_dic[player.name].append(player.cash-10)
		#print(f"\tPlayer: {player.name}")
		for hand in player.hands + player.dead_hands:
			#print(f"\t\tHand: ({hand.cur_bet}) {hand.allHand()} {'X' if hand in [y[0] for y in game[0]] else ''}")
			continue

print("\n")
for name in [player.name for player in test.players]:
	print(name, "\n")
	print("Win %:", "%.2f" % (sum(win_dic[name])/test.iter*100))
	print("Total winnings:", "%.0f" % (sum(cash_dic[name])))
	print()
	if sum(win_dic[name]) != 0:
		print("Average Win:", "%.2f" % (sum([cash_dic[name][x] for x in range(len(cash_dic[name])) if win_dic[name][x]])/sum(win_dic[name])))
	else:
		print("Average Win:", 0)
	if sum(win_dic[name]) != len(win_dic[name]):
		print("Average Loss:", "%.2f" % (sum([cash_dic[name][x] for x in range(len(cash_dic[name])) if not win_dic[name][x]])/(len(win_dic[name])-sum(win_dic[name]))))
	else:
		print("Average Loss:", 0)
	print("\n")
