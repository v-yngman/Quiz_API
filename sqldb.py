import sqlite3
from sqlite3 import IntegrityError
import os
from typing import List, Tuple
from question import Question
from quiz_app import BaseValues


""" docstring """
class DB:
    db_url: str
    db_table_name_questions: str = "questions"
    # db_table_name_questions: str = "questions"
    # db_table_name_categories: str = "categories"
    db_table_name_categories: str = "categories"

    def __init__(self, db_url: str, db_table_name_questions: str, db_table_name_categories: str):
        self.db_url = db_url
        # self.db_table_name_questions = db_table_name_questions
        # self.db_table_name_categories = db_table_name_categories
        
        # Lånad ifrån lesson11
        if not os.path.exists(self.db_url):
            self.init_db()


    # Function to connect and interact with the DB
    def call_db(self, query, *args, fetch_one: bool=False):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        try:
            res = cur.execute(query, args)
            if fetch_one:
                data = res.fetchone()
            else:
                data = res.fetchall()
        except IntegrityError:
            data = None
        cur.close()
        conn.commit()
        conn.close()
        return data


    # Creating the tables and relations for the DB
    def init_db(self):
        create_question_query = f"""
        CREATE TABLE IF NOT EXISTS {self.db_table_name_questions} (
            id INTEGER PRIMARY KEY NOT NULL,
            category INTEGER NOT NULL,
            question VARCHAR(255) NOT NULL UNIQUE,
            answer_1 VARCHAR(255) NOT NULL,
            answer_2 VARCHAR(255) NOT NULL,
            answer_3 VARCHAR(255) NOT NULL,
            answer_4 VARCHAR(255) NOT NULL,
            correct_answer VARCHAR(255) NOT NULL,
            
            FOREIGN KEY (category) REFERENCES {self.db_table_name_categories} (id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
        create_category_query = f"""
        CREATE TABLE IF NOT EXISTS {self.db_table_name_categories} (
            id INTEGER PRIMARY KEY NOT NULL,
            category VARCHAR(255) NOT NULL UNIQUE
        )
        """
        self.call_db(create_question_query)
        self.call_db(create_category_query)


    # Search within the DB for specific questions based on entered col_name and value
    def search_in_db(self, col_name: str, look_for: str, fetch_one: bool) -> List[Question]:
        search_questions_query = f"""
        SELECT
            {self.db_table_name_questions}.id,
            {self.db_table_name_categories}.category,
            {self.db_table_name_questions}.question,
            {self.db_table_name_questions}.answer_1,
            {self.db_table_name_questions}.answer_2,
            {self.db_table_name_questions}.answer_3,
            {self.db_table_name_questions}.answer_4,
            {self.db_table_name_questions}.correct_answer
        FROM
            {self.db_table_name_questions}
        INNER JOIN
            {self.db_table_name_categories}
            ON {self.db_table_name_questions}.category = {self.db_table_name_categories}.id
        WHERE {self.db_table_name_questions}.{col_name} = ?
        """
        search_questions_query_category = f"""
        SELECT
            {self.db_table_name_questions}.id,
            {self.db_table_name_categories}.category,
            {self.db_table_name_questions}.question,
            {self.db_table_name_questions}.answer_1,
            {self.db_table_name_questions}.answer_2,
            {self.db_table_name_questions}.answer_3,
            {self.db_table_name_questions}.answer_4,
            {self.db_table_name_questions}.correct_answer
        FROM
            {self.db_table_name_questions}
        INNER JOIN
            {self.db_table_name_categories}
            ON {self.db_table_name_questions}.category = {self.db_table_name_categories}.id
        WHERE {self.db_table_name_categories}.{col_name} = ?
        """

        if col_name == "category":
            data = self.call_db(search_questions_query_category, look_for, fetch_one=fetch_one)
        else:
            data = self.call_db(search_questions_query, look_for, fetch_one=fetch_one)

        if data == None:
            return
        question_list = list()
        if fetch_one:
            id, category, question, answer_1, answer_2, answer_3, answer_4, correct_answer = data
            question_list.append(Question(id=id, category=category, question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, correct_answer=correct_answer))  
        else:
            for question in data:
                id, category, question, answer_1, answer_2, answer_3, answer_4, correct_answer = question
                question_list.append(Question(id=id, category=category, question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, correct_answer=correct_answer))
        return question_list


    # Match "category" str value with the corresponding "primary id"
    def get_category_id(self, category: str) -> int:
        get_category_id_query = f"""
        SELECT id FROM {self.db_table_name_categories}
        WHERE category = ?
        """
        res_id = self.call_db(get_category_id_query, category, fetch_one=True)
        if res_id != None:
            res_id = res_id[0]
        return res_id


    # Adding a new question to the DB
    def insert_question_to_db(self, question: Question) -> Tuple[bool, int]:
        insert_question_query = f"""
        INSERT INTO {self.db_table_name_questions} (
            category, 
            question, 
            answer_1, 
            answer_2, 
            answer_3, 
            answer_4,
            correct_answer 
            ) VALUES ( ?, ?, ?, ?, ?, ?, ? )
        """
        insert_category_query = f"""
        INSERT INTO {self.db_table_name_categories} (
            category
            ) VALUES ( ? )
        """
        res = self.search_in_db("question", question.question,  fetch_one=True)
        category_id = self.get_category_id(question.category)

        if res == None:
            if category_id == None:
                self.insert_category_to_db(question.category)
                category_id = self.get_category_id(question.category)
                self.call_db(insert_question_query, category_id, question.question, question.answer_1, question.answer_2, question.answer_3, question.answer_4, question.correct_answer)
                return (True, None)
            else:
                self.call_db(insert_question_query, category_id, question.question, question.answer_1, question.answer_2, question.answer_3, question.answer_4, question.correct_answer)
                return (True, None)
        else:
            db_id = res[0]
            return (False, db_id)


    # Adding a new 'category' to the 'category table'
    def insert_category_to_db(self, category: str):
        insert_category_query = f"""
        INSERT INTO 
            {self.db_table_name_categories} ( category )
        VALUES ( ? )
        """
        self.call_db(insert_category_query, category)
        return True


    # Returns all avaiable 'Questions' from the DB
    def fetch_all_questions(self) -> List[Question]:
        fetch_questions_query = f"""
        SELECT
            {self.db_table_name_questions}.id,
            {self.db_table_name_categories}.category,
            {self.db_table_name_questions}.question,
            {self.db_table_name_questions}.answer_1,
            {self.db_table_name_questions}.answer_2,
            {self.db_table_name_questions}.answer_3,
            {self.db_table_name_questions}.answer_4,
            {self.db_table_name_questions}.correct_answer
        FROM
            {self.db_table_name_questions}
        INNER JOIN
            {self.db_table_name_categories}
            ON {self.db_table_name_questions}.category = {self.db_table_name_categories}.id
        """
        data = self.call_db(fetch_questions_query)
        question_list = list()

        for question in data:
            id, category, question, answer_1, answer_2, answer_3, answer_4, correct_answer = question
            question_list.append(Question(id=id, category=category, question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, correct_answer=correct_answer))
        return question_list


    # Returns all avaiable 'Categories' from the DB
    def fetch_all_categories(self) -> List[Tuple[int, str]]:
            fetch_categories_query = f"""
            SELECT 
                *
            FROM 
                {self.db_table_name_categories}
            """
            data = self.call_db(fetch_categories_query)
            category_list = list()
            for category in data:
                category = category
                category_list.append(category)
            return category_list


    # Update the values for one existing 'Question'
    def update_question_table(self, id: int, updated_question: Question):
        id_check = self.search_in_db("id", id, fetch_one=True)
        if id_check == None:
            return False
        else:
            category_id = self.get_category_id(updated_question.category)
            if category_id == None:
                self.insert_category_to_db(updated_question.category)
                category_id = self.get_category_id(updated_question.category)
            updated_question.category = category_id
            update_question_query = f"""
            UPDATE {self.db_table_name_questions}
            SET 
                category = ?,
                question = ?,
                answer_1 = ?,
                answer_2 = ?,
                answer_3 = ?,
                answer_4 = ?,
                correct_answer  = ?
            WHERE id = ?
            """
            self.call_db(update_question_query, updated_question.category, updated_question.question, updated_question.answer_1, updated_question.answer_2, updated_question.answer_3, updated_question.answer_4, updated_question.correct_answer, id)
            return True


    # Deletes one existing 'Question'
    def delete_question(self, id: int):
        id_check = self.search_in_db("id", id, fetch_one=True)
        if id_check == None:
            return False
        delete_question_query = f"""
        DELETE FROM {self.db_table_name_questions}
        WHERE id = ?
        """
        self.call_db(delete_question_query, id)
        return True


if __name__ == "__main__":
    db_table_name_questions = BaseValues.table_name_questions
    db_table_name_categories = BaseValues.table_name_categories
    db = DB("Question.db", db_table_name_questions, db_table_name_categories)
    db.init_db()


