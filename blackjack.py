"""
This is an implementation of the blackjack game, consisting of three classes; Card, Deck and Player.
There are methods used for initialising the deck of cards, dealing cards to the player and the dealer,
and handling player's and dealer's wins and losses.
"""

import random

suits = ['Hearts', 'Tiles', 'Clovers', 'Pikes']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,
               'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    """
    Suits are Hearts, Tiles, Clovers and Pikes.
    Ranks are 2-10, J, Q, K and A.
    """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    """
    Deck consisting of 52 unique cards.
    Upon initialization, 52 cards are created and added to deck_cards.
    """

    def __init__(self):
        self.deck_cards = []
        for rank in ranks:
            for suit in suits:
                self.deck_cards.append(Card(suit,rank))

    def __str__(self):
        return Card.__str__(self.deck_cards[10])

    def shuffle(self):
        """Shuffle the deck cards"""
        return random.shuffle(self.deck_cards)


class Player:
    """Player class"""
    def __init__(self, name, money=100, betting_amount=0):
        self.player_cards = []
        self.name = name
        self.money = money
        self.betting_amount = betting_amount

    def __str__(self):
        return f"Player: {self.name}"

    def bet(self):
        """Player selects the amount of the bet he wants to place."""
        self.betting_amount = int(input(f"Hi {self.name}. Please enter the amount you want to bet.\n"))
        print(f"You bet {self.betting_amount}.\n")

def grab_card(deck, player):
    """Grab a card from the deck and add it to the player's cards."""
    card = deck.deck_cards.pop(0)
    player.player_cards.append(card)
    return card

def player_busts(player):
    """The player loses and the money he bet are deducted from his balance."""
    player.money -= player.betting_amount
    print(f"{player.name}, you lost the game.\nYour balance is {player.money}\n")

def player_wins(player):
    """The player wins the game and he wins 1.5*money he bet."""
    player.money += 1.5*player.betting_amount
    print(f"{player.name}, you won the game! Your balance is {player.money}.\n")

def dealer_busts(dealer, player):
    """When the dealer loses the game, the player wins double the money he bet."""
    player.money += 2*player.betting_amount
    print(f"Dealer lost. {player.name}, you won the game and your balance is {player.money}!\n")

def dealer_wins(dealer, player):
    """When the dealer wins the game, the player loses the money he bet."""
    player.money -= player.betting_amount
    print(f"Dealer won. {player.name}, you lost {player.betting_amount} and your balance is {player.money}.\n")

def choose_ace_value(total, card):
    """
    If the total value of the player's cards is greater than 10,
    the Ace will count as 1 because otherwise the player would lose.
    However, if it's less or equal to 10, the Ace will count as 11.
    """

    if total <= 10:
        card.value = 11
    else:
        card.value = 1

if __name__ == "__main__":
    # Initialize deck and shuffle the cards
    deck = Deck()
    deck.shuffle()

    # Initialize player and ask him to place a bet
    player_name = input("Hey, what's your name?\n")
    player = Player(player_name)
    player.bet()
    player_total = 0

    dealer = Player("Dealer")
    dealer_total = 0

    # Hand the first 2 cards to the player and the dealer
    player_first_card = grab_card(deck, player)
    dealer_first_card = grab_card(deck, dealer)

    # Update the total of the player and the dealer.
    # If their first cards were an Ace, the value will be 11 by default
    player_total += player_first_card.value
    dealer_total += dealer_first_card.value

    # Hand the next 2 cards to the player and the dealer
    player_second_card = grab_card(deck, player)
    dealer_second_card = grab_card(deck, dealer)

    if player_second_card.rank == 'Ace':
        choose_ace_value(player_total, player_second_card)
    if dealer_second_card.rank == 'Ace':
        if dealer_first_card.value == 10:
            dealer_second_card.value = 1
        else:
            choose_ace_value(dealer_total, dealer_second_card)

    player_total += player_second_card.value
    dealer_total += dealer_second_card.value

    print(f"{player.name}, your cards are:\n{player_first_card}\n{player_second_card}\nYour cards' total value is {player_total}\n")
    print(f"{dealer.name},'s first card is:\n{dealer_first_card}\nHis card value is {dealer_first_card.value}\n")

    game_on = True

    while game_on:
        if player_total == 21 and dealer_total != 21:
            player_wins(player)
            break

        # print(f"{player.name}, your cards' total value is {player_total}\n")
        another_card = input(f"{player.name}, do you want another card? Y/N?\n")
        while another_card == 'Y' and player_total<21:
            card = grab_card(deck, player)
            print(f"\nYou raised {card} with a value of {card.value}\n")

            # Check if grabbed card is an Ace.
            if card.rank == 'Ace':
                choose_ace_value(player_total, card)
                print(f"You got an Ace which will count as {card.value}\n")

            player_total += card.value
            print(f"{player.name}, your cards are:")
            for player_card in player.player_cards:
                print(f"{player_card}")
            print(f"Your cards' total value is {player_total}\n")

            if player_total == 21 and dealer_total != 21:
                player_wins(player)
                break

            if player_total > 21:
                player_busts(player)
                break

            another_card = input(f"{player.name}, do you want another card? Y/N?\n")

        print("\nDealer's cards are: ")
        for dealer_card in dealer.player_cards:
            print(dealer_card)

        if player_total == 21 and dealer_total != 21:
            break

        if player_total > 21:
            break

        # Once player says he doesn't want another card, it's dealer's turn
        while dealer_total <= 16:
            card = grab_card(deck, dealer)
            if card.rank == 'Ace':
                choose_ace_value(dealer_total, card)
                print(f"Dealer got an ace which counts as {card.value}\n")

            dealer_total += card.value
            print(f"\nDealer raised {card} with a value of {card.value}\n")
            print(f"Dealer's total card value is {dealer_total}\n")
        if dealer_total > 21:
            dealer_busts(dealer, player)
            break
        if dealer_total == 21:
            dealer_wins(dealer, player)
            break

        # Find the winner
        if dealer_total > player_total:
            dealer_wins(dealer, player)
        elif dealer_total < player_total:
            player_wins(player)
        else:
            print(f"No one won.\n")
        break
