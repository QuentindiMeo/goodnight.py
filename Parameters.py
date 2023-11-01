#!/usr/bin/env python3.10

from os import path, remove as rm
from random import randint as rand

from Exit import exitCode, gnUsage, gnExit

SAVE_FILE:        str  = "preferences.sav"
DEF_TOGGLE_EMOJI: bool = False
DEF_SOURCE:       str  = "source.log"
DEF_FOR_WHOM:     str  = ""

class Parameters:
    def __str__(self) -> str:
        return f"{self.nbFragments} fragments, " \
                f"emoji: {self.toggleEmoji}, " \
                f"source: '{self.source}', " \
                f"to '{self.forWhom}'"

    def __init__(self, n: int, e: bool = DEF_TOGGLE_EMOJI, source: str = DEF_SOURCE, forWhom: str = DEF_FOR_WHOM):
        self.nbFragments = n
        self.toggleEmoji = e
        self.source      = source
        self.forWhom     = forWhom

def saveParameters(p: Parameters):
    print(f"Saving parameters to file '{SAVE_FILE}'...")
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(f"nbFragments={p.nbFragments}\n")
            f.write(f"emoji={p.toggleEmoji}\n")
            f.write(f"src={p.source}\n")
            f.write(f"who={p.forWhom}\n")
    except Exception as e:
        print(f"Error writing to file '{SAVE_FILE}': {e}")
        gnExit(exitCode.ERR_INV_FIL)
    print("") # newline for separation from the final prompt

def fromCommandLine(p: Parameters, saving: bool = False) -> Parameters:
    nbFragments: int  = p.nbFragments
    toggleEmoji: bool = p.toggleEmoji
    source:      str  = p.source
    forWhom:     str  = p.forWhom

    while (nbFragments == 0):
        try:
            buf: str = input("Number of fragments to draw: ")
            nbFragments = (rand(2, 4) if buf == "" else int(buf))
            if (buf == ""):
                print(f"\t... using default value: {nbFragments}, picked randomly between 2 and 4.")
        except Exception as e:
            print(f"Invalid input: {e}")
    if (toggleEmoji == DEF_TOGGLE_EMOJI):
        buf: str = input("Add emoji between fragments (y/n): ")
        if (buf.lower() == "y" or buf.lower().startswith("yes")):
            toggleEmoji = True
        elif (not (buf.lower() == "n" or buf.lower().startswith("no"))):
            print("\t... using default value: no (False).")
    if (source == DEF_SOURCE):
        source = input("Source file: ")
        if (source == ""):
            source = DEF_SOURCE
            print(f"\t... using default value: {DEF_SOURCE}.")
    if (forWhom == DEF_FOR_WHOM):
        forWhom = input("For whom the goodnight is: ")
        if (forWhom == ""):
            print("\t... using default value: \"\" (no name used)).")
    newP: Parameters = Parameters(nbFragments, toggleEmoji, source, forWhom)
    if (saving): saveParameters(newP)
    return newP

def fromParameters(ac: int, av: list[str]) -> Parameters:
    nbFragments: int = 0
    toggleEmoji: bool = DEF_TOGGLE_EMOJI
    source:      str  = DEF_SOURCE
    forWhom:     str  = DEF_FOR_WHOM
    saving:      bool = False

    if ("-D" in av and ("-i" in av or "--ignore" in av)):
        if ("-h" in av or "--help" in av):
            gnExit(exitCode.HELP)
        print("Cannot use both '-D' and '-i'/'--ignore' at the same time.")
        gnUsage()
        gnExit(exitCode.ERR_INV_ARG)
    # TODO add support for strings like "-nsew"
    i: int = 1 # iterator needs tracking for jumping over argument values
    while (i < ac): # hence can't use a for in range loop
        if (av[i] == "-h" or av[i] == "--help"):
            gnExit(exitCode.HELP)
        elif (av[i] == "-n" or av[i] == "--nb-fragments"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'.")
                gnExit(exitCode.ERR_INV_ARG)
            try:
                nbFragments = int(av[i + 1]); i += 1
                if (nbFragments <= 0):
                    raise ValueError("Number of fragments must be positive.")
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
        elif (av[i] == "-D"):
            saving = True
        elif (av[i] == "-i" or av[i] == "--ignore"):
            return fromCommandLine(Parameters(nbFragments, toggleEmoji, source, forWhom))
        else:
            print(f"Invalid argument '{av[i]}'.")
            gnExit(exitCode.ERR_INV_ARG)
        i += 1
    p: Parameters = Parameters(nbFragments, toggleEmoji, source, forWhom)
    return fromCommandLine(p, True) if (saving) else p

def fromFile(file: str = SAVE_FILE) -> Parameters:
    p: Parameters = defaultParameters()
    if (not path.isfile(file)):
        print(f"File '{file}' does not exist. Creating preferences file...")
        return fromCommandLine(p, True)
    try:
        with open(file, "r") as f:
            # TODO draw parameters from file
            pass
    except Exception as e:
        print(f"Error reading file '{file}': {e}")
        gnExit(exitCode.ERR_INV_FIL)
    return p

def defaultParameters() -> Parameters:
    return Parameters(rand(2, 4))

def getParameters(ac: int = 1, av: list[str] = []) -> Parameters:
    return fromParameters(ac, av) if (ac > 1) else fromFile()