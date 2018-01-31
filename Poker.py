import pygame
from pygame.locals import *
import sys
import random
import itertools
import numpy

class Player:                         #プレイヤーの情報を持つところ
    def __init__(self):
        self.num = 6
        self.hnd = []
        self.pt = 200
        self.bet = 0
        self.st = ""
        self.lst = False

    def number(self):
        return self.num

    def deal(self,card):
        self.hnd.append(card)

    def show_hand(self):
        return self.hnd

    def betting(self,bt):
        if bt>0:
            self.pt -= bt
        self.bet += bt

    def show_bet(self):
        return self.bet

    def show_point(self):
        return self.pt

    def get_point(self,bt):
        self.pt += bt

    def state(self,stt):
        self.st = stt

    def show_state(self):
        return self.st

    def last(self, tf):
        self.lst = tf

    def show_last(self):
        return self.lst
    def reset(self):
        self.hnd = []
        self.st = ""
        self.lst = False


def shuf(cards):     #カードをシャッフルする
    return random.sample(cards,len(cards))

def Best_hand(a):
    a = All_hand(a)
    if len(a)>=6:
        for i in range(6):
            if a[i][0] == "Drop":
                return a[i]
    else:
        if a[0][0] == "Drop":
                return a[0]
    while len(a) != 1:
        if power(a[0],a[1]) == "1":
            del a[0]
        elif power(a[0],a[1]) == "0":
            del a[1]
    else:
        return a[0]

def myhand(card):
    hand = {"Flush":0,"Straight":0,"Royal":0,"Four":0,"Three":0,"Two1":0,"Two2":0,"Full_House":0,"Drop":0}
    card.sort(key=lambda x:x[0])
    card.sort(key=lambda x:x[1])
    if card[0][1] == 0:
        hand["Drop"] = 1
    if card[0][0] == card[1][0]== card[2][0]== card[3][0]== card[4][0]:
        hand["Flush"] = card[0][1]
    if card[0][1] == 1 and card[1][1] == 10 and card[2][1] == 11 and card[3][1] == 12 and card[4][1] == 13:
        hand["Royal"] = card[0][1]
    if card[0][1] == card[1][1] - 1 == card[2][1] - 2 == card[3][1] - 3 == card[4][1] - 4:
        hand["Straight"] = card[4][1]
    if card[0][1] == card[1][1] == card[2][1] == card[3][1] or card[1][1] == card[2][1] == card[3][1] == card[4][1]:
        hand["Four"] = card[2][1]
    if card[0][1] == card[1][1] == card[2][1] or card[1][1] == card[2][1] == card[3][1] or card[2][1] == card[3][1] == card[4][1]:
        hand["Three"] = card[2][1]
    if card[0][1] == card[1][1] or card[1][1] == card[2][1]:
        hand["Two1"] = card[1][1]
    if card[2][1] == card[3][1] or card[3][1] == card[4][1]:
        hand["Two2"] = card[3][1]
    if card[0][1] == card[1][1] == card[2][1] and card[3][1] == card[4][1]:
        hand["Full_House"] = card[2][1]
    if card[0][1] == card[1][1] and card[2][1] == card[3][1] == card[4][1]:
        hand["Full_House"] = card[2][1]

    if hand["Drop"] == 1:
        return ["0"]
    if hand["Flush"] != 0 and hand["Royal"] != 0:
        return ["10"]
    if hand["Flush"] != 0 and hand["Straight"] != 0:
        return ["9",hand["Flush"]]
    if hand["Four"] != 0:
        return ["8",hand["Four"]]
    if hand["Full_House"] != 0:
        return ["7",hand["Full_House"]]
    if hand["Flush"] != 0 and hand["Straight"] == 0 and hand["Royal"] == 0:
        return ["6",hand["Flush"],card[4][1]]
    if hand["Flush"] == 0 and hand["Straight"] != 0:
        return ["5",hand["Straight"]]
    if hand["Flush"] == 0 and hand["Royal"] != 0: 
        return ["5",hand["Royal"]]
    if hand["Three"] != 0: #3card
        return ["4",hand["Three"]]
    if hand["Two1"] != 0 and hand["Two2"] != 0:  #2pair
        return ["3",hand["Two1"],hand["Two2"]]
    if hand["Two1"] != 0: #1apir
        return ["2",hand["Two1"]]
    if hand["Two2"] != 0: #1pair
        return ["2",hand["Two2"]]
    else:  #nopair
        return ["1",card[0][1],card[1][1],card[2][1],card[3][1],card[4][1]]

def cards_of_7(cards):
    a = list(itertools.combinations(cards,5))
    b = []
    for i in range(len(a)):
        c = list(a[i])
        b.append(c)
    return b

def All_hand(a):
    all_hand = []
    for i in range(len(list(itertools.combinations(a,5)))):
        all_hand.append(myhand(cards_of_7(a)[i]))
    return all_hand
num_hand = {"Drop":0,"Royal_Straight_Flush":10,"Straight_Flush":9,"Four_of_a_Kind":8,"Full_House":7,"Flush":6,"Straight":5,
            "Three_of_a_Kind":4,"Two_Pair":3,"Two_of_a_Kind":2,"No_Pair":1} 
num_hand_a = {"0":"Drop","10":"Royal Straight Flush","9":"Straight Flush","8":"Four of a Kind","7":"Full House","6":"Flush","5":"Straight",
            "4":"Three of a Kind","3":"Two Pair","2":"Two of a Kind","1":"No Pair"} 
def power(hand1,hand2):
    if hand1[0] == "0":
        return "1"
    if hand2[0] == "0":
        return "0"
    if hand1[0] == "10":
        return "0"
    if hand2[0] == "10":
        return "1"
    if hand1[0] == "9" and hand2[0] == "9":
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1"
    if hand1[0] == "9":
        return "0"
    if hand2[0] == "9":
        return "1"
    if hand1[0] == "8" and hand2[0] == "8":
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1"
    if hand1[0] == "8":
        return "0"
    if hand2[0] == "8":
        return "1"
    if hand1[0] == "7" and hand2[0] == "7":
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1"
    if hand1[0] == "7":
        return "0"
    if hand2[0] == "7":
        return "1"
    if hand1[0] == "6" and hand2[0] == "6":
        if hand1[1] != 1 or hand2[1] != 1:
            if hand1[1] == 1:
                return "0"
            if hand2[1] == 1:
                return "1"
        if hand1[2] >= hand2[2]:
            return "0"
        if hand1[2] < hand2[2]:
            return "1"
    if hand1[0] == "6":
        return "0"
    if hand2[0] == "6":
        return "1"
    if hand1[0] == "5" and hand2[0] == "5":
        if hand1[1] != 1 or hand2[1] != 1:
            if hand1[1] == 1:
                return "0"
            if hand2[1] == 1:
                return "1"
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1"
    if hand1[0] == "5":
        return "0"
    if hand2[0] == "5":
        return "1"
    if hand1[0] == "4" and hand2[0] == "4":
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1"
    if hand1[0] == "4":
        return "0"
    if hand2[0] == "4":
        return "1"
    if hand1[0] == "3" and hand2[0] == "3":
        if hand1[1] == 1:
            return "0"
        if hand2[1] == 1:
            return "1"
        if hand1[2] > hand2[2]:
            return "0"
        if hand1[2] < hand2[2]:
            return "1"
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1"
    if hand1[0] == "3":
        return "0"
    if hand2[0] == "3":
        return "1"
    if hand1[0] == "2" and hand2[0] == "2":
        if hand1[1] != 1 or hand2[1] != 1:
            if hand1[1] == 1:
                return "0"
            if hand2[1] == 1:
                return "1"
        if hand1[1] >= hand2[1]:
            return "0"
        if hand1[1] < hand2[1]:
            return "1" 
    if hand1[0] == "2":
        return "0"
    if hand2[0] == "2":
        return "1" 
    if hand1[1] == 1:
        return "0"   
    if hand2[1] == 1:
        return "1" 
    for i in range(4,0,-1):
        if hand1[i] > hand2[i]:
            return "0"
        if hand1[i] < hand2[i]:
            return "1"
    if hand1[0] >= hand2[0]:
        return "0"
    if hand1[0] < hand2[0]:
        return "1"

def win(a,b,c,d,e,f):
    a = Best_hand(a)
    b = Best_hand(b)
    c = Best_hand(c)
    d = Best_hand(d)
    e = Best_hand(e)
    f = Best_hand(f)
    if power(a,b) == power(a,c) == power(a,d) == power(a,e) == power(a,f) == "0":
        return [0,a[0]]
    if power(b,a) == power(b,c) == power(b,d) == power(b,e) == power(b,f) == "0":
        return [1,b[0]]
    if power(c,a) == power(c,b) == power(c,d) == power(c,e) == power(c,f) == "0":
        return [2,c[0]]
    if power(d,a) == power(d,b) == power(d,c) == power(d,e) == power(d,f) == "0":
        return [3,d[0]]
    if power(e,a) == power(e,b) == power(e,c) == power(e,d) == power(e,f) == "0":
        return [4,e[0]]
    else:
        return [5,f[0]]


def betting_turn(player_i,turn_p):                     #プレイヤーがどの行動ができるか判定する
    call_f, check_f, raise_f, bet_f = [False for i in range(4)]
    if not(player_i[turn_p].show_state()=="FOLD"):    #プレイヤーがフォールドしていないとき
        right,left = [1,1]
        while player_i[(turn_p-right+player_i[turn_p].number())%player_i[turn_p].number()].show_state() == "FOLD":  #右隣のフォールドしているプレイヤーを飛ばす
            right += 1
        while player_i[(turn_p+left)%player_i[turn_p].number()].show_state() == "FOLD":   #左隣のフォールドしているプレイヤーを飛ばす
            left += 1
        if player_i[turn_p].show_bet() == player_i[(turn_p-right+player_i[turn_p].number())%player_i[turn_p].number()].show_bet() and player_i[turn_p].show_bet() == player_i[(turn_p+left)%player_i[turn_p].number()].show_bet():    #左右のプレイヤーとベット額が同じのとき
            if player_i[turn_p].show_last():
                #次の段階へ
                return [1,1,1,1,1]
            elif right == 6:
                return [2,2,2,2,2]
            elif player_i[turn_p-right].show_bet()>0:   #ビックベットのひと
                check_f = True
                raise_f = True
            else:                                      #全員チェック
                check_f = True
                bet_f = True
        elif right == 6:
            return [2,2,2,2,2]
        else:                                          #一般
            call_f = True
            raise_f = True

    return [call_f, check_f, raise_f, bet_f, True]

def act_bet(player_i,turn_p,act_f,bet_c,t_bet):
    num = player_i[turn_p].number()
    if act_f[4] or player_i[turn_p].show_state()=="FOLD":
                    player_i[turn_p].state("FOLD")
                    print("FOLD")

    elif act_f[0]:
                    player_i[turn_p].betting(bet_c-player_i[turn_p].show_bet())
                    player_i[turn_p].state("CALL")
                    print("CALL")

    elif act_f[1]:
                    player_i[turn_p].state("CHECK")
                    player_i[turn_p].last(True)
                    print("CHECK")

    elif act_f[2]:
                    player_i[turn_p].betting(bet_c*2-player_i[turn_p].show_bet())
                    bet_c*=2
                    player_i[turn_p].state("RAISE")
                    player_i[turn_p].last(True)
                    print("RAISE")

    elif act_f[3]:
                    player_i[turn_p].betting(t_bet)
                    bet_c=t_bet
                    player_i[turn_p].state("BET")
                    player_i[turn_p].last(True)
                    print("BET")

    else:
        return [player_i,turn_p,act_f,bet_c,t_bet]
    print("BET",player_i[turn_p].show_bet(),"\n")
    turn_p = (turn_p+1)%num
    return [player_i,turn_p,act_f,bet_c,t_bet]

def bet_round(player_i,turn_p,bet_a,bet_c,game_st,bilist,betbet):
            act_flag =[False for i in range(5)]               #どの行動を選択したかを保存するところ
            player_st = betting_turn(player_i,turn_p)      #どの行動がとれるか
            if player_st == [1,1,1,1,1]:
                for i in range(player_i[0].number()):
                    bet_a += player_i[i].show_bet()
                    player_i[i].betting(-player_i[i].show_bet())
                    player_i[i].last(False)
                bet_c = 0
                game_st +=1                  #次の段階へ
                ###
                print("\nPOT",bet_a)
                print("\nNext Round\n")
                print("Community Cards")
              
                ###
            elif player_st == [2,2,2,2,2]:
                game_st = 10
            else:
                ###test
                tmp_bet=2
                if turn_p == 0:
                    if player_i[0].show_state()=="FOLD":
                        act_flag = [0,0,0,0,1]
                    else:
                        act_flag = bilist
                        if act_flag[3]:
                            tmp_bet = betbet
                else:
                    if player_i[turn_p].show_state() != "FOLD":
                        pygame.time.delay(300)
                    if len(player_i[turn_p].show_hand()) == 2: #カードが2枚の時
                        if player_i[turn_p].show_hand()[0][1] !=  player_i[turn_p].show_hand()[1][1]: #カードが異なる数字なら
                            ran = random.randint(1,100)
                            if ran <= 45:   #45%で降りる
                                if player_i[turn_p].show_state() == "RAISE":
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                                else:
                                    act_flag = [0,0,0,0,1]
                            elif ran > 90:   #10%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                else:
                                    act_flag = [0,0,1,0,0]
                            else:   #45%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                        else:   #カードが同じなら
                            ran = random.randint(1,100)
                            if ran <= 50:   #50%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                else:
                                    act_flag = [0,0,1,0,0] 
                            else:   #50%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                    #CALL,CHECK,RAISE,BET,FOLD
                    
                    elif len(player_i[turn_p].show_hand()) == 5: #カードが五枚以上の時
                        if int(myhand(player_i[turn_p].show_hand())[0]) >= 5: #ストレート以上の強さなら
                            ran = random.randint(1,100)
                            if player_i[turn_p].show_state() == "RAISE":
                                if bet_c == 0:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                            elif ran <= 60:   #60%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0] 
                            else:   #40%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                        elif int(myhand(player_i[turn_p].show_hand())[0]) == 4: #スリーカードなら
                            ran = random.randint(1,100)
                            if player_i[turn_p].show_state() == "RAISE":
                                if bet_c == 0:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                            elif ran <= 40:   #40%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0] 
                            if ran > 90:  #10%で降りる
                                act_flag = [0,0,0,0,1]
                            else:   #50%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                        elif int(myhand(player_i[turn_p].show_hand())[0]) == 3: #ツーペアの時
                            ran = random.randint(1,100)
                            if player_i[turn_p].show_state() == "RAISE":
                                if bet_c == 0:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                            elif ran <= 20:   #20%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0] 
                            elif ran > 85: #15%で降りる
                                act_flag = [0,0,0,0,1]
                            else:   #65%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                        else:
                            ran = random.randint(1,100)
                            if ran <= 5:   #5%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0]
                            elif ran > 55: #45%で降りる
                                act_flag = [0,0,0,0,1]
                            else:   #50%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]        
                    elif len(player_i[turn_p].show_hand()) >= 6: #カードが6枚以上の時
                        if int(Best_hand(player_i[turn_p].show_hand())[0]) >= 5: #ストレート以上の強さなら
                            ran = random.randint(1,100)
                            if player_i[turn_p].show_state() == "RAISE":
                                if bet_c == 0:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                            elif ran <= 60:   #60%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0] 
                            else:   #40%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                        elif int(Best_hand(player_i[turn_p].show_hand())[0]) == 4: #スリーカードなら
                            ran = random.randint(1,100)
                            if player_i[turn_p].show_state() == "RAISE":
                                if bet_c == 0:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                            elif ran <= 40:   #40%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0] 
                            if ran > 99:  #10%で降りる
                                act_flag = [0,0,0,0,1]
                            else:   #50%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                        elif int(Best_hand(player_i[turn_p].show_hand())[0]) == 3: #ツーペアなら
                            ran = random.randint(1,100)
                            if player_i[turn_p].show_state() == "RAISE":
                                if bet_c == 0:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    act_flag = [1,0,0,0,0]
                            elif ran <= 20:   #20%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0] 
                            elif ran >95: #15%で降りる
                                act_flag = [0,0,0,0,1]
                            else:   #65%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                        else:
                            ran = random.randint(1,100)
                            if ran <= 5:   #5%で上げる
                                if bet_c ==0:
                                    act_flag = [0,0,0,1,0]
                                    tmp_bet = 3
                                else:
                                    act_flag = [0,0,1,0,0]
                            elif ran > 70: #45%で降りる
                                act_flag = [0,0,0,0,1]
                            else:   #50%でそのまま
                                if player_i[turn_p].show_bet()==bet_c:
                                    act_flag = [0,1,0,0,0]
                                else:
                                    if bet_c == 0:
                                        act_flag = [0,1,0,0,0]
                                    else:
                                        act_flag = [1,0,0,0,0]
                     
                    elif bet_c ==0:
                        act_flag = [0,0,0,1,0]   #BET
                        tmp_bet = 3
                    elif player_i[turn_p].show_bet()==bet_c:
                        act_flag = [0,1,0,0,0]   #チェック
                    else:
                        act_flag = [1,0,0,0,0]   #コール
                ###
                [player_i,turn_p,act_flag,bet_c,tmp_bet] = act_bet(player_i,turn_p,act_flag,bet_c,tmp_bet)
            return [player_i,turn_p,bet_a,bet_c,game_st,player_st]

def testinput(state_list):
    act = input("action? :")
    if act == "CALL":
        state_list[0]=True
    elif act == "CHECK":
        state_list[1]=True
    elif act == "RAISE":
        state_list[2]=True
    elif act == "BET":
        state_list[3]=True
    else:
        state_list[4]=True
    return state_list

def split_image(image, dx):
    """イメージを幅dxのイメージに分割
    分割したイメージを格納したリストを返す"""
    imageList = []
    width = image.get_width()
    height = image.get_height()
    for i in range(0, width, dx):
        surface = pygame.Surface((dx,height))
        surface.blit(image, (0,0), (i,0,dx,height))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert_alpha()
        imageList.append(surface)
    return imageList
 
class Item_image(pygame.sprite.Sprite):
    def __init__(self, filename, xy, dx):
        self.x,self.y = xy
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = split_image(pygame.image.load(filename).convert(),dx)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    def update_mark(self, mk):
        if mk[0] == "s":
            self.image = self.images[1]
        elif mk[0
                ] == "h":
            self.image = self.images[2]
        elif mk[0] == "c":
            self.image = self.images[3]
        elif mk[0] == "d":
            self.image = self.images[4]
        else:
            self.image = self.images[0]
    def update_number(self, card):
            if card[0] == "s" or card[0] == "c":
                self.image = self.images[card[1]]
            elif card[0] == "h" or card[0] == "d":
                self.image = self.images[card[1]+13]
            else:
                self.image = self.images[0]
    def update_button(self,j,btn):
        if btn:
            self.image = self.images[j+1]
        else:
            self.image = self.images[0]
    def clear(self):
        self.image = self.images[0]
    def update_(self, k):
        self.image = self.images[k]


def main():
    
    pygame.init()                                   # Pygameの初期化
    screen = pygame.display.set_mode((900, 600))    # 大きさ900*600の画面を生成
    pygame.display.set_caption("Poker")              # タイトルバーに表示する文字
    
    #スプライトの作成
    card_group = pygame.sprite.RenderUpdates()
    Item_image.containers = card_group

    #表示位置の設定
    position = numpy.array([[350,420],[30,280],[30,140],[350,30],[660,140],[660,280],[290,230]])
    pos_markoff = numpy.array([16,40])
    pos_markminioff = numpy.array([4,22])
    pos_numoff = numpy.array([4,4])
    pos_cardoff = numpy.array([60,0])
    pos_textoff = numpy.array([130,10])
    pos_betoff = numpy.array([[80,-30],[230,20],[230,20],[80,90],[-40,20],[-40,20]])

    position_button = [(630,400),(740,400),(630,470),(740,470),(630,540)]
    position_plus = [(170,410),(170,490)]

    #画像を読み込んでリストに
    trumpImg = split_image(pygame.image.load("trump.png").convert(), 50)
    markImg = [Item_image("mark.png",position[i%6]+pos_markoff+pos_cardoff*(i//6),32) for i in range(12)]
    markImg += [Item_image("mark.png",position[6]+pos_markoff+pos_cardoff*i,32) for i in range(5)]
    markminiImg = [Item_image("markmini.png",position[i%6]+pos_markminioff+pos_cardoff*(i//6),16) for i in range(12)]
    markminiImg += [Item_image("markmini.png",position[6]+pos_markminioff+pos_cardoff*i,16) for i in range(5)]
    numImg = [Item_image("number.png",position[i%6]+pos_numoff+pos_cardoff*(i//6),16) for i in range(12)]
    numImg += [Item_image("number.png",position[6]+pos_numoff+pos_cardoff*i,16) for i in range(5)]
    buttonImg = [Item_image("button.png",position_button[i],90) for i in range(5)]
    backImg = pygame.image.load("back2.jpg").convert()
    windowImg = split_image(pygame.image.load("window.png").convert(),240)
    plusImg = [Item_image("plus.png",position_plus[i],40) for i in range(2)]
    plusImg[1].update_(1)
    playerwindowImg = split_image(pygame.image.load("playerwindow.png").convert(),80)
    chipImg = split_image(pygame.image.load("chip.png").convert(),15)[0]

    # フォントの作成
    sysfont = pygame.font.SysFont(None, 25)
    # テキストを描画したSurfaceを作成
    playerTextImg = [sysfont.render("Player"+str(i+1), True, (255,255,255)) for i in range(6)]
    
    #カードの表裏
    open_cards = [False for i in range(17)]

    trump = [[m,x] for m in ("s","h","c","d") for x in range(1,14)]   #トランプの生成
    Cards_deck = []                                 #山札
    Community_cards =[]                                  #オープンするカード

    START,BET1,BET2,BET3,BET4,SHOWDOWN,NEXTGAME = (0,1,2,3,4,5,6)  #ゲームの段階
    game_state = 0                                 #初期化

    playernum = 6                                  #プレイヤー人数
    player = [Player() for i in range(playernum)]        #プレイヤーの手札
    dtm = random.randint(0,5)

    buttoninputlist = [False for i in range(5)]

    window_flag = False
    next_flag = False

    bet_display = 2
    handname = 100
    

    while (1):

        if game_state == START:
            Cards_deck = shuf(trump)    #山札をシャッフル
            for i in range(playernum*2+5):
                if i < playernum*2:
                    player[i%playernum].deal(Cards_deck[i])     #プレイヤーに2枚ずつ手札を配る
                else:
                    Community_cards.append(Cards_deck[i])             #オープンするホールカード5枚を決定

            player[dtm].betting(1)           #スモールブラインド
            player[dtm].state("SB")
            player[(dtm+1)%player[0].number()].betting(2)         #ビックブラインド
            player[(dtm+1)%player[0].number()].state("BB")
            player[(dtm+2)%player[0].number()].last(True)
            turn_cur = (dtm+2)%player[0].number()            #現在の手番を決定
            game_state = BET1           #次の段階へ
            bet_cur = 2                 #現在のベット額
            bet_all = 0                 #ベットの合計
            for i in range(0,12,6):
                open_cards[i]=True
            player_state=[False for i in range(5)]
            ###
            print("Your hand\n",player[0].show_hand(),"\n")
            print("Player",dtm+1,"\nSB\nBET 1\n")
            print("Player",(dtm+1)%6+1,"\nBB\nBET 2\n")
            ###

        elif game_state == BET1:
            player,turn_cur,bet_all,bet_cur,game_state,player_state=bet_round(player,turn_cur,bet_all,bet_cur,game_state,buttoninputlist,bet_display)
            buttoninputlist = [False for i in range(5)]
            if game_state == BET2:
                for i in range(3):
                    open_cards[i+12]=True
                print(Community_cards[0],Community_cards[1],Community_cards[2])

        elif game_state==BET2:
            player,turn_cur,bet_all,bet_cur,game_state,player_state=bet_round(player,turn_cur,bet_all,bet_cur,game_state,buttoninputlist,bet_display)
            buttoninputlist = [False for i in range(5)]
            if game_state == BET3:
                open_cards[15]=True
                print(Community_cards[0],Community_cards[1],Community_cards[2],Community_cards[3])

        elif game_state == BET3:
            player,turn_cur,bet_all,bet_cur,game_state,player_state=bet_round(player,turn_cur,bet_all,bet_cur,game_state,buttoninputlist,bet_display)
            buttoninputlist = [False for i in range(5)]
            if game_state == BET4:
                open_cards[16]=True
                print(Community_cards)

        elif game_state == BET4:
            player,turn_cur,bet_all,bet_cur,game_state,player_state=bet_round(player,turn_cur,bet_all,bet_cur,game_state,buttoninputlist,bet_display)
            buttoninputlist = [False for i in range(5)]

        elif game_state == SHOWDOWN:
            for i in range(6):
                if not player[i].show_state() == "FOLD":
                    if i==0:
                        print("YOU",player[i].show_hand())
                    else:
                        print("Player",i+1,player[i].show_hand())
                        for j in range(i,12,6):
                            open_cards[j]=True

            droper = [["x",0] for i in range(7)]
            hans = [[] for i in range(6)]
            for i in range(6):
                if player[i].show_state()=="FOLD":
                    hans[i] = droper
                else:
                    hans[i] = player[i].show_hand() + Community_cards
            winner,handname = win(hans[0],hans[1],hans[2],hans[3],hans[4],hans[5])
            print("Winner is Player",winner+1)
            print("Get",bet_all,"Points!")
            player[winner].get_point(bet_all)
            game_state=NEXTGAME

        elif game_state == NEXTGAME:
            window_flag = True
            if next_flag:
                for i in range(6):
                    player[i].reset()
                Community_cards = []
                dtm = (dtm+1)%6
                open_cards = [False for i in range(17)]
                window_flag = False
                next_flag = False
                handname = 100
                game_state = START

        elif game_state == 10:
            winner = turn_cur
            player[winner].get_point(bet_all)
            game_state = NEXTGAME
        
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()
            # マウスクリックされたボタンを検知
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                player_state
                for i in range(5):
                        bx = x - position_button[i][0]
                        by = y - position_button[i][1]
                        if bx>0 and bx<90 and by>0 and by<50 and player_state[i]:
                                buttoninputlist = [j==i for j in range(5)]
                if window_flag:
                    if x>115 and x<210 and y>505 and y<540:
                        next_flag = True
                if x>170 and x<210 and y>410 and y<430:
                    bet_display+=1
                if x>170 and x<210 and y>490 and y<510:
                    if bet_display >=3:
                        bet_display-=1
        if turn_cur==0:
            for i in range(5):
                buttonImg[i].update_button(i,player_state[i])

        #画像の描画
        screen.fill((0,0,0))        # 画面を黒色(#000000)に塗りつぶし
        screen.blit(backImg,(0,0))
        for i in range(12):
            if open_cards[i]:
                screen.blit(trumpImg[2],position[i%6]+pos_cardoff*(i//6))
                markImg[i].update_mark(Cards_deck[i])
                markminiImg[i].update_mark(Cards_deck[i])
                numImg[i].update_number(Cards_deck[i])
            else:
                markImg[i].clear()
                markminiImg[i].clear()
                numImg[i].clear()
                screen.blit(trumpImg[1],position[i%6]+pos_cardoff*(i//6))
            if i < 6:
                if i==turn_cur:
                    screen.blit(playerwindowImg[1],position[i]+(120,0))
                else:
                    screen.blit(playerwindowImg[0],position[i]+(120,0))
                screen.blit(playerTextImg[i],(position[i]+pos_textoff))
                stateTextImg = [sysfont.render(str(player[j].show_state()), True, (255,255,255)) for j in range(6)]
                screen.blit(stateTextImg[i],(position[i]+pos_textoff+(0,20)))
                pointTextImg = [sysfont.render(str(player[j].show_point()), True, (255,255,255)) for j in range(6)]
                screen.blit(pointTextImg[i],(position[i]+pos_textoff+(0,40)))
                betTextImg = [sysfont.render(str(player[j].show_bet()), True, (255,255,255)) for j in range(6)]
                if player[i].show_bet()>0:
                    screen.blit(betTextImg[i],position[i]+pos_betoff[i])
                    screen.blit(chipImg,position[i]+pos_betoff[i]+(-20,0))
        for i in range(12,17):
            if open_cards[i]:
                screen.blit(trumpImg[2],position[6]+pos_cardoff*(i-12))
                markImg[i].update_mark(Cards_deck[i])
                markminiImg[i].update_mark(Cards_deck[i])
                numImg[i].update_number(Cards_deck[i])
            else:
                markImg[i].clear()
                markminiImg[i].clear()
                numImg[i].clear()
                screen.blit(trumpImg[1],position[6]+pos_cardoff*(i-12))

        card_group.draw(screen)
        pottextImg = sysfont.render("POT     "+str(bet_all), True, (255,255,255))
        betdisplayImg = sysfont.render(str(bet_display), True, (255,255,255))
        screen.blit(pottextImg,(400,160))
        screen.blit(betdisplayImg,(180,450))
        screen.blit(chipImg,(440,160))
        if window_flag:
            screen.blit(windowImg[0],(40,400))
            winmsgImg = sysfont.render("Winner is Player"+str(winner+1), True, (255,255,255))
            screen.blit(winmsgImg,(90,440))
            if not handname == 100:
                handTextImg = sysfont.render(num_hand_a[str(handname)], True, (255,255,255))
                screen.blit(handTextImg,(130,470))
        pygame.display.update()     # 画面を更新
        

if __name__ == "__main__":
    main()