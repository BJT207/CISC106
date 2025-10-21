from bakery import assert_equal

def convert_hand(card: int) -> str:
    """
    Takes in an int representing a card and converts it to a user readable string

    Args:
        card (int): The card being converted from an int. Can be 2-14

    Returns:
        str: strings of ints 2-9. 10 11 12 13 14 returns X J Q K A respectively
    """
    if card < 10 :
        return str(card)
    elif card == 10:
        return "X"
    elif card == 11:
        return "J"
    elif card == 12:
        return "Q"
    elif card == 13:
        return "K"
    else:
        return "A"
        

def hand_to_string(hand: list[int]) -> str:
    """
    Takes in the cards in the players hand as an int and returns a user readable string of the hand

    Args:
        hand (list[int]): Takes in a list of the players cards as ints
        
    Returns:
        str: the string containing the combined human readable string
    """
    return convert_hand(hand[0]) + " " + convert_hand(hand[1]) + " " + convert_hand(hand[2])


assert_equal(hand_to_string([2,9,10]),"2 9 X")
assert_equal(hand_to_string([11,12,13]),"J Q K")
assert_equal(hand_to_string([14,9,10]),"A 9 X")

def sort_hand(hand: list[int]) -> list[int]:
    """
    Sorts a list representing a players hand from greatest to least

    Args:
        hand (list[int]): The players current hand as a list of ints

    Returns:
        list[int]: The hand ordered from greatest to least
    """
    sorted_hand = [hand[0],hand[1],hand[2]]
    if sorted_hand[0] <= sorted_hand[1]:
        sorted_hand = [sorted_hand[1], sorted_hand[0],sorted_hand[2]]
    if sorted_hand[1] <= sorted_hand[2]:
        sorted_hand = [sorted_hand[0], sorted_hand[2],sorted_hand[1]]
    if sorted_hand[0] <= sorted_hand[1]:
        sorted_hand = [sorted_hand[1], sorted_hand[0],sorted_hand[2]]     
    return sorted_hand

assert_equal(sort_hand([2,2,3]),[3,2,2])
assert_equal(sort_hand([2,3,4]),[4,3,2])
assert_equal(sort_hand([2,4,3]),[4,3,2])
assert_equal(sort_hand([4,3,2]),[4,3,2])

def has_triple(hand: list[int]) -> bool:
    '''
    takes in a list representing the users hand and returns wheter or not hey have a tripple

    Args:
        hand (list[int]): The players current hand as a list

    Returns:
        boot: Returns whether the player does or does not have a tripple
    '''
    
    if hand[0] == hand[1] == hand[2]:
        return True
    return False

assert_equal(has_triple([2,3,4]),False)
assert_equal(has_triple([11,11,11]),True)
assert_equal(has_triple([2,2,4]),False)

def has_straight(hand: list[int]) -> bool:
    '''
    Takes in a order sorted list representing the users current hand and returns whether the
    user has a straight
    
    Args:
        hand (list[int]) : a list representing the players current hand
    
    Returns:
        bool: Whether or no the user has a straight
    '''
    if (hand[0] > hand[1] > hand[2]) and (hand[0] == hand[1] + 1) and (hand[1] == hand[2] + 1):
        return True
    return False

assert_equal(has_straight([4,3,2]),True)
assert_equal(has_straight([11,4,3]),False)
assert_equal(has_straight([4,3,3]),False)

def has_pair(hand: list[int]) -> bool:
    '''
    Takes in a list representing the users hand and return whether or not they have a pair
    
    Args:
        hand (list[int]) : takes in a sorted list of the users hand
    
    Returns:
        bool: whether the user has a strait or not
    '''
    if (hand[0] == hand[1] or hand[1] == hand[2]) and not (hand[0] == hand[1] == hand[2]):
        return True
    return False

assert_equal(has_pair([4,3,3]), True)
assert_equal(has_pair([4,3,2]), False)
assert_equal(has_pair([3,3,3]), False)

def score_hand(hand: list[int]) -> int:
    '''
    Score hand takes in the users current hand as a list of ints and scores it
    
    Args:
        hand (list[int]) : users current hand as a list of ints
    
    Returns:
        int: Score of the hand using base 16
    '''
    if has_triple(hand):
        first_digit = 16
    elif has_straight(hand):
        first_digit = 15
    elif has_pair(hand):
        first_digit = hand[1]
    else:
        first_digit = 0
    return first_digit*(16**3) + hand[0]*(16**2) + hand[1]*16 + hand[2]

assert_equal(score_hand([4,4,4]),66628)
assert_equal(score_hand([4,4,3]),17475)
assert_equal(score_hand([4,3,2]),62514)

def dealer_plays(hand: list[int]) -> bool:
    '''
    Takes in a list sorted least to greatest and decides whether the dealer should play based on 
    if the value of their highest card is at least a queen or contains a feature
    Args:
        hand (list[int]) : list of ints detailing the dealers hand
    Returns:
        bool: weather or not the dealer plays based on their hand
    '''
    if score_hand(sort_hand(hand)) >= (12*(16**2)):
        return True
    return False

assert_equal(dealer_plays([13,2,2]), True)
assert_equal(dealer_plays([13,13,2]), True)
assert_equal(dealer_plays([11,3,2]), False)
assert_equal(dealer_plays([2,2,2]), True)

def play_round() -> int:
    '''
    Determines how many points the player has won or lost in a round
    Args:
    
    Returns:
        int: number of points won or lost
    '''
    player_hand = sort_hand(deal())
    print(hand_to_string(player_hand))
    if get_choice() == 'p':
        dealer_hand = sort_hand(deal())
        print(hand_to_string(dealer_hand))
        if dealer_plays(dealer_hand):
            if score_hand(player_hand) > score_hand(dealer_hand):
                return 20
            return -20
        return 10
    return -10

"""
End of Student Defined Code (Minus Drafter Bugfixes for the UI)
Begin Instructor Code...
"""


def get_choice() -> str:
    """
    Get user input and return either 'p' or 'f' depending on the player's choice.
    """
    answer= ' '
    while answer not in 'pf':
        answer=input("Please enter either 'p' or 'f':")
    return answer

from random import randint

def deal() -> list[int]:
    """
    Simple random card dealing function that returns three randomly chosen cards,
    represented as integers between 2 and 14.
    """
    return [randint(2, 14), randint(2, 14), randint(2, 14)]

#score = 0
#while True:
#    score += play_round()
#    print("Your score is", score, "- Starting a new round!")
    
from drafter import *
from dataclasses import dataclass

@dataclass
class State:
    hand: list[int]
    dealer_hand: list[int]
    score: int


def decide_game(state: State) -> str:
    if not dealer_plays(sort_hand(state.dealer_hand)):
        state.score += 10
        dealer_action = "folded"
    elif score_hand(sort_hand(state.dealer_hand)) > score_hand(sort_hand(state.hand)):
        state.score += -20
        dealer_action = "won"
    else:
        state.score += 20
        dealer_action = "lost"
    return dealer_action


@route
def index(state: State):
    state.hand = deal()
    state.dealer_hand = deal()
    return Page(
        state,
        [
            Header("New round!"),
            "Your score: " + str(state.score),
            "Your hand: " + hand_to_string(state.hand),
            Button("Fold", fold),
            Button("Play", play),
        ],
    )


@route
def fold(state: State):
    state.score -= 10
    return Page(
        state,
        [
            Header("You folded!"),
            "You lost 10 points. Your score is now " + str(state.score),
            Button("Start new game", index),
        ],
    )


@route
def play(state: State):
    dealer_action = decide_game(state)
    return Page(
        state,
        [
            Header("Dealer " + dealer_action + "!"),
            "Your hand: " + hand_to_string(state.hand),
            "The dealer's hand: " + hand_to_string(state.dealer_hand),
            "The dealer " + dealer_action + " and your score is now " + str(state.score) + " points.",
            Button("Start new game", index),
        ],
    )
    
start_server(State([], [], 0))