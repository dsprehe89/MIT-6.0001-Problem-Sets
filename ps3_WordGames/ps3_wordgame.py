# This game was created based on the MIT Opencourseware 6.0001 - Problem Set 3
# https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/
#
# Creator: Daniel Sprehe
# Date: 4/10/2020
# Word Game
# -----------------------------------

import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3,
    'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# Imports a word list from the file 'word_games_words.txt'
WORDLIST_FILENAME = "ps3_word_games_words.txt"


# Returns a list of valid words. Words are strings of lowercase letters.
def load_words():
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


# Returns a dictionary where keys are letters and values are number of times that letter is in represented
def get_frequency_dict(sequence):
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# Problem #1: Scoring a word
def get_word_score(word, n):
    word_score1 = 0
    for letter in word.lower():
        word_score1 += SCRABBLE_LETTER_VALUES[letter]

    word_score2 = 7 * len(word) - 3 * (n-len(word))
    if word_score2 < 1:
        word_score2 = 1

    return word_score1 * word_score2


# Displays the letters currently in the hand.
def display_hand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


# You will need to modify this for Problem #4.
# Returns a random hand containing n lowercase letters.
def deal_hand(n):
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    hand['*'] = 1

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


# Problem #2: Update a hand by removing letters
# Uses up the letters in the given word and returns the new hand.
def update_hand(hand, word):
    new_hand = dict(hand)
    for letter in word.lower():
        new_hand[letter] = new_hand.get(letter, 0) - 1
        if new_hand[letter] < 1:
            new_hand.pop(letter)
    return new_hand


# Problem #3: Test word validity
# Returns True if word is in the word_list and is entirely composed of letters in the hand.
def is_valid_word(word, hand, word_list):
    test_hand = dict(hand)
    if '*' not in word:
        if word.lower() not in word_list:
            return False
    else:
        test_word = word
        test_case = False
        for letter in VOWELS:
            test_word = word.replace('*', letter)
            if test_word in word_list:
                test_case = True
        if not test_case:
            return False

    for letter in word.lower():
        test_hand[letter] = test_hand.get(letter, 0) - 1
        if test_hand[letter] < 0:
            return False

    return True


# Problem #5: Playing a hand
def calculate_handlen(hand):
    total = 0
    for value in hand.values():
        total += value
    return total


# Allows the user to play the given hand
def play_hand(hand, word_list):
    # Keep track of the total score
    total_score = 0

    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) != 0:

        # Display the hand
        print('\nCurrent Hand:', end=' ')
        display_hand(hand)

        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')

        # If the input is two exclamation points:
        if word == '!!':
            break

        # Otherwise (the input is not two exclamation points):
        else:

            # If the word is valid:
            if is_valid_word(word, hand, word_list):

                # Tell the user how many points the word earned,
                # and the updated total score
                score = get_word_score(word, calculate_handlen(hand))
                total_score += score
                print(f'"{word}" earned {score} points. Total: {total_score} points.\n')

            # Otherwise (the word is not valid):
            # Reject invalid word (print a message)
            else:
                print('That is not a valid word. Please choose another word.\n')

            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
            if calculate_handlen(hand) == 0:
                print('Ran out of letters.')

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print(f'Total score for this hand: {total_score} points')
    print('-'*10)

    # Return the total score as result of function
    return total_score


# Problem #6.1: Substituting a single letter from your hand
def substitute_hand(hand, letter):
    if letter.lower() not in hand:
        print('You did not have that letter in your hand to substitute')
        return hand

    num_letter = hand.pop(letter)

    while True:
        if letter in VOWELS:
            new_letter = random.choice(VOWELS)
        else:
            new_letter = random.choice(CONSONANTS)
        if (new_letter not in hand) and (new_letter != letter):
            break

    hand[new_letter] = num_letter
    return hand


# Problem #6.2: Playing a game
def play_game(word_list):
    total_score = 0
    i = 0
    # How many hands are we playing?
    num_hands = int(input('\nEnter total number of hands: '))

    # Generate the first hand
    hand = deal_hand(HAND_SIZE)

    while True:
        # Show the hand
        print('Current hand:', end=' ')
        display_hand(hand)

        # Make any substitutions.
        sub = input('\nWould you like to substitute a letter? ')
        if sub.lower() == 'yes':
            sub_letter = input('Which letter would you like to replace: ')
            hand = substitute_hand(hand, sub_letter)

        # Play the hand
        total_score += play_hand(hand, word_list)
        i += 1

        # Break out of loop if num_hands is reached
        if i == num_hands:
            break

        # Play the same hand or generate a new hand
        new_hand = input('\nWould you like ot replay the hand? ')
        if new_hand == 'yes':
            continue
        hand = deal_hand(HAND_SIZE)

    print(f'Total score over all hands: {total_score}')


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
