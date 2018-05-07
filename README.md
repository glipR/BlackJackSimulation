# Welcome!

## What is the project?

To implement (and simulate) the process of playing Blackjack, as well as strategies surrounding it

## How to run?

To run the simulation run the following in command line in `src` directory:

`python3 Game.py`

To change the settings of the simulation, change the contents of `Game.py`

## How does it work?

The code base is partmentalised into multiple independently moving parts, so as to assist the design process:

1. `constants.py` - Multiple constants which are used by nearly all classes
	* Face names and values
	* Suit names and ordering
	* Response codes for dealing and betting
	* Card description for verbose output
2. `Game.py` - Dedicated to the control flow of the game blackjack.
	* Deals cards
	* Facilitates Bets
	* Stores all information
3. `Deck.py` - Simple implementation of what a normal deck in blackjack is.
	* Get a random card (With or without replacement)
	* Reset the deck to its original state
4. `GameState.py` - Container for the board information, queried by `Player`s when deciding bet and hit responses.
	* Stores the current bets, as well as all hands
	* Can be queried for things like highest bet
5. `Hand.py` - Holds all the cards in a hand, to be used by Players.
	* Can be queried if the hand is valid
	* Finding the highest card in a hand
	* The current score of the hand
6. `Player.py` - Majority of the AI implementation, Handles every a player would in a normal game
	* Stores the players hands and betting money
	* Can be queried for a dealing or betting response, dependent on the current game state

As such, any new implementation of player AI should extend the class `Player.py`

## TODO

Version 0.1

* Separate `Player.py` into its generic definition and the default AI, called `Default.py`
* Change how card comparison works in `Game.py` to better represent how BlackJack works
* Add functionality for splitting, implemented by the `Player` class