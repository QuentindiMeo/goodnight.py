#!/usr/bin/env python3.10

from random import randint as rand
from re import search as matches

from Utils import rreplace, askConfirmation
from Contents import Contents
from Parameters import Parameters
from Types import WeightedList as Wlist
from Exit import exitCode, gnExit

HEAD_PHRASES: str = "## PHRASES.log"
HEAD_EMOJI:   str = "## EMOJI.log"
HEAD_NICKS:   str = "## NICKNAMES.log"
ASK_CONCAT:   str = "\nDo you want to concatenate the contents?"

def pickRandElement(elems: list[str]) -> str: return elems[rand(0, len(elems) - 1)]

def applyWeighting(input: list[list[str]]) -> list[Wlist]:
    output: list[Wlist] = []
    for line in input:
        line = str(line).replace("\"'", "\"").replace("'\"", "\"").replace("\\'", "'") \
            .replace("[", "").replace("]", "")
        line = rreplace(rreplace(line, ", ", ","), "\\'", "'")
        if   (matches("^':", line)): raise ValueError("weighting marker with no value")
        elif (not matches("^'[0-9]+:", line)): # no weighting marker
            elems: list[str] = line.split(",")
            output.append((pickRandElement(elems), 1))
        else:
            weight = int(line[1:].split(":")[0])
            if (weight == 0): continue # no weighting means element is never picked
            elems: list[str] = line[1:].split(":")[1].strip().split(",")
            output.append((pickRandElement(elems), weight))
    return output

def extractor(lines: list[str], i: int) -> (list[list[str]], int):
    output: list[list[str]] = []

    diff: int = 1
    while (i < len(lines) and not lines[i].startswith("## ")):
        extract = rreplace(lines[i].strip(), ", ", ",").split(",")
        output.append(extract)
        i += 1; diff += 1
    return (output, diff)

def contentsExtractor(p: Parameters) -> Contents:
    phrases: list[list[str]] = []
    emoji:   list[list[str]] = []
    nicks:   list[list[str]] = []

    try:
        with open(p.source, "r") as f:
            lines = f.readlines()

        # vvv remove empty lines and comments, and \n at the end of each line
        lines = [l[:-1] for l in lines if (len(l.strip()) > 1 and not l.strip().startswith("$"))]
        for line in lines:
            line = rreplace(rreplace(line, "  ", " "), ", ", ",")
        if (HEAD_PHRASES not in lines or (p.toggleEmoji and HEAD_EMOJI not in lines)):
            raise FileNotFoundError("Corrupted or invalid file: missing header")

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

        if (len(phrases) == 0):
            print(f"No phrase was found in '{p.source}'."); gnExit(exitCode.ERR_INV_PHR)
        if (p.toggleEmoji and len(emoji) == 0):
            print(f"No emoji was found in '{p.source}'.");  gnExit(exitCode.ERR_INV_EMO)

        # TODO warning if duplicate line; PROBLEM list is unhashable...
        # if (phrases != list(dict.fromkeys(phrases)) or emoji != list(dict.fromkeys(emoji)) or nicks != list(dict.fromkeys(nicks))):
        #     print(f"Duplicate entry was found in '{p.source}'.")
        #     askConfirmation("Do you want to continue regardless?", exitCode.ERR_DUP_ENT)

        c = Contents(
            applyWeighting(phrases), applyWeighting(emoji), applyWeighting(nicks)
        )
        c.phrases = [(p[0][1:-1], p[1]) for p in c.phrases]
        c.emoji   = [(e[0][1:-1], e[1]) for e in c.emoji]
        c.nicks   = [(n[0][1:-1], n[1]) for n in c.nicks]
    except FileNotFoundError as e:
        print(f"Error reading from file '{p.source}': {e}"); gnExit(exitCode.ERR_INV_FIL)
    except ValueError as e:
        print(f"Error reading from file '{p.source}': {e}"); gnExit(exitCode.ERR_INV_WEI)
    if (p.verboseMode): print(c)
    return c