# PARAMETERS.PY #

from os import path, chmod
from signal import SIGTERM
from random import randint as rand
from re import search as matches
from copy import deepcopy as dup

from Utils import isIn, sendSignal, beval, askConfirmation, askConfirmationNumber, runParameterDuplicateChecks
from Longparam import applyLongParameters
from Types import Parameters, SetParams
from Exit import exitCode, gnExit

FILE_AV:     list[str] = ["--no-copy", "-n", "-e", "-s", "-w", "-N", "-r", "-o", "-a", "-t", "-d"]
PAR_HAS_ARG: list[str] = ["b", "n", "s", "w", "N", "t", "d"]
COMMENT_MARKER:    str = "--"
DEF_PREFFPATH:     str = "./assets/preferences.sav"
DEF_COPY:         bool = True
DEF_NB_PHRASES:    str = "?"
DEF_NB_DBOUND:     str = "2,5"
DEF_NB_UBOUND:     str = "999"
DEF_EMOJI:        bool = False
DEF_SOURCE:        str = "./assets/default.log"
DEF_FOR_WHOM:      str = ""
DEF_NICK_NTH:      str = "0"
DEF_REPETITION:   bool = False
DEF_STEP:         bool = False
DEF_ALTERNATE:    bool = False
DEF_TIMES:         str = "1"
DEF_INFINITE:     bool = False
DEF_DELAY:         str = "0"
DEF_VERBOSITY:    bool = False
DEF_SAVE_PREF:    bool = False
MAT_LONGPAR_INPUT: str = r"^\-\-[a-zA-Z\-]*\=.*$"
MAT_INTEGER_INPUT: str = r"^\-?[0-9]+$"
MAT_BOUNDED_INPUT: str = r"^[0-9]+,[0-9]+$"
MAT_FLOATNB_INPUT: str = r"^[0-9]+(\.[0-9]+)?$"
MAT_THEPKEY_INPUT: str = r"^p$"
MAT_NAME_LOGFILE:  str = r".*\.log$"
MAT_NAME_SAVFILE:  str = r".*\.sav$"
MAT_DEFAULTING_Y:  str = "\t... using default value: yes (True)."
MAT_DEFAULTING_N:  str = "\t... using default value: no (False)."

def saveParameters(p: Parameters) -> None:
    print(f"Saving preferences in file '{p.prefFile}'...")
    if (p.infinite): p.times = "infinite"
    try:
        with open(p.prefFile, "w") as f:
            f.write(f"copy={p.copy}\n")
            f.write(f"nbPhrases={p.nbPhrases}\n")
            f.write(f"emoji={p.emoji}\n")
            f.write(f"source={p.source}\n")
            f.write(f"forWhom={p.forWhom}\n")
            f.write(f"nickNth={p.nickNth}\n")
            f.write(f"allowRep={p.allowRep}\n")
            f.write(f"step={p.step}\n")
            f.write(f"alternate={p.alternate}\n")
            f.write(f"times={p.times}\n")
            f.write(f"delay={p.delay}\n")
        chmod(p.prefFile, 0o644)
    except PermissionError as e:
        print(f"Error writing to file '{p.prefFile}': {e}"); gnExit(exitCode.ERR_INV_PER)

def deduceRemaining(alreadySet: SetParams) -> list[str]:
    remaining: list[str] = dup(FILE_AV)
    if (alreadySet is None): return remaining
    for s in alreadySet:
        if (s in remaining): remaining.remove(s)
    return remaining
def fromCommandLine(p: Parameters) -> Parameters:
    copy:      bool = p.copy
    nbPhrases:  str = p.nbPhrases
    emoji:     bool = p.emoji
    source:     str = p.source
    forWhom:    str = p.forWhom
    nickNth:    str = p.nickNth
    allowRep:  bool = p.allowRep
    step:      bool = p.step
    alternate: bool = p.alternate
    times:      str = p.times
    infinite:  bool = p.infinite
    delay:    float = p.delay
    randomOrNumber:  str = DEF_NB_PHRASES
    timesOrInfinite: str = DEF_TIMES
    buf: str = "" # buffer for user input

    if (p.verbose): print(f"VVVV: Entering CLI handling with set parameters: {p.setParams}")
    toSet: list[str] = deduceRemaining([] if (p.setParams is None) else p.setParams)
    if (p.verbose): print(f"VVVV: Remaining parameters to set: {toSet}")
    if ("--no-copy" in toSet):
        confirmed: bool = askConfirmation("Copy the result to your clipboard")
        if (not confirmed):
            copy = False
            if (p.verbose): print(f"VVVV: Clipboard copy toggle set to {copy}.")
        else: print(MAT_DEFAULTING_Y)
    if ("-n" in toSet):
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
                    isMatching = matches(MAT_INTEGER_INPUT, buf) is not None
                    if (not isMatching):
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
    if ("-e" in toSet):
        confirmed: bool = askConfirmation("Add emoji between phrases")
        if (confirmed):
            emoji = True
            if (p.verbose): print(f"VVVV: Emoji toggle set to {emoji}.")
        else: print(MAT_DEFAULTING_N)
    if ("-s" in toSet):
        source: str = ""
        isMatching: bool = False
        while (not isMatching):
            source = input("What source file to use: ").strip()
            isMatching = matches(MAT_NAME_LOGFILE, source) is not None
            if (source == ""):
                source = DEF_SOURCE
                print(f"\t... using default value: {DEF_SOURCE.strip()}.")
            elif (isMatching and p.verbose): print(f"VVVV: Source file set to '{source}'.")
            elif (not isMatching): print("\tInvalid input: must be a .log file.")
    if ("-w" in toSet):
        forWhom = input("For whom the goodnight is: ").strip()
        if (forWhom == ""):
            print(f"\t... using default value: '{DEF_FOR_WHOM.strip()}' (no name used)).")
        elif (p.verbose): print(f"VVVV: For whom the goodnight is set to '{forWhom}'.")
    if ("-N" in toSet):
        isMatching: bool = False
        while (nickNth == DEF_NICK_NTH and not isMatching):
            buf: str = ""
            while (not isMatching):
                buf = input("Place the nickname after the nth phrase\n\t(-1 [nowhere] | 0 [random] | int): ").strip()
                isMatching = matches(MAT_INTEGER_INPUT, buf) is not None
                if (not isMatching):
                    print("\tInvalid input: N must be positive, 0 (random position) or -1 (no nickname).")
            nickNth = str(0 if buf == "" else int(buf))
            if (buf == ""):
                print(f"\t... using default value: {nickNth.strip()}.")
            elif (int(nickNth) < -1):
                print("N must be positive, 0 (random position) or -1 (no nickname)."); nickNth = DEF_NICK_NTH
            if (p.verbose):
                match nickNth:
                    case "-1": nth = "nowhere"
                    case "0":  nth = "random"
                    case _:    nth = nickNth
                print(f"VVVV: Index of phrase after which the nickname is printed set to {nth}.")
    if ("-r" in toSet):
        confirmed: bool = askConfirmation("Allow repetition of phrases if you ask for more than there are in the source file")
        if (confirmed):
            allowRep = True
            if (p.verbose): print(f"VVVV: Repetition toggle set to {allowRep}.")
        else: print(MAT_DEFAULTING_N)
    if ("-o" in toSet):
        confirmed: bool = askConfirmation("Use the even-numbered phrase gaps as \"and\"s instead of commas")
        if (confirmed):
            step = True
            if (p.verbose): print(f"VVVV: Step toggle set to {step}.")
        else: print(MAT_DEFAULTING_N)
    if (emoji and "-a" in toSet):
        confirmed: bool = askConfirmation("Alternate between \"and\"s, and emoji instead of commas")
        if (confirmed):
            alternate = True
            if (p.verbose): print(f"VVVV: Alternating set to {alternate}.")
        else: print(MAT_DEFAULTING_N)
    if ("-t" in toSet):
        while (timesOrInfinite != "t" and timesOrInfinite != "i"):
            timesOrInfinite = input("Play the goodnight x times or infinitely (t/i): ").strip().lower()
        if (timesOrInfinite == "t"): # play x times...
            isMatching: bool = False
            while (times == DEF_TIMES and not isMatching):
                buf: str = ""
                while (not isMatching):
                    buf = input("Number of times to iterate (int): ").strip()
                    isMatching = matches(MAT_INTEGER_INPUT, buf) is not None
                    if (not isMatching):
                        print("\tInvalid input: must be a positive integer.")
                times = str(1 if buf == "" else int(buf))
                if (buf == ""):
                    print(f"\t... using default value: {times.strip()}.")
                elif (int(times) < 1):
                    print("The number of iterations must be positive."); times = DEF_TIMES
                if (p.verbose): print(f"VVVV: Number of iterations set to {times}.")
        else: # play infinitely...
            confirmed: bool = askConfirmation("Toggle infinite mode on")
            if (confirmed):
                infinite = True
                if (p.verbose): print(f"VVVV: Infinite mode set to {infinite}.")
            else: print(MAT_DEFAULTING_N)
    if ("-d" in toSet):
        newDelay = DEF_DELAY
        isMatching: bool = False
        while (newDelay == DEF_DELAY and not isMatching):
            while (not isMatching):
                buf = input("Delay between every iteration (in ms), or p (press Enter): ").strip()
                isMatching = matches(MAT_FLOATNB_INPUT, buf) is not None or matches(MAT_THEPKEY_INPUT, buf) is not None
                if (not isMatching):
                    print("\tInvalid input: must be a positive float number or p.")
            if (buf[0] != 'p'):
                newDelay = str(0 if buf == "" else int(buf))
                if (buf == ""):
                    print(f"\t... using default value: {newDelay}.")
                elif (int(newDelay) < 0):
                    print("The number of iterations cannot be negative."); newDelay = DEF_DELAY
                while (int(newDelay) > 10000):
                    buf = askConfirmationNumber(f"\twarning: you set the delay to a long time ({newDelay.strip()})")
                    if (buf == "y"): break
                    newDelay = buf
            else: newDelay = buf
            if (p.verbose): print(f"VVVV: Delay between iterations set to {newDelay}.")
        delay = float(newDelay)
    if (p.verbose): print("") # marking the end of parameter prints if any
    newP = Parameters({
        "copy": copy,
        "nbPhrases": nbPhrases if nbPhrases != DEF_NB_PHRASES else DEF_NB_DBOUND, "emoji": emoji, "source": source.strip(), "forWhom": forWhom.strip(), "nickNth": nickNth,
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

    verbose: bool = False if ("--verbose" not in av or "--verbose=false" in str(av).lower()) else True

    if (verbose): print(f"VVVV: Entering sanitization with av: {av}")
    def getSanitizedAv(ac: int, av: list[str]) -> tuple[int, list[str]]:
        newAv: list[str] = [av[0]]

        def isMultiOptional(s: str) -> bool: return (len(s) > 2 and s[0] == '-' and s[1] != '-')

        try:
            for i in range(1, ac): # check for multi-optional parameters and unwrap them
                if (isMultiOptional(av[i])):
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

    def getPreferencesFile(ac: int, av: list[str]) -> str:
        ARG_PREF: str = "--pref-file="
        if (verbose): print(f"VVVV: Entering preferences file handling with av: {av}")
        for i in range(ac):
            if (av[i] == "-p" or av[i] == "--pref-file"):
                return av[i + 1].strip() + ("" if av[i + 1].endswith(".sav") else ".sav")
            if (av[i].startswith(ARG_PREF)):
                return av[i][len(ARG_PREF):].strip() + ("" if av[i].endswith(".sav") else ".sav")
        return DEF_PREFFPATH
    extractP: Parameters = defaultParameters() if ("--ignore" in av) else fromFile(getPreferencesFile(ac, av), extraction = True)
    try:
        if (verbose): print(f"VVVV: Entering long parameters handling with av: {av}")
        av = applyLongParameters(av, "--verbose" in av and "--verbose=false" not in str(av).lower())
    except ValueError as e:
        print(f"Invalid argument: {e}"); gnExit(exitCode.ERR_INV_ARG)

    verbose = "--verbose" in av and "'--verbose', 'False'" not in str(av)
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
    prefFile:   str = extractP.prefFile
    setParams: SetParams = extractP.setParams

    i: int = 1 # iterator needs tracking for jumping over PAR_HAS_ARG arguments
    while (i < ac): # hence can't use a for in range loop
        match av[i]:
            case "--default": return defaultParameters(fromParameter = True)
            case "--no-copy":
                setParams.append("--no-copy")
                if (i + 1 == ac): copy = False; break
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    copy = not eval(av[i + 1]); i += 1
                else: copy = False

            case "-b" | "--bounds":
                setParams.append("-n")
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
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
                i += 1
            case "-n" | "--nb-phrases":
                setParams.append("-n")
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    nbPhrases = str(int(av[i + 1]))
                    if (int(nbPhrases) < 1):
                        raise ValueError("The number of phrases must be positive.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
                i += 1
            case "-e" | "--emoji":
                setParams.append("-e")
                if (i + 1 == ac): emoji = True; break
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    emoji = eval(av[i + 1]); i += 1
                else: emoji = True
            case "-s" | "--source":
                setParams.append("-s")
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                source: str = av[i + 1]
                if (not matches(MAT_NAME_LOGFILE, source)): source += ".log"
                i += 1
            case "-w" | "--for-whom":
                setParams.append("-w")
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                forWhom = str(av[i + 1])
                i += 1
            case "-N" | "--nick-nth":
                setParams.append("-N")
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    nickNth = str(int(av[i + 1]))
                    if (int(nickNth) < -1):
                        raise ValueError("N for --nick-nth must be positive, 0 (random position) or -1 (no nickname).")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
                i += 1

            case "-r" | "--allow-repetition":
                setParams.append("-r")
                if (i + 1 == ac): allowRep = True; break
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    allowRep = eval(av[i + 1]); i += 1
                else: allowRep = True
            case "-o" | "--other-step":
                setParams.append("-o")
                if (i + 1 == ac): step = True; break
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    step = eval(av[i + 1]); i += 1
                else: step = True
            case "-a" | "--alternate":
                setParams.append("-a")
                if (i + 1 == ac): alternate = True; break
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    alternate = eval(av[i + 1]); i += 1
                else: alternate = True
            case "-t" | "--times":
                setParams.append("-t")
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    times = str(int(av[i + 1]))
                    if (int(times) < 1):
                        raise ValueError("The number of iterations must be positive.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
                i += 1
            case "-i" | "--infinite":
                setParams.append("-t")
                if (i + 1 == ac): infinite = True; break
                setParams.append(av[i])
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    infinite = eval(av[i + 1]); i += 1
                else: infinite = True
            case "-d" | "--delay":
                setParams.append("-d")
                if (i + 1 >= ac):
                    print(f"Missing argument for '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
                try:
                    if (not matches(MAT_FLOATNB_INPUT, av[i + 1]) and not matches(MAT_THEPKEY_INPUT, av[i + 1])):
                        raise ValueError("Delay must be a positive float number or 'p'.")
                    newDelay: str = str(int(av[i + 1])) if av[i + 1] != 'p' else av[i + 1]
                    if (int(newDelay) < 0):
                        raise ValueError("The delay cannot be negative.")
                except ValueError as e:
                    print(f"Invalid argument for '{av[i]}': {e}"); gnExit(exitCode.ERR_INV_ARG)
                i += 1
            case "--ignore":
                if (i + 1 < ac and beval(av[i + 1]) == False): break
                return fromCommandLine(Parameters({
                    "copy": copy,
                    "nbPhrases": nbPhrases, "emoji": emoji, "source": source, "forWhom": forWhom, "nickNth": nickNth,
                    "allowRep": allowRep, "step": step, "alternate": alternate, "times": times, "infinite": infinite, "delay": delay,
                    "verbose": verbose, "saving": saving, "prefFile": prefFile, "setParams": setParams
                }))
            case "-S" | "--save":
                setParams.append("-S")
                if (i + 1 == ac): saving = True; break
                nextArg: str = av[i + 1].capitalize()
                if (nextArg in ["True", "False"]):
                    saving = eval(av[i + 1]); i += 1
                else: saving = True
            case "-p" | "--pref-file": i += 1 # still needs to be here to avoid an invalid parameter error

            case "--verbose":
                if (i + 1 < ac):
                    if (beval(av[i + 1]) == False): break
                    i += 1
                verbose = True
            case "-h" | "--help": gnExit(exitCode.HELP)

            case _: print(f"Invalid argument '{av[i]}'."); gnExit(exitCode.ERR_INV_ARG)
        i += 1
    return fromCommandLine(Parameters({
            "copy": copy,
            "nbPhrases": nbPhrases, "emoji": emoji, "source": source, "forWhom": forWhom, "nickNth": nickNth,
            "allowRep": allowRep, "step": step, "alternate": alternate, "times": times, "infinite": infinite, "delay": delay,
            "verbose": verbose, "saving": saving, "prefFile": prefFile, "setParams": setParams
        }))

def fromFile(savefile: str = DEF_PREFFPATH, extraction: bool = False, noParam: bool = False) -> Parameters:
    p: Parameters = defaultParameters(savefile)

    if (not path.isfile(p.prefFile)):
        print(f"File '{p.prefFile}' does not exist...", end = "\n" if p.saving or (not extraction and noParam) else "")
        if (extraction): p.nbPhrases = DEF_NB_DBOUND
        else: p = fromCommandLine(p)
        if (p.saving or (not extraction and noParam)): saveParameters(p)
        print(" using default parameters.")
        return p
    try:
        with open(p.prefFile, "r") as f: lines = f.readlines()
    except FileNotFoundError as e:
        print(f"Error reading file '{p.prefFile}': {e}"); gnExit(exitCode.ERR_INV_FIL)

    lines: list[str] = [line.strip() for line in lines]
    try:
        for line in lines:
            if (len(line) == 0 or line.startswith(COMMENT_MARKER)): continue # comments
            pref, val = line[:line.find('=')].strip(), line[line.find('=') + 1:].strip()
            match pref:
                case "copy":      p.copy      = beval(val); p.setParams.append("--no-copy")
                case "nbPhrases": p.nbPhrases =       val ; p.setParams.append("-n")
                case "emoji":     p.emoji     = beval(val); p.setParams.append("-e")
                case "source":    p.source    =       val ; p.setParams.append("-s")
                case "forWhom":   p.forWhom   =       val ; p.setParams.append("-w")
                case "nickNth":   p.nickNth   =       val ; p.setParams.append("-N")
                case "allowRep":  p.allowRep  = beval(val); p.setParams.append("-r")
                case "step":      p.step      = beval(val); p.setParams.append("-o")
                case "alternate": p.alternate = beval(val); p.setParams.append("-a")
                case "times":     p.times     =       val ; p.setParams.append("-t")
                case "delay":     p.delay     =       val ; p.setParams.append("-d")
                case _: raise ValueError(f"Invalid line '{line}'")
    except ValueError as e:
        print(f"Error reading file '{p.prefFile}': {e}"); gnExit(exitCode.ERR_INV_SAV)
    if (noParam): p.pickNbPhrases()
    return p

def defaultParameters(savefile: str = DEF_PREFFPATH, fromParameter: bool = False) -> Parameters:
    p = Parameters({
            "copy": DEF_COPY,
            "nbPhrases": DEF_NB_DBOUND if fromParameter else DEF_NB_PHRASES, "emoji": DEF_EMOJI, "source": DEF_SOURCE, "forWhom": DEF_FOR_WHOM, "nickNth": DEF_NICK_NTH,
            "allowRep": DEF_REPETITION, "step": DEF_STEP, "alternate": DEF_ALTERNATE, "times": DEF_TIMES, "infinite": DEF_INFINITE, "delay": DEF_DELAY,
            "verbose": DEF_VERBOSITY, "saving": DEF_SAVE_PREF, "prefFile": savefile, "setParams": [] if not fromParameter else FILE_AV
        })
    if (fromParameter): p.pickNbPhrases()
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip()
    return p
def getParameters(ac: int, av: list[str]) -> Parameters:
    p: Parameters
    try:
        p = fromParameters(ac, av) if (ac > 1) else fromFile(extraction = False, noParam = True)
    except EOFError:
        sendSignal(SIGTERM) # SIGTERM is caught by CtrlDHandler, which terminates the program
        exit(exitCode.FAILURE.value) # this is a failsafe in case the signal is not caught
    p.source = p.source.strip(); p.forWhom = p.forWhom.strip() # eliminate trailing spaces used to dodge CLI cases
    if (p.times == "infinite"): p.infinite = True; p.times = DEF_TIMES
    return p
