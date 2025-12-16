import os
from typing import List
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, status, Body
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
    con = None
    try:
        con = get_connection()
        kahoots = db.get_all_kahoots(con)
        return kahoots
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.get("/kahoots/{kahoot_id}", response_model=schemas.Kahoot, status_code=status.HTTP_200_OK)
def get_kahoot(kahoot_id: int):
    """get a specific kahoot by id"""
    con = None
    try:
        con = get_connection()
        kahoot = db.get_kahoot(con, kahoot_id)
        if not kahoot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kahoot not found")
        return kahoot
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()
    
@app.post("/kahoots/", status_code=status.HTTP_201_CREATED)
def create_kahoot(kahoot: schemas.KahootCreate):
    """create a new kahoot"""
    con = None
    try:
        con = get_connection()
        kahoot_id = db.create_kahoot(con, kahoot)
        return {"id": kahoot_id, "message": "Kahoot created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()
    
@app.delete("/kahoots/{kahoot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kahoot(kahoot_id: int):
    """delete a kahoot by id"""
    con = None
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
    finally:
        if con:
            con.close()

@app.put("/kahoots/{kahoot_id}", status_code=status.HTTP_200_OK)
def update_kahoot(kahoot_id: int, kahoot: schemas.KahootCreate = Body(...)):
    """update a kahoot"""
    con = None
    try:
        con = get_connection()
        update_kahoot = db.update_kahoot(con, kahoot_id, kahoot)
        return {"id": update_kahoot, "message": "Kahoot updated successfully"}

    except exceptions.ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()


#questions endpoints

@app.get("/kahoots/{kahoot_id}/questions/", response_model=List[schemas.Question], status_code=status.HTTP_200_OK)
def get_questions(kahoot_id: int):
    """get all questions for a specific kahoot"""
    con = None
    try:
        con = get_connection()
        questions = db.get_all_questions_quiz(con, kahoot_id)
        return questions
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.get("/kahoots/{kahoot_id}/questions/{question_id}", response_model=schemas.Question, status_code=status.HTTP_200_OK)
def get_question(kahoot_id: int, question_id: int):
    """get a specific question by id for a specific kahoot"""
    con = None
    try:
        con = get_connection()
        question = db.get_question(con, kahoot_id, question_id)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        return question
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.post("/questions/", status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuestionCreate):
    """create a new question for a specific kahoot"""
    con = None
    try:
        con = get_connection()
        question_id = db.create_question(con, question)
        return {"id": question_id, "message": "Question created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.put("/questions/{question_id}", status_code=status.HTTP_200_OK)
def update_question(question_id: int, question: schemas.QuestionCreate):
    """update a question by id"""
    con = None
    try:
        con = get_connection()
        updated_question_id = db.update_question(
            con,
            question_id,
            question
            )
        return {"id": updated_question_id, "message": "Question updated successfully"}
    except exceptions.ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int):
    """delete a question by id"""
    con = None
    try:
        con = get_connection()
        deleted_id = db.delete_question(con, question_id)
        return {"id": deleted_id, "message": "Question deleted successfully"}
    except exceptions.ResourceNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()
    

#answers endpoints

@app.get(
    "/questions/{question_id}/answers",
    response_model=List[schemas.Answer],
    status_code=status.HTTP_200_OK,
)
def get_answers_by_question(question_id: int):
    """Get all answers for a specific question"""
    con = None
    try:
        con = get_connection()
        answers = db.get_answers_by_question(con, question_id)
        return answers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.post("/answers/", status_code=status.HTTP_201_CREATED)
def create_answer(answer: schemas.AnswerCreate):
    """Create a new answer"""
    con = None
    try:
        con = get_connection()
        answer_id = db.create_answer(con, answer)
        return {"id": answer_id, "message": "Answer created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.put("/answers/{answer_id}", status_code=status.HTTP_200_OK)
def update_answer(answer_id: int, answer: schemas.AnswerCreate):
    """Update an answer"""
    con = None
    try:
        con = get_connection()
        updated_id = db.update_answer(
            con, answer_id, answer.answer_text, answer.is_correct
        )
        return {"id": updated_id, "message": "Answer updated successfully"}
    except exceptions.AnswerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.delete("/answers/{answer_id}", status_code=status.HTTP_200_OK)
def delete_answer(answer_id: int):
    """Delete an answer"""
    con = None
    try:
        con = get_connection()
        deleted_id = db.delete_answer(con, answer_id)
        return {"id": deleted_id, "message": "Answer deleted successfully"}
    except exceptions.AnswerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


# player/participant endpoints


@app.get("/game-sessions/{game_session_id}/participants/", response_model=List[schemas.Participant], status_code=status.HTTP_200_OK)
def get_participants(game_session_id: int):
    """Get all participants for a game session"""
    con = None
    try:
        con = get_connection()
        participants = db.get_participants(con, game_session_id)
        return participants
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()


@app.get("/participants/{participant_id}", response_model=schemas.Participant, status_code=status.HTTP_200_OK)
def get_participant(participant_id: int):
    """Get a single participant by ID"""
    con = None
    try:
        con = get_connection()
        participant = db.get_participant(con, participant_id)
        return participant
    except exceptions.PlayerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()


@app.post("/participants/", status_code=status.HTTP_201_CREATED)
def create_participant(participant: schemas.ParticipantCreate):
    """Create a new participant (join a game session)"""
    con = None
    try:
        con = get_connection()
        participant_id = db.create_participant(con, participant)
        return {"id": participant_id, "message": "Participant created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.delete("/participants/{participant_id}", status_code=status.HTTP_200_OK)
def delete_participant(participant_id: int):
    """Delete a participant (when they leave the game session)"""
    con = None
    try:
        con = get_connection()
        deleted_id = db.delete_participant(con, participant_id)
        return {"id": deleted_id, "message": "Participant removed successfully"}
    except exceptions.PlayerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.put("/participants/{participant_id}/username", status_code=status.HTTP_200_OK)
def update_participant_username(participant_id: int, new_username: str):
    """Update participant's username"""
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            "UPDATE participants SET username = %s WHERE id = %s RETURNING id;",
            (new_username, participant_id)
        )
        result = cursor.fetchone()
        if not result:
            raise exceptions.PlayerNotFoundException(participant_id)
        con.commit()
        return {"id": result[0], "message": "Username updated successfully"}
    except exceptions.PlayerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

# game seession endpoints


@app.get(
    "/game-sessions/",
    response_model=List[schemas.GameSession],
    status_code=status.HTTP_200_OK,
)
def get_all_game_sessions():
    """Get all game sessions"""
    con = None
    try:
        con = get_connection()
        sessions = db.get_game_sessions(con)
        return sessions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.get(
    "/game-sessions/{session_id}",
    response_model=schemas.GameSession,
    status_code=status.HTTP_200_OK,
)
def get_game_session(session_id: int):
    """Get a single game session by ID"""
    con = None
    try:
        con = get_connection()
        session = db.get_game_session(con, session_id)
        return session
    except exceptions.GameSessionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.get(
    "/game-sessions/pin/{pin}",
    response_model=schemas.GameSession,
    status_code=status.HTTP_200_OK,
)
def get_game_session_by_pin(pin: str):
    """Get a game session by PIN"""
    con = None
    try:
        con = get_connection()
        session = db.get_game_session_by_pin(con, pin)
        return session
    except exceptions.GameSessionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.post("/game-sessions/", status_code=status.HTTP_201_CREATED)
def create_game_session(session: schemas.GameSessionCreate):
    """Create a new game session"""
    con = None
    try:
        con = get_connection()
        session_id = db.create_game_session(con, session)
        return {"id": session_id, "message": "Game session created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.put("/game-sessions/{session_id}/end", status_code=status.HTTP_200_OK)
def end_game_session(session_id: int):
    """End a game session"""
    con = None
    try:
        con = get_connection()
        ended_id = db.end_game_session(con, session_id)
        return {"id": ended_id, "message": "Game session ended successfully"}
    except exceptions.GameSessionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()
    
@app.delete("/game-sessions/{session_id}", status_code=status.HTTP_200_OK)
def delete_game_session(session_id: int):
    """Delete a game session"""
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            "DELETE FROM game_sessions WHERE id = %s RETURNING id;",
            (session_id,)
        )
        result = cursor.fetchone()
        if not result:
            raise exceptions.GameSessionNotFoundException(session_id)
        con.commit()
        return {"id": result[0], "message": "Game session deleted successfully"}
    except exceptions.GameSessionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.patch("/game-sessions/{session_id}/active", status_code=status.HTTP_200_OK)
def update_game_session_active(session_id: int, is_active: bool):
    """Toggle game session active status (PATCH = partial update)"""
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            "UPDATE game_sessions SET is_active = %s WHERE id = %s RETURNING id;",
            (is_active, session_id)
        )
        result = cursor.fetchone()
        if not result:
            raise exceptions.GameSessionNotFoundException(session_id)
        con.commit()
        return {"id": result[0], "message": "Active status updated successfully"}
    except exceptions.GameSessionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

#player score endpoint


@app.post("/player-answers/", status_code=status.HTTP_201_CREATED)
def submit_answer(player_answer: schemas.PlayerAnswerCreate):
    con = None
    try:
        con = get_connection()
        score_id = db.submit_answer(con, player_answer)
        return {"id": score_id, "message": "Answer submitted successfully"}
    except exceptions.AnswerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.get(
    "/game-sessions/{session_id}/leaderboard",
    response_model=List[schemas.LeaderboardEntry],
    status_code=status.HTTP_200_OK,
)
def get_leaderboard(session_id: int):
    """Get the leaderboard for a game session"""
    con = None
    try:
        con = get_connection()
        leaderboard = db.get_leaderboard(con, session_id)
        return leaderboard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()


@app.get(
    "/game-sessions/{session_id}/participants/{participant_id}/answers",
    response_model=List[schemas.PlayerAnswer],
    status_code=status.HTTP_200_OK,
)
def get_player_scores(session_id: int, participant_id: int):
    """Get all scores for a specific player in a game session"""
    con = None
    try:
        con = get_connection()
        scores = db.get_participant_answers(con, session_id, participant_id)
        return scores
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        if con:
            con.close()

@app.patch("/participants/{participant_id}/score", status_code=status.HTTP_200_OK)
def update_participant_score(participant_id: int, final_score: int):
    """Update only the participant's score (PATCH = partial update)"""
    con = None
    try:
        con = get_connection()
        updated_id = db.update_participant_score(con, participant_id, final_score)
        return {"id": updated_id, "message": "Score updated successfully"}
    except exceptions.PlayerNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if con:
            con.close()

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Kahoot-like Quiz API",
        "docs": "/docs",
        "version": "1.0.0",
    }