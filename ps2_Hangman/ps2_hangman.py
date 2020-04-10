# This game was created based on the MIT Opencourseware 6.0001 - Problem Set 2
# https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/
#
# Creator: Daniel Sprehe
# Date: 4/8/2020
# Hangman Game
# -----------------------------------

import random
import string
from os import system

WORDLIST_FILENAME = "ps2_hangman_words.txt"


def clear_screen(): return system('cls')


def load_words():
    """
    Returns a list of valid words. All sords are strings of lowercase letters.

    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word_guessed(secret_word, letters_guessed):
    for i in secret_word:
        if i not in letters_guessed:
            return False
    return True


def show_guessed_word(secret_word, letters_guessed, num_guesses, num_warnings):
    clear_screen()
    shown_word = ''
    word = ''
    for i in secret_word:
        if i in letters_guessed:
            shown_word += i + ' '
            word += i
        else:
            shown_word += '_ '
            word += '_'
    print('\n\n')
    print(f'The secret word looks like:  "{shown_word}"')
    print()
    hangman_printout(num_guesses, num_warnings)
    print()
    return word


def get_available_letters(letters_guessed):
    all_letters = string.ascii_lowercase
    available_letters = ''
    for i in all_letters:
        if i not in letters_guessed:
            available_letters += i + ' '

    available_letters = available_letters[:-1]
    return available_letters


def game_start():
    print('\n\nWelcome to the Hangman Game!\n')
    print('The rules are simple, guess a letter from the available list.')
    print('    - Guess wrong 6 times or guess 3 unavailable letters/characters and you lose')
    print('    - Fully guess the secret word and you win.\n')
    print('------------------------------------------------\n')
    print('We have 2 versions of the game, one is normal difficulty and one is easier.')
    print('After 5 incorrect guesses the easier version will start giving you hints.')

    while True:
        play = input('Which would you like to play (easy/hard)?  ')
        if play.lower() == 'easy' or play.lower() == 'hard':
            break
        else:
            play = input('That was not a valid entry. Try again (easy/hard)?  ')

    return play


def hangman_printout(num_guesses, num_warnings):
    if num_guesses == 0:
        print('__________')
        print('|         |')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|_____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 1:
        print('__________')
        print('|         |')
        print('|         O')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|_____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 2:
        print('__________')
        print('|         |')
        print('|         O')
        print('|         | ')
        print('|')
        print('|')
        print('|')
        print('|_____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 3:
        print('__________')
        print('|         |')
        print('|         O')
        print('|        /|')
        print('|')
        print('|')
        print('|')
        print('|_____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 4:
        print('__________')
        print('|         |')
        print('|         O')
        print('|        /|\\')
        print('|')
        print('|')
        print('|')
        print('|____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 5:
        print('__________')
        print('|         |')
        print('|         O')
        print('|        /|\\')
        print('|         |')
        print('|')
        print('|')
        print('|_____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 6:
        print('__________')
        print('|         |')
        print('|         O')
        print('|        /|\\')
        print('|         |')
        print('|        /')
        print('|')
        print('|_____________')
        print()
        print(f'You have {7-num_guesses} guesses and {3 - num_warnings} warnings left.')

    elif num_guesses == 7:
        print('__________')
        print('|         |')
        print('|         O')
        print('|        /|\\')
        print('|         |')
        print('|        / \\')
        print('|')
        print('|_____________')
        print()
        print('You lose')


def get_user_guess(letters_guessed, num_warnings):
    available_letters = get_available_letters(letters_guessed)

    print('The letters available to guess from are:')
    print(f'-"{available_letters}"')
    print()
    print(f'You have already guessed: "{user_guessed_letters(letters_guessed)}"')
    letter = input('What would you like to guess: ').lower()

    while letter not in available_letters:
        num_warnings += 1
        if num_warnings == 3:
            break
        print(f'You have {3-num_warnings} warnings left.')
        letter = input('That was not a valid guess. Try Again: ').lower()

    return letter, num_warnings


def user_guessed_letters(letters_guessed):
    letters = ''
    for letter in letters_guessed:
        letters += letter + ', '
    letters = letters[:-2]
    return letters


def match_with_gaps(my_word, other_word):
    for i in range(len(my_word)):
        if my_word[i] != '_' and my_word[i] != other_word[i]:
            return False
    return True


def short_wordlist(secret_word, wordlist):
    possible_words = []
    for word in wordlist:
        if len(word) == len(secret_word):
            possible_words.append(word)
    return possible_words


def show_possible_matches(my_word, wordlist):
    possible_words = ''
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_words += word + ', '
    possible_words = possible_words[:-2]
    print("The below words could be the secret word")
    print(f'- {possible_words}')
    print()


def hangman_with_hints():
    wordlist = load_words()
    secret_word = random.choice(wordlist)
    wordlist = short_wordlist(secret_word, wordlist)
    num_guesses = 0
    num_warnings = 0
    letters_guessed = []

    word = show_guessed_word(secret_word, letters_guessed, num_guesses, num_warnings)

    while True:
        letter, num_warnings = get_user_guess(letters_guessed, num_warnings)
        letters_guessed.append(letter)

        if letter not in secret_word:
            num_guesses += 1

        word = show_guessed_word(secret_word, letters_guessed, num_guesses, num_warnings)

        if num_guesses > 4:
            show_possible_matches(word, wordlist)

        # Did the user guess the word or use up all their guesses/warnings?
        if is_word_guessed(secret_word, letters_guessed):
            print('Congrats, you guessed the secret word')
            break
        if num_guesses >= 7:
            print(f'The secret word was \'{secret_word}\'.')
            break
        elif num_warnings >= 3:
            print('You were warned, now you lose')
            break


def hard_hangman():
    wordlist = load_words()
    secret_word = random.choice(wordlist)
    num_guesses = 0
    num_warnings = 0
    letters_guessed = []

    show_guessed_word(secret_word, letters_guessed, num_guesses, num_warnings)

    while True:
        letter, num_warnings = get_user_guess(letters_guessed, num_warnings)
        letters_guessed.append(letter)

        if letter not in secret_word:
            num_guesses += 1

        show_guessed_word(secret_word, letters_guessed, num_guesses, num_warnings)

        # Did the user guess the word or use up all their guesses/warnings?
        if is_word_guessed(secret_word, letters_guessed):
            print('Congrats, you guessed the secret word')
            break
        if num_guesses >= 7:
            print(f'The secret word was \'{secret_word}\'.')
            break
        elif num_warnings >= 3:
            print('You were warned, now you lose')
            break


def hangman():
    game = game_start()
    if game == 'easy':
        hangman_with_hints()
    elif game == 'hard':
        hard_hangman()


hangman()
