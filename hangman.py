import random
import json

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

def read_json_file(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def filter_questions_by_difficulty(questions, difficulty):
    return [q for q in questions if q['difficulty'] == difficulty]

def select_random_question(questions):
    random_index = random.randint(0, len(questions) - 1)
    selected_question = questions.pop(random_index)  # Remove the selected question to avoid repetition
    return selected_question

def select_random_letters_from(word):
    word_length = len(word)
    
    # Determine number of letters to hide based on word length
    if word_length <= 3:
        num_missing = 1
    elif word_length >= 6:
        num_missing = 3
    else:
        num_missing = 2

    # Randomly select indices to hide letters
    letters_indices = random.sample(range(word_length), num_missing)
    word_list = list(word)
    
    # Replace selected letters with underscores
    for index in letters_indices:
        word_list[index] = '_'
    
    obscured_word = ''.join(word_list)
    print('Guess the word:', obscured_word)
    
    return letters_indices

def get_user_input():
    return input('Guess a letter: ').strip().lower()

def show_answer(correct_word, revealed_indices):
    obscured_word = ''.join([correct_word[i] if i in revealed_indices else '_' for i in range(len(correct_word))])
    print("Current word:", obscured_word)
    return obscured_word == correct_word  # True if fully revealed

def ask_file_name():
    while True:
        print("What programming language would you like to play?")
        print("1. Python")
        print("2. Java")
        print("3. JavaScript")
        print("4. HTML")
        print("5. C#")
        print("6. Ruby")
        
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
            print("Invalid choice. Please enter a number from 1 to 6 corresponding to the programming language.")

def play_level(questions, difficulty):
    print(f"\nStarting {difficulty.capitalize()} Level (10 Questions)")
    correct_answers = 0
    total_questions = 10

    for i in range(total_questions):
        question = select_random_question(questions)
        print("\nQuestion:", question['question'])
        
        answer = question['answer'].lower()
        
        #Hide letters based on word length rules
        hidden_indices = select_random_letters_from(answer)  # returns list of indices to hide
        revealed_indices = set(range(len(answer))) - set(hidden_indices)        
        attempts = len(hidden_indices) + 2        
        original_attempts = attempts

        while attempts > 0:
            if show_answer(answer, revealed_indices):
                print("Well done! You guessed the word!")
                correct_answers += 1
                break
            
            user_input = get_user_input()

            if len(user_input) != 1 or not user_input.isalpha():
                    print("Invalid input! Please enter a single letter (A-Z).")
                    continue

            if user_input in answer:
                # Reveal all instances of the guessed letter
                revealed_indices.update(index for index, letter in enumerate(answer) if letter == user_input)
                print(f"Correct! '{user_input}' is in the word.")
            else:
                print(f"'{user_input}' is not in the word.")
                attempts -= 1
                mistakes_made = (original_attempts - attempts)
                stage_index = min(len(HANGMAN_PICS) - 1, mistakes_made * (len(HANGMAN_PICS) - 1) // original_attempts)
                print(HANGMAN_PICS[stage_index])
                print(f"Remaining attempts: {attempts}")
        
        if attempts == 0:
            print(f"Out of attempts! The correct word was: {answer}")

    print(f"\nYou got {correct_answers} out of {total_questions} correct in the {difficulty} level!")
    return correct_answers

def play_all_levels(all_questions):
    total_score = 0

    # Play Easy Level
    easy_questions = filter_questions_by_difficulty(all_questions, 'easy')
    easy_score = play_level(easy_questions, 'easy')
    if easy_score >= 8:  # 80% of 10 questions
        total_score += easy_score
        # Play Medium Level
        medium_questions = filter_questions_by_difficulty(all_questions, 'medium')
        medium_score = play_level(medium_questions, 'medium')
        if medium_score >= 8:  # 80% of 10 questions
            total_score += medium_score
            # Play Hard Level
            hard_questions = filter_questions_by_difficulty(all_questions, 'hard')
            hard_score = play_level(hard_questions, 'hard')
            if hard_score >= 8:  # 80% of 10 questions
                total_score += hard_score
                print("\nCongratulations! You completed all levels!")
            else:
                print("\nYou did not score enough to complete the hard level.")
        else:
            print("\nYou did not score enough to complete the medium level.")
    else:
        print("\nYou did not score enough to complete the easy level.")

    return total_score

def run_game(file_name):
    # Load questions from the selected JSON file
    all_questions = read_json_file(file_name)

    # Play all levels
    total_score = play_all_levels(all_questions)

    print("\nGame Over! Your total score is:", total_score)

if __name__ == "__main__":
    words_file = ask_file_name()
    run_game(words_file)
