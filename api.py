from typing import List
from fastapi import FastAPI
from question import Question
from sqldb import DB
from quiz_app import BaseValues

# uvicorn api:app --reload

db_table_name_questions = BaseValues.table_name_questions
db_table_name_categories = BaseValues.table_name_categories

app = FastAPI()
db = DB("Question.db", db_table_name_questions, db_table_name_categories)

# 
@app.get("/")
def root():
    return "Hello and welcome to Victors Quiz"


# API to get all 'Questions' from the DB
@app.get("/questions")
def fetchall_questions():
    res = db.fetch_all_questions()
    print(f"""
    Returns a list of all avaiable questions
    ---------------------------
    {res}
    """)
    return res


# API to get all 'categories' from the DB
@app.get("/categories")
def fetchall_categories():
    res = db.fetch_all_categories()
    print("""
    Returns a list of all avaiable categories
    ---------------------------
    {res}
    """)
    return res


# API to search and return the 'Question' results from the DB
@app.get("/search_questions/{col_name}")
def search_for_question(search_dict: dict):
    col_name = search_dict["col_name"]
    look_for = search_dict["look_for"]
    fetch_one = search_dict["fetch_one"]
    res = db.search_in_db(col_name, look_for, fetch_one)
    if res == None:
        print("No questions were found")
        return None
    else:
        print(f"""
        Returns all question(s) with search criteria
        ---------------------------
        Column: {col_name}
        Look for: {look_for} 
        ---------------------------
        {res}
        """)
    return res


# API to add one new 'Question' to the DB
@app.post("/add_question")
def add_question(question: Question):
    res, db_id = db.insert_question_to_db(question)
    if res:
        print(f"""
        The bellow Question was successfully added!
        ---------------------------
        {question}
        """)
        return "The new Question was added successfully!"
    else:
        print(f"""
        The following Question already exists in the database
        ---------------------------
        Question: '{question.question}'
        With ID: {db_id}
        """)
        return f"\nQuestion: '{question.question}'\nAlready exists in the database.\nWith ID: {db_id}"


# API to add a list of new 'Questions' to the DB
@app.post("/add_question_from_file")
def add_question_from_file(question_list: List[Question]):
    added_values = []
    skipped_values = []
    for question in question_list:
        res, db_id = db.insert_question_to_db(question)
        if res:
            added_values.append(question)
        else:
            skipped_values.append(db_id)

    print(f"""
    The following Questions were added successfully!
    ---------------------------
    {added_values}
    """)
    print(f"""
    The following Questions already exists in the database
    ---------------------------
    {skipped_values}
    """)
    return (added_values, skipped_values)
    

# API to update the values for one existing 'Questions' in the DB
@app.put("/update_question/{id}")
def update_question(id: int, update_question: Question):
    res = db.update_question_table(id, update_question)
    if res:
        print(f"""
        The Question with ID: {id}, was updated successfully!
        """)
        return "Question with ID: " + str(id) + " was updated successfully!"
    else:
        print(f""" 
        No Question with ID {id} exists in the database.
        """)
        return "No Question with ID: " + str(id) + " exists in the database."


# API to delete one existing 'Questions' in the DB
@app.delete("/delete_question/{id}")
def delete_question(id: int):
    res = db.delete_question(id)
    if res:
        print(f"""
        Question with ID: {id} was deleted successfully!
        """)
        return "Question with ID: " + str(id) + " was deleted successfully!"
    else:
        print(f""" 
        No Question with ID {id} exists in the database.
        """)
        return "Invalid ID! No Question with ID: " + str(id) + " exists."
