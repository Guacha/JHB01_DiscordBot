import random
from collections import deque
from typing import List, Tuple


class PeneLoteria:
    pass


class Card:

    def __init__(self, suit, denomination):
        self.denomination = denomination
        self.suit = suit

    def __str__(self):
        return f"{self.denomination} de {self.suit}"


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

    def __init__(self, deck: Deck):
        self.message = None
        self.player: BlackjackPlayer = None
        self.deck: Deck = deck
        self.dealer_hand = []
        self.deck.shuffle()

    def set_player(self, discord_user, bet):
        self.player = BlackjackPlayer(discord_user, bet)

    def set_ui(self, message):
        self.message = message

    def deal_hands(self):
        for _ in range(2):
            card = self.deck.draw_card()
            self.player.add_card(card)
            card = self.deck.draw_card()
            self.dealer_hand.append(card)

    def get_winners(self) -> Tuple[bool, float]:

        dealer_value = self.get_dealer_value()

        # Si el dealer tiene blackjack
        if dealer_value == 21 and len(self.dealer_hand) == 2:
            return False, 0

        # Si el dealer tiene 5 cartas
        if dealer_value <= 21 and len(self.dealer_hand) == 5:
            return False, 0

        # Si el jugador tiene 21 y 5 cartas
        if self.player.get_numeric_value() == 21 and len(self.player.hand) == 5:
            return True, 64

        # Si el jugador tiene blackjack
        if self.player.get_numeric_value() == 21 and len(self.player.hand) == 2:
            return True, 8

        # Si el jugador tiene 5 cartas y no se ha pasado del 21
        if self.player.get_numeric_value() < 21 and len(self.player.hand) == 5:
            return True, 8

        if dealer_value > 21:
            # All players under 21 win
            if self.player.get_numeric_value() <= 21:
                return True, 4

        else:
            # All players closer to 21 than the dealer win
            player_num_hand = self.player.get_numeric_value()

            if player_num_hand <= 21:
                if player_num_hand > dealer_value:
                    return True, 1.5

                else:
                    return False, 0

    def get_dealer_hit(self) -> bool:

        dealer_value = self.get_dealer_value()

        if dealer_value < 17:
            return True

        else:
            return False

    def get_dealer_value(self) -> int:
        value = 0
        aces = 0
        for card in self.dealer_hand:
            if card.denomination == 'J' or card.denomination == 'Q' or card.denomination == 'K':
                value += 10

            elif card.denomination == 'A':
                aces += 1

            else:
                value += int(card.denomination)

        for _ in range(aces):

            if value >= 11:
                value += 1
            else:
                value += 11

        return value

    def hit_player(self):
        self.player.add_card(self.deck.draw_card())


class Player:

    def __init__(self, discord_user, bet: int):
        self.name = discord_user.name
        self.bet = bet
        self.user = discord_user


class BlackjackPlayer(Player):

    def __init__(self, discord_user, bet: int):
        super().__init__(discord_user, bet)
        self.hand: list[Card] = []

    def get_numeric_value(self) -> int:
        value = 0
        aces = 0
        for card in self.hand:
            if card.denomination == 'J' or card.denomination == 'Q' or card.denomination == 'K':
                value += 10

            elif card.denomination == 'A':
                aces += 1

            else:
                value += int(card.denomination)

        for _ in range(aces):

            if value >= 11:
                value += 1
            else:
                value += 11

        return value

    def add_card(self, card: Card):
        self.hand.append(card)


if __name__ == '__main__':
    p1 = BlackjackPlayer("Julián", 5, None)

    bj_game = Blackjack(p1, None)

    bj_game.deal_hands()
    print("Manos repartidas\n")
    player = bj_game.player
    print(f"Turno de {player.name}")
    while True:
        print(f"Tu mano: {[carta.denomination for carta in player.hand]} (Valor: {player.get_numeric_value()})")
        op = input("Hit or Stop: ")

        if op == 'hit' or op == 'h':
            draw_card = bj_game.deck.draw_card()
            print(f"Carta obtenida: {draw_card}")
            player.add_card(draw_card)

            if player.get_numeric_value() > 21:
                print(f"Perdiste maldito manco: (Valor de mano: {player.get_numeric_value()})")
                break

        else:
            break

    print(f"Mano del dealer: {[card.denomination for card in bj_game.dealer_hand]} (Valor: {bj_game.get_dealer_value()})")
    while bj_game.get_dealer_hit():
        carta = bj_game.deck.draw_card()
        bj_game.dealer_hand.append(carta)
        print(f"Carta sacada: {carta}")

    if bj_game.get_dealer_value() > 21:
        print("El dealer se pasó!")

    else:
        print("El dealer no pide más!")

    player_win, mult = bj_game.get_winners()

    if player_win:
        print(f"{player.name} gana! Recibe {mult}x su apuesta ({mult*player.bet})")

    else:
        print("La casa gana!")

