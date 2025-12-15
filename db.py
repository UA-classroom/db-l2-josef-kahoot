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

#fetching all kahoots
def get_all_kahoots(con):
    """get all kahoots from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM kahoots;")
            kahoots = cursor.fetchall()
    return kahoots

#creating a kahoot
def create_kahoot(con, kahoot: schemas.KahootCreate):
    """create a new kahoot in the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO kahoots (title, category) VALUES (%s, %s) RETURNING id;",
                (kahoot.title, kahoot.category),
            )
            kahoot_id = cursor.fetchone()["id"]
    return kahoot_id

#get a singular kahoot
def get_kahoot(con, kahoot_id: int):
    """get a single kahoot by id from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM kahoots WHERE id = %s""", (kahoot_id,))
            kahoot = cursor.fetchone()
            if not kahoot:
                raise exceptions.KahootNotFoundException(kahoot_id)
            return kahoot

#update a kahoot      
def update_kahoot(con, kahoot_id: int, kahoot: schemas.KahootCreate):
    """update a kahoot in the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE kahoots SET title = %s, category = %s WHERE id = %s RETURNING id;""",
                (kahoot.title, kahoot.category, kahoot_id),
            )
            updated_kahoot = cursor.fetchone()
            if not updated_kahoot:
                raise exceptions.KahootNotFoundException(kahoot_id)
            return updated_kahoot["id"]

#delete a kahoot
def delete_kahoot(con, kahoot_id: int):
    """delete a kahoot from the database"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM kahoots WHERE id = %s RETURNING id;""",
                (kahoot_id,),
            )
            deleted_kahoot = cursor.fetchone()
            if not deleted_kahoot:
                raise exceptions.KahootNotFoundException(kahoot_id)
            return deleted_kahoot["id"]
        

#question functions

#get all questions for a specific quiz
def get_all_questions_quiz(con, kahoot_id):
    """get all questions for a specific quiz"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM questions WHERE kahoot_id = %s ORDER BY id;",
                (kahoot_id,),
            )
            questions = cursor.fetchall()
    return questions

#get a singular question
def get_question(con, kahoot_id, question_id: int):
    """get a single question by id"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT * FROM questions WHERE id = %s AND kahoot_id = %s""", (question_id,kahoot_id))
            question = cursor.fetchone()
            if not question:
                raise exceptions.QuestionNotFoundException(question_id)
            return question

def create_question(con, question: schemas.QuestionCreate):
    """Create a new question"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO questions (kahoot_id, question_text, time_limit) VALUES (%s, %s, %s) RETURNING id;",
                (question.kahoot_id, question.question_text, question.time_limit),
            )
            question_id = cursor.fetchone()["id"]
    return question_id


def update_question(con, question_id, question_text, time_limit):
    """Update a question"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE questions SET question_text = %s, time_limit = %s WHERE id = %s RETURNING id;",
                (question_text, time_limit, question_id),
            )
            result = cursor.fetchone()
            if not result:
                raise exceptions.QuestionNotFoundException(f"Question with id {question_id} not found")
            return result["id"]


def delete_question(con, question_id):
    """Delete a question"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM questions WHERE id = %s RETURNING id;", (question_id,))
            result = cursor.fetchone()
            if not result:
                raise exceptions.QuestionNotFoundException(f"Question with id {question_id} not found")
            return result["id"]


# answer functions

def get_answers_by_question(con, question_id):
    """Get all answers for a specific question"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM answers WHERE question_id = %s;",
                (question_id,),
            )
            answers = cursor.fetchall()
    return answers


def create_answer(con, answer: schemas.AnswerCreate):
    """Create a new answer"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO answers (question_id, answer_text, is_correct) VALUES (%s, %s, %s) RETURNING id;",
                (answer.question_id, answer.answer_text, answer.is_correct),
            )
            answer_id = cursor.fetchone()["id"]
    return answer_id


def update_answer(con, answer_id, answer_text, is_correct):
    """Update an answer"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE answers SET answer_text = %s, is_correct = %s WHERE id = %s RETURNING id;",
                (answer_text, is_correct, answer_id),
            )
            result = cursor.fetchone()
            if not result:
                raise exceptions.AnswerNotFoundException(f"Answer with id {answer_id} not found")
            return result["id"]


def delete_answer(con, answer_id):
    """Delete an answer"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM answers WHERE id = %s RETURNING id;", (answer_id,))
            result = cursor.fetchone()
            if not result:
                raise exceptions.AnswerNotFoundException(f"Answer with id {answer_id} not found")
            return result["id"]


# participant / player functions

def get_participants(con, game_session_id: int):
    """Get all participants for a game session"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM participants WHERE game_session_id = %s ORDER BY joined_at DESC;",
                (game_session_id,)
            )
            participants = cursor.fetchall()
    return participants


def get_participant(con, participant_id: int):
    """Get a single participant by ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM participants WHERE id = %s;", (participant_id,))
            participant = cursor.fetchone()
            if not participant:
                raise exceptions.PlayerNotFoundException(participant_id)
            return participant


def create_participant(con, participant: schemas.ParticipantCreate):
    """Create a new participant (join a game session)"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO participants (game_session_id) VALUES (%s) RETURNING id;",
                (participant.game_session_id,),
            )
            participant_id = cursor.fetchone()["id"]
    return participant_id

def delete_participant(con, participant_id: int):
    """Delete a participant (when they leave the game session)"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM participants WHERE id = %s RETURNING id;",
                (participant_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise exceptions.PlayerNotFoundException(participant_id)
            return result["id"]

def update_participant_score(con, participant_id: int, final_score: int, rank: int = None):
    """Update a participant's final score and rank"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            if rank is not None:
                cursor.execute(
                    "UPDATE participants SET final_score = %s, rank = %s WHERE id = %s RETURNING id;",
                    (final_score, rank, participant_id)
                )
            else:
                cursor.execute(
                    "UPDATE participants SET final_score = %s WHERE id = %s RETURNING id;",
                    (final_score, participant_id)
                )
            result = cursor.fetchone()
            if not result:
                raise exceptions.PlayerNotFoundException(participant_id)
            return result["id"]
# game session functions

def get_game_sessions(con):
    """Get all game sessions"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM game_sessions ORDER BY created_at DESC;")
            sessions = cursor.fetchall()
    return sessions


def get_game_session(con, session_id):
    """Get a single game session by ID"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM game_sessions WHERE id = %s;", (session_id,))
            session = cursor.fetchone()
            if not session:
                raise exceptions.GameSessionNotFoundException(f"Game session with id {session_id} not found")
            return session


def get_game_session_by_pin(con, pin):
    """Get a game session by PIN"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM game_sessions WHERE pin = %s;", (pin,))
            session = cursor.fetchone()
            if not session:
                raise exceptions.GameSessionNotFoundException(f"Game session with pin {pin} not found")
            return session


def create_game_session(con, session: schemas.GameSessionCreate):
    """Create a new game session"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO game_sessions (kahoot_id, pin) VALUES (%s, %s) RETURNING id;",
                (session.kahoot_id, session.session_pin),
            )
            session_id = cursor.fetchone()["id"]
    return session_id


def end_game_session(con, session_id):
    """End a game session by setting is_active to false"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "UPDATE game_sessions SET is_active = FALSE WHERE id = %s RETURNING id;",
                (session_id,),
            )
            result = cursor.fetchone()
            if not result:
                raise exceptions.GameSessionNotFoundException(f"Game session with id {session_id} not found")
            return result["id"]


#player score/ leaderboard functions

def submit_answer(con, player_answer: schemas.PlayerAnswerCreate):
    """Submit a player's answer and calculate points"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            # Check if the answer is correct
            cursor.execute(
                "SELECT is_correct FROM answers WHERE id = %s;",
                (player_answer.answer_id,),
            )
            answer = cursor.fetchone()
            if not answer:
                raise exceptions.AnswerNotFoundException(player_answer.answer_id)

            # Calculate points (1000 base points if correct, bonus for speed)
            points_earned = 0
            if answer["is_correct"]:
                # Faster responses get more points (max 1000, min 500)
                time_bonus = max(0, 500 - int(player_answer.time_taken * 10))
                points_earned = 500 + time_bonus

            # Insert the score into player_answers table
            cursor.execute(
                """INSERT INTO player_answers
                (session_id, participant_id, question_id, answer_id, time_taken, points_earned)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
                (
                    player_answer.session_id,
                    player_answer.participant_id,
                    player_answer.question_id,
                    player_answer.answer_id,
                    player_answer.time_taken,
                    points_earned,
                ),
            )
            score_id = cursor.fetchone()["id"]
            
            # Update participant's final_score
            cursor.execute(
                """UPDATE participants 
                SET final_score = final_score + %s 
                WHERE id = %s;""",
                (points_earned, player_answer.participant_id)
            )
    return score_id

def get_leaderboard(con, game_session_id: int):
    """Get the leaderboard for a game session"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    p.id as participant_id,
                    u.username,
                    COALESCE(SUM(pa.points_earned), 0) as total_score,
                    COUNT(CASE WHEN a.is_correct THEN 1 END) as correct_answers
                FROM participants p
                LEFT JOIN users u ON p.user_id = u.id
                LEFT JOIN player_answers pa ON p.id = pa.participant_id AND pa.session_id = %s
                LEFT JOIN answers a ON pa.answer_id = a.id
                WHERE p.game_session_id = %s
                GROUP BY p.id, u.username
                ORDER BY total_score DESC;
                """,
                (game_session_id, game_session_id),
            )
            leaderboard = cursor.fetchall()
    return leaderboard


def get_participant_answers(con, session_id: int, participant_id: int):
    """Get all answers for a specific participant in a game session"""
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT pa.*, q.question_text, a.answer_text, a.is_correct
                FROM player_answers pa
                JOIN questions q ON pa.question_id = q.id
                JOIN answers a ON pa.answer_id = a.id
                WHERE pa.session_id = %s AND pa.participant_id = %s
                ORDER BY pa.id;
                """,
                (session_id, participant_id),
            )
            answers = cursor.fetchall()
    return answers
