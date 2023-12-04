#
# card game
# author: Leo Paggen
# v1.1
#

from random import shuffle
import matplotlib.pyplot as plt # optional, only if using metrics
import seaborn as sns # same as above
import time

# a few global lists to gather information about the games
stats = {"win_player" : [], "rounds" : [], "num_wars" : [], "win_first" : []} # dictionary of lists, keeps statistics about the games

# set up class for deck
class Deck(object):
    """
    Does not accept parameters
    
    This creates a 52 card deck to play the game
    """
    suit = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
    rank_val = [None, None, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    rank_names = [None, None, 'Two', 'Three', 'Four', 'Five',
                 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack',
                 'Queen', 'King', 'Ace']
    index_tracker = {"i" : 0, "j" : 0} # tracks the i, j indices used later in round()
    is_war = False # boolean indicator, handles the issue with autoplay when recursion is used
    def __init__(self):
        self.deck = []
        self.p1_deck = []
        self.p2_deck = []
        self.used_cards = []
        self.build()
        self.shuffle()
        self.deal()

    def build(self):
        #builds the deck of the game
        for i in self.suit:
            for j in self.rank_val[2:]:
                card = Card(j, i)
                self.deck.append(card)

    def shuffle(self):
        #shuffles the deck of the game
        shuffle(self.deck)
        print("Deck has been shuffled")

    def show(self):
        #displays the whole deck
        print(self.deck)

    def deal(self):
        #deals cards to both players
        self.p1_deck = self.deck[:26]
        self.p2_deck = self.deck[26:]
        print("Both players have been dealt 26 cards")

class Card(Deck):
    #Child class of Deck
    #Has all the attributes regarding cards
    def __init__(self, r, s):
        self.rank = r
        self.suit = s

    def __repr__(self):
        return self.rank_names[self.rank] + ' of ' + self.suit

    def __gt__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

class Game(Deck):
    #Child class of Deck
    #Contains all methods used to power the game
    def __init__(self):
        super().__init__() # init attributes of parent class
        self.autoplay = False
        self.startround = True
        self.wars_played = 0
        self.roundcount = 1 # incremental

    def players(self):
        p1_name = str(input("Player 1 name -> "))
        p2_name = str(input("Player 2 name -> "))
        print(f"Welcome to war, {p1_name} and {p2_name}")

    def round(self, fast = False, auto = False):
        #Starts a new round for both players
        if not auto:
            if self.roundcount == 1:
                self.autoplay = input("Autoplay on? (y/n) ")
                while self.autoplay != 'y' and self.autoplay != 'n':
                    self.autoplay = input("Autoplay on? (y/n) ")
                if self.autoplay == 'y':
                    self.autoplay = True
                else:
                    self.autoplay = False

        if auto:
            self.autoplay = True

        while len(self.p1_deck) > 0 and len(self.p2_deck) > 0:
            if self.autoplay:
                self.startround = True
                print(f"### Round {self.roundcount}")
            if not self.autoplay:
                self.startround = str(input(f"Start round {self.roundcount} ? (y/n)"))
                while self.startround != 'y' and self.startround != 'n':
                    self.startround = str(input(f"Start round {self.roundcount} ? (y/n)"))
                if self.startround == 'y':
                    continue
                else:
                    pass

            # user wants to play, let's go (proceed is always True here)
            # manipulate the index tracker dictionary
            i, j = self.index_tracker.values() # just takes the values and assigns to i, j
            if self.is_war:
                print(self.is_war)
            if len(self.p1_deck) > i and len(self.p2_deck) > j:
                print(f"Player 1 card: {self.p1_deck[i]}\nPlayer 2 card: {self.p2_deck[j]}")
                print(self.index_tracker)
            else:
                print("One of the players does not have enough cards to proceed with the war!\nExiting game...")
                break

            # 3 conditions to check, <, >, ==
            # using i and j, modular
            if (self.p1_deck[i] > self.p2_deck[j]) and (len(self.p1_deck) > i and len(self.p2_deck) > j):
                print("\tPlayer 1 wins this round")
                cards_to_stack = [self.p1_deck[0], self.p2_deck[0]]
                shuffle(cards_to_stack)
                self.p1_deck.extend(cards_to_stack)
                if len(self.p1_deck) > 0 and len(self.p2_deck) > 0:
                    print("d1")
                    self.p1_deck.pop(0) # make sure to remove top card from deck
                    self.p2_deck.pop(0)
                elif (self.is_war is True) and len(self.p1_deck) > i and len(self.p2_deck) > j:
                    print("d2")
                    cards_to_stack = [self.p1_deck[0], self.p1_deck[1],
                                      self.p2_deck[0], self.p2_deck[1]]
                    shuffle(cards_to_stack)
                    self.p1_deck.extend(cards_to_stack)
                    self.p1_deck.pop(0)
                    self.p1_deck.pop(1)
                    self.p2_deck.pop(0)
                    self.p2_deck.pop(1)
                    self.is_war = False
                else:
                    print("d3")
                    pass
                print(f"\t\tp1 has {len(self.p1_deck)} cards") # debug
                print(f"\t\tp2 has {len(self.p2_deck)} cards") # debug

            elif (self.p1_deck[i] < self.p2_deck[j]) and (len(self.p1_deck) > i and len(self.p2_deck) > j):
                print("\tPlayer 2 wins this round")
                cards_to_stack = [self.p1_deck[0], self.p2_deck[0]]
                shuffle(cards_to_stack)
                self.p2_deck.extend(cards_to_stack)
                if len(self.p1_deck) > 0 and len(self.p2_deck) > 0:
                    print("d4")
                    self.p1_deck.pop(0) # make sure to remove top card from deck
                    self.p2_deck.pop(0)
                elif (self.is_war is True) and len(self.p1_deck) > i and len(self.p2_deck) > j:
                    print("d5")
                    cards_to_stack = [self.p1_deck[0], self.p1_deck[1],
                                      self.p2_deck[0], self.p2_deck[1]]
                    shuffle(cards_to_stack)
                    self.p2_deck.extend(cards_to_stack)
                    self.p2_deck.pop(0)
                    self.p2_deck.pop(1)
                    self.p1_deck.pop(0)
                    self.p1_deck.pop(1)
                    self.is_war = False
                else:
                    print("d6")
                    pass
                print(f"\t\tp1 has {len(self.p1_deck)} cards") # debug
                print(f"\t\tp2 has {len(self.p2_deck)} cards") # debug

            elif (self.p1_deck[i] == self.p2_deck[j]) and (len(self.p1_deck) > i and len(self.p2_deck) > j):
                print("d7")
                self.index_tracker["i"] += 2
                self.index_tracker["j"] += 2
                self.wars_played += 1
                self.is_war = True
                print("\t**** WAR ****")
                continue
            
            else:
                print("d8")
                break

            self.index_tracker["i"] = 0 # reset both i and j to 0 for further rounds
            self.index_tracker["j"] = 0 # should work just fine
            self.roundcount += 1
            if self.autoplay and fast:
                time.sleep(0.0)
            elif self.autoplay and not fast:
                time.sleep(0.2)

        # while loop exited
        self.save_results()

    def save_results(self):
        # determine the winner
        num_cards = [] # stores length of p1 and p2 decks to determine a winner
        print("Saving results")
        num_cards.append(len(self.p1_deck))
        num_cards.append(len(self.p2_deck))
        max_cards = max(num_cards)
        idxwin = num_cards.index(max_cards)
        if idxwin == 0:
            winner = 1
        else:
            winner = 2
        stats['win_player'].append(winner) # saves winning player (1 or 2)

        # save number of rounds played
        stats["rounds"].append(self.roundcount)

        # save number of wars during game
        stats["num_wars"].append(self.wars_played)

        # print the overall stats
        print(stats)

def wargame(fast = False, metrics = False):
    """
    Starts a game of war in your terminal.

    Parameters:
    - fast (bool): If True, the game will run faster.
                   Default is False.
    - metrics (bool): If True, a series of plots will
                    be built based on the results of
                    1000 instances of the game.
                    Default is False.

    Returns:
    None
    """
    deck = Game()
    if not fast and not metrics:
        deck.round()
    if fast and not metrics:
        deck.round(fast = True)
    if not fast and metrics:
        deck.round(fast = False)
    if fast and metrics:
        for i in range(1000):
            deck = Game()
            deck.round(fast = True, auto = True)

if __name__ == "__main__":
    wargame()
