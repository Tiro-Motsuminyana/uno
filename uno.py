import random
"""
uno card break down
19 number cards (1 zero and 2 of each number up to 9)
2 reverse cards.
2 skip cards.
2 draw 2 cards.
4 wild draw 4 cards.
4 wild cards.
"""

COLOURS = ["Red", "Green", "Blue", "Yellow"]
SPECIALS = ["skip", "reverse", "+2"]
WILDS = ["+4", "wild"]

class Card:
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value

    def __eq__(self, other):
        return self.colour == other.colour and self.value == other.value

    def __str__(self):
        return f"{self.colour} {self.value}"

    def is_playable_on(self, top_card, current_colour):
        return (
            self.colour == current_colour
            or self.value == top_card.value
            or self.value == "wild"
        )


class Deck:
    def __init__(self):
        self.cards = self._build_deck()
        self.discard_pile=[]
        random.shuffle(self.cards)

    def _build_deck(self):
        cards = []
        for colour in COLOURS:
            cards.append(Card(colour, "0"))
            for n in range(1, 10):
                cards.append(Card(colour, str(n)))
                cards.append(Card(colour, str(n)))
            for action in SPECIALS:
                cards.append(Card(colour, action))
                cards.append(Card(colour, action))
        for _ in range(4):
            cards.append(Card("wild", "+4"))
            cards.append(Card("wild", "wild"))
        return cards
    def discard(self,card):
        self.discard_pile.append(card)

    def draw(self, n=1):
        while True:
            try:
                drawn = [self.cards.pop() for _ in range(n)]
                break
            except IndexError:
                self.cards=self.discard_pile
        return drawn if n > 1 else drawn[0]


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck, n=1):
        self.hand.extend(deck.draw(n))

    def play(self, card, top_card, current_colour):
        if card in self.hand and card.is_playable_on(top_card, current_colour):
            self.hand.remove(card)
            return card
        raise ValueError(f"Invalid play: {card}")


class Game:
    def __init__(self, player_names):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.discard_pile=self.deck.discard_pile
        self.current_colour = None
        self.direction = 1  # 1 = clockwise, -1 = counter
        self.turn_index = 0
        self.pending_draw = 0

        # initial hands
        for player in self.players:
            player.draw(self.deck, 7)

        # first card
        while True:
            card = self.deck.draw()
            if card.colour != "wild" and card.value not in SPECIALS and not card.value.startswith("+"):
                self.discard_pile.append(card)
                self.current_colour = card.colour
                break
            else:
                self.deck.cards.insert(0, card)

    @property
    def top_card(self):
        return self.discard_pile[-1]

    def next_turn(self):
        self.turn_index = (self.turn_index + self.direction) % len(self.players)

    def play_turn(self, player, card):
        """Play a card and apply effects"""
        if player != self.players[self.turn_index]:
            raise ValueError("Not this player's turn!")

        played = player.play(card, self.top_card, self.current_colour)
        self.discard_pile.append(played)
        self.apply_effects(played)
        self.next_turn()

    def apply_effects(self, card):
        if card.colour == "wild":
            print('What colour would you like to play on after this turn')
            if card.value == "+4":
                self.pending_draw += 4
        else:
            self.current_colour = card.colour
            if card.value == "skip":
                self.next_turn()
            elif card.value == "reverse":
                self.direction *= -1
            elif card.value == "+2":
                self.pending_draw += 2
def run_cli_game():
    print("Welcome to UNO!")
    player_names = input("Enter player names separated by commas: ").split(",")
    game = Game([name.strip() for name in player_names])

    while True:
        player = game.players[game.turn_index]
        print(f"\n--- {player.name}'s turn ---")
        print(f"Top card: {game.top_card} (current colour: {game.current_colour})")
        print("Your hand:")
        for i, card in enumerate(player.hand):
            print(f"{i}: {card}")
        if game.pending_draw > 0:
            print(f"You must draw {game.pending_draw} cards!")
            player.draw(game.deck, game.pending_draw)
            game.pending_draw = 0
            game.next_turn()
            continue

        choice = input("Pick a card index to play, or type 'draw': ").strip()

        if choice.lower() == "draw":
            new_card = game.deck.draw()
            print(f"You drew: {new_card}")
            if new_card.is_playable_on(game.top_card, game.current_colour):
                play_now = input("Play this card? (y/n): ").strip().lower()
                if play_now == "y":
                    game.play_turn(player, new_card)
                else:
                    player.hand.append(new_card)
                    game.next_turn()
            else:
                player.hand.append(new_card)
                game.next_turn()
        else:
            try:
                card_index = int(choice)
                selected = player.hand[card_index]
                game.play_turn(player, selected)
            except (ValueError, IndexError) as e:
                print("Invalid choice, try again.")
                continue

        # check win
        if not player.hand:
            print(f"{player.name} wins the game!")
            break


if __name__ == "__main__":
    run_cli_game()

