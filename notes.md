# QUIZ APP

## TASK 1: Set up
- Create project
- Install packages
- Verify that the files are working

## TASK 2: Create API
- Import FastAPI
- Create the app
- Run with uvicorn
- Create base routes:
    - Root
    - Get_Question - get
        - Fetch all
        - Fetch specific Questions
    - Add_Question - post
        - Manually
        - From csv file
    - Delete_Question - delete
    - Update_Question - update

## TASK 3: Create the program
- Menu
    - Add question
    - Delete question
    - Update question
    - Show all questions
    - Show some questions
    - Close the program

## TASK 4: Create the data
## TASK 5: Store in sqlite3

## Current functions
- Seed the database
    - from json file
    - add unique questions to db
    - give errormessage for questions alredy in db

- menu
    - Fetch all Questions
        - Prints out all avaiable questions in the db

    - Add Question
        - Manually add one question
            - add unique questions to db
            - give errormessage for questions alredy in db
        ## - Add questions from csv file
            - add unique questions to db
            - give errormessage for questions alredy in db
            

    - Update Question
        - Manually update one question
            - give errormessage if input ID doesn´t exist
            - keep previous values for "" inputs
            - update the remaining columns with the user input
    - Delete Question
        - Manually delete one question
            - give errormessage if input ID doesn´t exist
            - delete question for valid ID
    - Exit

- sqlite3 db
    - allows no dublicate questions