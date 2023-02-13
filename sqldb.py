import sqlite3
from sqlite3 import IntegrityError
import os
from typing import List, Tuple

class DB:
    db_url: str
    db_table_name_1: str = "questions"
    db_table_name_2: str = "categories"


    def __init__(self, db_url: str):
        self.db_url = db_url
        
        # Lånad ifrån lesson11
        if not os.path.exists(self.db_url):
            self.init_db()


    def call_db(self, query, *args, fetch_one: bool=False):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        res = cur.execute(query, args)
        if fetch_one:
            data = res.fetchone()
        else:
            data = res.fetchall()

        # CATCH SQLITE ERROR FOR UNIQUE VALUES
        # try:
        #     res = cur.execute(query, args)
        #     if fetch_one:
        #         data = res.fetchone()
        #     else:
        #         data = res.fetchall()
        # except IntegrityError:
        #     data = None

        cur.close()
        conn.commit()
        conn.close()
        return data


    def init_db(self):
        create_question_query = f"""
        CREATE TABLE IF NOT EXISTS {self.db_table_name_1} (
            id INTEGER PRIMARY KEY NOT NULL,
            category INTEGER NOT NULL,
            question VARCHAR(255) NOT NULL UNIQUE,
            answer_1 VARCHAR(255) NOT NULL,
            answer_2 VARCHAR(255) NOT NULL,
            answer_3 VARCHAR(255) NOT NULL,
            answer_4 VARCHAR(255) NOT NULL,
            correct_answer VARCHAR(255) NOT NULL,
            
            FOREIGN KEY (category) REFERENCES {self.db_table_name_2} (id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
        
        create_category_query = f"""
        CREATE TABLE IF NOT EXISTS {self.db_table_name_2} (
            id INTEGER PRIMARY KEY NOT NULL,
            category VARCHAR(255) NOT NULL,
        )
        """
        self.call_db(create_question_query)
        self.call_db(create_category_query)

    
    def search_in_db(self, col_name: str, value: str) -> List[Tuple[str]]:
        search_db_query = f"""
        SELECT * FROM {self.db_table_name}
        WHERE {col_name} = ?
        """
        res = self.call_db(search_db_query, value, fetch_one=True)
        return res


if __name__ == "__main__":
    db = DB("Question.db")

    db.init_db()
