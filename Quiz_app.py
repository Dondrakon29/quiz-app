import json
from datetime import datetime

def load_questions():
    try:
        with open("questions.json", "r") as file:
            questions = json.load(file)

        return questions

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []    


questions = load_questions()

def load_results():
    try:
        with open("results.json", "r") as file:
            results = json.load(file)

        return results

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def save_results(results):
    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)


def save_quiz_result(score, total_questions, percent):
    results = load_results()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    result = {
        "score": score,
        "total": total_questions,
        "percent": percent,
        "date": current_date 
    }

    results.append(result)
    save_results(results)


def show_results():
    results = load_results()

    if not results:
        print("No results yet")
        return

    print("Attempt history:")

    for index, result in enumerate(results, start=1):
        date = result.get("date", "no date")

        print(f'{index}. {result["score"]}/{result["total"]} | {result["percent"]}% | {date}')    

def get_user_answer(question):
    options_count = len(question["options"])

    while True:
        user_answer = input("Your answer: ").strip()

        try:
            number = int(user_answer)
        except ValueError:
            print("Answer must be a number")
            continue

        if number < 1 or number > options_count:
            print(f"Choose a number from 1 to {options_count}")
            continue

        return user_answer    


def show_question(index, question, total_questions):
    print(f"Question {index}/{total_questions}")
    print(question["question"])

    for option in question["options"]:
        print(option)



def check_answer(question, user_answer):
    if user_answer == question["answer"]:
        print("Correct!")
        return True
    
    print("Wrong!")

    correct_index = int(question["answer"]) - 1
    correct_option = question["options"][correct_index]

    print("Correct answer:", correct_option)

    return False


def get_result_message(percent):
    if percent == 100:
        return "Excellent!"
    elif percent >= 60:
        return "Good job!"
    else:
        return "Keep practicing!"


def show_menu():
    print("1 - Start quiz")
    print("2 - Show results")
    print("0 - Exit")


def run_quiz(questions):
      
    if not questions:
        print("No questions found")
        return
    
    score = 0
    total_questions = len(questions)

    print("Welcome to Quiz App!")
    print(f"You have {total_questions} questions.")
    print("Choose the correct answer number.")
    print()

    for index, question in enumerate(questions, start=1):
        show_question(index, question, total_questions)
        
        
        user_answer = get_user_answer(question)

        if check_answer(question, user_answer):
            score += 1

        print()

    percent = round(score / total_questions * 100)
    result_message = get_result_message(percent)    

    print("Quiz finished")
    print(f"Your score: {score}/{total_questions}")
    print(f"Result: {percent}%")
    print(result_message)

    save_quiz_result(score, total_questions, percent)

    print("Result saved")
    print()

    show_results()

    print()
    print("Returning to menu...")


def run_app():
    while True:
        show_menu()

        choice = input("Choose option: ").strip()

        if choice == "1":
            run_quiz(questions)
        elif choice == "2":
            show_results()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Wrong choice")

        print()

if __name__ == "__main__":
    run_app()                                  


    