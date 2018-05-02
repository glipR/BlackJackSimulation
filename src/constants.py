
#CARD INDEXES
SUIT = 0
FACE = 1
VIS = 2

#SUIT AND FACE ENCODINGS
SUITS = ["S", "H", "D", "C"]
FACES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

#SUIT HIERARCHY
SUIT_SCORE = {"S":1,
			  "H":2,
			  "D":3,
			  "C":4}

FACE_SCORE = {"A": 1,
			  "K": 2,
			  "Q": 3,
			  "J": 4,
			  "T": 5,
			  "9": 6,
			  "8": 7,
			  "7": 8,
			  "6": 9,
			  "5":10,
			  "4":11,
			  "3":12,
			  "2":13}

#REAL NAME MAPPINGS
SUIT_NAMES = {"S": "Spade",
			  "H": "Heart",
			  "D": "Diamond",
			  "C": "Club"}

FACE_NAMES = {"A": "Ace",
			  "2": "Two",
			  "3": "Three",
			  "4": "Four",
			  "5": "Five",
			  "6": "Six",
			  "7": "Seven",
			  "8": "Eight",
			  "9": "Nine",
			  "T": "Ten",
			  "J": "Jack",
			  "Q": "Queen",
			  "K": "King"}

#PLAYING RESPONSES
HIT = 0
DONE = 1
FOLD = 2

GOOD = 0
OVER = 1

#BETTING RESPONSES
FOLD = 0
FOLLOW = 1
RAISE = 2
STAND = 3

#MINIMUM VALUES
MIN_VALUE = {"A": 1,
			 "2": 2,
			 "3": 3,
			 "4": 4,
			 "5": 5,
			 "6": 6,
			 "7": 7,
			 "9": 9,
			 "8": 8,
			 "T":10,
			 "J":10,
			 "Q":10,
			 "K":10}


def cardDescription(card):
	return FACE_NAMES[card[FACE]] + " of " + SUIT_NAMES[card[SUIT]] + "s"

def compareHighCard(card1, card2):
	"""
	Compares two cards, and returns which is the highest
	:param card1: card1
	:param card2: card2
	:return: 0 if card1, 1 if card2
	"""
	if FACE_SCORE[card1[FACE]] < FACE_SCORE[card2[FACE]]:
		return 0
	elif FACE_SCORE[card1[FACE]] > FACE_SCORE[card2[FACE]]:
		return 1
	else:
		if SUIT_SCORE[card1[SUIT]] < SUIT_SCORE[card2[SUIT]]:
			return 0
		else:
			return 1