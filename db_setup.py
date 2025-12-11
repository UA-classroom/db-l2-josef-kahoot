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
        with connection.cursor() as cur:
            cur.execute("""
                Create table if not exists usertype (
                    id SERIAL PRIMARY KEY,
                    is_admin BOOLEAN NOT NULL,
                    is_teacher BOOLEAN NOT NULL,
                    is_student BOOLEAN NOT NULL);
                    """)
            cur.execute("""
                Create table if not exists users (
                    id SERIAL PRIMARY KEY,
                    usertype_id BIGINT REFERENCES usertype(id) ON DELETE SET NULL,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                    """)
            
            # cur.execute(""" Create table if not exists kahoots (
            #             id SERIAL PRIMARY KEY,
            #             )
                        
            #             """)

if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
