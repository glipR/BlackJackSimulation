from constants import *
from GenericPlayer import *


class SimpleBully(GenericPlayer):
    def hitResponse(self, hand, state):
        #simple bully never hits, either it has something it
        #can bulshit with or he surrenders
        #this call should never be called
        return DONE	

    def betResponse(self, hand, state):
        #simple bully will always bet more when it can
        if state.cur_bet() > hand.cur_bet:
            return FOLLOW
        else:
            return RAISE


    def surrenderResponse(self, state):
        if self.hands[0].cards[self.hands[0].cards[1][VIS]][FACE] not in ["A","J","Q","K","T"]:
            return True
        return False

    def splitResponse(self, state):
        #two K/Q/T is a strong hand
        #no point in splitting unless you can get a scarier hand
        #2 split aces is the scariest hand
        #if the bot is persistant with two J and does not draw more,
        #it is a fair assumption that it has 21, given two cards, it is the strongest 21
        if self.hands[0].canSplit() and self.hands[0].cards[0][FACE] in ["A","J"]:
            return True
        return False

class OpenMindedBully(GenericPlayer):
    def hitResponse(self, hand, state):
        v=hand.score()
        if hand.cards[hand.cards[1][VIS]][FACE] not in ["A","J","Q","K","T"]:
            if v<12:
                return HIT
        return DONE	

    def betResponse(self, hand, state):
        #bully will always bet more when it can
        if state.cur_bet() > hand.cur_bet:
            return FOLLOW
        else:
            return RAISE


    def surrenderResponse(self, state):
        if self.hands[0].cards[self.hands[0].cards[1][VIS]][FACE] in ["A","J","Q","K","T"]:
            return False
        if self.hands[0].score()<12 and int(self.hands[0].cards[self.hands[0].cards[1][VIS]][FACE]) > 6:
            return False
        return True

    def splitResponse(self, state):
        if self.hands[0].canSplit() and self.hands[0].cards[0] not in ["T","K","Q","5","6","7","8","9"]:
            return True
        return False

class Calculator(GenericPlayer):
    def bust2(self,num):
        if num > 21:
            return 21
        else:
            return num-1
        
    def getSurrounding(self,state):
        visible={}
        total=0
        for i in FACES:
            visible[i]=0

        otherHands = state.getHandsExcluding(self.name)
        for hand in otherHands:
            visible[hand.cards[hand.cards[1][VIS]][FACE]]+=1
            total+=1
            for i in range(2,len(hand)):
                visible[hand.cards[i][FACE]]+=1
                total+=1
        for hand in self.hands:
            for card in hand.cards:
                total+=1
                visible[card[FACE]] += 1

        for key in visible.keys():
            visible[key]=4-visible[key]
        return [total,visible]
    
    def info(self,state):
        temp = self.getSurrounding(state)
        total = temp[0]
        visible = temp[1]
        current = self.hands[0].score()
        pool = 22*[0]
        for key in visible.keys():
            if key != 'A':
                after = current + MIN_VALUE[key]
                pool[self.bust2(after)] += 4-visible[key]
            else:
                pool[self.bust2(current+1)] += 2 - 0.5 * visible[key]
                pool[self.bust2(current+11)] += 2 - 0.5 * visible[key]                         

        otherHands = state.getHandsExcluding(self.name)
        others = len(otherHands)*[0]
        for i in range(len(otherHands)):
            others[i] = 22*[0]
        
        for hand in range(len(others)):
            for key in visible:
                count_aces = 0
                card_sum = 0
                for card in otherHands[hand].cards:
                    if card[VIS] != 0:
                        if card[FACE] == "A":
                            count_aces += 1
                        card_sum += MIN_VALUE[card[FACE]]
                for _ in range(count_aces):
                    if card_sum < 12:
                        card_sum += 10
                if key != 'A':
                    after = card_sum + MIN_VALUE[key]
                    others[hand][self.bust2(after)] += 4-visible[key]
                else:
                    others[hand][self.bust2(card_sum+1)] += 2 - 0.5 * visible[key]
                    others[hand][self.bust2(card_sum+11)] += 2 - 0.5 * visible[key]

        prWin = 0
        for i in range(1,21):
            mult = 1
            for item in others:
                mult *= sum(item[:i])+item[21]
            mult *= pool[i]
            mult /= total ** (len(others)+1)
            prWin += mult

        return prWin
    
    def hitResponse(self, hand, state):
        if hand.score() > 18:
            return DONE

        
        count_aces = 0
        card_sum = 0
        for hand in self.hands:
            for card in hand.cards:
                if card[FACE] == "A":
                    count_aces += 1
                card_sum += MIN_VALUE[card[FACE]]
        temp = self.getSurrounding(state)
        busts = 0
        for key in temp[1].keys():
            if MIN_VALUE[key] + card_sum>21:
                busts += temp[1][key]

        if busts/temp[0]>0.3:
            return DONE
        return HIT

    def betResponse(self, hand, state):
        i = self.info(state)
        if state.cur_bet() > hand.cur_bet:
            if i > 0.10:
                return FOLLOW
            return FOLD
            
        else:
            if i > 0.1:
                return RAISE
            return FOLLOW


    def surrenderResponse(self, state):
        if self.info(state) < 0.05:
            return True
        return False

    

    def splitResponse(self, state):
        return False
        
    

class LuckyDisciple(GenericPlayer):
    def table2(self):
        table = open("table.txt").readlines()
        for i in range(21):
            table[i] = table[i][:-1].split('	')
        return table
    
    def hitResponse(self, hand, state):
        table = self.table2()
        scores = hand.score()
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'h' in table[scores-1][MIN_VALUE[card]-1].lower():
                return HIT  
        return DONE	

    def betResponse(self, hand, state):
        table = self.table2()
        scores = hand.score()
        flag=True
        flag2=True
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'SU' != table[scores-1][MIN_VALUE[card]-1]:
                flag=False
            if 'D' in table[scores-1][MIN_VALUE[card]-1]:
                flag2=False

        if flag:
            return FOLD
    
        if state.cur_bet() > hand.cur_bet:
            return FOLLOW
        else:
            if not flag2:
                return RAISE
            return FOLLOW


    def surrenderResponse(self, state):
        table = self.table2()
        scores = self.hands[0].score()
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'SU' not in table[scores-1][MIN_VALUE[card]-1]:
                return False  
        return True

    def splitResponse(self, state):
        
        table = self.table2()
        if not self.hands[0].canSplit():
            return False
        table3 = open("split.txt").readlines()
        for i in range(10):
            table3[i] = table3[i][:-1].split('\t')
        
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'SP' in table3[hand.score()//2-1][MIN_VALUE[card]-1]:
                return True
        return False

class UnluckyDisciple(GenericPlayer):
    def table2(self):
        table = open("table.txt").readlines()
        for i in range(21):
            table[i] = table[i][:-1].split('\t')
        return table
    
    def hitResponse(self, hand, state):
        table = self.table2()
        scores = hand.score()
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'h' not in table[scores-1][MIN_VALUE[card]-1].lower():
                return DONE  
        return HIT	

    def betResponse(self, hand, state):
        table = self.table2()
        #simple bully will always bet more when it can
        scores = hand.score()
        flag2=True
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'SU' == table[scores-1][MIN_VALUE[card]-1]:
                return FOLD
            if 'D' not in table[scores-1][MIN_VALUE[card]-1]:
                flag2=False
    
        
        if state.cur_bet() > hand.cur_bet:
            return FOLLOW
        else:
            if flag2:
                return RAISE
            return FOLLOW


    def surrenderResponse(self, state):
        table = self.table2()
        scores = self.hands[0].score()
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'SU' in table[scores-1][MIN_VALUE[card]-1].lower():
                return True  
        return False

    def splitResponse(self, state):
        table = self.table2()
        if not self.hands[0].canSplit():
            return False
        table3 = open("split.txt").readlines()
        for i in range(10):
            table3[i] = table3[i][:-1].split('\t')
        
        for hand in state.getHandsExcluding(self.name):
            card = hand.cards[hand.cards[1][VIS]][FACE]
            if 'SP' not in table3[hand.score()//2-1][MIN_VALUE[card]-1]:
                return False
        return True
