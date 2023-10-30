#!/usr/bin/env python3.10

from random import randint as rand

class Parameters:
    def __str__(self) -> str:
        return f"{self.nbFragments} fragments, emoji: {self.toggleEmoji}, to '{self.forWhom}'"

    def __init__(self, n: int, e: bool = True, forWhom: str = ""):
        self.nbFragments = n
        self.toggleEmoji = e
        self.forWhom     = forWhom

def fromCommandLine(ac: int, av: list[str]) -> Parameters:
    p: Parameters = Parameters(rand(2, 4))
    # TODO
    return p

def fromFile(file: str = "parameters.sav") -> Parameters:
    p: Parameters = Parameters(rand(2, 4))
    # TODO
    return p

def drawParameters(ac = 0, av = []) -> Parameters:
    return fromFile() if (ac == 0) else fromCommandLine(ac, av)
def defaultParameters() -> Parameters:
    return Parameters(rand(2, 4))

def getParameters(ac: int, av: list[str]) -> Parameters:
    p: Parameters = {}
    # TODO
    if   (1): p = drawParameters(ac, av)
    elif (1): p = drawParameters()
    else    : p = defaultParameters()
    return p
