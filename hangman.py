from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
import random
from typing import Iterable, List, Sequence, Set, Tuple

HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]

DIFFICULTIES = ("easy", "medium", "hard")
QUESTIONS_PER_LEVEL = 10
PASS_THRESHOLD = 0.80  # 80%
ANSI_RESET = "\x1b[0m"
ANSI_RED = "\x1b[31m"
ANSI_GREEN = "\x1b[32m"
ANSI_YELLOW = "\x1b[33m"
ANSI_CYAN = "\x1b[36m"
ANSI_BLUE = "\x1b[34m"
ANSI_MAGENTA = "\x1b[35m"

LANGUAGE_COLORS = {
    "Python": ANSI_BLUE,
    "Java": ANSI_RED,
    "JavaScript": ANSI_YELLOW,
    "HTML": ANSI_MAGENTA,
    "C#": ANSI_GREEN,
    "Ruby": ANSI_RED,
}


@dataclass(frozen=True)
class Question:
    prompt: str
    answer: str
    difficulty: str


def read_json_file(file_name: str) -> List[Question]:
    path = Path(file_name)
    if not path.exists():
        path = Path(__file__).with_name(file_name)
    with path.open("r", encoding="utf-8") as file:
        raw_items = json.load(file)

    questions: List[Question] = []
    for item in raw_items:
        prompt = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip().lower()
        difficulty = str(item.get("difficulty", "")).strip().lower()
        if not prompt or not answer or difficulty not in DIFFICULTIES:
            continue
        questions.append(Question(prompt=prompt, answer=answer, difficulty=difficulty))

    if not questions:
        raise ValueError("No valid questions found in the JSON file.")

    return questions


def filter_questions_by_difficulty(
    questions: Sequence[Question], difficulty: str
) -> List[Question]:
    return [q for q in questions if q.difficulty == difficulty]


def select_random_questions(
    questions: Sequence[Question], count: int, rng: random.Random
) -> List[Question]:
    if len(questions) <= count:
        return list(questions)
    return rng.sample(list(questions), count)


def choose_hidden_indices(word: str, rng: random.Random) -> Set[int]:
    word_length = len(word)
    if word_length <= 3:
        num_missing = 1
    elif word_length >= 6:
        num_missing = 3
    else:
        num_missing = 2
    return set(rng.sample(range(word_length), num_missing))


def get_user_input() -> str:
    while True:
        user_input = input("Guess a letter: ").strip().lower()
        if len(user_input) != 1 or not user_input.isalpha():
            print(colorize("Invalid input! Please enter a single letter (A-Z).", ANSI_RED))
            continue
        return user_input


def colorize(text: str, color: str, enabled: bool = True) -> str:
    if not enabled:
        return text
    return f"{color}{text}{ANSI_RESET}"


def render_word(word: str, revealed_indices: Set[int], colorize_output: bool = True) -> str:
    placeholder = colorize("_", ANSI_YELLOW, colorize_output)
    return "".join(word[i] if i in revealed_indices else placeholder for i in range(len(word)))


def colorize_hangman(pic: str, enabled: bool = True) -> str:
    if not enabled:
        return pic
    colored = (
        pic.replace("O", colorize("O", ANSI_RED))
        .replace("|", colorize("|", ANSI_RED))
        .replace("/", colorize("/", ANSI_RED))
        .replace("\\", colorize("\\", ANSI_RED))
    )
    return colored


def show_answer(
    correct_word: str, revealed_indices: Set[int], colorize_output: bool = True
) -> bool:
    obscured_word = render_word(correct_word, revealed_indices, colorize_output)
    print("Current word:", obscured_word)
    return obscured_word == correct_word


def ask_file_name() -> str:
    while True:
        print("What programming language would you like to play?")
        print(f"1. {colorize('Python', LANGUAGE_COLORS['Python'])}")
        print(f"2. {colorize('Java', LANGUAGE_COLORS['Java'])}")
        print(f"3. {colorize('JavaScript', LANGUAGE_COLORS['JavaScript'])}")
        print(f"4. {colorize('HTML', LANGUAGE_COLORS['HTML'])}")
        print(f"5. {colorize('C#', LANGUAGE_COLORS['C#'])}")
        print(f"6. {colorize('Ruby', LANGUAGE_COLORS['Ruby'])}")
        
        choice = input("Enter the number corresponding to your choice: ")
        
        if choice == '1':
            return "python.json"
        elif choice == '2':
            return "java.json"
        elif choice == '3':
            return "javascript.json"
        elif choice == '4':
            return "html.json"
        elif choice == '5':
            return "csharp.json"
        elif choice == '6':
            return "ruby.json"
        else:
            print(
                colorize(
                    "Invalid choice. Please enter a number from 1 to 6 corresponding to the programming language.",
                    ANSI_RED,
                )
            )


def play_level(questions: Sequence[Question], difficulty: str, rng: random.Random) -> int:
    print(f"\nStarting {difficulty.capitalize()} Level ({QUESTIONS_PER_LEVEL} Questions)")
    correct_answers = 0
    total_questions = QUESTIONS_PER_LEVEL

    selected = select_random_questions(questions, total_questions, rng)

    for i, question in enumerate(selected, start=1):
        print(f"\nQuestion {i}:", question.prompt)

        answer = question.answer

        hidden_indices = choose_hidden_indices(answer, rng)
        revealed_indices = set(range(len(answer))) - hidden_indices
        attempts = len(hidden_indices) + 2
        original_attempts = attempts
        guessed_letters: Set[str] = set()

        while attempts > 0:
            if show_answer(answer, revealed_indices):
                print("Well done! You guessed the word!")
                correct_answers += 1
                break

            user_input = get_user_input()

            if user_input in guessed_letters:
                print(colorize(f"You already guessed '{user_input}'. Try another letter.", ANSI_RED))
                continue
            guessed_letters.add(user_input)

            if user_input in answer:
                # Reveal all instances of the guessed letter
                revealed_indices.update(index for index, letter in enumerate(answer) if letter == user_input)
                print(colorize(f"Correct! '{user_input}' is in the word.", ANSI_GREEN))
            else:
                print(colorize(f"'{user_input}' is not in the word.", ANSI_RED))
                attempts -= 1
                mistakes_made = (original_attempts - attempts)
                stage_index = min(len(HANGMAN_PICS) - 1, mistakes_made * (len(HANGMAN_PICS) - 1) // original_attempts)
                print(colorize_hangman(HANGMAN_PICS[stage_index]))
                print(f"Remaining attempts: {attempts}")
        
        if attempts == 0:
            print(f"Out of attempts! The correct word was: {answer}")

    print(f"\nYou got {correct_answers} out of {len(selected)} correct in the {difficulty} level!")
    return correct_answers


def play_all_levels(all_questions: Sequence[Question], rng: random.Random) -> int:
    total_score = 0
    required_to_pass = math.ceil(QUESTIONS_PER_LEVEL * PASS_THRESHOLD)

    # Play Easy Level
    easy_questions = filter_questions_by_difficulty(all_questions, "easy")
    easy_score = play_level(easy_questions, "easy", rng)
    if easy_score >= required_to_pass:
        total_score += easy_score
        # Play Medium Level
        medium_questions = filter_questions_by_difficulty(all_questions, "medium")
        medium_score = play_level(medium_questions, "medium", rng)
        if medium_score >= required_to_pass:
            total_score += medium_score
            # Play Hard Level
            hard_questions = filter_questions_by_difficulty(all_questions, "hard")
            hard_score = play_level(hard_questions, "hard", rng)
            if hard_score >= required_to_pass:
                total_score += hard_score
                print("\nCongratulations! You completed all levels!")
            else:
                print("\nYou did not score enough to complete the hard level.")
        else:
            print("\nYou did not score enough to complete the medium level.")
    else:
        print("\nYou did not score enough to complete the easy level.")

    return total_score


def run_game(file_name: str, rng: random.Random) -> None:
    all_questions = read_json_file(file_name)
    total_score = play_all_levels(all_questions, rng)

    print("\nGame Over! Your total score is:", total_score)

if __name__ == "__main__":
    rng = random.Random()
    words_file = ask_file_name()
    try:
        run_game(words_file, rng)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"Unable to start game: {exc}")
