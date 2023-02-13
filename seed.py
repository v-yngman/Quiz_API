import sqlite3
import json
from sqldb import DB

db = DB("Question.db")
db_table_name = DB.db_table_name

insert_question_query = f"""
    INSERT INTO {db_table_name} (
        category, 
        question, 
        answer_1, 
        answer_2, 
        answer_3, 
        answer_4,
        correct_answer 
        ) VALUES ( ?, ?, ?, ?, ?, ?, ? )
    """


with open('seed.json', "r") as seed:
    data = json.load(seed)
    added_values = []
    skipped_values = []

    for question in data:
        question_str = question["question"]
        res = db.search_in_db("question", question_str)
        if res == None:
            db.call_db(insert_question_query, question["category"], question["question"], question["answer_1"], question["answer_2"], question["answer_3"], question["answer_4"], question["correct_answer"])
            added_values.append(question_str)
        else:
            db_id = res[0]
            skipped_values.append((question_str, db_id))

    if not added_values == []:
        print("_________________")
        print("\nWas successfully added:\n")
        for element in added_values:
            print(f"Question: '{element}'")
    
    if not skipped_values == []:
        print("_________________")
        print("\nAlready exists in the database:\n")
        for element in skipped_values:
            print(f"ID: {element[1]}, Question: '{element[0]}'")
        print("_________________")