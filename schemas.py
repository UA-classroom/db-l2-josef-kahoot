from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Kahoot Schemas
class KahootCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None
    


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
    time_limit: int = Field(default=30, ge=5, le=300)  # seconds


class Question(BaseModel):
    id: int
    kahoot_id: int
    media_id: Optional[int] = None
    question_text: str
    time_limit: int | None = None
    points: int | None = None


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
    username: str = Field(..., min_length=1, max_length=100)


class Participant(BaseModel):
    id: int
    username: str
    created_at: datetime


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
    player_id: int
    username: str
    total_score: int
    correct_answers: int
