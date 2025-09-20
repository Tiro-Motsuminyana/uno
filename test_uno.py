import pytest
from uno import Card, Deck, Player, Game  # adjust import path as needed


# ---------------------------
# Card tests
# ---------------------------
def test_card_playable_same_colour():
    red_five = Card("Red", "5")
    red_skip = Card("Red", "skip")
    assert red_skip.is_playable_on(red_five, red_five.colour)


def test_card_playable_same_number():
    red_five = Card("Red", "5")
    green_five = Card("Green", "5")
    assert green_five.is_playable_on(red_five, "Red")


def test_card_playable_wild():
    wild = Card("wild", "wild")
    red_five = Card("Red", "5")
    assert wild.is_playable_on(red_five, "Red")


# ---------------------------
# Deck tests
# ---------------------------
def test_deck_draw_reduces_size():
    deck = Deck()
    initial_size = len(deck.cards)
    card = deck.draw()
    assert isinstance(card, Card)
    assert len(deck.cards) == initial_size - 1


def test_deck_empty_then_refills():
    deck = Deck()
    # empty the deck
    while deck.cards:
        deck.draw()
    # should refill from discard pile (but we need discard_pile set)
    deck.discard_pile = [Card("Red", "5")]
    c = deck.draw()
    assert isinstance(c, Card)


# ---------------------------
# Player tests
# ---------------------------
def test_player_draw_adds_cards():
    deck = Deck()
    p = Player("Alice")
    p.draw(deck, 3)
    assert len(p.hand) == 3


def test_player_play_removes_card():
    p = Player("Bob")
    c = Card("Red", "7")
    notC= Card("Red","4")
    p.hand.append(c)
    played = p.play(c,notC,"Red")
    assert played == c
    assert c not in p.hand


# ---------------------------
# Game tests
# ---------------------------
def test_game_starts_with_one_card_on_table():
    g = Game(["A", "B"])
    assert isinstance(g.top_card, Card)


def test_turn_rotation():
    g = Game(["A", "B", "C"])
    first_turn = g.turn_index
    g.next_turn()
    assert g.turn_index == (first_turn + 1) % 3


def test_play_turn_changes_top_card():
    g = Game(["A", "B"])
    p = g.players[0]
    # force a valid card
    card = Card(g.top_card.colour, g.top_card.value)
    p.hand.append(card)
    g.play_turn(p, card)
    assert g.top_card == card
    assert card not in p.hand
