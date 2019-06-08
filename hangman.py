import json
import string
from random import choice

_dictionary = []
_alpha = list(string.ascii_lowercase)
_used_words = []
_current_word = []
_current_state = ""
_guesses = []
_wrong = 0

def load_file():
    f = open('words_dictionary.json', 'r')
    dictionary_json = f.read()
    f.close()
    return list(json.loads(dictionary_json).keys())

def init():
    _current_word = []
    _current_state = ""
    _guesses = []
    _wrong = 0

def greet():
    print("""\
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    |                                           |
    |                                           |
    |                   Hangman...             _O_
    |                                           H
    |                                          / \\
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """)

def display_rules():
    print("""
    To play:
        1) Enter a letter
        2) Press enter
        3) You lose if the man dies
    """)

def replay():
    question = "Would you like to play again?"
    selected = input("{} (y, yes, n, no)\n".format(question))
    invalid = selected.lower() not in ['y','yes','n','no']
    if invalid:
        print("""Invalid input...
        Please enter one of: y, yes, n, no
        """)
    return selected in ['y','yes']

def select_word():
    new_word = False
    while not new_word:
        word = choice(_dictionary)
        new_word = word not in _used_words and len(word) > 3
    return word

def print_game():
    print("\n{}\n".format(" ".join(_current_state)))
    print("Guessed letters: {}".format(" ".join(_guesses)))
    print("Guesses left: {}".format(6 - _wrong))

def handle_choice():
    global _guesses, _wrong, _current_state
    invalid = True
    while invalid:
        ch = input("Enter a letter...\n")
        invalid = ch.lower() not in _alpha or ch.lower() in _guesses
        if invalid:
            print("\nInvalid input...\nPlease enter a letter not already guessed\nGuesses: {0}".format(" ".join(_guesses)))
    _guesses += [ch]
    if ch in _current_word:
        for i, ltr in enumerate(_current_word):
            if ltr == ch:
                _current_state[i] = ch
    else:
        _wrong += 1

if __name__ == "__main__":
    _dictionary = load_file()
    done = False
    greet()
    display_rules()
    while not done:
        init()
        finished = False
        _current_word = select_word()
        _current_state = ["_"] * len(_current_word)
        print('\n===================================\n')
        while not finished:
            print_game()
            handle_choice()
            win = "_" not in _current_state
            finished = _wrong == 6 or win
        if win:
            print("You Win!")
            print("The word was {}".format(_current_word))
        else:
            print("You Lost...")
            print("The word was {}".format(_current_word))
        done = not replay()