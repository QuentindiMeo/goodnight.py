#!/usr/bin/env python3.10

from re import search as matches
from random import randint as rand

from Utils import rreplace
from Types import Parameters, Contents, WeightedList as Wlist, WeightedElement as Welem
from Exit import exitCode, gnExit

PHRASES_LOG: str = "## PHRASES.log"
EMOJI_LOG:   str = "## EMOJI.log"
NICKS_LOG:   str = "## NICKNAMES.log"

def pickRandElement(elems: list[str]) -> str: return elems[rand(0, len(elems) - 1)]

def applyWeighting(input: list[list[str]], verboseMode: bool = False) -> list[Wlist]:
    output: list[Wlist] = []
    for line in input:
        if (verboseMode): print(":::", line)
        line = str(line).replace("'\"", "\"").replace("\"'", "\"").replace("\\'", "'") \
            .replace("[", "").replace("]", "")
        line = rreplace(rreplace(line, ", ", ","), "\\'", "'")
        if (matches("^':", line) != None): raise ValueError("weighting marker with no value")
        elif (matches("^'[0-9]+:", line) == None): # no weighting marker
            elems: list[str] = line.split(",")
            output.append((pickRandElement(elems), 1))
        else:
            weight = int(line[1:].split(":")[0])
            if (weight == 0): continue # no weighting means element is never picked
            elems: list[str] = line[1:].split(":")[1].split(",")
            output.append((pickRandElement(elems), weight))
    if (verboseMode):
        for (i, (elem, weight)) in enumerate(output): print(f"{i + 1}: {elem} ({weight})")
    return output

def extractor(lines: list[str], i: int) -> (list[list[str]], int):
    output: list[list[str]] = []

    diff: int = 1
    while (i < len(lines) and not lines[i].startswith("## ")):
        extract = rreplace(lines[i].strip(), ", ", ",").split(",")
        output.append(extract)
        i += 1; diff += 1
    return (output, diff)

def sourceExtractor(sourceFile: str, p: Parameters) -> Contents:
    phrases: list[list[str]] = []
    emoji:   list[list[str]] = []
    nicks:   list[list[str]] = []

    try:
        with open(sourceFile, "r") as f:
            lines = f.readlines()
        # vvv remove empty lines and comments, and \n at the end of each line
        lines = [l[:-1] for l in lines if (len(l.strip()) > 1 and not l.strip().startswith("$"))]
        for line in lines:
            line = rreplace(rreplace(line, "  ", " "), ", ", ",")
        if (PHRASES_LOG not in lines or (p.toggleEmoji and EMOJI_LOG not in lines)):
            raise FileNotFoundError("Corrupted or invalid file: missing header")
        i: int = 0; skipLines: int = 0
        while (i < len(lines)):
            if   (lines[i] == PHRASES_LOG): (phrases, skipLines) = extractor(lines, i + 1)
            elif (lines[i] == EMOJI_LOG)  : (emoji,   skipLines) = extractor(lines, i + 1)
            elif (lines[i] == NICKS_LOG)  : (nicks,   skipLines) = extractor(lines, i + 1)
            i += skipLines; skipLines = 0
    except FileNotFoundError as e:
        print(f"Error reading from file '{sourceFile}': {e}"); gnExit(exitCode.ERR_INV_FIL)

    if (len(phrases) == 0):
        print(f"No phrase was found in '{sourceFile}'."); gnExit(exitCode.ERR_INV_PHR)
    if (p.toggleEmoji and len(emoji) == 0):
        print(f"No emoji was found in '{sourceFile}'.");  gnExit(exitCode.ERR_INV_EMO)

    try:
        c = Contents(
            applyWeighting(phrases, p.verboseMode),
            applyWeighting(emoji,   p.verboseMode),
            applyWeighting(nicks,   p.verboseMode)
        )
    except ValueError as e:
        print(f"Error reading from file '{sourceFile}': {e}"); gnExit(exitCode.ERR_INV_WEI)
    if (p.verboseMode): print(c)
    return c