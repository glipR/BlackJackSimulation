from GenericPlayer import *

class HumanPlayer(GenericPlayer):

	def hitResponse(self, hand, state):
		print(state.printState(self))
		while True:
			x = input("1: HIT, 2: DONE")
			try:
				if int(x) == 1:
					return HIT
				elif int(x) == 2:
					return DONE
			except:
				continue
		

	def betResponse(self, hand, state):
		board_bet = state.cur_bet()
		if board_bet > hand.cur_bet:
			print(state.printState(self))
			while True:
				x = input("1: FOLLOW, 2: FOLD")
				try:
					if int(x) == 1:
						return FOLLOW
					elif int(x) == 2:
						return FOLD
				except:
					continue
		else:
			print(state.printState(self))
			while True:
				x = input("1: RAISE, 2: STAND")
				try:
					if int(x) == 1:
						return RAISE
					elif int(x) == 2:
						return STAND
				except:
					continue

	def surrenderResponse(self, state):
		print(state.printState(self))
		result = ""
		while not(result.lower() in ["y", "n"]):
			result = input("Would you like to surrender? (Y/N): ")
		return True if result=="y" else False

	def splitResponse(self, state):
		if self.hands[0].canSplit():
			print(state.printState(self))
			result = ""
			while not(result.lower() in ["y", "n"]):
				result = input("Would you like to split? (Y/N): ")
			return True if result=="y" else False
		return False