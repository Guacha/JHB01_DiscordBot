import random
from collections import deque


class PeneLoteria:
    pass


class Card:

    def __init__(self, suit, denomination):
        self.denomination = denomination
        self.suit = suit


class Deck:

    def __init__(self, include_jokers=False):
        self.cards = deque()

        suits = ['Corazones', 'Picas', 'Trébol', 'Diamantes']

        denoms = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        for suit in suits:
            for denom in denoms:
                self.cards.append(Card(suit, denom))

        if include_jokers:
            self.cards.append(Card(None, "Joker"))

    def shuffle(self):
        random.shuffle(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def random_card(self) -> Card:
        selected = random.choice(self.cards)
        self.cards.remove(selected)
        return selected

    def draw_card(self) -> Card:
        return self.cards.pop()


class Blackjack:

    def __init__(self, players: list, deck: Deck):
        self.players: list[BlackjackPlayer] = players
        self.deck = deck
        self.dealer_hand = []
        self.deck.shuffle()

    def deal_hands(self):
        for player in self.players:
            for _ in range(2):
                card = self.deck.draw_card()
                player.hand.append(card)


class Player:

    def __init__(self, name: str, bet: int, discord_user):
        self.name = name
        self.bet = bet
        self.user = discord_user


class BlackjackPlayer(Player):

    def __init__(self, name: str, bet: int, discord_user):
        super().__init__(name, bet, discord_user)
        self.hand: list[Card] = []

    def get_numeric_value(self):
        pass


if __name__ == '__main__':
    p1 = BlackjackPlayer("Julián", 5, None)
    p2 = BlackjackPlayer("Miguel", 5, None)
    p3 = BlackjackPlayer("PP", 5, None)

    players = [p1, p2, p3]

    bj_game = Blackjack(players, Deck())

    bj_game.deal_hands()
    print("Manos repartidas")

    for player in bj_game.players:
        print(f"Turno de {player.name}")
        while True:
            print(f"Tu mano: {[carta.denomination for carta in player.hand]} (Valor: {player.get_numeric_value()})")
            op = input("Hit or Stop: ")
            break
