"""
Custom exceptions for the Kahoot like Quiz API
"""


class QuizAppException(Exception):
    """Base exception for all quiz application errors"""

    pass


class ResourceNotFoundException(QuizAppException):
    """Base exception for when a resource is not found"""

    pass


class QuizNotFoundException(ResourceNotFoundException):
    """Raised when a quiz is not found"""

    def __init__(self, quiz_id: int):
        self.quiz_id = quiz_id
        super().__init__(f"Quiz with id {quiz_id} not found")


class QuestionNotFoundException(ResourceNotFoundException):
    """Raised when a question is not found"""

    def __init__(self, question_id: int):
        self.question_id = question_id
        super().__init__(f"Question with id {question_id} not found")


