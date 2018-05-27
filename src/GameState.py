from constants import *


class gameState:
    def __init__(self):
        self.players = []

    def reset(self):
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)

    def getHandsExcluding(self, player):
        hands = []
        for player1 in self.players:
            if player1 != player:
                hands = hands + player1.hands
        return hands

    def getPlayersExcluding(self, player):
        tmp_players = []
        for player1 in self.players:
            if player1 != player:
                tmp_players.append(player1)
        return tmp_players

    def getBetsExcluding(self, player):
        bets = []
        for player1 in self.players:
            if player1 != player:
                bets.append([player1.cur_bet, player1.cash+player1.cur_bet])
        return bets

    def cur_bet(self):
        all_bets = []
        for player in self.players:
            for hand in player.hands:
                all_bets.append(hand.cur_bet)
        return max(all_bets)

    def printState(self, to):
        bets = []
        hands = []
        name = []
        for player in self.players:
            for hand in player.hands:
                bets.append(str(hand.cur_bet))
                hands.append(hand.knownHand() if player != to else "".join([card[FACE] for card in hand.cards]))
                name.append(player.name if player != to else "YOU")
        return  "Bet: \t" + "\t".join(bets) + "\n" + "Hand:\t" + "\t".join(hands) + "\n" + "Name:\t" + "\t".join(name)

    def players_alive(self):
        inc = 0
        for player in self.players:
            if not player.dead:
                if len(player.hands) > 0:
                    inc += 1
        return inc
