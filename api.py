from typing import List
from fastapi import FastAPI
from question import Question
from sqldb import DB

# uvicorn api:app --reload

app = FastAPI()
db = DB("Question.db")
db_table_name = "questions"

app.questions: List[Question] = []


@app.get("/")
def root():
    return "Hello and welcome to Victors Quiz"


@app.get("/questions")
def fetchall_questions():
    fetchall_questions_query = f"""
    SELECT * FROM {db_table_name}
    """
    data = db.call_db(fetchall_questions_query)
    question_list = list()
    for row in data:
        id, category, question, answer_1, answer_2, answer_3, answer_4, correct_answer = row
        question_list.append(Question(id=id, category=category, question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, correct_answer=correct_answer))
    print("Returns a list of all avaiable questions")
    print(data)
    return question_list


@app.get("/question/{id}")
def get_question(id: int):
    get_question_query = f"""
    SELECT * FROM {db_table_name}
    WHERE id = ?
    """
    res = db.call_db(get_question_query, id)
    print("Returns a single question with ID: " + str(id))
    return res


@app.post("/add_question")
def add_question(question: Question):
    insert_query = f"""
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
    res = db.search_in_db("question", question.question)
    if res == None:
        db.call_db(insert_query, question.category, question.question, question.answer_1, question.answer_2, question.answer_3, question.answer_4, question.correct_answer)
        return "The new Question was added successfully!"
    else:
        db_id = res[0]
        return f"\nQuestion: '{question.question}'\nAlready exists in the database.\nWith ID: {db_id}"


@app.post("/add_question_from_file")
def add_question_from_file(question_list: List[Question]):
    print(question_list)
    return "The new Questions were added successfully!"


@app.put("/update_question/{id}")
def update_question(id: int, update_question: Question):
    update_question_query = f"""
    UPDATE {db_table_name}
    SET category = ?,
        question = ?,
        answer_1 = ?,
        answer_2 = ?,
        answer_3 = ?,
        answer_4 = ?,
        correct_answer  = ?
    WHERE id = ?
    """
    db.call_db(update_question_query, update_question.category, update_question.question, update_question.answer_1, update_question.answer_2, update_question.answer_3, update_question.answer_4, update_question.correct_answer, id)
    return "Question with ID: " + str(id) + " was updated successfully!"


@app.delete("/delete_question/{id}")
def delete_question(id: int):
    delete_question_query = f"""
    DELETE FROM {db_table_name}
    WHERE id = ?
    """
    db.call_db(delete_question_query, id)
    return "Question with ID: " + str(id) + " was deleted successfully!"