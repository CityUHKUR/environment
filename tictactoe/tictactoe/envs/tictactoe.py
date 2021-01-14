import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


def getRow(index):
    return (index / 3) | 0


def getColumn(index):
    return index % 3


def getIndex(r, c):
    return r * 3 + c


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidAction(Error):
    """Exception raised for errors due to invalid action.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class TicTacToeENV(gym.Env):

    def __init__(self, metadata={}):
        self.metadata = {'player': 1, 'enemy': 2}
        self.metadata.update(metadata)
        self.boardState = np.zeros((9))
        self.LINES = {}
        for i in range(8):
            self.LINES[i] = []
        self.player = self.metadata['player']
        self.enemy = self.metadata['enemy']
        self.turn = 1
        self.end_game = False
        for i in range(3):

            for j in range(3):
                self.LINES[i].append(getIndex(i, j))
                self.LINES[i + 3].append(getIndex(j, i))

            self.LINES[6].append(getIndex(i, i))
            self.LINES[7].append(getIndex(i, 2 - i))

    def checkLineCondition(self, entries, hasNumberOfCell, playerID):
        return len(list(filter(lambda x: x == playerID, self.boardState[entries]))) >= hasNumberOfCell

    def checkWinCondition(self, playerID):

        for j in range(8):

            if self.checkLineCondition(self.LINES[j], 3, playerID):

                return True
        return False

    def reward(self, state):
        if self.checkWinCondition(self.player):
            return 100
        elif self.checkWinCondition(self.enemy):
            return -1
        else:
            return 1

    def step(self, action):
        s = self.boardState[action]
        if self.end_game:
            raise InvalidAction("Player {} has Win, please start a new game"
                                .format(
                                    self.self.player if self.checkWinCondition(
                                        self.player) else self.enemy))
        else:
            if self.boardState[action] != 0:
                raise InvalidAction(
                    "cell is played before, please choice another cell")
            else:
                self.boardState[action] = self.turn

        self.turn = self.enemy if (
            self.turn == self.player) else self.player
        self.end_game = self.checkWinCondition(
            self.player) or self.checkWinCondition(self.enemy)

        return s, self.end_game, self.reward(self.boardState), self.boardState

    def reset(self):
        self.boardState = np.zeros((3, 3))
        self.turn = self.player

    def close(self):
        return None
