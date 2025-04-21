import random
import time
from termcolor import colored
from colorama import init

# Inisialisasi Colorama
init()

# Simbol untuk kartu
SUIT_SYMBOLS = {
    'Hearts': '♥',
    'Diamonds': '♦',
    'Clubs': '♣',
    'Spades': '♠'
}

# Warna simbol
SUIT_COLORS = {
    'Hearts': 'red',
    'Diamonds': 'blue',
    'Clubs': 'green',
    'Spades': 'yellow'
}

DEALER_NAME = colored("Dealer", "magenta")

# Warna acak untuk chip
CHIP_COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    return deck

def format_hand(hand, dealer=False):
    """Format kartu untuk tampilan dengan warna."""
    formatted = []
    for rank, suit in hand:
        card = f"{rank}{SUIT_SYMBOLS[suit]}"
        if dealer:
            formatted.append(colored(card, 'magenta'))  # Kartu dealer berwarna ungu
        else:
            formatted.append(colored(card, SUIT_COLORS[suit]))
    return ' '.join(formatted)

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card, _ in hand:
        if card in ['Jack', 'Queen', 'King']:
            value += 10
        elif card == 'Ace':
            aces += 1
            value += 11
        else:
            value += int(card)

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

def blackjack_game(chips):
    deck = create_deck()
    random.shuffle(deck)

    while True:
        bet = int(input(f"\nEnter your bet (1-{chips} chips): "))
        if 1 <= bet <= chips:
            break
        print(f"Invalid bet! You only have {chips} chips.")

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print("\nYour hand:", format_hand(player_hand), "-> Total:", format_total(calculate_hand_value(player_hand)))
    print(f"{DEALER_NAME}'s visible card:", format_hand([dealer_hand[0]], dealer=True))

    if calculate_hand_value(dealer_hand) == 21:
        print(f"\n{DEALER_NAME} has Blackjack! {DEALER_NAME} wins.")
        return chips - bet

    player_turn = True
    while True:
        if player_turn:
            choice = input("\nDo you want to 'hit' or 'stand'? ").lower()
            if choice == 'hit':
                player_hand.append(deck.pop())
                print("Your hand:", format_hand(player_hand), "-> Total:", format_total(calculate_hand_value(player_hand)))
                if calculate_hand_value(player_hand) > 21:
                    print(f"\n{colored('You busted! Dealer wins.', 'red')}")
                    return chips - bet
            elif choice == 'stand':
                player_turn = False
            else:
                print("Invalid input. Please type 'hit' or 'stand'.")
                continue

        if not player_turn:
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print(f"\n{DEALER_NAME} hits!")
                print(f"{DEALER_NAME}'s hand:", format_hand(dealer_hand, dealer=True), "-> Total:", format_total(calculate_hand_value(dealer_hand)))

                if calculate_hand_value(dealer_hand) > 21:
                    print(f"\n{colored('Dealer busted! You win!', 'yellow')}")
                    return chips + bet

            print(f"\n{DEALER_NAME} stands.")
            break

    # Tambahkan jeda sebelum mengungkapkan hasil akhir
    print("\nBoth players have chosen to stand. Revealing results...")
    time.sleep(2)  # Jeda 2 detik

    print("\nFinal Results:")
    print("Your hand:", format_hand(player_hand), "-> Total:", format_total(calculate_hand_value(player_hand)))
    print(f"{DEALER_NAME}'s hand:", format_hand(dealer_hand, dealer=True), "-> Total:", format_total(calculate_hand_value(dealer_hand)))

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value > dealer_value:
        print(colored("You win!", "yellow"))
        return chips + bet
    elif player_value == dealer_value:
        print("It's a tie!")
        return chips
    else:
        print(colored("You lose!", "red"))
        return chips - bet

def format_total(value):
    """Format total kartu dengan warna cyan dan bold (tanpa garis)."""
    return colored(f"{value}", "cyan", attrs=["bold"])

def color_chips(chips):
    """Menghasilkan warna acak untuk chip yang ditampilkan."""
    return colored(f"{chips}", random.choice(CHIP_COLORS), attrs=["bold"])

if __name__ == "__main__":
    print("Welcome to Blackjack!")
    chips = int(input("Enter the number of chips you want to start with: "))
    
    while chips > 0:
        print(f"\nCurrent chips: {color_chips(chips)}")
        chips = blackjack_game(chips)

        if chips <= 0:
            print("\nYou have run out of chips. Game over!")
            break

        while True:
            play_again = input("\nDo you want to play again? (yes/no): ").lower()
            if play_again in ['yes', 'no']:
                break
            print("Invalid input. Please type 'yes' or 'no'.")

        if play_again != 'yes':
            print(f"\nThanks for playing! You leave with {color_chips(chips)} chip(s).")
            break
    else:
        print("\nThanks for playing! You leave with 0 chips.")
