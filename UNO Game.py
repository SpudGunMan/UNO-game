import random
import time


color = ('RED','GREEN','BLUE','YELLOW')
rank = ('0','1','2','3','4','5','6','7','8','9','Skip','Reverse','Draw2','Draw4','Wild')
ctype = {'0':'number','1':'number','2':'number','3':'number','4':'number','5':'number','6':'number',
            '7':'number','8':'number','9':'number','Skip':'action','Reverse':'action','Draw2':'action',
            'Draw4':'action_nocolor','Wild':'action_nocolor'}

class Card:

    def __init__(self, color, rank):
        self.rank = rank
        if ctype[rank] == 'number':
            self.color = color
            self.cardtype = 'number'
        elif ctype[rank] == 'action':
            self.color = color
            self.cardtype = 'action'
        else:
            self.color = None
            self.cardtype = 'action_nocolor'

    def __str__(self):
        if self.color == None:
            return self.rank
        else:
            return self.color + " " + self.rank


class Deck:

    def __init__(self):
        self.deck = []
        for clr in color:
            for ran in rank:
                if ctype[ran] != 'action_nocolor':
                    self.deck.append(Card(clr, ran))
                    self.deck.append(Card(clr, ran))
                else:
                    self.deck.append(Card(clr, ran))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.cards = []
        self.cardsstr = []
        self.number_cards = 0
        self.action_cards = 0

    def add_card(self, card):
        self.cards.append(card)
        self.cardsstr.append(str(card))
        if card.cardtype == 'number':
            self.number_cards += 1
        else:
            self.action_cards += 1

    def remove_card(self, place):
        self.cardsstr.pop(place - 1)
        return self.cards.pop(place - 1)

    def cards_in_hand(self):
        for i in range(len(self.cardsstr)):
            print(f' {i + 1}.{self.cardsstr[i]}')

    def single_card(self, place):
        return self.cards[place - 1]

    def no_of_cards(self):
        return len(self.cards)


#Funciton to randomly select who starts first
def choose_first():
    if random.randint(0,1)==0:
        return 'Player'
    else:
        return 'Pc'


#Function to check if the card thrown by Player/PC is a valid card by comparing it with the top card
def single_card_check(top_card,card):
    if card.color==top_card.color or top_card.rank==card.rank or card.cardtype=='action_nocolor':
        return True
    else:
        return False


#FOR PC ONLY
#To check if PC has any valid card to throw 
def full_hand_check(hand,top_card):
    for c in hand.cards:
        if c.color==top_card.color or c.rank == top_card.rank or c.cardtype=='action_nocolor':
            return hand.remove_card(hand.cardsstr.index(str(c))+1)
    else:
        return 'no card'


#Function to check if either wins
def win_check(hand):
    if len(hand.cards)==0:
        return True
    else:
        return False


#Function to check if last card is an action card (GAME MUST END WITH A NUMBER CARD)
def last_card_check(hand):
    for c in hand.cards:
        if c.cardtype!='number':
            return True
        else:
            return False


#The gaming loop
while True:

    print('Welcome to UNO! Finish your cards first to win')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    for i in range(7):
        player_hand.add_card(deck.deal())

    pc_hand = Hand()
    for i in range(7):
        pc_hand.add_card(deck.deal())

    top_card = deck.deal()
    if top_card.cardtype != 'number':
        while top_card.cardtype != 'number':
            top_card = deck.deal()
    print('\nStarting Card is: {}'.format(top_card))
    time.sleep(1)
    playing = True

    turn = choose_first()
    print(turn + ' will go first')

    while playing:

        if turn == 'Player':
            print('\nTop card is: ' + str(top_card))
            print('\nYour cards: ')
            player_hand.cards_in_hand()
            if player_hand.no_of_cards() == 1:
                print('Player yells UNO!!')
            choice = input("\nHit/Card# or Pull/Draw? (h/p): ")
            if choice.lower().startswith('h') or choice.isnumeric():
                if choice.isnumeric():
                    pos = int(choice)
                else:
                    pos = int(input('Enter index of card: '))
                temp_card = player_hand.single_card(pos)
                if single_card_check(top_card, temp_card):
                    if temp_card.cardtype == 'number':
                        top_card = player_hand.remove_card(pos)
                        turn = 'Pc'
                    else:
                        if temp_card.rank == 'Skip':
                            turn = 'Player'
                            top_card = player_hand.remove_card(pos)
                        elif temp_card.rank == 'Reverse':
                            turn = 'Player'
                            top_card = player_hand.remove_card(pos)
                        elif temp_card.rank == 'Draw2':
                            pc_hand.add_card(deck.deal())
                            pc_hand.add_card(deck.deal())
                            top_card = player_hand.remove_card(pos)
                            turn = 'Pc'
                        elif temp_card.rank == 'Draw4':
                            for i in range(4):
                                pc_hand.add_card(deck.deal())
                            top_card = player_hand.remove_card(pos)
                            draw4color = input('Change color to: ')
                            if draw4color != draw4color.upper():
                                draw4color = draw4color.upper()
                            # assume single character first letter of color
                            if draw4color[0] in [c[0] for c in color]:
                                draw4color = [c for c in color if c[0] == draw4color[0]][0]
                                print('Color changes to', draw4color)
                            top_card.color = draw4color
                            turn = 'Pc'
                        elif temp_card.rank == 'Wild':
                            top_card = player_hand.remove_card(pos)
                            wildcolor = input('Change color to: ')
                            if wildcolor != wildcolor.upper():
                                wildcolor = wildcolor.upper()
                            # assume single character first letter of color
                            if wildcolor[0] in [c[0] for c in color]:
                                wildcolor = [c for c in color if c[0] == wildcolor[0]][0]
                                print('Color changes to', wildcolor)
                            top_card.color = wildcolor
                            turn = 'Pc'
                else:
                    print('{} cannot be used on {}'.format(temp_card, top_card))
            elif choice.lower().startswith('p') or choice.lower().startswith('d'):
                temp_card = deck.deal()
                print('You got: ' + str(temp_card))
                time.sleep(1)
                if single_card_check(top_card, temp_card):
                    player_hand.add_card(temp_card)
                else:
                    print('Cannot use this card')
                    player_hand.add_card(temp_card)
                    turn = 'Pc'
            if win_check(player_hand):
                print('\nPLAYER WON!!')
                playing = False
                break

        if turn == 'Pc':
            if pc_hand.no_of_cards() == 1:
                print('PC Yells UNO!!')
            temp_card = full_hand_check(pc_hand, top_card)
            time.sleep(1)
            if temp_card != 'no card':
                print(f'\nPC throws: {temp_card}')
                time.sleep(1)
                if temp_card.cardtype == 'number':
                    top_card = temp_card
                    turn = 'Player'
                else:
                    if temp_card.rank == 'Skip':
                        turn = 'Pc'
                        top_card = temp_card
                    elif temp_card.rank == 'Reverse':
                        turn = 'Pc'
                        top_card = temp_card
                    elif temp_card.rank == 'Draw2':
                        player_hand.add_card(deck.deal())
                        player_hand.add_card(deck.deal())
                        top_card = temp_card
                        turn = 'Player'
                    elif temp_card.rank == 'Draw4':
                        for i in range(4):
                            player_hand.add_card(deck.deal())
                        top_card = temp_card
                        draw4color = pc_hand.cards[0].color
                        print('Color changes to', draw4color)
                        top_card.color = draw4color
                        turn = 'Player'
                    elif temp_card.rank == 'Wild':
                        top_card = temp_card
                        wildcolor = pc_hand.cards[0].color
                        print("Color changes to", wildcolor)
                        top_card.color = wildcolor
                        turn = 'Player'
            else:
                print('\nPC pulls a card from deck')
                time.sleep(1)
                temp_card = deck.deal()
                if single_card_check(top_card, temp_card):
                    print(f'PC throws: {temp_card}')
                    time.sleep(1)
                    if temp_card.cardtype == 'number':
                        top_card = temp_card
                        turn = 'Player'
                    else:
                        if temp_card.rank == 'Skip':
                            turn = 'Pc'
                            top_card = temp_card
                        elif temp_card.rank == 'Reverse':
                            turn = 'Pc'
                            top_card = temp_card
                        elif temp_card.rank == 'Draw2':
                            player_hand.add_card(deck.deal())
                            player_hand.add_card(deck.deal())
                            top_card = temp_card
                            turn = 'Player'
                        elif temp_card.rank == 'Draw4':
                            for i in range(4):
                                player_hand.add_card(deck.deal())
                            top_card = temp_card
                            draw4color = pc_hand.cards[0].color
                            print('Color changes to', draw4color)
                            top_card.color = draw4color
                            turn = 'Player'
                        elif temp_card.rank == 'Wild':
                            top_card = temp_card
                            wildcolor = pc_hand.cards[0].color
                            print('Color changes to', wildcolor)
                            top_card.color = wildcolor
                            turn = 'Player'
                else:
                    print('PC doesnt have a card')
                    time.sleep(1)
                    pc_hand.add_card(temp_card)
                    turn = 'Player'
            print('\nPC has {} cards remaining'.format(pc_hand.no_of_cards()))
            print('Player has {} cards remaining'.format(player_hand.no_of_cards()))
            time.sleep(1)
            if win_check(pc_hand):
                print('\nPC WON!!')
                playing = False

    new_game = input('Would you like to play again? (y/n)')
    if new_game == 'y':
        continue
    else:
        print('\nThanks for playing!!')
        break
