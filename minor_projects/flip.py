import random

# Author Nik Kirstein

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
            if input_money >= bet:
                break
            elif input_money == 0:
                print("Hey! Who are you trying to cheat here!")
            else:
                print("Not enough money, please input a valid bet")
        except:
            print('Please enter a number or "Q"')
            continue  # ignore it, we know its not a number
    return bet


def print_stats(starting_mon, current_mon, num_flips, num_wins, num_loss): 
    """
    Prints the stats for your simulation run of how many money you lost, won, wins, losses, flip numbers, etc.
    Returns None
    """
    print("\nNum Heads:", num_wins, "   |||   Heads percentage: ", str(round((num_wins/num_flips * 100), 3)) + "%")
    print("Num Tails:", num_loss, "   |||   Tails percentage: ", str(round((num_loss/num_flips * 100), 3)) + "%")

    print("Starting Money:", starting_mon, "   |||   ", "Ending Money:", current_mon)
    print("Net end:", (current_mon-starting_mon))
    return 
 

def main():
    money = start_money = int(input("Insert starting money\n"))
    num_flips = int(input("Number of times to play?\n"))
    num_wins = num_loss = 0

    for i in range(num_flips):
        if money == 0:
            print("Out of money")
            break
        print("\nRound: " + str(i+1))
        game_bet = make_bet(money)
        if game_bet == "q" or game_bet == "Q":
            break
        flip = random.randint(1,100)
        print("Rolled a " + str(flip))
        if flip > 51: # change to 50 if you want equal odds.
            print("Heads")
            num_wins += 1
            money += game_bet
            print("New Money:", money)
        else:
            print("Tails")
            num_loss += 1
            money -= game_bet
            print("New Money:", money)
        
    print_stats(start_money, money, num_flips, num_wins, num_loss)
    
main()
