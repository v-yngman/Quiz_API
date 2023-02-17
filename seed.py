from typing import List
import requests
import json
from question import Question


class JsonSeed:
    base_url: str
    questions_dict: dict


    def __init__(self, base_url, questions_dict):
        self.base_url = base_url
        self.questions_dict = questions_dict


    def url(self, route: str):
        base_url = self.base_url
        return base_url + route
    

    # Populating the DB with Question class objects from a json file
    def seed_db_from_json_file(self, filename: str):
        encoding_str = "utf-8"
        data = self.read_json_file(filename, encoding_str)

        question_list = []
        for question_dict in data:
            question = Question(category=question_dict["category"], question=question_dict["question"], answer_1=question_dict["answer_1"], answer_2=question_dict["answer_2"], answer_3=question_dict["answer_3"], answer_4=question_dict["answer_4"], correct_answer=question_dict["correct_answer"])
            question_list.append(question.dict())

        res = requests.post(self.url("/add_question_from_file"), json=question_list)
        added_values, skipped_values = res.json()
        self.print_seed_status(added_values, skipped_values)
        

    # Display what Questions got added to the DB and what Questions that were skipped
    def print_seed_status(self, added_values: List[Question], skipped_values: List[Question]):
        if not added_values == []:
            print("_________________")
            print("\nWas successfully added:\n")
            for question in added_values:
                question = Question(**question)
                print(f"Question: '{question.question}'")
        
        if not skipped_values == []:
            print("_________________")
            print("\nAlready exists in the database:\n")
            for question in skipped_values:
                question = Question(**question)
                print(f"ID: {question.id}, Question: '{question.question}'")
            print("_________________")


    # Opens and stores the data within a json file
    def read_json_file(self, filename: str, encoding_str: str) -> List[dict[Question]]:
        with open(filename, "r", encoding=encoding_str) as file:
            data = json.load(file)
            return data


    # Creating a list of dicts with all the unique Questions within the database
    def update_json_object(self, data: List[dict[Question]], new_question: List[dict[Question]]) -> List[dict[Question]]:
        for question in new_question:
            data.append(question)
        new_data = []
        for item in data:
            if item not in new_data:
                new_data.append(item)
        return new_data


    # Updating the json file with the Questions stored in the Data variable
    def update_json_file(self, data: List[dict[Question]], filename: str, encoding_str: str):
        with open(filename, "w") as file:
            json.dump(data, file, indent=True)
        return "Json file is updated"


if __name__ == "__main__":
    test_dict = {
            "category": "",
            "question": "",
            "answer_1": "",
            "answer_2": "",
            "answer_3": "",
            "answer_4": "",
            "correct_answer": "" 
            }
    test_url = "http://127.0.0.1:8000"
    filename = 'seed.json'

    JS = JsonSeed(test_url, test_dict)
    JS.seed_db_from_json_file(filename)
    
    question_dict = JS.questions_dict
    
    filename = 'seed copy.json'
    encoding_str = "utf-8"
    question_dict = {
        "category": "Animal",
        "question": "What is the fastest animal in the world?",
        "answer_1": "Cheetah",
        "answer_2": "Golden Eagle",
        "answer_3": "Sailfish",
        "answer_4": "Peregrine falcon",
        "correct_answer": "Peregrine falcon" 
        }
    
    new_dict_list = []
    new_dict_list.append(question_dict)

    data = JS.read_json_file(filename, encoding_str)
    print("Check: 1")
    print(data)

    new_data = JS.update_json_object(data, new_dict_list)
    print("Check: 2")
    print(new_data)

    res = JS.update_json_file(new_data, filename, encoding_str)
    print("Check: 3")
    data = JS.read_json_file(filename, encoding_str)

    print("Check: 4")
    print(data)
