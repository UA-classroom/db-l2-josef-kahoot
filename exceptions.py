"""
Custom exceptions for the Kahoot like Quiz API
"""


class KahootAppException(Exception):
    """Base exception for all kahoot application errors"""

    pass


class ResourceNotFoundException(KahootAppException):
    """Base exception for when a resource is not found"""

    pass


class KahootNotFoundException(ResourceNotFoundException):
    """Raised when a kahoot is not found"""

    def __init__(self, kahoot_id: int):
        self.kahoot_id = kahoot_id
        super().__init__(f"Kahoot with id {kahoot_id} not found")


class QuestionNotFoundException(ResourceNotFoundException):
    """Raised when a question is not found"""

    def __init__(self, question_id: int):
        self.question_id = question_id
        super().__init__(f"Question with id {question_id} not found")


class AnswerNotFoundException(ResourceNotFoundException):
    """Raised when an answer is not found"""

    def __init__(self, answer_id: int):
        self.answer_id = answer_id
        super().__init__(f"Answer with id {answer_id} not found")

