#!/usr/bin/env python3.10

from os import path, chmod
from random import randint as rand
from re import search as matches

from Utils import isIn, rremove, askConfirmation, askConfirmationNumber
from Types import Parameters
from Exit import exitCode, gnExit

FILE_AV:     list[str] = ["-n", "-e", "-s", "-w", "--allow-repetition", "--other-step"]
PAR_HAS_ARG: list[str] = ["b", "n", "s", "w"]
SAVE_FILEPATH:    str  = "preferences.sav"
DEF_NB_PHRASES:   str  = "?"
DEF_MAX_UBOUND:   str  = "999"
DEF_EMOJI:        bool = False
DEF_SOURCE:       str  = "./assets/source.log " # same as below
DEF_FOR_WHOM:     str  = " " # space to skip the CLI if the user used the default value as a parameter
DEF_REPETITION:   bool = False
DEF_STEP:         bool = False
DEF_ALTERNATE:    bool = False
DEF_COPY:         bool = True
DEF_VERBOSITY:    bool = False
DEF_SAVE_PREF:    bool = False
MAT_BOUNDED_INPUT: str = r"^[0-9]+,[0-9]+$"
MAT_DEFAULTING_Y:  str = "\t... using default value: yes (True)."
MAT_DEFAULTING_N:  str = "\t... using default value: no (False)."

def saveParameters(p: Parameters) -> None:
    print(f"Saving preferences in file '{SAVE_FILEPATH}'...")
    try:
        with open(SAVE_FILEPATH, "w") as f:
            f.write(f"copy={p.copy}\n")
            f.write(f"nbPhrases={p.nbPhrases}\n")
            f.write(f"emoji={p.emoji}\n")
            f.write(f"src={p.source}\n")
            f.write(f"who={p.forWhom}\n")
            f.write(f"allowRep={p.allowRep}\n")
            f.write(f"step={p.step}\n")
            f.write(f"alternate={p.alternate}\n")
        chmod(SAVE_FILEPATH, 0o644)
    except Exception as e:
        print(f"Error writing to file '{SAVE_FILEPATH}': {e}"); gnExit(exitCode.ERR_INV_FIL)

def fromCommandLine(p: Parameters, av: list[str] = []) -> Parameters:
    copy:      bool = p.copy
    nbPhrases: str  = p.nbPhrases
    emoji:     bool = p.emoji
    source:    str  = p.source
    forWhom:   str  = p.forWhom
    allowRep:  bool = p.allowRep
    step:      bool = p.step
    alternate: bool = p.alternate
    infinite:  bool = p.infinite # TODO --infinite : infinite loop, continue with key press
    saving:    bool = p.saving
    verbose:   bool = p.verbose
    randomOrNumber: str = DEF_NB_PHRASES

    if (copy == DEF_COPY and "--no-copy" not in av):
        confirmed: bool = askConfirmation("Copy the result to your clipboard")
        if (not confirmed):
            copy = False
            if (verbose): print("\tClipboard copy toggle set to {copy}.")
        else: print(MAT_DEFAULTING_Y)
    if (nbPhrases == DEF_NB_PHRASES and "-n" not in av and "--nb-phrases" not in av and "-b" not in av and "--bounds" not in av):
        while (randomOrNumber != "r" and randomOrNumber != "n"):
            randomOrNumber = input("Use a random range or number of phrases (r/n): ").strip().lower()
        if (randomOrNumber == "r"): # random quantity of phrases in bounds...
            bounds = "?"
            while (bounds == "?"):
                bounds = input("Bounds of the random range: ").strip()
                if (not matches(MAT_BOUNDED_INPUT, bounds)):
                    print("\tBounds must be of the form \"x,y\"."); bounds = "?"
                    continue
                (lowerBound, upperBound) = (int(bounds.split(",")[0]), int(bounds.split(",")[1]))
                if (int(upperBound) > int(DEF_MAX_UBOUND)): upperBound = DEF_MAX_UBOUND
                while (int(bounds.split(",")[1]) > 6):
                    buf = askConfirmationNumber(f"Warning: you set the upper bound to a large number ({upperBound})")
                    if (buf == "y"): break
                    bounds = str(lowerBound) + "," + buf
                nbPhrases = bounds
        else: # determined number of phrases...
            while (nbPhrases == DEF_NB_PHRASES):
                buf: str = input("Number of phrases to draw: ")
                nbPhrases = str(rand(2, 5) if buf == "" else int(buf))
                if (buf == ""):
                    print(f"\t... using default value: {nbPhrases}, picked randomly between 2 and 5.")
                elif (int(nbPhrases) < 1):
                    print("The number of phrases must be higher than 0."); nbPhrases = DEF_NB_PHRASES
                if (int(nbPhrases) > int(DEF_MAX_UBOUND)): nbPhrases = DEF_MAX_UBOUND
                while (int(nbPhrases) > 6):
                    buf = askConfirmationNumber(f"Warning: you set the number of phrases to a large number ({nbPhrases})")
                    if (buf == "y"): break
                    nbPhrases = buf
        if (verbose): print(f"\tNumber of phrases set to {nbPhrases}.")
    if (emoji == DEF_EMOJI and "-e" not in av and "--emoji" not in av):
        confirmed: bool = askConfirmation("Add emoji between phrases")
        if (confirmed):
            emoji = True
            if (verbose): print("\tEmoji toggle set to {emoji}.")
        else: print(MAT_DEFAULTING_N)
    if (source == DEF_SOURCE and "-s" not in av and "--source" not in av):
        source = input("What source file to use: ")
        if (source == ""):
            source = DEF_SOURCE
            print(f"\t... using default value: {DEF_SOURCE.strip()}.")
        elif (verbose): print(f"\tSource file set to '{source}'.")
    if (forWhom == DEF_FOR_WHOM and "-w" not in av and "--for-whom" not in av):
        forWhom = input("For whom the goodnight is: ").strip()
        if (forWhom == ""):
            print(f"\t... using default value: {DEF_FOR_WHOM.strip()} (no name used)).")
        elif (verbose): print(f"\tFor whom the goodnight is set to '{forWhom}'.")
    if (allowRep == DEF_REPETITION and "--allow-repetition" not in av):
        confirmed: bool = askConfirmation("Allow repetition of phrases if you ask for more than there are in the source file")
        if (confirmed):
            allowRep = True
            if (verbose): print("\tRepetition toggle set to {allowRep}.")
        else: print(MAT_DEFAULTING_N)
    if (step == DEF_STEP and "-o" not in av and "--other-step" not in av):
        confirmed: bool = askConfirmation("Use the even-numbered phrase gaps as \"and\"s instead of commas")
        if (confirmed):
            step = True
            if (verbose): print("\tStep toggle set to {step}.")
        else: print(MAT_DEFAULTING_N)
    if (emoji and alternate == DEF_ALTERNATE and "-a" not in av and "--alternate" not in av):
        confirmed: bool = askConfirmation("Alternate between \"and\"s, and emoji instead of commas")
        if (confirmed):
            alternate = True
            if (verbose): print("\tAlternating set to {alternate}.")
        else: print(MAT_DEFAULTING_N)
    newP = Parameters(c = copy, n = nbPhrases if nbPhrases != DEF_NB_PHRASES else "2,5", e = emoji, s = source.strip(), w = forWhom.strip(), \
                      r = allowRep, a = alternate, o = step, v = verbose, sav = saving)
    if (p.saving): saveParameters(newP)
    newP.pickNbPhrases()
    return newP

def fromParameters(ac: int, av: list[str]) -> Parameters:
    if (("-n" in av or "--nb-phrases" in av) and ("-b" in av or "--bounds" in av)):
        print("Cannot use both -n/--nb-phrases and -b/--bounds at the same time."); gnExit(exitCode.ERR_INV_ARG)

    def getSanitizedAv(ac: int, av: list[str]) -> (int, list[str]):
        newAv: list[str] = [av[0]]

        def isMultiOptional(s: str) -> bool: return (len(s) > 2 and s[0] == '-' and s[1] != '-')

        try:
            for i in range(1, ac):
                if (isMultiOptional(av[i])):
                    s = "".join(dict.fromkeys(av[i]))[1:] # av[i] without duplicates
                    if (isIn(PAR_HAS_ARG, s)):
                        raise ValueError(f"One of the parameters in '{s}' needs an argument.")
                    for c in s:
                        newAv.append("-" + c)
                else:
                    newAv.append(av[i])
        except ValueError as e:
            print(f"Invalid argument: {e}"); gnExit(exitCode.ERR_INV_ARG)
        newAv = list(dict.fromkeys(newAv)) # filter out all possible duplicates

        if ("--default" in newAv): # --default ignores all other parameters
            newAv.remove("--default"); newAv.insert(1, "--default")
        # if newAv has -i or --ignore, move them to the end (because they instantly jump to CLI)
        if ("--ignore" in newAv): newAv.remove("--ignore"); newAv.append("-i")
        if ("-i" in newAv):   newAv = rremove(newAv, "-i"); newAv.append("-i")
        return (len(newAv), newAv)
    (ac, av) = getSanitizedAv(ac, av)

    verbose: bool = DEF_VERBOSITY if ("--verbose" not in av) else (not DEF_VERBOSITY)
    if (verbose): print(f"\tProgram arguments interpreted as: {av}")

    extractP: Parameters = defaultParameters() if ("-i" in av) else fromFile(extraction = True)
    copy:      bool = extractP.copy
    nbPhrases: str  = extractP.nbPhrases
    emoji:     bool = extractP.emoji
    source:    str  = extractP.source
    forWhom:   str  = extractP.forWhom
    allowRep:  bool = extractP.allowRep
    step:      bool = extractP.step
    alternate: bool = extractP.alternate
    infinite:  bool = extractP.infinite
    saving:    bool = extractP.saving

    i: int = 1 # iterator needs tracking for jumping over PAR_HAS_ARG arguments
    while (i < ac): # hence can't use a for in range loop
        match av[i]:
            case "--default": return defaultParameters(fromParameter = True)
            case "--no-copy": copy = False

            case "-b" | "--bounds":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    if (matches(MAT_BOUNDED_INPUT, av[i + 1]) == None):
                        raise ValueError("Bounds must be of the form \"x,y\".")
                    (lowerBound, upperBound) = (int(av[i + 1].split(",")[0]), int(av[i + 1].split(",")[1]))
                    if (lowerBound > upperBound):
                        raise ValueError("The upper bound cannot be lower than the lower bound.")
                    if (lowerBound == 0):
                        raise ValueError("Bounds must be positive.")
                    if (int(upperBound) > int(DEF_MAX_UBOUND)): upperBound = DEF_MAX_UBOUND
                    nbPhrases = str(lowerBound) + "," + str(upperBound)
                    buf = str(upperBound)
                    while (upperBound > 6):
                        buf = askConfirmationNumber(f"Warning: you set the upper bound to a large number ({buf})")
                        if (buf == "y"): break
                        nbPhrases = nbPhrases[0:nbPhrases.find(",")] + ',' + buf
                        print(f"\t... bounds set to {nbPhrases}.")
                    i += 1
                except Exception as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-n" | "--nb-phrases":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    nbPhrases = str(int(av[i + 1])); i += 1
                    if (int(nbPhrases) < 1):
                        raise ValueError("The number of phrases must be higher than 0.")
                    if (int(nbPhrases) > int(DEF_MAX_UBOUND)): nbPhrases = DEF_MAX_UBOUND
                    while (int(nbPhrases) > 6):
                        buf = askConfirmationNumber(f"Warning: you set the number of phrases to a large number ({nbPhrases})")
                        if (buf == "y"): break
                        nbPhrases = buf
                    print(f"\t... number of phrases set to {nbPhrases}.")
                except Exception as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-e" | "--emoji": emoji = True
            case "-s" | "--source":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    source: str = av[i + 1]; i += 1
                    if (not matches(r".*\.log$", source)): source += ".log"
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-w" | "--for-whom":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    forWhom = str(av[i + 1]); i += 1
                    if (forWhom != "" and not forWhom.isalnum()):
                        raise ValueError("For whom the goodnight is must be alphanumeric.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)

            case "-r" | "--allow-repetition": allowRep = True
            case "-o" | "--other-step": step = True
            case "-a" | "--alternate": alternate = True
            case "-i" | "--ignore":
                return fromCommandLine(Parameters(c=copy, n=nbPhrases, e=emoji, s=source, w=forWhom, r=allowRep, a=alternate, o=step, v=verbose, sav=saving))
            case "-S" | "--save": saving = True

            case "--verbose": pass # still needs to be here to avoid an invalid parameter error
            case "-h" | "--help": gnExit(exitCode.HELP)

            case _: print(f"Invalid argument '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
        i += 1
    return fromCommandLine(Parameters(c=copy, n=nbPhrases, e=emoji, s=source, w=forWhom, r=allowRep, a=alternate, o=step, v=verbose, sav=saving), av + FILE_AV)

def fromFile(file: str = SAVE_FILEPATH, extraction: bool = False, noParam: bool = False) -> Parameters:
    p: Parameters = defaultParameters()

    if (not path.isfile(file)):
        print(f"File '{file}' does not exist...")
        if (extraction): p.nbPhrases = "2,5"
        else: p = fromCommandLine(p)
        if (p.saving or (not extraction and noParam)):
            saveParameters(p)
        return p
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if   (line.startswith("copy=")):      p.copy        = eval(line[len("copy="):-1])
                elif (line.startswith("nbPhrases=")): p.nbPhrases   =      line[len("nbPhrases="):-1]
                elif (line.startswith("emoji=")):     p.emoji       = eval(line[len("emoji="):-1])
                elif (line.startswith("src=")):       p.source      =      line[len("src="):-1]
                elif (line.startswith("who=")):       p.forWhom     =      line[len("who="):-1]
                elif (line.startswith("allowRep=")):  p.allowRep    = eval(line[len("allowRep="):-1])
                elif (line.startswith("step=")):      p.step        = eval(line[len("step="):-1])
                elif (line.startswith("alternate=")): p.alternate   = eval(line[len("alternate="):-1])
                else: raise ValueError(f"Invalid line '{line}'")
    except Exception as e:
        print(f"Error reading file '{file}': {e}"); gnExit(exitCode.ERR_INV_FIL)
    if (noParam): p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip() # eliminate trailing spaces used to dodge CLI cases
    return p

def defaultParameters(fromParameter: bool = False) -> Parameters:
    p = Parameters(c = DEF_COPY, n = "2,5" if fromParameter else DEF_NB_PHRASES, e = DEF_EMOJI, s = DEF_SOURCE, w = DEF_FOR_WHOM, \
                    r = DEF_REPETITION, a = DEF_ALTERNATE, o = DEF_STEP, v = DEF_VERBOSITY, sav = DEF_SAVE_PREF)
    if (fromParameter): p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip()
    return p
def getParameters(ac: int, av: list[str]) -> Parameters:
    p = fromParameters(ac, av) if (ac > 1) else fromFile(extraction = False, noParam = True)
    if (ac > 1): print("") # marking the end of parameter prints if any
    return p
