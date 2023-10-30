#!/usr/bin/env python3.10

from random import randint as rand

from typing import NewType

def drawParameters(ac = 0, av = []) -> Parameters:
    if (ac == 0): return fromFile()
    return fromCommandLine(ac, av)

def defaultParameters() -> Parameters:
    return Parameters(rand(2, 4))

class Parameters:
    def __init__(n: int, e: bool = True, forWhom: str = ""):
        self.nbFragments = n
        self.toggleEmoji = e
        self.forWhom     = forWhom
