from enum import Enum
from random import randint

class Suit(str, Enum):
    SPADE = "Spade"
    CLUB = "Club"
    HEART = "Heart"
    DIAMOND = "Diamond"

class Rank(str, Enum):
    ACE = "Ace"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"

class Card:

    suit = None
    rank = None

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        return self.rank + " of " + self.suit + "s"
    
class Deck:
    
    deck = []

    def __init__(self):
        for suit in Suit:
            for rank in Rank:
                self.deck.append(Card(suit, rank))

    def __str__(self) -> str:
        asStr = ""
        for card in self.deck:
            asStr = asStr + str(card) + ", "
        return asStr

    def shuffle(self):
        for i in range(0, len(self.deck)):
            tmp = self.deck[i]
            shuf = randint(0, len(self.deck) - 1)
            self.deck[i] = self.deck[shuf]
            self.deck[shuf] = tmp
    
    def deal(self):
        return self.deck.pop()

deck = Deck()

deck.shuffle()

print(str(deck))