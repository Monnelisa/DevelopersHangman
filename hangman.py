import random
import json
import speech_recognition as sr



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
    if word_length <= 3:
        num_missing = 1
    elif word_length > 6:
        num_missing = 3
    else:
        num_missing = 2

    letters_indices = random.sample(range(word_length), num_missing)
    word_list = list(word)
    
    for index in letters_indices:
        word_list[index] = ' _ '
    
    obscured_word = ''.join(word_list)
    print('Guess the word: ' + obscured_word)
    
    return letters_indices


def get_user_input():
    return input('Complete the word: ')


def show_answer(user_word, correct_word):
    if user_word == correct_word:
        print("The word was:", correct_word)
        print("Well done! You got it right!")
        return True
    else:
        print("The word was:", correct_word)
        print("Wrong! Try better next time.")
        return False


def ask_file_name():
    while True:
        choice = input("What programing language would you like to play? 1 for Python, 2 for Java): ")
        if choice == '1':
            return "python.json"
        elif choice == '2':
            return "java.json"
        else:
            print("Invalid choice. Please enter 1 for Python or 2 for Java.")


def play_level(questions, difficulty):
    print(f"\nStarting {difficulty.capitalize()} Level (10 Questions)")
    correct_answers = 0
    total_questions = 10

    for i in range(total_questions):
        question = select_random_question(questions)
        print("\nQuestion:", question['question'])

        answer = question['answer']
        select_random_letters_from(answer)

        user_input = get_user_input()
        if show_answer(user_input, answer):
            correct_answers += 1

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
