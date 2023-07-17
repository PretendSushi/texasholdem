
from enum import Enum
from random import randint

class Suit(str, Enum):
    SPADE = "Spade"
    CLUB = "Club"
    HEART = "Heart"
    DIAMOND = "Diamond"

class Rank(Enum):
    ACE = ("Ace", 14)
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("Jack", 11)
    QUEEN = ("Queen", 12)
    KING = ("King", 13)

    def __new__(cls, label, value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ < other._value_
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ <= other._value_
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ > other._value_
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ >= other._value_
        return NotImplemented

    def __str__(self):
        return self.label

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.rank < other.rank
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.rank <= other.rank
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.rank > other.rank
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.rank >= other.rank
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.rank == other.rank and self.suit == other.suit
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.rank} of {self.suit}s"

    def __repr__(self):
        return self.__str__()

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self):
        for i in range(len(self.deck)):
            j = randint(i, len(self.deck) - 1)
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]

    def deal(self):
        return self.deck.pop()



class Player:
    def __init__(self, name, cards=None):
        self.name = name
        self.cards = cards if cards is not None else []

    def setCards(self, card):
        self.cards.append(card)

    def showHand(self):  # New method to print the player's hand
        print(f"{self.name}'s hand: {self.cards}")


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()

    def gameStart(self):
        print("Game Start:")
        for i in range(1, 4):
            name = "Player " + str(i)
            self.players.append(Player(name))

    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            for _ in range(2):  # Each player receives 2 cards
                player.setCards(self.deck.deal())

    def revealRiver(self):
        self.river = [self.deck.deal() for _ in range(5)]  # Reveal 5 cards on the "river"
        print("River cards: ", self.river)

class CheckWin:
    HAND_RANKS = {
        "high_card": 1,
        "pair": 2,
        "two_pair": 3,
        "three_kind": 4,
        "straight": 5,
        "flush": 6,
        "full_house": 7,
        "four_kind": 8,
        "straight_flush": 9,
        "royal_flush": 10,
    }

    def identify_hand(self, cards):
        card_values = [card.rank for card in cards]
        card_suits = [card.suit for card in cards]
        card_counts = {value: card_values.count(value) for value in card_values}
        suit_counts = {suit: card_suits.count(suit) for suit in card_suits}
        
        # Checking for a Flush or Straight Flush
        flush_suit = next((suit for suit, count in suit_counts.items() if count >= 5), None)
        if flush_suit:
            flush_cards = [card for card in cards if card.suit == flush_suit]
            flush_cards.sort(key=lambda card: card.rank, reverse=True)
            if self.is_straight([card.rank for card in flush_cards]):
                if flush_cards[0].rank == 14:  # If highest card is an Ace
                    return (self.HAND_RANKS["royal_flush"], flush_cards[:5])
                else:
                    return (self.HAND_RANKS["straight_flush"], flush_cards[:5])
            else:
                return (self.HAND_RANKS["flush"], flush_cards[:5])
        
        # Checking for Four of a Kind or Full House
        four_kind_value = next((value for value, count in card_counts.items() if count == 4), None)
        if four_kind_value:
            four_kind_cards = [card for card in cards if card.rank == four_kind_value]
            kicker = max(card for card in cards if card.rank != four_kind_value)
            return (self.HAND_RANKS["four_kind"], four_kind_cards + [kicker])
        
        three_kind_value = next((value for value, count in card_counts.items() if count == 3), None)
        pair_values = [value for value, count in card_counts.items() if count == 2]
        if three_kind_value and pair_values:
            full_house_cards = [card for card in cards if card.rank in [three_kind_value] + pair_values]
            full_house_cards.sort(key=lambda card: card.rank, reverse=True)
            return (self.HAND_RANKS["full_house"], full_house_cards)
        
        # Checking for Straight
        if self.is_straight(card_values):
            straight_cards = sorted((card for card in cards if card.rank._value_ in range(max(card_values)._value_-4, max(card_values)._value_+1)), key=lambda card: card.rank, reverse=True)
            return (self.HAND_RANKS["straight"], straight_cards)
        # Checking for Three of a Kind or Two Pair
        if three_kind_value:
            three_kind_cards = [card for card in cards if card.rank == three_kind_value]
            kickers = sorted((card for card in cards if card.rank != three_kind_value), key=lambda card: card.rank, reverse=True)
            return (self.HAND_RANKS["three_kind"], three_kind_cards + kickers[:2])
        elif len(pair_values) >= 2:
            two_pair_cards = [card for card in cards if card.rank in pair_values]
            two_pair_cards.sort(key=lambda card: card.rank, reverse=True)
            kicker = max(card for card in cards if card.rank not in pair_values)
            return (self.HAND_RANKS["two_pair"], two_pair_cards[:4] + [kicker])
        
        # Checking for Pair
        pair_value = next((value for value, count in card_counts.items() if count == 2), None)
        if pair_value:
            pair_cards = [card for card in cards if card.rank == pair_value]
            kickers = sorted((card for card in cards if card.rank != pair_value), key=lambda card: card.rank, reverse=True)
            return (self.HAND_RANKS["pair"], pair_cards + kickers[:3])
        
        # If no other hand, it's a High Card
        cards.sort(key=lambda card: card.rank, reverse=True)
        return (self.HAND_RANKS["high_card"], cards[:5])

    def is_straight(self, values):
        unique_values = list(set(values))
        unique_values.sort(reverse=True)
        for i in range(len(unique_values) - 4):
            if unique_values[i]._value_ - unique_values[i+4]._value_ == 4:
                return True
        # Check for 'wheel' straight: 5-4-3-2-A
        if set(unique_values) & {Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE} == {Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE}:
            return True
        return False

def main():
    game = Game()
    game.gameStart()
    game.deal()

    for player in game.players:
        print(f"{player.name}'s hand: {player.cards}")

    game.revealRiver()

    checker = CheckWin()
    best_hand = (0, [])
    best_player = None
    for player in game.players:
        player_hand = player.cards + game.river
        hand_rank, best_cards = checker.identify_hand(player_hand)
        print(f"{player.name}'s best hand: {best_cards} of rank {hand_rank}")
        if hand_rank > best_hand[0] or (hand_rank == best_hand[0] and best_cards[0].rank > best_hand[1][0].rank):
            best_hand = (hand_rank, best_cards)
            best_player = player
    print(f"Best hand: {best_hand[1]} of rank {best_hand[0]} by {best_player.name}")

if __name__ == "__main__":
    main()
