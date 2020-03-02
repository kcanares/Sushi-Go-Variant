import math
from collections import defaultdict

*****************************************************************************
def comp10001go_score_group(cards):
    """Returns an integer score for a group of cards based on the COMP10001GO 
    game rules"""
    
    score = 0

    # a dictionary of the score each value is worth
    card_value = {'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                   '7': 7, '8': 8, '9': 9, '0': 10,
                   'J': 11, 'Q': 12, 'K': 13}

    # dictionary with keys being suits and values being what the opposite
    # colour suits are
    opposite_colour = {'H': ['C', 'S'], 'D': ['C', 'S'], 'C': ['H', 'D'],
                       'S': ['H', 'D']}

    # counts the number of each card type in the group
    card_count = defaultdict(int)
    for card in cards:
        card_count[card[0]] += 1

    # If an N-of-a-kind group is present, the product of the card's value and 
    # N factorial is added to the score. The presence of a factorial group is
    # also noted
    factorial_present = False
    for card, count in card_count.items():
        if count == len(cards) and count >= 2 and card != 'A':
            score += card_value[card] * math.factorial(count)
            factorial_present = True

    # sorts the cards in ascending order based on the cards' individual values
    for i in range(len(cards)):
        for j in range(1, len(cards)):
            if card_value[cards[j - 1][0]] > card_value[cards[j][0]]:
                (cards[j - 1], cards[j]) = (cards[j], cards[j - 1])

    # creates list of aces
    ace_list = []
    for card in cards:
        if card[0] == 'A':
            ace_list.append(card)


    # creates a run_list starting with the lowest valued card in the run
    run_list = [cards[0]]
    for i in range(1, len(cards)):
        if (card_value[run_list[-1][0]] == card_value[cards[i][0]] - 1 and 
        run_list[-1][1] in opposite_colour[cards[i][1]]):
            run_list.append(cards[i])
            
        # looks at whether there's a gap between a card in the run list and the
        # given group of cards. Checks whether this gap can be filled with 
        # aces. If it can, the aces and the cards preceding and following the
        # aces are added to the run list. 
        elif (0 < card_value[cards[i][0]] - card_value[run_list[-1][0]] - 1 <= 
              len(ace_list)):
            ace_gap = card_value[cards[i][0]] - card_value[run_list[-1][0]] - 1
            for j in range(ace_gap):
                for ace in ace_list:
                    
                    # The aces' value is replaced with the card it is replacing
                    if ace[1] in opposite_colour[run_list[-1][1]]:
                        new_value = str(card_value[run_list[-1][0]] + 1)
                        run_list.append(new_value + ace[1])
                        ace_list.remove(ace)
            if cards[i][1] in opposite_colour[run_list[-1][1]]:
                run_list.append(cards[i])
        else:
            break

    # score of the run list is computed given that there's a valid run
    if len(run_list) == len(cards) and len(run_list) >= 3:
        for card in run_list:
            score += card_value[card[0]]

    # if there is no valid groups present, the individual scores of every card
    # are deducted
    if ((len(run_list) != len(cards) or len(run_list) < 3) and 
        not factorial_present):
        for card in cards:
            score -= card_value[card[0]]

    return score

******************************************************************************
def comp10001go_valid_groups(groups):
    """returns a Boolean indicating whether all groups are valid or not. 
    Validity meaning that the group is a singleton card, a valid N-of-a-kind
    or a valid run."""
    
    # a dictionary that counts valid and invalid groups
    validity_count = {'valid': 0, 'invalid': 0}
    
    if not groups:
        return True
    
    MIN_SCORE = 4
    SINGLETON_LENGTH = 1
    MAX_NO_OF_CARDS_IN_RUN = 12
    
    for group in groups:
        if len(group) == SINGLETON_LENGTH:
            validity_count['valid'] += 1
        elif len(group) > MAX_NO_OF_CARDS_IN_RUN:
            validity_count['invalid'] += 1
        elif comp10001go_score_group(group) <= MIN_SCORE:
            validity_count['invalid'] += 1
        else:
            validity_count['valid'] += 1
    
    if validity_count['invalid'] > 0:
        return False
    else:
        return True
