from typing import List, Tuple
import requests
from question import Question
from seed import JsonSeed

# python quiz_app.py
class BaseValues:
    base_url = "http://127.0.0.1:8000"
    encoding_str = "utf-8"
    questions_dict = {
            "category": "",
            "question": "",
            "answer_1": "",
            "answer_2": "",
            "answer_3": "",
            "answer_4": "",
            "correct_answer": "" 
            }
    table_name_questions = "questions"
    table_name_categories = "categories"


value = BaseValues()
js = JsonSeed(value.base_url, value.questions_dict)

# To call the API
def url(route: str):
    base_url = value.base_url
    return base_url + route


# User menu
def print_menu_edit_data():
    print("""
    Edit Data
    -------------------------------------
    1: Search for Question(s)
    2: Add Question
    3: Update Question
    4: Delete Question
    5: Return to 'Main Menu'
    """)


# Get all the 'Questions' from the DB
def fetchall_questions() -> List[Question]:
    print("Fetching all Questions")
    questions_list = []
    res = requests.get(url("/questions"))
    for question in res.json():
        question = Question(**question)
        questions_list.append(question)
    return questions_list


# Add one new 'Question' to the DB
def add_question():
    print("Add Question")
    question_dict = value.questions_dict
    for key in question_dict:
        question_dict[key] = input(f"{key}: ")
    new_question = Question(category=question_dict["category"], question=question_dict["question"], answer_1=question_dict["answer_1"], answer_2=question_dict["answer_2"], answer_3=question_dict["answer_3"], answer_4=question_dict["answer_4"], correct_answer=question_dict["correct_answer"])
    res = requests.post(url("/add_question"), json=(new_question.dict()))
    print(res.json())


# Update the values for one existing 'Question'
def update_question():
    print("_________________")
    print("Update Question")
    id_to_update = None
    running = False

    # Loops until valid ID has been entered
    while not running:
        id_to_update = input("ID of the question to update: ")
        id_to_update, running = validate_int_input(id_to_update)
    data = {
        "col_name": "id",
        "look_for": id_to_update,
        "fetch_one": "True"
    }
    
    res = search_in_db(data)
    if res == None:
        return
    print_questions(res)
    print("Enter new values (leave blank if same): ")
    # new_question = questions_dict()
    new_question = value.questions_dict
    new_question = res[0].dict()
    for key in new_question:
        if key != "id":
            user_input = input(f"{key}: ")
            if not user_input == "":
                new_question[key] = user_input
    update_question = Question(category=new_question["category"], question=new_question["question"], answer_1=new_question["answer_1"], answer_2=new_question["answer_2"], answer_3=new_question["answer_3"], answer_4=new_question["answer_4"], correct_answer=new_question["correct_answer"])
    res = requests.put(url(f"/update_question/{id_to_update}"), json=update_question.dict())
    print(res.text)


# Delete one existing 'Question' in the DB
def delete_question():
    print("_________________")
    print("Delete Question")
    id_to_delete = 0
    running = False
    while not running:
        id_to_delete = input("ID of the question you wish to delete: ")
        id_to_delete, running = validate_int_input(id_to_delete)
    res = requests.delete(url(f"/delete_question/{id_to_delete}"))
    print(res.json())


# Get user input for criterias to search for 'Questions' in the DB
def get_search_criterias() -> dict:
    print("_________________")
    print("Getting search criterias: ")
    column_options = """
    1: ID
    2: Category
    3: Question
    """
    data = {
        "col_name": "",
        "look_for": "",
        "fetch_one": ""
    }
    while True:
        print(column_options)
        choice = input("Please choose what column to search in: ")
        match choice:
            case "1":
                data["col_name"] = "id"
                data["fetch_one"] = True
                data["look_for"] = input("Enter the 'id' you're looking for: ")
                break
            case "2":
                data["col_name"] = "category"
                data["fetch_one"] = False
                category_list = requests.get(url(f"/categories"))
                print("Avaiable Categories: ")
                print("_________________")
                for element in category_list.json():
                    id, category = element
                    print(f"{id}: '{category}'")
                print("_________________")
                data["look_for"] = input("Enter the 'category' you're looking for: ")
                break
            case "3":
                data["col_name"] = "question"
                data["fetch_one"] = True
                data["look_for"] = input("Enter the 'question' you're looking for: ")
                break
            case _:
                print("Please enter a valid choice")
                continue
    return data


# Search the DB using the search criterias entered
def search_in_db(search_dict: dict) -> List[Question]:
    col_name = search_dict["col_name"]
    res = requests.get(url(f"/search_questions/{col_name}"), json=(search_dict))
    if res.json() == None or res.json() == []:
        print("No questions were found with the selected criterias.")
        return None
    else:
        questions_list = list()
        for question in res.json():
            question = Question(**question)
            questions_list.append(question)
        return questions_list


# Displays the 'Question'
def print_questions(questions_list: List[Question]):
    if questions_list == None:
        return
    else:
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
        print("_________________")


# Verify that the user entered a INTEGER
def validate_int_input(user_input: str) -> Tuple[int, bool]:
    user_input = user_input.strip()
    try:
        id = int(user_input)
    except ValueError:
        print("Invalid value. Please enter ID as integer.")
        return (None, False)
    else:
        return (id, True)


# Main program
def quiz_app():
    while True:
        print_menu_edit_data()
        choice = input("Please choose action: ")
        choice = choice.strip()
        match choice:
            case "1":
                search_criterias = get_search_criterias()
                questions_list = search_in_db(search_criterias)
                if questions_list != None:
                    print_questions(questions_list)
            case "2":
                add_question()
            case "3":
                update_question()
            case "4":
                delete_question()
            case "5":
                return
            case _:
                print("Please enter a valid choice")


while __name__ == "__main__":
    quiz_app()