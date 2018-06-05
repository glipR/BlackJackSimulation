from constants import *
from Game import *
import copy

class Test(Game):

	def __init__(self):
		self.iter = 1000

	def simulateReset(self):
		final = []
		for array in generate(2):
			results = []
			for x in range(self.iter):
				#print(f"Game: {x+1}")
				Game.__init__(self)
				self.players = []
				self.playing_players = []
				for x in array:
					if x == 0:
						self.players.append(Bots.SimpleBully(name= "Simple Bully"))
					if x == 1:
						self.players.append(Bots.LuckyDisciple(name= "Lucky Disciple"))
					if x == 2:
						self.players.append(Bots.UnluckyDisciple(name= "Unlucky Disciple"))
					if x == 3:
						self.players.append(Bots.OpenMindedBully(name= "Open Minded Bully"))
					if x == 4:
						self.players.append(Bots.Calculator(name= "Calculator"))
				self.playing_players = [player for player in self.players]
				self.verbose = False
				self.playGame()
				results.append([self.winning_players,self.players])
			final.append(results)
		return final


def generate(n):
	tmp = []
	array = list(range(n))
	c = [0]*n
	tmp.append(copy.copy(array))
	i = 0
	while i < n:
		if c[i] < i:
			if i%2 ==0:
				array[0], array[i] = array[i], array[0]
			else:
				array[c[i]], array[i] = array[i], array[c[i]]
			tmp.append(copy.copy(array))
			c[i] += 1
			i=0
		else:
			c[i] = 0
			i += 1
	return tmp



test = Test()
res = test.simulateReset()
for match in res:
	win_dic = {}
	cash_dic = {}
	i = 0
	first = True
	for game in match:
		i += 1
		#print(f"Game: {i}")
		start = first
		for player in game[1]:
			if start:
				first = False
				win_dic[player.name] = []
				cash_dic[player.name] = []
			#print(player.name +":", len(player.hands), len(player.removing))
			win_dic[player.name].append(True if len(player.hands) - len(player.removing) > 0 else False)
			cash_dic[player.name].append(player.cash-10)
			#print(f"\tPlayer: {player.name}")
			for hand in player.hands + player.dead_hands:
				#print(f"\t\tHand: ({hand.cur_bet}) {hand.allHand()} {'X' if hand in [y[0] for y in game[0]] else ''}")
				continue
	for player in match[0][1]:
		win_percent = (sum(win_dic[player.name])/test.iter*100)
		total_winnings = (sum(cash_dic[player.name]))
		if sum(win_dic[player.name]) != 0:
			average_win = (sum([cash_dic[player.name][x] for x in range(len(cash_dic[player.name])) if win_dic[player.name][x]])/sum(win_dic[player.name]))
		else:
			average_win = 0
		if sum(win_dic[player.name]) != len(win_dic[player.name]):
			average_loss = (sum([cash_dic[player.name][x] for x in range(len(cash_dic[player.name])) if not win_dic[player.name][x]])/(len(win_dic[player.name])-sum(win_dic[player.name])))
		else:
			average_loss = 0
		## NAME, ORDER, WIN%, TOTAL_WINNINGS, AVG_WIN, AVG_LOSS
		print(",".join([player.name, str(match[0][1].index(player)), "%.2f" % win_percent, "%.2f" % total_winnings, "%.2f" % average_win, "%.2f" % average_loss]))

# print("\n")
# for name in [player.name for player in test.players]:
# 	print(name, "\n")
# 	print("Win %:", "%.2f" % (sum(win_dic[name])/test.iter*100))
# 	print("Total winnings:", "%.0f" % (sum(cash_dic[name])))
# 	print()
# 	if sum(win_dic[name]) != 0:
# 		print("Average Win:", "%.2f" % (sum([cash_dic[name][x] for x in range(len(cash_dic[name])) if win_dic[name][x]])/sum(win_dic[name])))
# 	else:
# 		print("Average Win:", 0)
# 	if sum(win_dic[name]) != len(win_dic[name]):
# 		print("Average Loss:", "%.2f" % (sum([cash_dic[name][x] for x in range(len(cash_dic[name])) if not win_dic[name][x]])/(len(win_dic[name])-sum(win_dic[name]))))
# 	else:
# 		print("Average Loss:", 0)

# 	print("\n")
