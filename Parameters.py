#!/usr/bin/env python3.10

from os import path
from random import randint as rand

from Exit import exitCode, gnUsage, gnExit

class Parameters:
    def __str__(self) -> str:
        return f"{self.nbFragments} fragments, " \
                f"emoji: {self.toggleEmoji}, " \
                f"source: '{self.source}', " \
                f"to '{self.forWhom}'"

    def __init__(self, n: int, e: bool = False, source: str = "source.log", forWhom: str = ""):
        self.nbFragments = n
        self.toggleEmoji = e
        self.source      = source
        self.forWhom     = forWhom

def fromCommandLine(p: Parameters) -> Parameters:
    nbFragments: int  = p.nbFragments
    toggleEmoji: bool = p.toggleEmoji
    source:      str  = p.source
    forWhom:     str  = p.forWhom

    while (nbFragments == 0):
        try:
            buf: str = input("Number of fragments to draw: ")
            nbFragments = (rand(2, 4) if buf == "" else int(buf))
            if (buf == ""):
                print(f"Using default value: {nbFragments} picked randomly between 2 and 4.")
        except Exception as e:
            print(f"Invalid input: {e}")
    if (toggleEmoji == False):
        buf: str = input("Add emoji between fragments (y/n): ")
        if (buf.lower() == "y" or buf.lower().startswith("yes")):
            toggleEmoji = True
        elif (buf == ""):
            print("Using default value: \"no (False)\".")
    if (source == ""):
        source = input("Source file: ")
        if (source == ""):
            print("Using default value: \"source.log\".")
    if (forWhom == ""):
        forWhom = input("For whom the goodnight is: ")
        if (forWhom == ""):
            print("Using default value: \"\".")
    return Parameters(nbFragments, toggleEmoji, source, forWhom)

def fromParameters(ac: int, av: list[str]) -> Parameters:
    nbFragments: int = 0
    toggleEmoji: bool = False
    source:      str = "source.log"
    forWhom:     str = ""

    i: int = 1 # iterator needs tracking for jumping over argument values
    while (i < ac): # hence can't use a for in range loop
        if   (av[i] == "-n" or av[i] == "--nb-fragments"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'.")
                gnExit(exitCode.ERR_INV_ARG)
            try:
                nbFragments = int(av[i + 1]); i += 1
            except Exception as e:
                print(f"Invalid argument for '{av[i]}': {e}")
                gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-e" or av[i] == "--emoji"):
            toggleEmoji = True
        elif (av[i] == "-s" or av[i] == "--source"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'.")
                gnExit(exitCode.ERR_INV_ARG)
            try:
                source = str(av[i + 1]); i += 1
                if (not path.isfile(source)):
                    raise ValueError(f"The mentioned source file '{av[i]}' cannot be found.")
            except ValueError as e:
                print(f"Invalid argument for '{av[i]}': {e}")
                gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-w" or av[i] == "--for-whom"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'.")
                gnExit(exitCode.ERR_INV_ARG)
            try:
                forWhom = str(av[i + 1]); i += 1
                if (not forWhom.isalnum()):
                    raise ValueError("For whom the goodnight is must be alphanumeric.")
            except ValueError as e:
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
    p: Parameters = defaultParameters()
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

def defaultParameters() -> Parameters:
    return Parameters(rand(2, 4))

def getParameters(ac: int = 1, av: list[str] = []) -> Parameters:
    return fromParameters(ac, av) if (ac > 1) else fromFile()