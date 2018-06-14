from constants import *
from Game import *
import copy


#This test checks for cases where the board is overwhelmingly of a single strategy.

class Test(Game):

	def __init__(self):
		self.iter = 1000

	def simulateReset(self):
		final = []
		comb = generate(5)
		i = 0
		for array in comb:
			#print(f"Testing, {i}/{len(comb)} completed.")
			i += 1
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

## Changed from permutations to 4vs1 permutations
def generate(n):
	tmp = []
	for x in range(n):
		for y in range(n):
			if x != y:
				for z in range(n):
					tmp2 = [x]*n
					tmp2[z] = y
					tmp.append(tmp2)
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
	names = [p.name for p in match[0][1]]
	set_names = list(set(names))
	assert len(set_names) == 2, "Should be exactly 2 distinct bots"

	alone = set_names[0] if names.count(set_names[0]) == 1 else set_names[1]
	group = set_names[1] if names.count(set_names[0]) == 1 else set_names[0]
	for player in match[0][1]:
		if player.name == alone:
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
			## NAME, ORDER, WIN%, TOTAL_WINNINGS, AVG_WIN, AVG_LOSS, GROUP_AGAINST
			print(",".join([player.name, str(match[0][1].index(player)), "%.2f" % win_percent, "%.2f" % total_winnings, "%.2f" % average_win, "%.2f" % average_loss, group]))
