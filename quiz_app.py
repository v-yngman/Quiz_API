from typing import List, Tuple
import requests
from question import Question

# python quiz_app.py

def url(route: str):
    base_url = "http://127.0.0.1:8000"
    return base_url + route


def questions_dict():
    questions_dict = {
        "category": "",
        "question": "",
        "answer_1": "",
        "answer_2": "",
        "answer_3": "",
        "answer_4": "",
        "correct_answer": "" 
        }
    return questions_dict


print("Hello from quiz app")


# User menu
def print_menu():
    print("""
    1: Fetch all Questions
    2: Add Question
    3: Update Question
    4: Delete Question
    5: Exit
    """)


# Fetch all avaiable questions
def fetchall_questions():
    print("Fetching all Questions")
    questions_list = []
    res = requests.get(url("/questions"))
    for question in res.json():
        question = Question(**question)
        questions_list.append(question)
    return questions_list


def print_questions(questions_list: List[Question]):
    for question in questions_list:
        print("_________________")
        print(f"ID: {question.id}")
        print(f"Category: {question.category}")
        print(f"Question: {question.question}")
        print(f"Answer_1: {question.answer_1}")
        print(f"Answer_2: {question.answer_2}")
        print(f"Answer_3: {question.answer_3}")
        print(f"Answer_4: {question.answer_4}")
        print(f"Correct_Answer: {question.correct_answer}")


# Add one new question
def add_question():
    print("Add Question Manually")
    question_dict = questions_dict()

    for key in question_dict:
        question_dict[key] = input(f"{key}: ")
    new_question = Question(category=question_dict["category"], question=question_dict["question"], answer_1=question_dict["answer_1"], answer_2=question_dict["answer_2"], answer_3=question_dict["answer_3"], answer_4=question_dict["answer_4"], correct_answer=question_dict["correct_answer"])
    res = requests.post(url("/add_question"), json=(new_question.dict()))
    print(res.json())


# Add one new question
def add_question_from_file():
    question_dict = questions_dict()
    
    print("Add Questions from File")
    for key in question_dict:
        # print(f"{key}: ")
        question_dict[key] = input(f"{key}: ")

    new_question = Question(category=question_dict["category"], question=question_dict["question"], answer_1=question_dict["answer_1"], answer_2=question_dict["answer_2"], answer_3=question_dict["answer_3"], answer_4=question_dict["answer_4"], correct_answer=question_dict["correct_answer"])
    res = requests.post(url("/add_question"), json=(new_question.dict()))
    print(res.json())
    
    # res = requests.post(url("/add_question_from_file"))
    # print(res.json())


# Update one question
def update_question(questions_list: List[Question]):
    print("_________________")
    print("Update Question")

    # Loops until valid ID has been entered
    id_to_update = None
    running = False
    while not running:
        id_to_update = input("ID of the question to update: ")
        id_to_update, running = validate_int_input(id_to_update)

    # Matching the ID with database
    list_index, id_exists = check_for_id(id_to_update, questions_list)
    if not id_exists:
        return
    
    # 
    question_list = []
    question = questions_list[list_index].dict()
    question_list.append(questions_list[list_index])
    print_questions(question_list)

    print("_________________")
    print("Enter new values (leave blank if same): ")

    new_question = question
    for key in new_question:
        if key != "id":
            user_input = input(f"{key}: ")
            if not user_input == "":
                new_question[key] = user_input

    update_question = Question(category=new_question["category"], question=new_question["question"], answer_1=new_question["answer_1"], answer_2=new_question["answer_2"], answer_3=new_question["answer_3"], answer_4=new_question["answer_4"], correct_answer=new_question["correct_answer"])
    res = requests.put(url(f"/update_question/{id_to_update}"), json=update_question.dict())
    print(res.text)


# Delete one question
def delete_question(questions_list: List[Question]):
    print("_________________")
    print("Delete Question")
    id_to_delete = 0
    running = False
    while not running:
        id_to_delete = input("ID of the question you wish to delete: ")
        id_to_delete, running = validate_int_input(id_to_delete)
    
    _, id_exists = check_for_id(id_to_delete, questions_list)
    if id_exists:
        res = requests.delete(url(f"/delete_question/{id_to_delete}"))
        print(res.json())


def check_for_id(id: int, questions_list: List[Question]) -> Tuple[int, bool]:
    id_exists = False
    list_index = None
    for index, question in enumerate(questions_list):
        if question.id == int(id):
            list_index = index
            id_exists = True
    
    if not id_exists:
        print(f"Question with ID: {id}, does not exist")
        return (list_index, False)
    return (list_index, True)


def validate_int_input(user_input: str) -> Tuple[int, bool]:
    user_input = user_input.strip()
    try:
        id_to_delete = int(user_input)
    except ValueError:
        print("Invalid value. Please enter ID as integer.")
        return (None, False)
    else:
        return (id_to_delete, True)


# Main program
def main():
    print_menu()
    choice = input("Please choose action: ")
    choice = choice.strip()
    match choice:
        case "1":
            questions_list = fetchall_questions()
            print_questions(questions_list)
        case "2":
            # add_question_from_file()
            add_question()
        case "3":
            questions_list = fetchall_questions()
            update_question(questions_list)
        case "4":
            questions_list = fetchall_questions()
            delete_question(questions_list)
        case "5":
            exit()
        case _:
            print("Please enter a valid choice")


# Run main() when we run this file as "__main__"
while __name__ == "__main__":
    main()