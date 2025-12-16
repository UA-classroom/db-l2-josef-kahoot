from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Kahoot Schemas
class KahootCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=50)
    


class Kahoot(BaseModel):
    id: int
    title: str
    category: str  
    creation_date: datetime  
    description: Optional[str] = None


# Question Schemas
class QuestionCreate(BaseModel):
    kahoot_id: int
    question_text: str = Field(..., min_length=1, max_length=500)
    question_type: str = Field(default="multiple_choice")
    time_limit: int = Field(default=30, ge=5, le=300)  # seconds
    points: int = Field(default=1000, ge=0)

class Question(BaseModel):
    id: int
    kahoot_id: int
    media_id: Optional[int] = None
    question_text: str
    question_type: str
    time_limit: int  
    points: int


# Answer/Option Schemas
class AnswerCreate(BaseModel):
    question_id: int
    answer_text: str = Field(..., min_length=1, max_length=255)
    is_correct: bool


class Answer(BaseModel):
    id: int
    question_id: int
    answer_text: str
    is_correct: bool


# Player Schemas
class ParticipantCreate(BaseModel):
    game_session_id: int
    user_id: Optional[int] = None
    username: Optional[str] = Field(None, min_length=1, max_length=100)


class Participant(BaseModel):
    id: int
    game_session_id: int
    user_id: Optional[int] = None
    username: Optional[str] = None
    joined_at: datetime
    final_score: int
    rank: Optional[int] = None

# Game Session Schemas
class GameSessionCreate(BaseModel):
    kahoot_id: int
    session_pin: str = Field(..., min_length=4, max_length=8)


class GameSession(BaseModel):
    id: int
    kahoot_id: int
    session_pin: str
    is_active: bool
    started_at: datetime


# Player/participant Score/answer Schemas
class PlayerAnswerCreate(BaseModel):
    session_id: int
    participant_id: int
    question_id: int
    answer_id: int
    time_taken: float 

class PlayerAnswer(BaseModel):
    id: int
    session_id: int
    participant_id: int
    question_id: int
    answer_id: int
    time_taken: float
    points_earned: int


# Leaderboard Schema
class LeaderboardEntry(BaseModel):
    participant_id: int
    username: str
    total_score: int
    correct_answers: int
