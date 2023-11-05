#!/usr/bin/env python3.10

from os import path, remove as rm, chmod
from random import randint as rand
from re import search as matches
from enum import Enum

from Exit import exitCode, gnUsage, gnExit

SAVE_FILEPATH:    str  = "preferences.sav"
DEF_NB_PHRASES:   str  = "?"
DEF_TOGGLE_EMOJI: bool = False
DEF_SOURCE:       str  = "source.log " # same as below
DEF_FOR_WHOM:     str  = " " # space to skip the CLI if the user used the default value as a parameter
DEF_REPETITION:   bool = False
DEF_VERBOSE_MODE: bool = False

class Parameters:
    def pickNbPhrases(self):
        if (',' in self.nbPhrases):
            (lowerBound, upperBound) = (int(self.nbPhrases.split(",")[0]), int(self.nbPhrases.split(",")[1]))
            self.nbPhrases = str(rand(lowerBound, upperBound))

    def toString(self) -> str:
        return \
                f"{self.nbPhrases} phrases, " \
                f"emoji: {self.toggleEmoji}, " \
                f"source: {self.source}, " \
                f"for {self.forWhom}, " \
                f"repetition: {self.allowRep}"
    def __str__(self) -> str:
        return \
                f"\t{self.nbPhrases} phrases\n" \
                f"\temoji: {self.toggleEmoji}\n" \
                f"\tsource file: {self.source}\n" \
                f"\tfor {self.forWhom}\n" \
                f"\trepetition: {self.allowRep}"

    def __init__(self, n: str, e: bool = DEF_TOGGLE_EMOJI, s: str = DEF_SOURCE, w: str = DEF_FOR_WHOM, r: bool = DEF_REPETITION, v: bool = DEF_VERBOSE_MODE, sav: bool = True):
        self.nbPhrases   = n
        self.toggleEmoji = e
        self.source      = s
        self.forWhom     = w
        self.allowRep    = r
        self.verboseMode = v
        self.savePref    = sav

def saveParameters(p: Parameters):
    print(f"Saving preferences in file '{SAVE_FILEPATH}'...")
    try:
        with open(SAVE_FILEPATH, "w") as f:
            f.write(f"nbPhrases={p.nbPhrases}\n")
            f.write(f"emoji={p.toggleEmoji}\n")
            f.write(f"src={p.source}\n")
            f.write(f"who={p.forWhom}\n")
            f.write(f"allowRep={p.allowRep}\n")
        chmod(SAVE_FILEPATH, 0o644)
    except Exception as e:
        print(f"Error writing to file '{SAVE_FILEPATH}': {e}")
        gnExit(exitCode.ERR_INV_FIL)
    print("") # newline for separation from the final prompt

def fromCommandLine(p: Parameters) -> Parameters:
    nbPhrases:   str  = p.nbPhrases
    toggleEmoji: bool = p.toggleEmoji
    source:      str  = p.source
    forWhom:     str  = p.forWhom
    allowRep:    bool = p.allowRep
    verboseMode: bool = p.verboseMode
    randomOrNumber: str = DEF_NB_PHRASES

    if (nbPhrases == DEF_NB_PHRASES):
        while (randomOrNumber != "r" and randomOrNumber != "n"):
            randomOrNumber = input("Use a random range or number of phrases (r/n): ").strip().lower()
        if (randomOrNumber == "r"):
            bounds = ""
            while (bounds == ""):
                bounds = input("Bounds of the random range: ").strip()
                if (not matches("^[0-9]+,[0-9]+$", bounds)):
                    print("\tBounds must be of the form \"x,y\".")
                    bounds = ""
                    continue
                buf: str = ""
                while (int(bounds.split(",")[1]) > 6 and buf != "y"):
                    (lowerBound, upperBound) = (int(bounds.split(",")[0]), int(bounds.split(",")[1]))
                    buf = input(f"Warning: you set the upper bound to a large number ({upperBound}). Continue or change (y/?): ").strip().lower()
                    if (buf == "y"): break
                    if (not matches("^[0-9]+$", buf)): print("Invalid input: must be a positive number or 'y'."); continue
                    bounds = str(lowerBound) + "," + buf
                nbPhrases = bounds
        else: # randomOrNumber == "n"
            while (nbPhrases == DEF_NB_PHRASES):
                try:
                    buf: str = input("Number of phrases to draw: ")
                    nbPhrases = str(rand(2, 5) if buf == "" else int(buf))
                    if (buf == ""):
                        print(f"\t... using default value: {nbPhrases}, picked randomly between 2 and 5.")
                    elif (int(nbPhrases) < 1):
                        print("The number of phrases must be higher than 0."); nbPhrases = DEF_NB_PHRASES
                    while (int(nbPhrases) > 6):
                        buf = input(f"Warning: you set the number of phrases to a large number ({nbPhrases}). Continue or change (y/?): ").strip().lower()
                        if (buf == "y"): break
                        if (not matches("^[0-9]+$", buf)): print("Invalid input: must be a positive number or 'y'."); continue
                        nbPhrases = buf
                except Exception as e:
                    print(f"Invalid input: {e}")
        if (verboseMode): print(f"\tNumber of phrases set to {nbPhrases}.")
    if (toggleEmoji == DEF_TOGGLE_EMOJI):
        buf: str = input("Add emoji between phrases (y/n): ")
        if (buf.lower() == "y" or buf.lower().startswith("yes")):
            toggleEmoji = True
            if (verboseMode): print("\tEmoji toggle set to True.")
        elif (not (buf.lower() == "n" or buf.lower().startswith("no"))):
            print("\t... using default value: no (False).")
    if (source == DEF_SOURCE):
        source = input("What source file to use: ")
        if (source == ""):
            source = DEF_SOURCE
            print(f"\t... using default value: {DEF_SOURCE.strip()}.")
        elif (verboseMode): print(f"\tSource file set to '{source}'.")
    if (forWhom == DEF_FOR_WHOM):
        forWhom = input("For whom the goodnight is: ").strip()
        if (forWhom == ""):
            print(f"\t... using default value: {DEF_FOR_WHOM.strip()} (no name used)).")
        elif (verboseMode): print(f"\tFor whom the goodnight is set to '{forWhom}'.")
    if (allowRep == DEF_REPETITION):
        buf: str = input("Allow repetition of phrases if you request more phrases then you have possibilities (y/n): ")
        if (buf.lower() == "y" or buf.lower().startswith("yes")):
            allowRep = True
            if (verboseMode): print("\tRepetition toggle set to True.")
        elif (buf.lower() == "n" or buf.lower().startswith("no")):
            print("\tRepetition toggle set to False.")
        else: print("\t... using default value: no (False).")
    newP = Parameters(nbPhrases, toggleEmoji, source.strip(), forWhom.strip(), allowRep, verboseMode, p.savePref)
    if (p.savePref): saveParameters(newP)
    else: print("") # newline for separation from the final prompt
    newP.pickNbPhrases()
    return newP

# TODO disallow parameter that needs an argument to be in a multi-optional parameter
def fromParameters(ac: int, av: list[str]) -> Parameters:
    if (("-n" in av or "--nb-phrases" in av) and ("-b" in av or "--bounds" in av)):
        print("Cannot use both -n/--nb-phrases and -b/--bounds at the same time."); gnExit(exitCode.ERR_INV_ARG)
    if ("--isave" in av and "-i" not in av and "--ignore" not in av): av.append("-i")
    def getPurifiedAv(ac: int, av: list[str]) -> (int, list[str]):
        newAc: int = 1
        newAv: list[str] = [av[0]]

        def isMultiOptional(s: str) -> bool: return (len(s) > 2 and s[0] == '-' and s[1] != '-')

        for i in range(1, ac + 1):
            if (not isMultiOptional(av[i])):
                newAv.append(av[i]); newAc += 1
            else:
                s = "".join(dict.fromkeys(av[i]))[1:] # av[i] without duplicates
                for c in s:
                    newAv.append("-" + c); newAc += 1
        newAv = list(dict.fromkeys(newAv)) # filter out all possible duplicates

        if ("--default" in newAv): # --default ignores all other parameters
            newAv.remove("--default"); newAv.insert(1, "--default")
        # if newAv has -i or --ignore, move them to the end (because they instantly jump to CLI)
        if ("-i" in newAv):
            newAv.remove("-i"); newAv.append("-i")
        if ("--ignore" in newAv):
            newAv.remove("--ignore"); newAv.append("--ignore")
        return (newAc, newAv)
    (ac, av) = getPurifiedAv(ac, av)
    verboseMode: bool = DEF_VERBOSE_MODE if ("--verbose" not in av) else (not DEF_VERBOSE_MODE)
    if (verboseMode): print(f"\tProgram arguments interpreted as: {av}\n")

    extractP: Parameters = defaultParameters(False) if "-i" in av else fromFile(extraction = True)
    nbPhrases:   str  = extractP.nbPhrases
    toggleEmoji: bool = extractP.toggleEmoji
    source:      str  = extractP.source
    forWhom:     str  = extractP.forWhom
    allowRep:    bool = extractP.allowRep
    isaving:     bool = False

    i: int = 1 # iterator needs tracking for jumping over argument values
    while (i < ac): # hence can't use a for in range loop
        if   (av[i] == "-h" or av[i] == "--help"):
            gnExit(exitCode.HELP)
        elif (av[i] == "--default"): return defaultParameters()
        elif (av[i] == "--verbose"): pass # still needs to be here to avoid an invalid parameter error
        elif (av[i] == "-b" or av[i] == "--bounds"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
            try:
                if (matches("^[0-9]+,[0-9]+$", av[i + 1]) == None):
                    raise ValueError("Bounds must be of the form \"x,y\".")
                (lowerBound, upperBound) = (int(av[i + 1].split(",")[0]), int(av[i + 1].split(",")[1]))
                if (lowerBound > upperBound):
                    raise ValueError("The upper bound cannot be lower than the lower bound.")
                if (lowerBound == 0):
                    raise ValueError("Bounds must be positive.")
                buf: str = ""
                while (upperBound > 6 and buf != "y"):
                    buf = input(f"Warning: you set the upper bound to a large number ({upperBound}). Continue or change (y/?): ").strip().lower()
                    if (buf == "y"): break
                    if (not matches("^[0-9]+$", buf)): print("Invalid input: must be a positive number or 'y'."); continue
                    upperBound = int(buf)
                nbPhrases = av[i + 1]; i += 1
                print(f"\t... bounds set to {nbPhrases}.")
            except Exception as e:
                print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-n" or av[i] == "--nb-phrases"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
            try:
                nbPhrases = str(int(av[i + 1])); i += 1
                if (int(nbPhrases) < 1):
                    raise ValueError("The number of phrases must be higher than 0.")
                while (int(nbPhrases) > 6):
                    buf = input(f"Warning: you set the number of phrases to a large number ({nbPhrases}). Continue or change (y/?): ").strip().lower()
                    if (buf == "y"): break
                    if (not matches("^[0-9]+$", buf)): print("Invalid input: must be a positive number or 'y'."); continue
                    nbPhrases = buf
                    print(f"\t... number of phrases set to {nbPhrases}.")
            except Exception as e:
                print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-e" or av[i] == "--emoji"):
            toggleEmoji = True
        elif (av[i] == "-s" or av[i] == "--source"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
            try:
                # TODO force source to be a .log file
                source: str = av[i + 1]; i += 1
            except ValueError as e:
                print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "-w" or av[i] == "--for-whom"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
            try:
                forWhom = str(av[i + 1]); i += 1
                if (forWhom != "" and not forWhom.isalnum()):
                    raise ValueError("For whom the goodnight is must be alphanumeric.")
            except ValueError as e:
                print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
        elif (av[i] == "--allow-repetition"): allowRep = True
        elif (av[i] == "-i" or av[i] == "--ignore"):
            return fromCommandLine(Parameters(nbPhrases, toggleEmoji, source, forWhom, allowRep, verboseMode, isaving))
        elif (av[i] == "--isave"): isaving = True
        else:
            print(f"Invalid argument '{av[i]}'.")
            gnExit(exitCode.ERR_INV_ARG)
        i += 1
    return fromCommandLine(Parameters(nbPhrases, toggleEmoji, source, forWhom, allowRep, verboseMode))

def fromFile(file: str = SAVE_FILEPATH, extraction: bool = False) -> Parameters:
    p: Parameters = defaultParameters()
    if (not path.isfile(file)):
        print(f"File '{file}' does not exist. Creating preferences file...")
        if (extraction): p.nbPhrases = DEF_NB_PHRASES
        return p if (extraction) else fromCommandLine(p)
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if   (line.startswith("nbPhrases=")): p.nbPhrases   =      line[len("nbPhrases="):-1]
                elif (line.startswith("emoji=")):     p.toggleEmoji = eval(line[len("emoji="):-1])
                elif (line.startswith("src=")):       p.source      =      line[len("src="):-1]
                elif (line.startswith("who=")):       p.forWhom     =      line[len("who="):-1]
                elif (line.startswith("allowRep=")):  p.allowRep    = eval(line[len("allowRep="):-1])
                else: raise ValueError(f"Invalid line '{line}'")
    except Exception as e:
        print(f"Error reading file '{file}': {e}"); gnExit(exitCode.ERR_INV_FIL)
    p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip()
    return p

def defaultParameters(fromParameter: bool = True) -> Parameters:
    p = Parameters("2,5" if fromParameter else DEF_NB_PHRASES, DEF_TOGGLE_EMOJI, DEF_SOURCE, DEF_FOR_WHOM, DEF_REPETITION, DEF_VERBOSE_MODE)
    p.pickNbPhrases()
    return p
def getParameters(ac: int, av: list[str]) -> Parameters:
    return fromParameters(ac, av) if (ac > 1) else fromFile()