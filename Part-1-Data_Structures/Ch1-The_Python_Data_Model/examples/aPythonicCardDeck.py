# Example 1-1. A deck as a sequence ofplaying cards
import collections
from random import choice

# This collections.namedtuple constructs a simple class 
# to represent individual cards
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    # List comp to create string from 2 to 10, then add the face cards.
    # Notice how order matters here, cards created in order 
    # Aces high
    ranks = [str(n) for n in range(2,11)] + list('JQKA')

    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        # List comp, create Card tuple for suit and rank
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]
        
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]


def main():
    deck = FrenchDeck()
    #print(f"There are {len(deck)} cards in a French deck.")
    #print(f"first card {deck[0]}")
    #print(f"last card {deck[-1]}")
    #print(f"Random card: {choice(deck)}")
    #print(f"Top three {deck[:3]}")
    #print(f"Aces: {deck[12::13]}")
    #print(f"All the cards:")
    #for card in deck:
    #    print(card)

    # Sorting, by rank (aces high)
    # by suit spades(highest),hearts,diamonds,clubs(lowest)
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

    def spades_high(card):
        rank_value = FrenchDeck.ranks.index(card.rank)
        return rank_value * len(suit_values) + suit_values[card.suit]
    for card in sorted(deck, key=spades_high):
        print(card)

if __name__ == "__main__":
    main()