#!/usr/bin/env python3.10

from os import path, chmod, name as osName
from random import randint as rand
from re import search as matches

from Utils import isIn, rremove, askConfirmation, askConfirmationNumber
from Exit import exitCode, gnExit

FILE_AV:     list[str] = ["-n", "-e", "-s", "-w", "--allow-repetition", "--other-step"]
PAR_HAS_ARG: list[str] = ["b", "n", "s", "w"]
SAVE_FILEPATH:    str  = "preferences.sav"
DEF_NB_PHRASES:   str  = "?"
DEF_MAX_UBOUND:   str  = "999"
DEF_TOGGLE_EMOJI: bool = False
DEF_SOURCE:       str  = "./assets/source.log " # same as below
DEF_FOR_WHOM:     str  = " " # space to skip the CLI if the user used the default value as a parameter
DEF_REPETITION:   bool = False
DEF_STEP:         bool = False
DEF_VERBOSE_MODE: bool = False
DEF_SAVE_PREF:    bool = False
MAT_NUMBERS_INPUT: str = r"^[0-9]+$"
MAT_INVALID_INPUT: str = "Invalid input: must be a positive number or 'y'."
MAT_DEFAULTING:    str = "\t... using default value: no (False)."

class Parameters:
    def pickNbPhrases(self) -> None:
        if (',' in self.nbPhrases):
            (lowerBound, upperBound) = (int(self.nbPhrases.split(",")[0]), int(self.nbPhrases.split(",")[1]))
            self.nbPhrases = str(rand(lowerBound, upperBound))

    def toString(self) -> str:
        source = self.source.split("\\" if osName == 'nt' else "/")[-1]
        wEmoji = "with" if self.toggleEmoji else "without"
        repetition = "allowed" if self.allowRep else "not allowed"
        step = ("even" if self.step else "odd") + "-numbered gaps"
        return \
                f"{self.nbPhrases} phrases, " \
                f"{wEmoji} emoji, " \
                f"source: {source}, " \
                f"for {self.forWhom}, " \
                f"repetition {repetition}, " \
                f"step: {step}"
    def __str__(self) -> str:
        return \
                f"\t{self.nbPhrases} phrases\n" \
                f"\temoji: {self.toggleEmoji}\n" \
                f"\tsource file: {self.source}\n" \
                f"\tfor: {self.forWhom}\n" \
                f"\trepetition: {self.allowRep}\n" \
                f"\tstep: {self.step}"

    def __init__(self, n: str, e: bool = DEF_TOGGLE_EMOJI, s: str = DEF_SOURCE, w: str = DEF_FOR_WHOM, \
                 r: bool = DEF_REPETITION, o: bool = DEF_STEP, v: bool = DEF_VERBOSE_MODE, sav: bool = DEF_SAVE_PREF) -> None:
        self.nbPhrases   = n
        self.toggleEmoji = e
        self.source      = s
        self.forWhom     = w
        self.allowRep    = r
        self.step        = o
        self.verboseMode = v
        self.saving      = sav

def saveParameters(p: Parameters) -> None:
    print(f"Saving preferences in file '{SAVE_FILEPATH}'...")
    try:
        with open(SAVE_FILEPATH, "w") as f:
            f.write(f"nbPhrases={p.nbPhrases}\n")
            f.write(f"emoji={p.toggleEmoji}\n")
            f.write(f"src={p.source}\n")
            f.write(f"who={p.forWhom}\n")
            f.write(f"allowRep={p.allowRep}\n")
            f.write(f"step={p.step}\n")
        chmod(SAVE_FILEPATH, 0o644)
    except Exception as e:
        print(f"Error writing to file '{SAVE_FILEPATH}': {e}"); gnExit(exitCode.ERR_INV_FIL)

def fromCommandLine(p: Parameters, av: list[str] = []) -> Parameters:
    nbPhrases:   str  = p.nbPhrases
    toggleEmoji: bool = p.toggleEmoji
    source:      str  = p.source
    forWhom:     str  = p.forWhom
    allowRep:    bool = p.allowRep
    step:        bool = p.step
    verboseMode: bool = p.verboseMode
    saving:      bool = p.saving
    randomOrNumber: str = DEF_NB_PHRASES

    if (nbPhrases == DEF_NB_PHRASES and "-n" not in av and "--nb-phrases" not in av and "-b" not in av and "--bounds" not in av):
        while (randomOrNumber != "r" and randomOrNumber != "n"):
            randomOrNumber = input("Use a random range or number of phrases (r/n): ").strip().lower()
        if (randomOrNumber == "r"):
            bounds = "?"
            while (bounds == "?"):
                bounds = input("Bounds of the random range: ").strip()
                if (not matches(r"^[0-9]+,[0-9]+$", bounds)):
                    print("\tBounds must be of the form \"x,y\"."); bounds = "?"
                    continue
                (lowerBound, upperBound) = (int(bounds.split(",")[0]), int(bounds.split(",")[1]))
                if (int(upperBound) > int(DEF_MAX_UBOUND)): upperBound = DEF_MAX_UBOUND
                while (int(bounds.split(",")[1]) > 6):
                    buf = askConfirmationNumber(f"Warning: you set the upper bound to a large number ({upperBound})")
                    if (buf == "y"): break
                    bounds = str(lowerBound) + "," + buf
                nbPhrases = bounds
        else: # randomOrNumber == "n"
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
        if (verboseMode): print(f"\tNumber of phrases set to {nbPhrases}.")
    if (toggleEmoji == DEF_TOGGLE_EMOJI and "-e" not in av and "--emoji" not in av):
        confirmed: bool = askConfirmation("Add emoji between phrases")
        if (confirmed):
            toggleEmoji = True
            if (verboseMode): print("\tEmoji toggle set to True.")
        else: print(MAT_DEFAULTING)
    if (source == DEF_SOURCE and "-s" not in av and "--source" not in av):
        source = input("What source file to use: ")
        if (source == ""):
            source = DEF_SOURCE
            print(f"\t... using default value: {DEF_SOURCE.strip()}.")
        elif (verboseMode): print(f"\tSource file set to '{source}'.")
    if (forWhom == DEF_FOR_WHOM and "-w" not in av and "--for-whom" not in av):
        forWhom = input("For whom the goodnight is: ").strip()
        if (forWhom == ""):
            print(f"\t... using default value: {DEF_FOR_WHOM.strip()} (no name used)).")
        elif (verboseMode): print(f"\tFor whom the goodnight is set to '{forWhom}'.")
    if (allowRep == DEF_REPETITION and "--allow-repetition" not in av):
        confirmed: bool = askConfirmation("Allow repetition of phrases if you ask for more phrases there are in the source file")
        if (confirmed):
            allowRep = True
            if (verboseMode): print("\tRepetition toggle set to True.")
        else:
            print("\tRepetition toggle set to False.")
    if (step == DEF_STEP and "-o" not in av and "--other-step" not in av):
        confirmed: bool = askConfirmation("Use the even-numbered phrase gaps as \"and\"s instead of commas")
        if (confirmed):
            step = True
            if (verboseMode): print("\tStep toggle set to True.")
        else: print(MAT_DEFAULTING)
    newP = Parameters(nbPhrases if nbPhrases != DEF_NB_PHRASES else "2,5", toggleEmoji, source.strip(), forWhom.strip(), \
                      allowRep, step, verboseMode, saving)
    if (p.saving): saveParameters(newP)
    newP.pickNbPhrases()
    return newP

def fromParameters(ac: int, av: list[str]) -> Parameters:
    if (("-n" in av or "--nb-phrases" in av) and ("-b" in av or "--bounds" in av)):
        print("Cannot use both -n/--nb-phrases and -b/--bounds at the same time."); gnExit(exitCode.ERR_INV_ARG)

    def getPurifiedAv(ac: int, av: list[str]) -> (int, list[str]):
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
        if ("--isave" in av):     newAv.remove("--isave");  newAv.append("-i"); newAv.append("-S")
        if ("--ignore" in newAv): newAv.remove("--ignore"); newAv.append("-i")
        if ("-i" in newAv):   newAv = rremove(newAv, "-i"); newAv.append("-i")
        return (len(newAv), newAv)
    (ac, av) = getPurifiedAv(ac, av)

    verboseMode: bool = DEF_VERBOSE_MODE if ("--verbose" not in av) else (not DEF_VERBOSE_MODE)
    if (verboseMode): print(f"\tProgram arguments interpreted as: {av}")

    extractP: Parameters = defaultParameters() if ("-i" in av) else fromFile(extraction = True)
    nbPhrases:   str  = extractP.nbPhrases
    toggleEmoji: bool = extractP.toggleEmoji
    source:      str  = extractP.source
    forWhom:     str  = extractP.forWhom
    allowRep:    bool = extractP.allowRep
    step:        bool = extractP.step
    saving:      bool = extractP.saving

    i: int = 1 # iterator needs tracking for jumping over argument values
    while (i < ac): # hence can't use a for in range loop
        if   (av[i] == "-h" or av[i] == "--help"): gnExit(exitCode.HELP)
        elif (av[i] == "--default"): return defaultParameters(fromParameter = True)
        elif (av[i] == "--isave" ):  pass # still needs to be here to avoid an invalid parameter error
        elif (av[i] == "--verbose"): pass # ^ same
        elif (av[i] == "-b" or av[i] == "--bounds"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
            try:
                if (matches(r"^[0-9]+,[0-9]+$", av[i + 1]) == None):
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
        elif (av[i] == "-n" or av[i] == "--nb-phrases"):
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
        elif (av[i] == "-e" or av[i] == "--emoji"): toggleEmoji = True
        elif (av[i] == "-s" or av[i] == "--source"):
            if (i + 1 >= ac):
                print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
            try:
                source: str = av[i + 1]; i += 1
                if (not matches(r".*\.log$", source)): source += ".log"
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
        elif (av[i] == "-r" or av[i] == "--allow-repetition"): allowRep = True
        elif (av[i] == "-o" or av[i] == "--other-step"): step = True
        elif (av[i] == "-i" or av[i] == "--ignore"):
            return fromCommandLine(Parameters(nbPhrases, toggleEmoji, source, forWhom, allowRep, step, verboseMode, saving))
        elif (av[i] == "-S" or av[i] == "--save"): saving = True
        else:
            print(f"Invalid argument '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
        i += 1
    return fromCommandLine(Parameters(nbPhrases, toggleEmoji, source, forWhom, allowRep, step, verboseMode, saving), av + FILE_AV)

def fromFile(file: str = SAVE_FILEPATH, extraction: bool = False, noParam: bool = False) -> Parameters:
    p: Parameters = defaultParameters()

    if (not path.isfile(file)):
        print(f"File '{file}' does not exist. Creating preferences file...")
        if (extraction): p.nbPhrases = "2,5"
        return p if extraction else fromCommandLine(p)
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if   (line.startswith("nbPhrases=")): p.nbPhrases   =      line[len("nbPhrases="):-1]
                elif (line.startswith("emoji=")):     p.toggleEmoji = eval(line[len("emoji="):-1])
                elif (line.startswith("src=")):       p.source      =      line[len("src="):-1]
                elif (line.startswith("who=")):       p.forWhom     =      line[len("who="):-1]
                elif (line.startswith("allowRep=")):  p.allowRep    = eval(line[len("allowRep="):-1])
                elif (line.startswith("step=")):      p.step        = eval(line[len("step="):-1])
                else: raise ValueError(f"Invalid line '{line}'")
    except Exception as e:
        print(f"Error reading file '{file}': {e}"); gnExit(exitCode.ERR_INV_FIL)
    if (noParam): p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip() # eliminate trailing spaces used to dodge CLI
    return p

def defaultParameters(fromParameter: bool = False) -> Parameters:
    p = Parameters("2,5" if fromParameter else DEF_NB_PHRASES, DEF_TOGGLE_EMOJI, DEF_SOURCE, DEF_FOR_WHOM, DEF_REPETITION, DEF_STEP, DEF_VERBOSE_MODE, DEF_SAVE_PREF)
    if (fromParameter): p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip()
    return p
def getParameters(ac: int, av: list[str]) -> Parameters:
    p = fromParameters(ac, av) if (ac > 1) else fromFile(noParam = True)
    if (ac > 1): print("") # marking the end of parameter prints if any
    return p
