# CONTENTSEXTRACTOR.PY #

from random import randint as rand
from re import search as matches

from Utils import rreplace, askConfirmation, hasDuplicates
from Parameters import Parameters
from Types import WeightedElement as WElement, UnweightedList as Ulist, Contents
from Exit import exitCode, gnExit

COMMENT_MARKER: str = "--"
HEADERS_MARKER: str = "## "
HEAD_PHRASES:   str = "## PHRASES.log"
HEAD_EMOJI:     str = "## EMOJI.log"
HEAD_NICKS:     str = "## NICKNAMES.log"
ASK_CONCAT:     str = "\nDo you want to concatenate the contents?"
MAT_WEI_MARKER: str = r"^':"
MAT_WEI_WEIGHT: str = r"^'[0-9]+:"

def pickRandElement(elements: list[str]) -> str: return elements[rand(0, len(elements) - 1)]

def applyWeighting(input: Ulist) -> list[WElement]:
    output: list[WElement] = []
    for line in input:
        line = str(line).replace("\"'", "\"").replace("'\"", "\"").replace("\\'", "'") \
            .replace("[", "").replace("]", "")
        line = rreplace(rreplace(line, ", ", ","), "\\'", "'")
        if   (matches(MAT_WEI_MARKER, line)): raise ValueError("weighting marker with no value")
        elif (not matches(MAT_WEI_WEIGHT, line)): # no weighting marker
            elements: list[str] = line.split(",")
            output.append((pickRandElement(elements), 1))
        else: # has weighting marker
            weight = int(line[1:].split(":")[0])
            if (weight == 0): continue # no weighting means element is never picked
            elements: list[str] = line[1:].split(":")[1].strip().split(",")
            output.append((pickRandElement(elements), weight))
    return output

def extractor(lines: list[str], i: int) -> tuple[Ulist, int]:
    output: Ulist = []

    diff: int = 1
    while (i < len(lines) and not lines[i].startswith(HEADERS_MARKER)):
        extract = rreplace(lines[i].strip(), ", ", ",").split(",")
        output.append(extract)
        i += 1; diff += 1
    return (output, diff)

def contentsExtractor(p: Parameters) -> Contents:
    phrases: Ulist = []
    emoji:   Ulist = []
    nicks:   Ulist = []
    lines:   list[str] = []

    try:
        with open(p.source, "r") as f: lines = f.readlines()
        # vvv remove empty lines and comments, and \n at the end of each line
        lines = [l[:-1] for l in lines if (len(l.strip()) > 1 and not l.strip().startswith(COMMENT_MARKER))]
        for line in lines:
            line = rreplace(rreplace(line, "  ", " "), ", ", ",")
        if (HEAD_PHRASES not in lines or (p.emoji and HEAD_EMOJI not in lines)):
            raise ValueError("Corrupted or invalid file: missing header")
    except FileNotFoundError | ValueError as e:
        print(f"Error reading from file '{p.source}': {e}")
        gnExit(exitCode.ERR_INV_FIL if isinstance(e, FileNotFoundError) else exitCode.ERR_INV_HEA)

    i: int = 0; skipLines: int = 0
    while (i < len(lines)):
        if   (lines[i] == HEAD_PHRASES):
            concat: bool = True
            (newPhrases, skipLines) = extractor(lines, i + 1)
            if (len(phrases) != 0):
                concat = askConfirmation(f"Several PHRASES.log headers were found in {p.source}" + ASK_CONCAT)
            phrases += newPhrases if concat else []
        elif (lines[i] == HEAD_EMOJI):
            concat: bool = True
            (newEmoji,   skipLines) = extractor(lines, i + 1)
            if (len(emoji) != 0):
                concat = askConfirmation(f"Several EMOJI.log headers were found in {p.source}" + ASK_CONCAT)
            emoji += newEmoji if concat else []
        elif (lines[i] == HEAD_NICKS):
            concat: bool = True
            (newNicks,   skipLines) = extractor(lines, i + 1)
            if (len(nicks) != 0):
                concat = askConfirmation(f"Several NICKNAMES.log headers were found in {p.source}" + ASK_CONCAT)
            nicks += newNicks if concat else []
        i += skipLines; skipLines = 0

    if (len(phrases) == 0):           print(f"No phrase was found in '{p.source}'."); gnExit(exitCode.ERR_INV_PHR)
    if (p.emoji and len(emoji) == 0): print(f"No emoji was found in '{p.source}'.");  gnExit(exitCode.ERR_INV_EMO)

    (dphrases, demoji, dnicks) = (hasDuplicates(phrases), hasDuplicates(emoji), hasDuplicates(nicks))
    if (dphrases or demoji or dnicks): # send warning if there's a duplicate entry in any of the three
        print(f"One or more duplicate entries were found in '{p.source}'.")
        askConfirmation("Do you want to continue regardless?", exitCode.ERR_DUP_ENT)
    if (p.verbose):
        if (dphrases): print("VVVV: Log file contains duplicate phrases.")
        if (demoji):   print("VVVV: Log file contains duplicate emoji.")
        if (dnicks):   print("VVVV: Log file contains duplicate nicknames.")

    c: Contents = Contents([], [], [])
    try:
        c = Contents(
            applyWeighting(phrases), applyWeighting(emoji), applyWeighting(nicks)
        )
    except ValueError as e:
        print(f"Error reading from file '{p.source}': {e}"); gnExit(exitCode.ERR_INV_WEI)
    c.phrases = [(p[0][1:-1], p[1]) for p in c.phrases] # remove dquotes around phrases
    c.emoji   = [(e[0][1:-1], e[1]) for e in c.emoji] # ^ same
    c.nicks   = [(n[0][1:-1], n[1]) for n in c.nicks] # ^ same

    if (p.verbose): print("VVVV:", c)
    return c