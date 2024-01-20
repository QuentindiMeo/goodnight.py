#!/usr/bin/env python3.10

from os import path, chmod
from random import randint as rand
from re import search as matches

from Utils import isIn, askConfirmation, askConfirmationNumber, runParameterDuplicateChecks
from Longparam import applyLongParameters
from Types import Parameters
from Exit import exitCode, gnExit

FILE_AV:     list[str] = ["--no-copy", "-n", "-e", "-s", "-w", "-r", "-o", "-a", "-t", "-d"]
PAR_HAS_ARG: list[str] = ["b", "n", "s", "w", "t", "d"]
SAVE_FILEPATH:     str = "preferences.sav"
DEF_COPY:         bool = True
DEF_NB_PHRASES:    str = "?"
DEF_NB_DBOUND:     str = "2,5"
DEF_NB_UBOUND:     str = "999"
DEF_EMOJI:        bool = False
DEF_SOURCE:        str = "./assets/source.log " # same as below
DEF_FOR_WHOM:      str = " " # same as below
DEF_NICK_NTH:      str = "0 " # space to skip the CLI if the user used the default value as a parameter
DEF_REPETITION:   bool = False
DEF_STEP:         bool = False
DEF_ALTERNATE:    bool = False
DEF_TIMES:         str = "1 " # same as above
DEF_INFINITE:     bool = False
DEF_DELAY:         str = "0 " # same as above
DEF_VERBOSITY:    bool = False
DEF_SAVE_PREF:    bool = False
MAT_LONGPAR_INPUT: str = r"^\-\-[a-zA-Z\-]*\=.*$"
MAT_INTEGER_INPUT: str = r"^[0-9]+$"
MAT_BOUNDED_INPUT: str = r"^[0-9]+,[0-9]+$"
MAT_FLOATNB_INPUT: str = r"^[0-9]+(\.[0-9]+)?$"
MAT_THEPKEY_INPUT: str = r"^p$"
MAT_NAME_LOGFILE:  str = r".*\.log$"
MAT_DEFAULTING_Y:  str = "\t... using default value: yes (True)."
MAT_DEFAULTING_N:  str = "\t... using default value: no (False)."

def saveParameters(p: Parameters) -> None:
    print(f"Saving preferences in file '{SAVE_FILEPATH}'...")
    if (p.infinite): p.times = "infinite"
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
            f.write(f"times={p.times}\n")
            f.write(f"delay={p.delay}\n")
        chmod(SAVE_FILEPATH, 0o644)
    except PermissionError as e:
        print(f"Error writing to file '{SAVE_FILEPATH}': {e}"); gnExit(exitCode.ERR_INV_PER)

def fromCommandLine(p: Parameters, av: list[str] = None) -> Parameters:
    copy:      bool = p.copy
    nbPhrases:  str = p.nbPhrases
    emoji:     bool = p.emoji
    source:     str = p.source
    forWhom:    str = p.forWhom
    allowRep:  bool = p.allowRep
    step:      bool = p.step
    alternate: bool = p.alternate
    times:      str = p.times
    infinite:  bool = p.infinite
    delay:    float = p.delay
    randomOrNumber:  str = DEF_NB_PHRASES
    timesOrInfinite: str = DEF_TIMES

    if (copy == DEF_COPY and "--no-copy" not in av):
        confirmed: bool = askConfirmation("Copy the result to your clipboard")
        if (not confirmed):
            copy = False
            if (p.verbose): print("VVVV: Clipboard copy toggle set to {copy}.")
        else: print(MAT_DEFAULTING_Y)
    if (nbPhrases == DEF_NB_PHRASES and "-n" not in av and "--nb-phrases" not in av and "-b" not in av and "--bounds" not in av):
        while (randomOrNumber != "r" and randomOrNumber != "n"):
            randomOrNumber = input("Use a random range or number of phrases (r/n): ").strip().lower()
        if (randomOrNumber == "r"): # random quantity of phrases in bounds...
            bounds = DEF_NB_PHRASES
            while (bounds == DEF_NB_PHRASES):
                bounds = input("Bounds of the random range: ").strip()
                if (not matches(MAT_BOUNDED_INPUT, bounds)):
                    print("\tBounds must be of the form \"x,y\"."); bounds = DEF_NB_PHRASES
                    continue
                (lowerBound, upperBound) = (int(bounds.split(",")[0]), int(bounds.split(",")[1]))
                if (int(upperBound) > int(DEF_NB_UBOUND)): upperBound = DEF_NB_UBOUND
                while (int(bounds.split(",")[1]) > 6):
                    buf = askConfirmationNumber(f"\twarning: you set the upper bound to a large number ({upperBound})")
                    if (buf == "y"): break
                    bounds = str(lowerBound) + "," + buf
                nbPhrases = bounds
        else: # determined number of phrases...
            while (nbPhrases == DEF_NB_PHRASES):
                isMatching: bool = False
                while (not isMatching):
                    buf = input("Number of phrases to draw: ").strip()
                    isMatching = matches(MAT_INTEGER_INPUT, buf)
                    if (isMatching):
                        print("\tInvalid input: must be a positive integer.")
                nbPhrases = str(rand(2, 5) if buf == "" else int(buf))
                if (buf == ""):
                    print(f"\t... using default value: {nbPhrases}, picked randomly between 2 and 5.")
                elif (int(nbPhrases) < 1):
                    print("The number of phrases must be positive."); nbPhrases = DEF_NB_PHRASES
                if (int(nbPhrases) > int(DEF_NB_UBOUND)): nbPhrases = DEF_NB_UBOUND
                while (int(nbPhrases) > 6):
                    buf = askConfirmationNumber(f"\twarning: you set the number of phrases to a large number ({nbPhrases})")
                    if (buf == "y"): break
                    nbPhrases = buf
        if (p.verbose): print(f"VVVV: Number of phrases set to {nbPhrases}.")
    if (emoji == DEF_EMOJI and "-e" not in av and "--emoji" not in av):
        confirmed: bool = askConfirmation("Add emoji between phrases")
        if (confirmed):
            emoji = True
            if (p.verbose): print("VVVV: Emoji toggle set to {emoji}.")
        else: print(MAT_DEFAULTING_N)
    if (source == DEF_SOURCE and "-s" not in av and "--source" not in av):
        source = input("What source file to use: ").strip()
        if (source == ""):
            source = DEF_SOURCE
            print(f"\t... using default value: {DEF_SOURCE.strip()}.")
        elif (p.verbose): print(f"VVVV: Source file set to '{source}'.")
    if (forWhom == DEF_FOR_WHOM and "-w" not in av and "--for-whom" not in av):
        forWhom = input("For whom the goodnight is: ").strip()
        if (forWhom == ""):
            print(f"\t... using default value: {DEF_FOR_WHOM.strip()} (no name used)).")
        elif (p.verbose): print(f"VVVV: For whom the goodnight is set to '{forWhom}'.")
    if (allowRep == DEF_REPETITION and "-r" not in av and "--allow-repetition" not in av):
        confirmed: bool = askConfirmation("Allow repetition of phrases if you ask for more than there are in the source file")
        if (confirmed):
            allowRep = True
            if (p.verbose): print("VVVV: Repetition toggle set to {allowRep}.")
        else: print(MAT_DEFAULTING_N)
    if (step == DEF_STEP and "-o" not in av and "--other-step" not in av):
        confirmed: bool = askConfirmation("Use the even-numbered phrase gaps as \"and\"s instead of commas")
        if (confirmed):
            step = True
            if (p.verbose): print("VVVV: Step toggle set to {step}.")
        else: print(MAT_DEFAULTING_N)
    if (emoji and alternate == DEF_ALTERNATE and "-a" not in av and "--alternate" not in av):
        confirmed: bool = askConfirmation("Alternate between \"and\"s, and emoji instead of commas")
        if (confirmed):
            alternate = True
            if (p.verbose): print("VVVV: Alternating set to {alternate}.")
        else: print(MAT_DEFAULTING_N)
    if (times == DEF_TIMES and "-t" not in av and "--times" not in av and infinite == DEF_INFINITE and "-i" not in av and "--infinite" not in av):
        while (timesOrInfinite != "t" and timesOrInfinite != "i"):
            timesOrInfinite = input("Play the goodnight x times or infinitely (t/i): ").strip().lower()
        if (timesOrInfinite == "t"): # play x times...
            while (times == DEF_TIMES):
                buf: str = ""
                while (not matches(MAT_INTEGER_INPUT, buf)):
                    buf = input("Number of times to iterate (int): ").strip()
                    if (not matches(MAT_INTEGER_INPUT, buf)):
                        print("\tInvalid input: must be a positive integer.")
                times = str(1 if buf == "" else int(buf))
                if (buf == ""):
                    print(f"\t... using default value: {times}.")
                elif (int(times) < 1):
                    print("The number of iterations must be positive."); times = DEF_TIMES
                if (p.verbose): print(f"VVVV: Number of iterations set to {times}.")
        else: # play infinitely...
            confirmed: bool = askConfirmation("Toggle infinite mode on")
            if (confirmed):
                infinite = True
                if (p.verbose): print("VVVV: Infinite mode set to {infinite}.")
            else: print(MAT_DEFAULTING_N)
    if (delay == DEF_DELAY and "-d" not in av and "--delay" not in av):
        while (delay == DEF_DELAY):
            isMatching: bool = False
            while (not isMatching):
                buf = input("Delay between every iteration (in ms), or p? (with ? a letter): ").strip()
                isMatching = matches(MAT_FLOATNB_INPUT, buf) or matches(MAT_THEPKEY_INPUT, buf)
                if (not isMatching):
                    print("\tInvalid input: must be a positive float number or p.")
            if (buf[0] != 'p'):
                delay = str(0 if buf == "" else int(buf))
                if (buf == ""):
                    print(f"\t... using default value: {delay}.")
                elif (int(delay) < 0):
                    print("The number of iterations cannot be negative."); delay = DEF_DELAY
                while (int(delay) > 10000):
                    buf = askConfirmationNumber(f"\twarning: you set the delay to a long time ({delay})")
                    if (buf == "y"): break
                    delay = buf
            else: delay = buf
            if (p.verbose): print(f"VVVV: Delay between iterations set to {delay}.")
    if (p.verbose): print("") # marking the end of parameter prints if any
    newP = Parameters({
        "copy": copy,
        "nbPhrases": nbPhrases if nbPhrases != DEF_NB_PHRASES else DEF_NB_DBOUND, "emoji": emoji, "source": source.strip(), "forWhom": forWhom.strip(), "nickNth": DEF_NICK_NTH,
        "allowRep": allowRep, "step": step, "alternate": alternate, "times": times, "infinite": infinite, "delay": delay,
        "verbose": p.verbose, "saving": p.saving
    })
    if (p.saving): saveParameters(newP)
    newP.pickNbPhrases()
    return newP

def fromParameters(ac: int, av: list[str]) -> Parameters:
    if (("-n" in av or "--nb-phrases" in av) and ("-b" in av or "--bounds" in av)):
        print("Cannot use both -n/--nb-phrases and -b/--bounds at the same time."); gnExit(exitCode.ERR_INV_ARG)
    if (("-t" in av or "--times" in av) and ("-i" in av or "--infinite" in av)):
        print("Cannot use both -t/--times and -i/--infinite at the same time."); gnExit(exitCode.ERR_INV_ARG)

    verbose: bool = DEF_VERBOSITY if ("--verbose" not in av) else (not DEF_VERBOSITY)

    if (verbose): print(f"VVVV: Entering sanitization with av: {av}")
    def getSanitizedAv(ac: int, av: list[str]) -> (int, list[str]):
        newAv: list[str] = [av[0]]

        def isMultioptional(s: str) -> bool: return (len(s) > 2 and s[0] == '-' and s[1] != '-')

        try:
            for i in range(1, ac): # check for multioptional parameters and unwrap them
                if (isMultioptional(av[i])):
                    s = "".join(dict.fromkeys(av[i]))[1:] # av[i] without duplicates
                    if (isIn(PAR_HAS_ARG, s)):
                        raise ValueError(f"One of the parameters in '{s}' needs an argument.")
                    for c in s:
                        newAv.append("-" + c)
                else:
                    newAv.append(av[i])
            runParameterDuplicateChecks(newAv)
        except ValueError as e:
            print(f"Invalid argument: {e}"); gnExit(exitCode.ERR_INV_ARG)

        if ("--default" in newAv): # --default ignores all other parameters
            newAv.remove("--default"); newAv.insert(1, "--default")
        # if newAv has --ignore, move it to the end (because it instantly jumps to CLI)
        if ("--ignore"  in newAv): newAv.remove("--ignore");  newAv.append("--ignore")
        if ("--default" in newAv): newAv.remove("--default"); newAv.append("--default")

        return (len(newAv), newAv)
    (ac, av) = getSanitizedAv(ac, av)

    extractP: Parameters = defaultParameters() if ("--ignore" in av) else fromFile(extraction = True)
    try:
        if (verbose): print(f"VVVV: Entering long parameters handling with av: {av}")
        av = applyLongParameters(av, "--verbose" in av)
    except ValueError as e:
        print(f"Invalid argument: {e}"); gnExit(exitCode.ERR_INV_ARG)

    verbose = "--verbose" in av
    if (verbose): print(f"VVVV: Program arguments interpreted as: {av}")
    av = [arg for arg in av if not matches(MAT_LONGPAR_INPUT, arg)] # remove all long parameters from av to avoid confusion
    ac = len(av)

    copy:      bool = extractP.copy
    nbPhrases:  str = extractP.nbPhrases
    emoji:     bool = extractP.emoji
    source:     str = extractP.source
    forWhom:    str = extractP.forWhom
    nickNth:    str = extractP.nickNth
    allowRep:  bool = extractP.allowRep
    step:      bool = extractP.step
    alternate: bool = extractP.alternate
    times:      str = extractP.times
    infinite:  bool = extractP.infinite
    delay:    float = extractP.delay
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
                    if (not matches(MAT_BOUNDED_INPUT, av[i + 1])):
                        raise ValueError("Bounds must be of the form \"x,y\".")
                    (lowerBound, upperBound) = (int(av[i + 1].split(",")[0]), int(av[i + 1].split(",")[1]))
                    if (lowerBound > upperBound):
                        raise ValueError("The upper bound cannot be lower than the lower bound.")
                    if (lowerBound == 0):
                        raise ValueError("Bounds must be positive.")
                    if (int(upperBound) > int(DEF_NB_UBOUND)): upperBound = int(DEF_NB_UBOUND)
                    nbPhrases = str(lowerBound) + "," + str(upperBound)
                    i += 1
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-n" | "--nb-phrases":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    nbPhrases = str(int(av[i + 1])); i += 1
                    if (int(nbPhrases) < 1):
                        raise ValueError("The number of phrases must be positive.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-e" | "--emoji": emoji = True
            case "-s" | "--source":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    source: str = av[i + 1]; i += 1
                    if (not matches(MAT_NAME_LOGFILE, source)): source += ".log"
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-w" | "--for-whom":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                forWhom = str(av[i + 1]); i += 1

            case "-r" | "--allow-repetition": allowRep = True
            case "-o" | "--other-step": step = True
            case "-a" | "--alternate": alternate = True
            case "-t" | "--times":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    times = str(int(av[i + 1])); i += 1
                    if (int(times) < 1):
                        raise ValueError("The number of iterations must be positive.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "-i" | "--infinite": infinite = True
            case "-d" | "--delay":
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    if (not matches(MAT_FLOATNB_INPUT, av[i + 1]) and not matches(MAT_THEPKEY_INPUT, av[i + 1])):
                        raise ValueError("Delay must be a positive float number or 'p'.")
                    if (av[i + 1][0] == 'p'):
                        delay = av[i + 1]; continue
                    delay = str(int(av[i + 1])); i += 1
                    if (int(delay) < 0):
                        raise ValueError("The delay cannot be negative.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
            case "--ignore":
                return fromCommandLine(Parameters({
                    "copy": copy,
                    "nbPhrases": nbPhrases, "emoji": emoji, "source": source, "forWhom": forWhom, "nickNth": nickNth,
                    "allowRep": allowRep, "step": step, "alternate": alternate, "times": times, "infinite": infinite, "delay": delay,
                    "verbose": verbose, "saving": saving
                }))
            case "-S" | "--save": saving = True

            case "--verbose": pass # still needs to be here to avoid an invalid parameter error
            case "-h" | "--help": gnExit(exitCode.HELP)

            case _: print(f"Invalid argument '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
        i += 1
    return fromCommandLine(Parameters({
            "copy": copy,
            "nbPhrases": nbPhrases, "emoji": emoji, "source": source, "forWhom": forWhom, "nickNth": nickNth,
            "allowRep": allowRep, "step": step, "alternate": alternate, "times": times, "infinite": infinite, "delay": delay,
            "verbose": verbose, "saving": saving
        }), av + FILE_AV)

def fromFile(savefile: str = SAVE_FILEPATH, extraction: bool = False, noParam: bool = False) -> Parameters:
    p: Parameters = defaultParameters()

    if (not path.isfile(savefile)):
        print(f"File '{savefile}' does not exist...")
        if (extraction): p.nbPhrases = DEF_NB_DBOUND
        else: p = fromCommandLine(p)
        if (p.saving or (not extraction and noParam)):
            saveParameters(p)
        return p
    try:
        with open(savefile, "r") as f:
            lines = f.readlines()
            for line in lines:
                if   (line.startswith("copy=")):      p.copy        = eval(line[len("copy="):-1])
                elif (line.startswith("nbPhrases=")): p.nbPhrases   =      line[len("nbPhrases="):-1]
                elif (line.startswith("emoji=")):     p.emoji       = eval(line[len("emoji="):-1])
                elif (line.startswith("src=")):       p.source      =      line[len("src="):-1]
                elif (line.startswith("who=")):       p.forWhom     =      line[len("who="):-1]
                elif (line.startswith("nicknth=")):   p.nicknth     =      line[len("who="):-1]
                elif (line.startswith("allowRep=")):  p.allowRep    = eval(line[len("allowRep="):-1])
                elif (line.startswith("step=")):      p.step        = eval(line[len("step="):-1])
                elif (line.startswith("alternate=")): p.alternate   = eval(line[len("alternate="):-1])
                elif (line.startswith("times=")):     p.times       =      line[len("times="):-1]
                elif (line.startswith("delay=")):     p.delay       =      line[len("delay="):-1]
                else: raise ValueError(f"Invalid line '{line}'")
    except Exception as e:
        print(f"Error reading file '{savefile}': {e}"); gnExit(exitCode.ERR_INV_FIL if isinstance(e, FileNotFoundError) else exitCode.ERR_INV_SAV)
    if (noParam): p.pickNbPhrases()
    return p

def defaultParameters(fromParameter: bool = False) -> Parameters:
    p = Parameters({
            "copy": DEF_COPY,
            "nbPhrases": DEF_NB_DBOUND if fromParameter else DEF_NB_PHRASES, "emoji": DEF_EMOJI, "source": DEF_SOURCE, "forWhom": DEF_FOR_WHOM, "nickNth": DEF_NICK_NTH,
            "allowRep": DEF_REPETITION, "step": DEF_STEP, "alternate": DEF_ALTERNATE, "times": DEF_TIMES, "infinite": DEF_INFINITE, "delay": DEF_DELAY,
            "verbose": DEF_VERBOSITY, "saving": DEF_SAVE_PREF
        })
    if (fromParameter): p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip()
    return p
def getParameters(ac: int, av: list[str]) -> Parameters:
    p = fromParameters(ac, av) if (ac > 1) else fromFile(extraction = False, noParam = True)
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip() # eliminate trailing spaces used to dodge CLI cases
    if (p.times == "infinite"): p.infinite = True; p.times = DEF_TIMES
    return p
