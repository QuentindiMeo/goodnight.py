#!/usr/bin/env python3.10

from os import path, remove as rm
from random import randint as rand

from Exit import exitCode, gnUsage, gnExit

SAVE_FILE:        str  = "preferences.sav"
DEF_NB_FRAGMENTS: int  = 0
DEF_TOGGLE_EMOJI: bool = False
DEF_SOURCE:       str  = "source.log"
DEF_FOR_WHOM:     str  = ""

class Parameters:
    def __str__(self) -> str:
        return f"{self.nbFragments} fragments, " \
                f"emoji: {self.toggleEmoji}, " \
                f"source: '{self.source}', " \
                f"to '{self.forWhom}'"

    def __init__(self, n: int, e: bool = DEF_TOGGLE_EMOJI, s: str = DEF_SOURCE, w: str = DEF_FOR_WHOM, v: bool = False):
        self.nbFragments = n
        self.toggleEmoji = e
        self.source      = s
        self.forWhom     = w
        self.verboseMode = v

def saveParameters(p: Parameters):
    print(f"Saving preferences in file '{SAVE_FILE}'...")
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

def fromCommandLine(p: Parameters, saving: bool = True) -> Parameters:
    nbFragments: int  = p.nbFragments
    toggleEmoji: bool = p.toggleEmoji
    source:      str  = p.source
    forWhom:     str  = p.forWhom
    verboseMode: bool = p.verboseMode

    while (nbFragments == 0):
        try:
            buf: str = input("Number of fragments to draw: ")
            nbFragments = (rand(2, 5) if buf == "" else int(buf))
            if (buf == ""):
                print(f"\t... using default value: {nbFragments}, picked randomly between 2 and 4.")
        except Exception as e:
            print(f"Invalid input: {e}")
    if (verboseMode): print(f"\tNumber of fragments set to {nbFragments}.")
    if (toggleEmoji == DEF_TOGGLE_EMOJI):
        buf: str = input("Add emoji between fragments (y/n): ")
        if (buf.lower() == "y" or buf.lower().startswith("yes")):
            toggleEmoji = True
            if (verboseMode): print("\tEmoji toggle set to True.")
        elif (not (buf.lower() == "n" or buf.lower().startswith("no"))):
            print("\t... using default value: no (False).")
    if (source == DEF_SOURCE):
        source = input("Source file: ")
        if (source == ""):
            source = DEF_SOURCE
            print(f"\t... using default value: {DEF_SOURCE}.")
        elif (verboseMode): print(f"\tSource file set to '{source}'.")
    if (forWhom == DEF_FOR_WHOM):
        forWhom = input("For whom the goodnight is: ")
        if (forWhom == ""):
            print("\t... using default value: \"\" (no name used)).")
        elif (verboseMode): print(f"\tFor whom the goodnight is set to '{forWhom}'.")
    newP: Parameters = Parameters(nbFragments, toggleEmoji, source, forWhom, verboseMode)
    if (saving): saveParameters(newP)
    else: print("") # newline for separation from the final prompt
    return newP

# TODO make random nbFragments boundable ("2,5", "1,7"...)
def fromParameters(ac: int, av: list[str]) -> Parameters:
    nbFragments: int  = 0
    toggleEmoji: bool = DEF_TOGGLE_EMOJI
    source:      str  = DEF_SOURCE
    forWhom:     str  = DEF_FOR_WHOM
    verboseMode: bool = False

    def getPurifiedAv(ac: int, av: list[str]) -> (int, list[str]):
        newAc: int = 1
        newAv: list[str] = [av[0]]

        def isMultiOptional(s: str) -> bool: return (s[0] == '-' and s[1] != '-' and len(s) > 2)

        for i in range(1, ac):
            if (not isMultiOptional(av[i])):
                newAv.append(av[i]); newAc += 1
            else:
                s = "".join(dict.fromkeys(av[i]))[1:] # av[i] without duplicates
                for c in s:
                    newAv.append("-" + c); newAc += 1

        newAv = list(dict.fromkeys(newAv)) # filter out all possible duplicates
        # if newAv has -i or --ignore, move them to the end (bc they instantly jump)
        if ("-i" in newAv):
            newAv.remove("-i"); newAv.append("-i")
        if ("--ignore" in newAv):
            newAv.remove("--ignore"); newAv.append("--ignore")
        return (newAc, newAv)
    (ac, av) = getPurifiedAv(ac, av)
    i: int = 1 # iterator needs tracking for jumping over argument values
    while (i < ac): # hence can't use a for in range loop
        if   (av[i] == "-h" or av[i] == "--help"):
            gnExit(exitCode.HELP)
        elif (av[i] == "--verbose"):
            verboseMode = True
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
        elif (av[i] == "-i" or av[i] == "--ignore"):
            return fromCommandLine(Parameters(nbFragments, toggleEmoji, source, forWhom, verboseMode), False)
        else:
            print(f"Invalid argument '{av[i]}'.")
            gnExit(exitCode.ERR_INV_ARG)
        i += 1
    if (verboseMode): print(f"av: {av}")
    p: Parameters = Parameters(nbFragments, toggleEmoji, source, forWhom, verboseMode)
    return fromCommandLine(p)

def fromFile(file: str = SAVE_FILE) -> Parameters:
    p: Parameters = defaultParameters()
    if (not path.isfile(file)):
        print(f"File '{file}' does not exist. Creating preferences file...")
        return fromCommandLine(p)
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if   (line.startswith("nbFragments=")): p.nbFragments = int( line[len("nbFragments="):-1])
                elif (line.startswith("emoji=")):       p.toggleEmoji = eval(line[len("emoji="):-1])
                elif (line.startswith("src=")):         p.source      = str( line[len("src="):-1])
                elif (line.startswith("who=")):         p.forWhom     = str( line[len("who="):-1])
                else: raise ValueError(f"Invalid line '{line}'")
    except Exception as e:
        print(f"Error reading file '{file}': {e}")
        gnExit(exitCode.ERR_INV_FIL)
    return p

def defaultParameters() -> Parameters:
    return Parameters(rand(2, 5))
# TODO set random nbFragments as a possible preference
def getParameters(ac: int, av: list[str]) -> Parameters:
    return fromParameters(ac, av) if (ac > 1) else fromFile()