from Cards import Deck, Card

class Player:
    name = None
    cards = []

    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def setCards(self, card):
        self.cards.append[card]

class Game:
    players = []
    deck = None

    def __init__(self):
        self.players = self.gameStart()
        self.deck = Deck()

    def gameStart(self):
        print("Game Start:")
        print("Enter \"start\" to start the game")
        start = False
        idx = 1
        while len(self.players) < 2 and start == False:
            inp = input("Enter the name for player " + idx)
            if inp == "start" and len(self.players) >= 2:
                if len(self.players < 2):
                    print("You must have at least 2 players, you have "+ len(self.players)+" players")
                start = True
            else:
                self.players.append(inp)

    def gameLoop(self):
        pass

    def deal(self):
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.setCards(self.deck.deal())
