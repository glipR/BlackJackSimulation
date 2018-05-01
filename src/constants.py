
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

def cardDescription(card):
	return FACE_NAMES[card[FACE]] + " of " + SUIT_NAMES[card[SUIT]] + "s"