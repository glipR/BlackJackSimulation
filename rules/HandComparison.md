# Hand Comparison

#### Implemented By:
`Game.py`

## Rules

### 1. Blackjack

If any hand is a blackjack (Jack + Ace), they win the round by default

> Hands: [KS, AC], [AS, JC], [QD, 5H, 6S], [JH, AD]
>
> Blackjack: No, Yes, No, Yes
>
> Winning Hands: [AS, JC], [JH, AD]

### 2. 21

If no blackjack, then any hand which scores 21 wins

### 3. 5 Card

If noone has a 21 of any card, but someone has a hand with 5-cards which is not busted, then they win.

> Hands: [AS, 4H, 5D], [3C, 2H, 6D, AC, 3S]
>
> Scores: 20, 15
>
> Winning Hand: [3C, 2H, 6D, AC, 3S]

### 4. Numeric

If none of these rules are met by a single hand, then all cards with the highest numeric score win.