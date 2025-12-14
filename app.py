import os
from typing import List
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, status
import schemas
import exceptions
import db

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""
app = FastAPI(title="Kahoot-like Quiz API", version="1.0.0")

#endpoints for the kahoots
@app.get("/kahoots/", response_model=List[schemas.Kahoot], status_code=status.HTTP_200_OK)
def get_kahoots():
    """get all kahoots"""
    # Endpoint to get all kahoots
    try:
        con = get_connection()
        kahoots = db.get_all_kahoots(con)
        return kahoots
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/kahoots/{kahoot_id}", response_model=schemas.Kahoot, status_code=status.HTTP_200_OK)
def get_kahoot(kahoot_id: int):
    """get a specific kahoot by id"""
    # Endpoint to get a specific kahoot by id
    try:
        con = get_connection()
        kahoot = db.get_kahoot(con, kahoot_id)
        if not kahoot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kahoot not found")
        return kahoot
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.post("/kahoots/create/", response_model=schemas.KahootCreate, status_code=status.HTTP_201_CREATED)
def create_kahoot(kahoot: schemas.KahootCreate):
    """create a new kahoot"""
    # Endpoint to create a new kahoot
    try:
        con = get_connection()
        kahoot_id = db.create_kahoot(con, kahoot)
        return {"id": kahoot_id, "message": "Kahoot created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.delete("/kahoots/{kahoot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kahoot(kahoot_id: int):
    """delete a kahoot by id"""
    # Endpoint to delete a kahoot by id
    try:
        con = get_connection()
        db.delete_kahoot(con, kahoot_id)
        return {"message": "Kahoot deleted successfully"}
    except exceptions.ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@app.put("/kahoots/{kahoot_id}", response_model=schemas.Kahoot, status_code=status.HTTP_200_OK)
def update_kahoot(kahoot_id: int, kahoot: schemas.KahootCreate):
    """update a kahoot"""
    # Endpoint to update a kahoot
    try:
        con = get_connection()
        update_kahoot = db.update_kahoot(con, kahoot_id, kahoot.title, kahoot.category)
        return {"id": update_kahoot, "message": "Kahoot updated successfully"}
        
    except exceptions.ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


#questions endpoints

@app.get("/kahoots/{kahoot_id}/questions/", response_model=List[schemas.Question], status_code=status.HTTP_200_OK)
def get_questions(kahoot_id: int):
    """get all questions for a specific kahoot"""
    # Endpoint to get all questions for a specific kahoot
    try:
        con = get_connection()
        questions = db.get_all_questions_quiz(con, kahoot_id)
        return questions
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/questions/{question_id}", response_model=schemas.Question, status_code=status.HTTP_200_OK)
def get_question(question_id: int):
    """get a specific question by id for a specific kahoot"""
    # Endpoint to get a specific question by id for a specific kahoot
    try:
        con = get_connection()
        question = db.get_question(con, question_id)
        if not question:    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        return question
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/questions", status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuestionCreate):
    """create a new question for a specific kahoot"""
    # Endpoint to create a new question for a specific kahoot
    try:
        con = get_connection()
        question_id = db.create_question(con, question)
        return {"id": question_id, "message": "Question created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/questions/{question_id}", status_code=status.HTTP_200_OK)
def update_question(question_id: int, question: schemas.QuestionCreate):
    """update a question by id"""
    # Endpoint to update a question by id
    try:
        con = get_connection()
        updated_question_id = db.update_question(
            con,
            question_id,
            question.question_text,
            question.time_limit,
            )
        return {"id": updated_question_id, "message": "Question updated successfully"}
    except exceptions.ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @app.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
