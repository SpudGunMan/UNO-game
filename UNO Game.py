import random
import time

color = ('RED', 'GREEN', 'BLUE', 'YELLOW')
rank = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw2', 'Draw4', 'Wild')
ctype = {'0': 'number', '1': 'number', '2': 'number', '3': 'number', '4': 'number', '5': 'number', '6': 'number',
         '7': 'number', '8': 'number', '9': 'number', 'Skip': 'action', 'Reverse': 'action', 'Draw2': 'action',
         'Draw4': 'action_nocolor', 'Wild': 'action_nocolor'}

# Player List
playerListUno = ['🤖Bot', ]
playWithBot = input('Do you want to play with the Uno Bot? (y/n): ').lower()
num_players = int(input('Enter number of players (including you): '))
for i in range(num_players):
    playerListUno.append(input(f'Enter Player {i + 1} name: '))
if playWithBot == 'n' and num_players >= 2:
    playerListUno.remove('🤖Bot')

print('\nPlayers in the game:')
for i in range(len(playerListUno)):
    print(f'{i + 1}. {playerListUno[i]}')

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
        if self.color is None:
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
        self.sort_cards()

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

    def sort_cards(self):
        self.cards.sort(key=lambda card: (
            card.color if card.color is not None else '',
            int(card.rank) if card.cardtype == 'number' and card.rank is not None else 0))
        self.cardsstr = [str(card) for card in self.cards]

def choose_first():
    random_player = random.choice(playerListUno)
    return random_player

def single_card_check(top_card, card):
    if card.color == top_card.color or top_card.rank == card.rank or card.cardtype == 'action_nocolor':
        return True
    else:
        return False

def full_hand_check(hand, top_card):
    for c in hand.cards:
        if c.color == top_card.color or c.rank == top_card.rank or c.cardtype == 'action_nocolor':
            return hand.remove_card(hand.cardsstr.index(str(c)) + 1)
    else:
        return 'no card'

def win_check(hand):
    if len(hand.cards) == 0:
        return True
    else:
        return False

def last_card_check(hand):
    for c in hand.cards:
        if c.cardtype != 'number':
            return True
        else:
            return False

def getNextPlayer(playerIndex, direction=1, skip=False):
    current_index = playerListUno.index(playerIndex)
    next_index = (current_index + direction) % len(playerListUno)
    if skip:
        next_index = (next_index + direction) % len(playerListUno)
    return playerListUno[next_index]

def getCurrentPlayer(playerIndex):
    return playerIndex

while True:
    print('Welcome to UNO! Finish your cards first to win')

    deck = Deck()
    deck.shuffle()

    hands = {player: Hand() for player in playerListUno}
    for player in playerListUno:
        for i in range(7):
            hands[player].add_card(deck.deal())

    top_card = deck.deal()
    if top_card.cardtype != 'number':
        while top_card.cardtype != 'number':
            top_card = deck.deal()
    print('\nStarting Card is: {}'.format(top_card))
    time.sleep(1)
    playing = True

    turn = choose_first()
    print('\n' + turn + ' goes first')
    direction = 1

    while playing:
        player = getCurrentPlayer(turn)
        print('\n' + player + "'s turn")
        if player != '🤖Bot':
            print('\nTop card is: ' + str(top_card))
            print('\nYour cards: ')
            hands[player].cards_in_hand()
            playableHand = False
            for i in range(len(hands[player].cardsstr)):
                if single_card_check(top_card, hands[player].single_card(i + 1)):
                    playableHand = True

            if hands[player].no_of_cards() == 1:
                print('{} Yells UNO!!'.format(player))
            if not playableHand:
                print('{} doesn\'t have a card'.format(player))
                choice = 'd'
            else:
                choice = input("\nHit/Card# or Pull/Draw? (h/p): ")
            if choice.lower().startswith('h') or choice.isnumeric():
                if choice.isnumeric():
                    pos = int(choice)
                else:
                    pos = int(input('Enter index of card: '))
                temp_card = hands[player].single_card(pos)
                if single_card_check(top_card, temp_card):
                    if temp_card.cardtype == 'number':
                        top_card = hands[player].remove_card(pos)
                        turn = getNextPlayer(player, direction)
                    else:
                        if temp_card.rank == 'Skip':
                            turn = getNextPlayer(player, direction, skip=True)
                            top_card = hands[player].remove_card(pos)
                        elif temp_card.rank == 'Reverse':
                            direction *= -1
                            turn = getNextPlayer(player, direction)
                            top_card = hands[player].remove_card(pos)
                        elif temp_card.rank == 'Draw2':
                            next_player = getNextPlayer(player, direction)
                            hands[next_player].add_card(deck.deal())
                            hands[next_player].add_card(deck.deal())
                            top_card = hands[player].remove_card(pos)
                            turn = getNextPlayer(player, direction)
                        elif temp_card.rank == 'Draw4':
                            next_player = getNextPlayer(player, direction)
                            for i in range(4):
                                hands[next_player].add_card(deck.deal())
                            top_card = hands[player].remove_card(pos)
                            draw4color = input('Change color to: ')
                            if draw4color != draw4color.upper():
                                draw4color = draw4color.upper()
                            if draw4color[0] in [c[0] for c in color]:
                                draw4color = [c for c in color if c[0] == draw4color[0]][0]
                                print('Color changes to', draw4color)
                            top_card.color = draw4color
                            turn = getNextPlayer(player, direction)
                        elif temp_card.rank == 'Wild':
                            top_card = hands[player].remove_card(pos)
                            wildcolor = input('Change color to: ')
                            if wildcolor != wildcolor.upper():
                                wildcolor = wildcolor.upper()
                            if wildcolor[0] in [c[0] for c in color]:
                                wildcolor = [c for c in color if c[0] == wildcolor[0]][0]
                                print('Color changes to', wildcolor)
                            top_card.color = wildcolor
                            turn = getNextPlayer(player, direction)
                else:
                    print('{} cannot be used on {}'.format(temp_card, top_card))
            elif choice.lower().startswith('p') or choice.lower().startswith('d'):
                temp_card = deck.deal()
                print('You got: ' + str(temp_card))
                time.sleep(1)
                if single_card_check(top_card, temp_card):
                    hands[player].add_card(temp_card)
                else:
                    print('Cannot use this card')
                    hands[player].add_card(temp_card)
                    turn = getNextPlayer(player, direction)
            if win_check(hands[player]):
                print('\n{} WON!!'.format(player))
                playing = False
                break
        
        print('{} has {} cards remaining'.format(player, hands[player].no_of_cards()))
        # Bot Logic
        if player == '🤖Bot':
            temp_card = full_hand_check(hands[player], top_card)
            time.sleep(1)
            if temp_card != 'no card':
                print(f'\nPC throws: {temp_card}')
                time.sleep(1)
                if temp_card.cardtype == 'number':
                    top_card = temp_card
                    turn = getNextPlayer(player, direction)
                else:
                    if temp_card.rank == 'Skip':
                        turn = getNextPlayer(player, direction, skip=True)
                        top_card = temp_card
                    elif temp_card.rank == 'Reverse':
                        direction *= -1
                        turn = getNextPlayer(player, direction)
                        top_card = temp_card
                    elif temp_card.rank == 'Draw2':
                        next_player = getNextPlayer(player, direction)
                        hands[next_player].add_card(deck.deal())
                        hands[next_player].add_card(deck.deal())
                        top_card = temp_card
                        turn = getNextPlayer(player, direction)
                    elif temp_card.rank == 'Draw4':
                        next_player = getNextPlayer(player, direction)
                        for i in range(4):
                            hands[next_player].add_card(deck.deal())
                        top_card = temp_card
                        draw4color = hands[player].cards[0].color
                        if hands[player].cards[0].color is None:
                            hands[player].cards[0].color = random.choice(color)
                        print('Color changes to', draw4color)
                        top_card.color = draw4color
                        turn = getNextPlayer(player, direction)
                    elif temp_card.rank == 'Wild':
                        top_card = temp_card
                        wildcolor = hands[player].cards[0].color
                        if hands[player].cards[0].color is None:
                            hands[player].cards[0].color = random.choice(color)
                        print("Color changes to", wildcolor)
                        top_card.color = wildcolor
                        turn = getNextPlayer(player, direction)
            else:
                print('\nPC pulls a card from deck')
                time.sleep(1)
                temp_card = deck.deal()
                if single_card_check(top_card, temp_card):
                    print(f'PC throws: {temp_card}')
                    time.sleep(1)
                    if temp_card.cardtype == 'number':
                        top_card = temp_card
                        turn = getNextPlayer(player, direction)
                    else:
                        if temp_card.rank == 'Skip':
                            turn = getNextPlayer(player, direction, skip=True)
                            top_card = temp_card
                        elif temp_card.rank == 'Reverse':
                            direction *= -1
                            turn = getNextPlayer(player, direction)
                            top_card = temp_card
                        elif temp_card.rank == 'Draw2':
                            next_player = getNextPlayer(player, direction)
                            hands[next_player].add_card(deck.deal())
                            hands[next_player].add_card(deck.deal())
                            top_card = temp_card
                            turn = getNextPlayer(player, direction)
                        elif temp_card.rank == 'Draw4':
                            next_player = getNextPlayer(player, direction)
                            for i in range(4):
                                hands[next_player].add_card(deck.deal())
                            top_card = temp_card
                            draw4color = hands[player].cards[0].color
                            print('Color changes to', draw4color)
                            top_card.color = draw4color
                            turn = getNextPlayer(player, direction)
                        elif temp_card.rank == 'Wild':
                            top_card = temp_card
                            wildcolor = hands[player].cards[0].color
                            print('Color changes to', wildcolor)
                            top_card.color = wildcolor
                            turn = getNextPlayer(player, direction)
                else:
                    print('PC doesn\'t have a card')
                    time.sleep(1)
                    hands[player].add_card(temp_card)
                    turn = getNextPlayer(player, direction)
            print('\nPC has {} cards remaining'.format(hands[player].no_of_cards()))
            if hands[player].no_of_cards() == 1:
                print('PC Yells UNO!!')
            time.sleep(1)
            if win_check(hands[player]):
                print('\nPC WON!!')
                playing = False

    new_game = input('Would you like to play again? (y/n)')
    if new_game == 'y':
        continue
    else:
        print('\nThanks for playing!!')
        break