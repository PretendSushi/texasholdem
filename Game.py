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