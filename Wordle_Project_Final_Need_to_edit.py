import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase

from rich.console import Console
from rich.theme import Theme

custom_console = Console(width=40, theme=Theme({"alert": "red on yellow"}))

LETTER_COUNT = 5
MAX_GUESSES = 5
WORDS_FILE_PATH = pathlib.Path(__file__).parent / "wordlist.txt"


def start_game():
    # Pre-process
    selected_word = pick_random_word(WORDS_FILE_PATH.read_text(encoding="utf-8").split("\n"))
    player_guesses = ["_" * LETTER_COUNT] * MAX_GUESSES

    # Process (main loop)
    with contextlib.suppress(KeyboardInterrupt):
        for idx in range(MAX_GUESSES):
            update_display(headline=f"Guess {idx + 1}")
            show_current_guesses(player_guesses, selected_word)

            player_guesses[idx] = make_guess(previous_guesses=player_guesses[:idx])
            if player_guesses[idx] == selected_word:
                break

    # Post-process
    end_game(player_guesses, selected_word, guessed_correctly=player_guesses[idx] == selected_word)


def update_display(headline):
    custom_console.clear()
    custom_console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")


def pick_random_word(word_list):
    valid_words = [
        word.upper()
        for word in word_list
        if len(word) == LETTER_COUNT
        and all(letter in ascii_letters for letter in word)
    ]
    if valid_words:
        return random.choice(valid_words)
    else:
        custom_console.print(
            f"No words of length {LETTER_COUNT} in the word list",
            style="alert",
        )
        raise SystemExit()


def show_current_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    Letter_List = []
    COUNT =0
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
                
                if letter not in Letter_List:
                    COUNT = COUNT + 10
                Letter_List.append(letter)

            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        custom_console.print("".join(styled_guess), justify="center")
    custom_console.print("\n" + "Your Score: " , COUNT )
    custom_console.print("\n" + "".join(letter_status.values()), justify="center")
    
    
        



def make_guess(previous_guesses):
    guess_input = custom_console.input("\nGuess word: ").upper()

    if guess_input in previous_guesses:
        custom_console.print(f"You've already guessed {guess_input}.", style="alert")
        return make_guess(previous_guesses)

    if len(guess_input) != LETTER_COUNT:
        custom_console.print(
            f"Your guess must be {LETTER_COUNT} letters.", style="alert"
        )
        return make_guess(previous_guesses)

    if any((invalid := letter) not in ascii_letters for letter in guess_input):
        custom_console.print(
            f"Invalid letter: '{invalid}'. Please use English letters.",
            style="alert",
        )
        return make_guess(previous_guesses)

    return guess_input


def end_game(guesses, word, guessed_correctly):
    update_display(headline="Game Over")
    show_current_guesses(guesses, word)

    if guessed_correctly:
        custom_console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        custom_console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")
    
        


if __name__ == "__main__":
    start_game()
