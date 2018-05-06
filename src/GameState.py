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
        return max(self.players, key = lambda x: x.cur_bet).cur_bet
