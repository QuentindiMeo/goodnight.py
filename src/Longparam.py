#!/usr/bin/env python3.10

from re import search as matches
from Utils import runParameterDuplicateChecks
from Exit import exitCode, gnExit

MAT_LONGPAR_INPUT: str = r"^\-\-[a-zA-Z\-]*\=.*$"
MAT_INTEGER_INPUT: str = r"^[0-9]+$"
MAT_BOUNDED_INPUT: str = r"^[0-9]+,[0-9]+$"
MAT_FLOATNB_INPUT: str = r"^[0-9]+(\.[0-9]+)?$"
MAT_THEPKEY_INPUT: str = r"^p$"
MAT_NAME_LOGFILE:  str = r".*\.log$"

def isBoolean(arg: str) -> bool:
    return arg == "True" or arg == "False"

def handleDelay(arg: str) -> str:
    if (not matches(MAT_THEPKEY_INPUT, arg) and \
        not matches(MAT_FLOATNB_INPUT, arg)): raise ValueError(f"unexpected delay value for '{arg}'")
    return arg

def handleString(arg: str) -> str:
    return arg

def handleInteger(arg: str) -> str:
    if (not matches(MAT_INTEGER_INPUT, arg)): raise ValueError(f"unexpected integer value for '{arg}'")
    return arg

def handleBounds(arg: str) -> str:
    if (not matches(MAT_BOUNDED_INPUT, arg)): raise ValueError(f"unexpected bounds value for '{arg}'")
    return arg

def handleBoolean(arg: str) -> str:
    value: str = arg[arg.find("=") + 1:]
    if (not isBoolean(arg[arg.find("=") + 1:])): raise ValueError(f"unexpected boolean value for '{arg}'")
    return "" if (eval(value) == False) else arg[:arg.find("=")]

def applyLongParameters(av: list[str], verbose: bool) -> list[str]:
    booleans: list[str] = ["default", "no-copy", "emoji", "allow-repetition", "other-step", "alternate", "infinite", "ignore", "save", "verbose", "help"]
    newAv:    list[str] = []
    for arg in av:
        if (not matches(MAT_LONGPAR_INPUT, arg)): newAv.append(arg); continue
        if (arg[2:arg.find("=")] in booleans): newAv.append(handleBoolean(arg))
        else:
            newAv.append(arg[:arg.find("=")])
            if   (arg.startswith("--bounds=")): newAv.append(handleBounds(arg[arg.find("=") + 1:]))
            elif (arg.startswith("--nb-phrases=")): newAv.append(handleInteger(arg[arg.find("=") + 1:]))
            elif (arg.startswith("--source=")): newAv.append(handleString(arg[arg.find("=") + 1:]))
            elif (arg.startswith("--for-whom=")): newAv.append(handleString(arg[arg.find("=") + 1:]))
            elif (arg.startswith("--times=")): newAv.append(handleInteger(arg[arg.find("=") + 1:]))
            elif (arg.startswith("--delay=")): newAv.append(handleDelay(arg[arg.find("=") + 1:]))
            else: print(f"Invalid argument '{arg}'."); gnExit(exitCode.ERR_INV_ARG)
    if (verbose or "--verbose" in newAv): print(f"VVVV: Diving through duplicate inspection for: {newAv}")
    runParameterDuplicateChecks(newAv)
    newAv = list(filter(None, newAv)) # remove empty strings
    if (verbose or "--verbose" in newAv): print(f"VVVV: New av with long parameters: {newAv}")
    return newAv
