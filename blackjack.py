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
    formatted = []
    for rank, suit in hand:
        card = f"{rank}{SUIT_SYMBOLS[suit]}"
        if dealer:
            formatted.append(colored(card, 'magenta'))
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
        print("\nPilihan Bet:")
        print(f"1. All in({chips} chips)")
        print(f"2. Half ({chips // 2} chips)")
        print(f"3. A quater ({chips // 4} chips)")
        print("4. Custom ")

        choice = input("\nPilih opsi Taruhan (1-4): ").strip()

        if choice == '1':
            bet = chips
        elif choice == '2':
            bet = chips // 2
        elif choice == '3':
            bet = chips // 4
        elif choice == '4':
            while True:
                try:
                    bet = int(input(f"Masukan Taruhan Mu (1-{chips} chips): "))
                    if 1 <= bet <= chips:
                        break
                    else:
                        print("Nilai Invalid. Coba Lagi.")
                except ValueError:
                    print("Input Invalid. Hanya Masukan Dalam Format Nomor.")
        else:
            print("Pilihan Invalid. Coba Lagi")
            continue

        break

    print(f"\nKamu Bertaruh {bet} chips.")

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print("\nYour hand:", format_hand(player_hand), "-> Total:", format_total(calculate_hand_value(player_hand)))
    print(f"{DEALER_NAME} Kartu Terlihat:", format_hand([dealer_hand[0]], dealer=True))

    if calculate_hand_value(dealer_hand) == 21:
        print(f"\n{DEALER_NAME} Mempunyai Blackjack! {DEALER_NAME} Menang.")
        return chips - bet

    player_turn = True
    while True:
        if player_turn:
            choice = input("\n'hit' Atau 'stand'? ").lower()
            if choice == 'hit':
                player_hand.append(deck.pop())
                print("Your hand:", format_hand(player_hand), "-> Total:", format_total(calculate_hand_value(player_hand)))
                if calculate_hand_value(player_hand) > 21:
                    print(f"\n{colored('Player Busted! Dealer Menanf.', 'red')}")
                    return chips - bet
            elif choice == 'stand':
                player_turn = False
            else:
                print("Input Invalid. Coba type 'hit' atau 'stand'.")
                continue

        if not player_turn:
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print(f"\n{DEALER_NAME} hits!")
                print(f"{DEALER_NAME} hand:", format_hand(dealer_hand, dealer=True), "-> Total:", format_total(calculate_hand_value(dealer_hand)))

                if calculate_hand_value(dealer_hand) > 21:
                    print(f"\n{colored('Dealer busted! Kamu Menang!', 'yellow')}")
                    return chips + bet

            print(f"\n{DEALER_NAME} stands.")
            break

    print("\nkedua Player Memilih Stand, Sedang Membuat Hasil...")
    time.sleep(4)

    print("\nHasil Final:")
    print("Your hand:", format_hand(player_hand), "-> Total:", format_total(calculate_hand_value(player_hand)))
    print(f"{DEALER_NAME} hand:", format_hand(dealer_hand, dealer=True), "-> Total:", format_total(calculate_hand_value(dealer_hand)))

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value > dealer_value:
        print(colored("Kamu Menang!", "yellow"))
        return chips + bet
    elif player_value == dealer_value:
        print("Draw!")
        return chips
    else:
        print(colored("Kamu Kalah!", "red"))
        return chips - bet

def format_total(value):
    return colored(f"{value}", "cyan", attrs=["bold"])

def color_chips(chips):
    return colored(f"{chips}", random.choice(CHIP_COLORS), attrs=["bold"])

if __name__ == "__main__":
    print("Selamat Datang Di Blackjack")
    chips = int(input("Masukan Chip Yang Kamu Punya: "))
    
    while chips > 0:
        print(f"\nChips: {color_chips(chips)}")
        chips = blackjack_game(chips)

        if chips <= 0:
            print("\nKamu Kehabisan Chip. Game over!")
            break

        while True:
            play_again = input("\nMain lagi? (yes/no): ").lower()
            if play_again in ['yes', 'no']:
                break
            print("Input Invalid Tolong type 'yes' atau 'no'.")

        if play_again != 'yes':
            print(f"\nTerimakasih Telah Bermain! Kamu Keluar Dengan Chip {color_chips(chips)} chip(s).")
            break
    else:
        print("\nTerimakasih Telah Bermain! Kamu Keluar Dengan 0 chip.")
