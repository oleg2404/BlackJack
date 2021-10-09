'''
Created on 26 Sep 2021

@author: Oleg Ovroutsky
'''
import random

#Initiallize the card deck
Hearts = {"A":(11,1),"K":10,"Q":10,"J":10,"10":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
Spades = {"A":(11,1),"K":10,"Q":10,"J":10,"10":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
Diamonds = {"A":(11,1),"K":10,"Q":10,"J":10,"10":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
Pikes = {"A":(11,1),"K":10,"Q":10,"J":10,"10":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
deck = {"Hearts":Hearts,"Spades":Spades,"Diamonds":Diamonds,"Pikes":Pikes}


class Player:
    """
    Created a Player class with constructors:
        :score: return the sum of player`s cards
        :bet: moves amount of chips from player to pot
        :hit: take another card action
    """
    def __init__(self,name,cards = [],balance = 500,):
        self.name = name
        self.balance = balance
        self.cards = cards
    
    def score(self):
        return check_sum(self.cards)
    
    def bet(self,_bet,_pot):
        if self.balance >= _bet and self.balance != 0:
            _pot.take_bet(_bet)
            self.balance -= _bet
        else:
            return False
    
    def hit(self):
        self.cards.append(draw())
    
class Pot:
    """ Pot class to keep the chips until a win or draw:
    
        :take_bet: place a bet.
        :pay_to: transfers chips to the winer or spliting when draw.
         """
         
    def __init__(self,balance = 0):
        self.balance = balance
    
    def take_bet(self,bet):
        self.balance += bet
    def pay_to(self,winner,player_1,computer,_pot):
        if winner == "draw":
            player_1.balance += (_pot.balance/2)
            computer.balance += (_pot.balance/2)
            self.balance = 0
        else:
            winner.balance += self.balance
            self.balance = 0
        

def draw():
    personal_deck = []
    personal_deck.append(from_deck())
    return personal_deck[0]
        
def from_deck():
    kind = random.choice(list(deck.keys()))
    kind_deck = deck[f"{kind}"]
    random_card = random.choice(list(kind_deck))
    deck[f"{kind}"].pop(random_card)
    return random_card

def check_sum(hand):
    cards2 = move_ace(hand)
    sum_all = 0
    for x in cards2:
        if x == "K" or x == "J" or x == "Q":
            sum_all += 10
        if x == "A":
            if (sum_all + 11) > 21:
                sum_all += 1
            else:
                sum_all += 11
        else:
            try:
                sum_all += int(x)
            except:
                pass
    return sum_all

def move_ace(hand):
    new_list = []
    cards2 = list(hand)
    for x in cards2:
        if x == "A":
            cards2.remove("A")
            cards2.append("A")
    return cards2

def burn(hand):
    return check_sum(hand) > 21
    
def hit_stand():
    while True:
        answer = input("Would you like to Hit or Stand?")
        if answer[0].upper() == "H":
            return "H"
            break
        if answer[0].upper() == "S":
            return "S"
            break
        else:
            continue
            
def check_start_win(player_hand,computer_hand):
    if check_sum(player_hand) == 21:
        if check_sum(computer_hand) == 21:
            return 0
        return 1
    if check_sum(computer_hand) == 21:
        return -1
    return 2
def first_step(player_1,computer,_pot):
    while True:
        try:
            first_bet = int(input(f"Please place bet, available funds: {player_1.balance}"))
        except:
            
            continue
        else:
            if first_bet > player_1.balance:
                continue
            else:
                break
    player_1.bet(first_bet,_pot)
    computer.bet(first_bet,_pot)
    

def play_game(player_1,computer,_pot,deck):
    _pot = _pot
    player_1.cards = []
    computer.cards = []
    player_1.hit()
    player_1.hit()
    computer.hit()
    computer.hit()
    game_status = "on"
    player_turn = True

    def com_print(computer,boolean):
        hidden_hand = ["XX"]
        if boolean:
            for x in computer.cards:
                hidden_hand.append(x)
            hidden_hand.remove(computer.cards[1])
            return hidden_hand
        else:
            return computer.cards

    def board(boolean):
        if boolean == True:
            print(f"Dealer:        {com_print(computer,True)}")
            print(f"\n\n\n\n")
            print(f"{player_1.name}:              {player_1.cards}")
            print(f"Chips: {player_1.balance}            Total: {player_1.score()}        Pot:{_pot.balance}")
        else:
            print(f"Dealer:        {com_print(computer,False)}")
            print(f"\n\n\n\n")
            print(f"{player_1.name}:              {player_1.cards}")
            print(f"Chips: {player_1.balance}            Total: {player_1.score()}        Pot:{_pot.balance}")

    while game_status == "on": 

        first_step(player_1,computer,_pot)
        board(True)
        
        if check_start_win(player_1.cards,computer.cards) == -1:
            _pot.pay_to(computer,player_1,computer,_pot)
            game_status = "computer won"
            break
        if check_start_win(player_1.cards,computer.cards) == 1:
            _pot.pay_to(player_1,player_1,computer,_pot)
            game_status = "player won"
            break
        if check_start_win(player_1.cards,computer.cards) == 0:
            _pot.pay_to("draw",player_1,computer,_pot)
            game_status = "draw"
            break
        else:
          
            while player_turn:
                answer = hit_stand()
                if answer == "S":
                    player_turn = False
                    break
                if answer == "H":
                    player_1.hit()
                    board(True)
                    if burn(player_1.cards):
                        game_status = "computer won"
                        _pot.pay_to(computer,player_1,computer,_pot)
                        print("You burned out!")
                        break
            while player_turn == False:
              
                board(True)
                while True:
                    if check_sum(computer.cards) <=15:
                        computer.hit()
                        continue
                    else:
                        if burn(computer.cards):
                            game_status = "player won"
                            _pot.pay_to(player_1,player_1,computer,_pot)
                            break
                        if check_sum(player_1.cards) > check_sum(computer.cards):
                            _pot.pay_to(player_1,player_1,computer,_pot)
                            game_status = "player won"
                            break
                        if check_sum(player_1.cards) < check_sum(computer.cards):
                            _pot.pay_to(computer,player_1,computer,_pot)
                            game_status = "computer won"
                            break
                        if check_sum(player_1.cards) == check_sum(computer.cards):
                            _pot.pay_to("draw",player_1,computer,_pot)
                            game_status = "draw"
                            break
                   
                    break
                break
            
        if game_status == "computer won":
            print("Computer won1")
        if game_status == "player won":
            print("Player won1")
        if game_status == "draw":
            print("Draw ")

        while True:
            board(False)
            try:
                inp = input("play again?Y/N")
            except:
                continue
            else:
                if inp[0].upper() == "Y":
                    game_status = "on"
                    player_turn = True
                    play_game(player_1,computer,_pot,deck)
                else:
                    break
                break
      
    print("bye")
    
def play():
    _pot = Pot()
    human_player = Player(name = input("Player name:"),cards = [],balance = 500)
    computer_player = Player(name = "Computer",cards = [],balance = 999999)
    play_game(human_player,computer_player,_pot,deck)    
    
play()
