# Developers Hangman Game

Welcome to the Developers Hangman Game! This is an interactive word-guessing game designed for developers and programming enthusiasts to test and expand their knowledge of programming languages and terminology.

## Features

- Interactive gameplay with programming language-related words.
- Words have missing letters for players to guess.
- Progressive difficulty levels from Easy to Hard.
- Minimum score of 80% required to advance to the next level.
- User-friendly interface (currently terminal-based).
- Colorized UI feedback: language options use signature colors, correct guesses are green, and mistakes/invalid inputs are red.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Monnelisa/DevelopersHangman.git
   ```
1. Navigate to the project directory:
   ```bash
   cd DevelopersHangman
   ```
1. Open the project in your preferred code editor.

## Usage

Currently, the game is terminal-based. To play, run the following command:

```bash
python hangman.py
```

## Gameplay

- Players will see underscores representing the missing letters of a word.
- Players guess one letter at a time.
- If a player guesses the word before running out of attempts, they win.
- Players need to meet the minimum score requirement to advance to the next level.

## Levels

The game has three difficulty levels:

- Easy: Basic programming terms and concepts.
- Medium: Intermediate programming concepts and terms.
- Hard: Advanced programming terminology.

Players must achieve at least 80% accuracy to progress through each level.

## Testing

Tests use `pytest`.

```bash
python -m pytest
```

## Project Structure

- `hangman.py`: Game logic and CLI entry point.
- `tests/test_hangman.py`: Unit tests for core game functions.
- `*.json`: Question banks for each programming language.

## Technologies Used

- Python
- JSON

## Project Plan

See `PROJECT_PLAN.md` for the phased improvement plan.

