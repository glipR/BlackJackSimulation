
#CARD INDEXES
SUIT = 0
FACE = 1

#SUIT AND FACE ENCODINGS
SUITS = ["S", "H", "C", "D"]
FACES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

#REAL NAME MAPPINGS
SUIT_NAMES = {"S": "Spade",
			  "H": "Heart",
			  "C": "Club",
			  "D": "Diamond"}
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