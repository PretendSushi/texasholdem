from Cards import Deck, Card
import copy

class Player:
    name = None
    cards = []
    chips = -1

    def __init__(self, name, startingChips):
        self.name = name
        self.chips = startingChips

    def setCards(self, card):
        self.cards.append[card]

    def addChips(self, winnings):
        self.chips += winnings

    def bet(self, bet):
        self.chips -= bet

class Game:
    players = []
    deck = None

    def __init__(self):
        self.players = self.gameStart()
        self.deck = Deck()
        self.gameLoop()

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
        
        startingChips = input("Enter the starting chips for each player")

        for player in self.players:
            name = player
            player = Player(name, startingChips)

    def gameLoop(self):
        self.gameStart()
        self.deal()
        
        print("Starting a new hand...")
        hands = 0
        currPlayers = copy.deepcopy(self.players) #make a copy of the player array to pop from
        while currPlayers > 1:
            pot = Pot() #initialize pot
            maxBet = 0 #highest bet is zero at the beginning
            #preflop
            print("Action is on " + currPlayers[hands])
            print("Current bet is: " + maxBet)
            print("Select your action: \n 1) Check or Call \n 2) Raise \n 3) Fold \n")
            action = input()
            action = int(action)
            while action < 0 or action > 3:
                print("Invalid selection. Please select an available action")
                action = input()
            self.gameplay(action, currPlayers, hands, pot, maxBet)

            #flop
            for i in range(3):
                print("Card " + (i+1) + " is" + self.deck.pop())     
            self.gameplay(action, currPlayers, hands, pot, maxBet)
            #turn
            print("Card 4 is " + self.deck.pop())
            self.gameplay(action, currPlayers, hands, pot, maxBet)
            #river
            print("Card 5 is " + self.deck.pop())
            self.gameplay(action, currPlayers, hands, pot, maxBet)

    def gameplay(self, action, currPlayers, hands, pot, maxBet):
        while True:
            for player in currPlayers:
                if action == 3:
                    del currPlayers[hands]
                else:
                    self.actions(action, player, pot)
                    if action == 2:
                        lastRaise = maxBet
            if lastRaise == maxBet:
                break
    
    def actions(self, action, player, pot):
        if action == 1:
            if maxBet > 0:
                player.bet(maxBet)
                print("Called")
            else:
                print("Checked")
                
            if action == 2: 
                maxBet = input("How much would you like to raise?")
                pot.addPot(maxBet)


    def deal(self):
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.setCards(self.deck.deal())


class Pot:
    total = 0

    def __init__(self):
        self.total = 0

    def addPot(self, value):
        self.total += value

    def giftPot(self, winner):
        winner.addChips(self.total)

class CheckWin:
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
            straight_cards = sorted((card for card in cards if card.rank in range(max(card_values)-4, max(card_values)+1)), key=lambda card: card.rank, reverse=True)
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
            if unique_values[i] - unique_values[i+4] == 4:
                return True
        # Check for 'wheel' straight: 5-4-3-2-A
        if set(unique_values) & {14, 2, 3, 4, 5} == {14, 2, 3, 4, 5}:
            return True
        return False