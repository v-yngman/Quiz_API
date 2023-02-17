from question import Question
from quiz_app import BaseValues, fetchall_questions, print_questions, quiz_app
from seed import JsonSeed

# User menu
def print_main_menu():
    print("""
        V I C T O R S
        Quiz Data Management App""")
    print("""
        Main menu
        -------------------------------------
        1: View the Data
        2: Edit the Data
        3: Seed the Database from Json File
        4: Update the Json File with DB Data
        5: Exit
    """)


# 
def seed_from_json_file(js_seed: JsonSeed, js_filename: str):    
    try:
        js_seed.seed_db_from_json_file(js_filename)
    except FileNotFoundError:
        print(f"File with name: '{js_filename}', does not exist.")
        return


# 
def get_json_filename() -> str:
    filename = input("Enter json filename: ")
    if filename.find('.json') != -1:
        js_filename = filename
    else:
        js_filename = filename + str('.json')
    return js_filename


# 
def update_json_file_fom_db(js_seed: JsonSeed, questions_dict: dict[Question], js_filename: str):
    data = fetchall_questions()
    new_dict_list = []
    for question in data:
        question = question.dict()
        new_question = questions_dict
        for key in question:
            if key != "id":
                new_question[key] = question[key]
        new_dict_list.append(new_question)

    try:
        data = js_seed.read_json_file(js_filename, BaseValues.encoding_str)
    except FileNotFoundError:
        print(f"File with name: '{js_filename}', does not exist.")
        return
    else:
        new_data = js_seed.update_json_object(data, new_dict_list)
        js_seed.update_json_file(new_data, js_filename, BaseValues.encoding_str)
        print(f"Json File: '{js_filename}' was successfully updated!")


# Main program
def main():
    js = JsonSeed(BaseValues.base_url, BaseValues.questions_dict)
    print_main_menu()
    choice = input("Please choose action: ")
    choice = choice.strip()
    match choice:
        case "1":
            print("View Data")
            questions_list = fetchall_questions()
            print_questions(questions_list)

        case "2":
            quiz_app()

        case "3":
            print("Seed the Database from Json File")
            js_filename = get_json_filename()
            seed_from_json_file(js, js_filename)

        case "4":
            print("Update the Json File with DB Data")
            js_filename = get_json_filename()
            update_json_file_fom_db(js, BaseValues.questions_dict, js_filename)

        case "5":
            print("Thank you for using my Quiz_app!")
            exit()

        case _:
            print("You did not enter a valid number.")


# Run main() when we run this file as "__main__"
while __name__ == "__main__":
    main()