import random

playing = True

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2,
          'Three': 3,
          'Four': 4,
          'Five': 5,
          'Six': 6,
          'Seven': 7,
          'Eight': 8,
          'Nine': 9,
          'Ten': 10,
          'Jack': 10,
          'Queen': 10,
          'King': 10,
          'Ace': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self):
        # Note this only happens once upon creation of a new Deck
        self.deck = []
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.deck.append(Card(suit, rank))  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        # Note this doesn't return anything
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def output_hand_str(self):
        return [str(card) for card in self.cards]


class Chips:
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("You have {} chips, what would you like to bet?\n".format(chips.total)))-3
        except ValueError:
            print("That is not a number, please choose an integer")
        else:
            if chips.bet < 1:
                print("To win without risk is to triumph without glory")
            elif chips.total < chips.bet:
                print("Uh oh, she ain't got no money in the bank!")
            else:
                return


def hit(deck, hand):
    # deal one off the deck and add it to the hand
    # check for aces
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        hit_or_stand_input = str(input("Would you like to hit or stand? Enter h for hit or s for stand\n"))
        if hit_or_stand_input.lower() == "h":
            hit(deck, hand)
        elif hit_or_stand_input.lower() == "s":
            print("Player stands, dealer is playing")
            playing = False
        else:
            print("Whoops, missed that button there, try again")
            continue
        break


def show_some(player, dealer):
    print("\nYou have in your hand:")
    print(*player.cards, sep=', ')
    print(f"The value of your cards is {player.value}")
    print(f"\nDealer has {dealer.cards[0]} and one hidden card")


def show_all(player, dealer):
    print("\nYou have in your hand:")
    print(*player.cards, sep=', ')
    print(f"The value of your cards is {player.value}")
    print("\nThe dealer has:")
    print(*dealer.cards, sep=', ')
    print(f"The value of the dealer's cards is {dealer.value}")


def player_busts(chips):
    print("Womp, womp, you went bust")
    chips.lose_bet()


def player_wins(chips):
    print("You win! ^-^")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer went bust, you win!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins, you lose")
    chips.lose_bet()


def push():
    print("Nobody wins")

# Onto the game!


if __name__ == "__main__":

    player_chips = Chips()

    while True:
        print("Hey friend, welcome to Blackjack, the game that Udemy made us code, "
              "whilst we have no idea what the rules are!")

        game_deck = Deck()
        game_deck.shuffle()

        take_bet(player_chips)

        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())

        show_some(player_hand, dealer_hand)

        while playing:
            hit_or_stand(game_deck, player_hand)
            show_some(player_hand, dealer_hand)
            if player_hand.value > 21:
                player_busts(player_chips)
                break

        if player_hand.value < 22:
            while dealer_hand.value < 17:
                dealer_hand.add_card(game_deck.deal())

            show_all(player_hand, dealer_hand)
            if dealer_hand.value > 21:
                dealer_busts(player_chips)
            elif player_hand.value > dealer_hand.value:
                player_wins(player_chips)
            elif player_hand.value == dealer_hand.value:
                push()
            elif player_hand.value < dealer_hand.value:
                dealer_wins(player_chips)

        print(f'You have {player_chips.total} in the bank')
        if player_chips.total == 0:
            print("You are a loser with no money, better luck next time")
            break
        continue_playing_input = str(input("Would you like to keep playing? Enter Y/N\n"))
        if continue_playing_input.lower() == "y":
            playing = True
            continue
        else:
            print("Thanks for playing! Hope to see you again soon, ta ta")
            break
