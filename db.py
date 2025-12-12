import psycopg2
from psycopg2.extras import RealDictCursor
import schemas
import exceptions
"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""
#quiz functions

#fetching multiple quizzes
def get_multiple_quizzes(con):
    """get all quizzes from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM kahoots;")
            quizzes = cursor.fetchall()
    return quizzes

#creating a quiz
def create_quiz(con, quiz: schemas.QuizCreate):
    """create a new quiz in the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO kahoots (title, category) VALUES (%s, %s) RETURNING id;",
                (quiz.title, quiz.category),
            )
            quiz_id = cursor.fetchone()["id"]
    return quiz_id

#get a singular quiz
def get_quiz(con, quiz_id: int):
    """get a single quiz by id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM kahoots WHERE id = %s""", (quiz_id,))
            quiz = cursor.fetchone()
            if not quiz:
                raise exceptions.QuizNotFoundException(quiz_id)
            return quiz

#update a quiz      
def update_quiz(con, quiz_id: int, quiz: schemas.QuizUpdate):
    """update a quiz in the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE kahoots SET title = %s, category = %s WHERE id = %s RETURNING id;""",
                (quiz.title, quiz.category, quiz_id),
            )
            updated_quiz = cursor.fetchone()
            if not updated_quiz:
                raise exceptions.QuizNotFoundException(quiz_id)
            return updated_quiz["id"]

#delete a quiz
def delete_quiz(con, quiz_id: int):
    """delete a quiz from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM kahoots WHERE id = %s RETURNING id;""",
                (quiz_id,),
            )
            deleted_quiz = cursor.fetchone()
            if not deleted_quiz:
                raise exceptions.QuizNotFoundException(quiz_id)
            return deleted_quiz["id"]
        

#question functions

#get all questions for a specific quiz
def get_all_questions_quiz(con, quiz_id):
    """get all questions for a specific quiz"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM questions WHERE quiz_id = %s ORDER BY created_at;",
                (quiz_id,),
            )
            questions = cursor.fetchall()
    return questions

#get a singular question
def get_question(con, question_id: int):
    """get a single question by id"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM questions WHERE id = %s""", (question_id,))
            question = cursor.fetchone()
            if not question:
                raise exceptions.QuestionNotFoundException(question_id)
            return question


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id
