import random
import os

# Author Nik Kirstein

def build_deck():
    """
    Builds a card deck.  For the purpose of Blackjack, all face cards are values of 10.
    Returns the Deck, a shuffled list of cards.
    """
    deck = [1, 1, 1, 1, 
            2, 2, 2, 2, 
            3, 3, 3, 3, 
            4, 4, 4, 4, 
            5, 5, 5, 5, 
            6, 6, 6, 6, 
            7, 7, 7, 7, 
            8, 8, 8, 8, 
            9, 9, 9, 9, 
            10, 10, 10, 10, # tens
            10, 10, 10, 10, # jacks
            10, 10, 10, 10, # queens
            10, 10, 10, 10, # kings
            ]
    deck = (deck[:] * 6) # number of decks to play with.
    random.shuffle(deck)
    # print(deck)
    return deck
    
    
def make_bet(input_money):
    """
    This is really an input handler.
    Asks a player for a bet, and also takes into account the money they have when making the bet.
    Some checking for cheeky players inputting 0 or not enough money.
    Returns the bet if an INT or Q is fet the function.
    """
    bet = None
    while(bet != "Q"):
        bet = (input("Insert bet or Q to quit: "))
        try:
            bet = int(bet)
            if bet == 0:
                print("Hey! Who are you trying to cheat here!")
            elif input_money >= bet and bet != 0:
                break
            else:
                print("Not enough money, please input a valid bet")
        except:
            print('Please enter a number')
            continue # ignore it, we know its not a number
    return bet
    
    
def hit_deck(in_deck):
    """
    Pops out a random card in the deck for play the game.
    Returns the card.
    """
    card_index = random.randint(0, (len(in_deck)-1))
    card = in_deck.pop(card_index)
    return card


def deal_player(deck):
    """
    Deals a player at the start of a round two cards.
    Returns the player's hand as a list of two cards.
    """
    current_player_hand = []
    current_player_hand.append(hit_deck(deck))
    current_player_hand.append(hit_deck(deck))
    return current_player_hand


def deal_computer(deck):
    """
    Deals the computer or "dealer" at the start of a round two cards.
    Returns the computer's hand as a list of two cards.
    """
    current_computer_hand = []
    current_computer_hand.append(hit_deck(deck))
    current_computer_hand.append(hit_deck(deck))
    return current_computer_hand
    
    
def evaluate_hand(round_hand):
    """
    Takes a hand of cards and evaluates the sum.
    Aces are 1 if the hand will go over 21
    Otherwise an Ace is 11 so if the hand will not go over 21, add an extra 10 to reach 11.
    Returns the sum of the hand.
    """
    has_ace = False
    if 1 in round_hand:
        has_ace = True
        # print("ACE")
    hand_sum = sum(round_hand)
    if has_ace and (hand_sum + 10) <= 21:
        hand_sum += 10
    
    return hand_sum
    
def play_round(money):
    """
    A large function to play single round of blackjack.
    This is essentially a main function if continued betting and betting simulation/strategies wasn't the point of this script.
    Takes the money input to be played in the round and plays through a round of Blackjack with player input prompts.
    Returns the money at the end of the round, either the player won, lost, or there was a "push" where the bets were returned.
    """
    blackjack_deck = build_deck()
    game_bet = make_bet(money)
    
    round_player_hand = deal_player(blackjack_deck)
    round_computer_hand = deal_computer(blackjack_deck)
    
    print("\nYour hand: ", round_player_hand, "||| Current Sum: ", evaluate_hand(round_player_hand))
    print("Dealers hand: [" + str(round_computer_hand[0]) +  ", Facedown Card (X)]")
    
    while(True):
        print("\nPlayer's turn!")
        if (evaluate_hand(round_player_hand)) == 21:
            print("Blackjack!")
            break
        response = (input("Hit or Stay? ")).lower()
        # print(response)
        if response == "hit":
            new_card = hit_deck(blackjack_deck)
            print("You drew a", new_card)
            round_player_hand.append(new_card)
            if (evaluate_hand(round_player_hand)) == 21:
                print("Your hand: ", round_player_hand, "||| Current Sum: ", evaluate_hand(round_player_hand), " - Blackjack!")
                break
            if (evaluate_hand(round_player_hand) > 21):
                print("Your hand: ", round_player_hand, "||| Current Sum:", evaluate_hand(round_player_hand), " - Bust!")
                break
            else:
                print("Your hand: ", round_player_hand, "||| Current Sum:", evaluate_hand(round_player_hand))
        if response == "stay":
            break
        if response != "hit" and response != "stay":
            print("Unknown input, please Hit or Stay")
    
    # Program in insurance bet here eventually
    
    print("\nDealer's turn!")
    print("Dealer flips up a " + str(round_computer_hand[1]))
    
    while(True):
        if evaluate_hand(round_computer_hand) == 21:
            print("Dealer's hand: ", round_computer_hand, "||| Current Sum: ", evaluate_hand(round_computer_hand), " - Blackjack!")
            break
        if evaluate_hand(round_computer_hand) > 21:
            print("Dealer's hand: ", round_computer_hand, "||| Current Sum: ", evaluate_hand(round_computer_hand), " - Bust!")
            break
        if evaluate_hand(round_computer_hand) >= 17 and evaluate_hand(round_computer_hand) < 21:
            print("Dealer's hand: ", round_computer_hand, "||| Current Sum: ", evaluate_hand(round_computer_hand), " - Dealer Stays")
            break
        if evaluate_hand(round_computer_hand) < 17:
            print("Dealer's hand: ", round_computer_hand, "||| Current Sum: ", evaluate_hand(round_computer_hand), " - Dealer Hits")
            new_card = hit_deck(blackjack_deck)
            print("Dealer drew a", new_card)
            round_computer_hand.append(new_card)
            # print("Dealer's hand: ", round_computer_hand, "||| Current Sum:", evaluate_hand(round_computer_hand))
            
    print("\nOUTCOME")
    if evaluate_hand(round_player_hand) == 21 and evaluate_hand(round_computer_hand) == 21:
        print("Push, bets returned")
        # money stays the same
    elif evaluate_hand(round_player_hand) < 21 and evaluate_hand(round_computer_hand) < 21 and evaluate_hand(round_player_hand) == evaluate_hand(round_computer_hand):
        print("Push, bets returned")
        # money stays the same
    elif evaluate_hand(round_player_hand) == 21 and evaluate_hand(round_computer_hand) < 21 or evaluate_hand(round_player_hand) == 21 and evaluate_hand(round_computer_hand) > 21:
        print("Player Blackjack win, paying out 3:2", "||| +" + str(game_bet *1.5))
        money += game_bet * 1.5
    elif evaluate_hand(round_player_hand) > 21:
        print("Bust hand, bet lost", " ||| -" + str(game_bet))
        money -= game_bet
    elif evaluate_hand(round_player_hand) < 21 and evaluate_hand(round_computer_hand) < 21 and evaluate_hand(round_player_hand) > evaluate_hand(round_computer_hand):
        print("Player had higher hand, paying out 1:1", "||| +" + str(game_bet))
        money += game_bet
    elif evaluate_hand(round_player_hand) < 21 and evaluate_hand(round_computer_hand) < 21 and evaluate_hand(round_player_hand) < evaluate_hand(round_computer_hand):
        print("Dealer had higher hand, bet lost", "||| -" + str(game_bet))
        money -= game_bet
    elif evaluate_hand(round_player_hand) < 21 and evaluate_hand(round_computer_hand) == 21:
        print("Dealer got blackjack, player had lower hand, bet lost")
        money -= game_bet
    elif evaluate_hand(round_player_hand) < 21 and evaluate_hand(round_computer_hand) > 21:
        print("Dealer busted with player still in play, player wins, paying out 1:1", "||| +" + str(game_bet))
        money += game_bet
    # Winning conditions and payouts.
    
    return money
    
    
def main():
    money = start_money = int(input("Insert starting money\n"))
    while(True):
        response = input("\nPlay Blackjack? (y/n) ").lower()
        if response == "y":
            os.system('cls')
            print("Current money:", money)
            if money == 0:
                print("Out of money!")
                break
            money = play_round(money)
            print("Your bank is now:", money)
            print("Net end:", money - start_money)
        if response == "n":
            break
        elif response != "y" and response != "n":
            print("Invalid input, please type 'y' or 'n'")
    
    print("\nYou walked away with", money)
    print("Your net end was", money-start_money)
        
    # hold on 17 hit below 17, this is apparently how Dealer's play.
    # if both bust, player loses
    # if player wins, wins 1:1
    # if player wins with blackjack, wins 3:2
    
main()
    