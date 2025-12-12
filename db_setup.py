import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    connection = get_connection()
    # Implement
    with connection:
        with connection.cursor() as cur:\
            #making a usertype table to differentiate between admin, teacher and student
            cur.execute("""
                Create table if not exists usertype (
                    id SERIAL PRIMARY KEY,
                    is_admin BOOLEAN NOT NULL,
                    is_teacher BOOLEAN NOT NULL,
                    is_student BOOLEAN NOT NULL);
                    """)
            #making a users table
            cur.execute("""
                Create table if not exists users (
                    id SERIAL PRIMARY KEY,
                    usertype_id BIGINT REFERENCES usertype(id) ON DELETE SET NULL,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                    """)
            #making a kahoots table
            cur.execute(""" Create table if not exists kahoots (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(100) NOT NULL,
                        category VARCHAR(50),
                        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                        """)
            #making a enum for the different ypes of managment
            cur.execute(""" CREATE TYPE kahoot_managment AS ENUM (
                        'owner', 'editor', 'viewer'); """)
            
            #making a kahoot_user_managment table to manage permissions
            cur.execute(""" Create table if not exists kahoot_user_managment (
                        kahoot_id BIGINT REFERENCES kahoots(id) ON DELETE CASCADE,
                        user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
                        PRIMARY KEY (kahoot_id, user_id),
                        managment_type kahoot_managment NOT NULL);
                        """)
            
            #making a media table
            cur.execute(""" Create table if not exists media (
                        id SERIAL PRIMARY KEY,
                        media_type VARCHAR(50) NOT NULL,
                        file_path TEXT NOT NULL);
                        """)
            #making a questions table
            cur.execute(""" Create table if not exists questions (
                        id SERIAL PRIMARY KEY,
                        kahoot_id BIGINT REFERENCES kahoots(id) ON DELETE CASCADE,
                        media_id BIGINT REFERENCES media(id) ON DELETE SET NULL,
                        question_text TEXT NOT NULL,
                        question_type VARCHAR(50) NOT NULL,
                        time_limit INT NOT NULL,
                        points INT NOT NULL);
                        """)

            cur.execute("""CREATE TABLE IF NOT EXISTS question_media (
                        question_id BIGINT REFERENCES questions(id) ON DELETE CASCADE,
                        media_id BIGINT REFERENCES media(id) ON DELETE CASCADE,
                        PRIMARY KEY (question_id, media_id),
                        display_order INT NOT NULL);
                        """)
            #making an answers table
            cur.execute(""" Create table if not exists answers (
                        id SERIAL PRIMARY KEY,
                        question_id BIGINT REFERENCES questions(id) ON DELETE CASCADE,
                        answer_text TEXT NOT NULL,
                        is_correct BOOLEAN NOT NULL);
                        """)
            #making a game_sessions table
            cur.execute(""" Create table if not exists game_sessions (
                        id SERIAL PRIMARY KEY,
                        kahoot_id BIGINT REFERENCES kahoots(id) ON DELETE CASCADE,
                        session_pin VARCHAR(10) UNIQUE NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                        """)
            #making a particpents table
            cur.execute(""" Create table if not exists participants (
                        id SERIAL PRIMARY KEY,
                        game_session_id BIGINT REFERENCES game_sessions(id) ON DELETE CASCADE,
                        user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
                        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        final_score INT DEFAULT 0,
                        rank INT);
                        """)
            #making a player_answers table
            cur.execute(""" Create table if not exists player_answers (
                        id SERIAL PRIMARY KEY,
                        session_id BIGINT REFERENCES game_sessions(id) ON DELETE CASCADE,
                        participant_id BIGINT REFERENCES participants(id) ON DELETE CASCADE,
                        question_id BIGINT REFERENCES questions(id) ON DELETE CASCADE,
                        answer_id BIGINT REFERENCES answers(id) ON DELETE CASCADE,
                        time_taken FLOAT NOT NULL,
                        points_earned INT NOT NULL);
                        """)

if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
