from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Kahoot Schemas
class KahootCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class Kahoot(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime


# Question Schemas
class QuestionCreate(BaseModel):
    quiz_id: int
    question_text: str = Field(..., min_length=1, max_length=500)
    time_limit: int = Field(default=30, ge=5, le=300)  # seconds


class Question(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    time_limit: int
    created_at: datetime


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
class PlayerCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)


class Player(BaseModel):
    id: int
    username: str
    created_at: datetime


# Game Session Schemas
class GameSessionCreate(BaseModel):
    quiz_id: int
    pin: str = Field(..., min_length=4, max_length=8)


class GameSession(BaseModel):
    id: int
    quiz_id: int
    pin: str
    is_active: bool
    created_at: datetime


# Player Score Schemas
class PlayerAnswerCreate(BaseModel):
    game_session_id: int
    player_id: int
    question_id: int
    answer_id: int
    response_time: int = Field(..., ge=0)  # milliseconds


class PlayerScore(BaseModel):
    id: int
    game_session_id: int
    player_id: int
    question_id: int
    answer_id: int
    response_time: int
    points_earned: int
    created_at: datetime


# Leaderboard Schema
class LeaderboardEntry(BaseModel):
    player_id: int
    username: str
    total_score: int
    correct_answers: int
