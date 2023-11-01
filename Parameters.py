#!/usr/bin/env python3.10

from os import path
from random import randint as rand

from Exit import exitCode, gnUsage, gnExit

class Parameters:
    def __str__(self) -> str:
        return f"{self.nbFragments} fragments, emoji: {self.toggleEmoji}, to '{self.forWhom}'"

    def __init__(self, n: int, e: bool = False, forWhom: str = ""):
        self.nbFragments = n
        self.toggleEmoji = e
        self.forWhom     = forWhom

def fromCommandLine(p: Parameters) -> Parameters:
    nbFragments: int = p.nbFragments
    toggleEmoji: bool = p.toggleEmoji
    forWhom: str = p.forWhom
    while (nbFragments == 0):
        try:
            nbFragments = int(input("Number of fragments to draw: "))
        except Exception as e:
            print(f"Invalid input: {e}")
    if (forWhom == ""):
        forWhom = input("For whom the goodnight is: ")
    return Parameters(nbFragments, toggleEmoji, forWhom)

def fromParameters(ac: int, av: list[str]) -> Parameters:
    nbFragments: int = 0
    toggleEmoji: bool = False
    forWhom: str = ""

    i: int = 1
    while (i < ac):
        if   (av[i] == "-n" or av[i] == "--nb-fragments"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'.")
                gnExit(exitCode.ERR_INV_ARG)
            try:
                nbFragments = int(av[i + 1])
                i += 1
            except Exception as e:
                print(f"Invalid argument for '{av[i]}': {e}")
                gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-e" or av[i] == "--emoji"):
            toggleEmoji = True
        elif (av[i] == "-w" or av[i] == "--for-whom"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'.")
                gnExit(exitCode.ERR_INV_ARG)
            try:
                forWhom = str(av[i + 1])
                i += 1
            except Exception as e:
                print(f"Invalid argument for '{av[i]}': {e}")
                gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-h" or av[i] == "--help"):
            gnExit(exitCode.HELP)
        else:
            print(f"Invalid argument '{av[i]}'.")
            gnExit(exitCode.ERR_INV_ARG)
        i += 1
    return Parameters(nbFragments, toggleEmoji, forWhom)

def fromFile(file: str = "parameters.sav") -> Parameters:
    p: Parameters = Parameters(rand(2, 4))
    if (not path.isfile(file)):
        print(f"File '{file}' does not exist.")
        if (file == "parameters.sav"):
            print("Creating parameters file...")
            return fromCommandLine(p)
        gnExit(exitCode.ERR_INV_FIL)
    try:
        with open(file, "r") as f:
            # TODO
            pass
    except Exception as e:
        print(f"Error reading file '{file}': {e}")
        gnExit(exitCode.ERR_INV_FIL)
    return p

def drawParameters(ac = 1, av = []) -> Parameters:
    return fromParameters(ac, av) if (ac != 1) else fromFile()
def defaultParameters() -> Parameters:
    return Parameters(rand(2, 4))

def getParameters(ac: int, av: list[str]) -> Parameters:
    if   (1): return drawParameters(ac, av)
    elif (1): return drawParameters()
    else    : return defaultParameters()
