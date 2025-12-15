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


class PlayerNotFoundException(ResourceNotFoundException):
    """Raised when a player is not found"""

    def __init__(self, player_id: int):
        self.player_id = player_id
        super().__init__(f"Player with id {player_id} not found")


class GameSessionNotFoundException(ResourceNotFoundException):
    """Raised when a game session is not found"""

    def __init__(self, identifier: int | str, identifier_type: str = "id"):
        self.identifier = identifier
        self.identifier_type = identifier_type
        if identifier_type == "pin":
            super().__init__(f"Game session with pin '{identifier}' not found")
        else:
            super().__init__(f"Game session with id {identifier} not found")


class DatabaseException(KahootAppException):
    """Raised when a database operation fails"""

    def __init__(self, operation: str, details: str = None):
        self.operation = operation
        self.details = details
        message = f"Database error during {operation}"
        if details:
            message += f": {details}"
        super().__init__(message)

