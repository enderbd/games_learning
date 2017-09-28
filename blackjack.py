import random


class Blackjack(object):
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.player_hand = []
        self.player_hand_total = 0
        self.house_hand = []
        self.house_hand_total = 0
        # self.deck.print_deck()

    def start_game(self):
        # while True:
        #     try:
        #         amount = int(raw_input('Enter bet: '))
        #         self.player.bet(amount)
        #         break
        #     except:
        #         print 'Enter a valid number for the amount'

        for i in range(2):
            # Player is 1
            self.hit(1)
            # House is 0
            self.hit(0)

        self.print_hand(1)
        self.print_hand(0)

    def hit(self, source):
        self.deck.hit()
        if source == 1:
            self.player_hand.append(self.deck.dealt_cards[-1])
        elif source == 0:
            self.house_hand.append(self.deck.dealt_cards[-1])

    def print_hand(self,source):
        if source == 1:
            print 'Player hand:'
            for i in range(len(self.player_hand)):
                self.deck.print_card(self.player_hand[i])
        elif source == 0:
            print 'House hand:'
            for i in range(len(self.house_hand)):
                if i == 0:
                    print 'House hidden'
                else:
                    self.deck.print_card(self.house_hand[i])

    def check_hand(self, source):
        print '--------------check hand'
        card_values = []
        total = 0
        ace = 0
        if source == 0:
            hand = self.house_hand
        elif source == 1:
            hand = self.player_hand

        for i in range(len(hand)):
            card = self.deck.cards[hand[i]]
            print card
            try:
                value = int(card.split(' ')[0])
                card_values.append(value)
            except:
                if card.split(' ')[0] == 'ace':
                    ace += 1
                else:
                    card_values.append(10)

        for v in card_values:
            total += v

        if source == 0:
            self.house_hand_total = total
            print 'House total: {total}'.format(total=total)
        elif source == 1:
            self.player_hand_total = total
            print 'Player total: {total}'.format(total=total)

    def house_play(self):
        self.check_hand(0)
        pass

    def play(self):
        self.start_game()
        while True:
            while True:
                try:
                    action = int(raw_input('Enter 1 for Hit, 2 for Stand: '))
                    break
                except:
                    print 'Action error, Enter 1 for Hit, 2 for Stand'
                    continue

            if action == 1:
                self.hit(1)
                self.print_hand(1)
                self.check_hand(1)
                if self.player_hand_total > 21:
                    print 'Player lost'
                    break
            elif action == 2:
                self.check_hand(1)
                while self.house_hand_total < 19:
                    self.hit(0)
                    self.check_hand(0)
                    self.print_hand(0)
                if self.house_hand_total > 21 or self.player_hand_total > self.house_hand_total:
                    print 'Player won'
                    self.print_hand(1)
                    break
                elif self.player_hand_total < self.house_hand_total <= 21:
                    print 'House won'
                    break
            elif action == 0:
                print 'Game aborted'
                break


class Player(object):
    def __init__(self, bank=100, name='Player 1'):
        self.player_bank = bank
        self.player_name = name
        self.player_bet = 0

    def bet(self,amount):
        self.player_bank -= amount
        self.player_bet = amount


class Deck(object):
    faces = {11: 'jack', 12: 'queen', 13: 'king'}
    deck_size = 52

    def __init__(self):
        self.deck = [i for i in range(Deck.deck_size)]
        self.cards = []
        self.dealt_cards = []
        self.create_cards()
        self.shuffle_deck()

    def create_cards(self):
        i = 0
        cards = []
        for color in ['clubs', 'diamonds', 'spades', 'hearts']:
            for n in range(1, 14):
                if n == 1:
                    cards.append('ace of ' + color)
                elif n > 10:
                    cards.append(Deck.faces[n] + ' of ' + color)
                else:
                    cards.append(str(n) + ' of ' + color)

                i += 1

        self.cards = cards

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def print_deck(self):
        deck_out = []
        for i in range(len(self.deck)):
            deck_out.append(self.cards[self.deck[i]])

        print deck_out

    def hit(self):
        self.dealt_cards.append(self.deck[-1])
        self.deck.pop()

    def print_card(self,index):
        print '{card}'.format(card = self.cards[index])


game = Blackjack()
game.play()
