from pydantic import BaseModel

# BaseModel allow us to use the class in API and the quiz_app
# No __init__ requires because it is built into BaseModel
class Question(BaseModel):
    id: int = None
    category: str
    question: str
    answer_1: str
    answer_2: str
    answer_3: str
    answer_4: str
    correct_answer: str

# config?
# pydantic?