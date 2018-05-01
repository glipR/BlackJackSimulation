SUIT = 0
FACE = 1

SUITS = ["S", "H", "C", "D"]
FACES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

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

def cardDescription(card):
	return FACE_NAMES[card[FACE]] + " of " + SUIT_NAMES[card[SUIT]] + "s"