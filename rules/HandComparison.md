# Hand Comparison

#### Implemented By:
`Game.py`

## Rules

### 1. Score Split

First, find the maximum score of all hands, and remove all hands which score is not equal to this

#### Example
> Hands: [AH, 6D], [TS, 9H], [7C, 8D, 4S]
>
> Scores: 17, 19, 19
>
> Remaining Hands: [TS, 9H], [7C, 8D, 4S] with score 19

### 2. Blackjack

If any of the hands are blackjack (Jack + Ace), they instantly win

If not, if any of the hands are 2-card 21, they instantly win

#### Example
> Hands: [JD, AS], [KH, AC], [TH, QC, AD], [JH, AH]
> 
> Scores: 21, 21, 21, 21
>
> Winners: [JD, AS], [JH, AH]

### 3. 5-Card

If no winners are selected so far and there is a hand with 5 cards present, they win

#### Example
> Hands: [3H, 5S, 2C, 8D, AS], [10H, 9C], [AD, 8C]
>
> Scores: 19, 19, 19
>
> Winner: [3H, 5S, 2C, 8D, AS]

### 4. End

If there are no winner cards yet, all remaining cards are winners

#### Example
> Hands: [2H, TS, 7H], [8H, 4C, AC, 2C, AS, 2S], [4D, KD, 2D, 3H]
>
> Scores: 19, 18, 19
>
> Hands After Rule 1: [2H, TS, 7H], [4D, KD, 2D, 3H]
>
> No blackjacks or 5 cards
>
> Winners: [2H, TS, 7H], [4D, KD, 2D, 3H]