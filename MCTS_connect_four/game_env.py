from abc import abstractmethod


class game_env:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_board(self, state):
        pass

    @abstractmethod
    def make_move(self, move):
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

    @abstractmethod
    def get_legal_moves(self) -> list:
        pass

    @abstractmethod
    def get_state(self) -> list:
        pass

    @abstractmethod
    def get_dict(self) -> dict:
        pass

    @abstractmethod
    def get_state_history(self) -> list:
        pass

    @abstractmethod
    def get_string(self) -> str:
        pass
