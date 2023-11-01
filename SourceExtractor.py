#!/usr/bin/env python3.10

from random import randint as rand

from Types import WeightedList as Wlist
from Exit import exitCode, gnExit

# TODO apply vvv to the code
def pickRandElement(line: list[str]) -> str: return line[rand(0, len(line) - 1)]

def applyWeighting(input: list[list[str]]) -> list[Wlist]:
    output: list[Wlist] = []
    # TODO weighting; do smart weighting, not just multiplying entries (str :: int)
    return output

PHRASES_LOG: str = "## PHRASES.log"
EMOJI_LOG:   str = "## EMOJI.log"
NICKS_LOG:   str = "## NICKNAMES.log"

def extractor(lines: list[str], i: int) -> (list[list[str]], int):
    output: list[list[str]] = []

    diff: int = 1
    while (i < len(lines) and not lines[i].startswith("## ")):
        output.append(lines[i].split(","))
        i += 1; diff += 1
    return (output, diff)

def sourceExtractor(sourceFile: str, toggleEmoji: bool) -> (list[str], str):
    phrases: list[list[str]] = []
    emoji:   list[list[str]] = []
    nicks:   list[list[str]] = []

    try:
        with open(sourceFile, "r") as f:
            lines = f.readlines()
            # vvv remove empty lines and comments, and \n at the end of each line
            lines = [l[:-1] for l in lines if (len(l.strip()) > 1 and not l.strip().startswith("$"))]
            for line in lines:
                while ("  " in line or ", " in line): line = line.replace("  ", " ").replace(", ", ",")
            if (PHRASES_LOG not in lines or (toggleEmoji and EMOJI_LOG not in lines)):
                raise FileNotFoundError("Corrupted or invalid file: missing header")
            i: int = 0; skipLines: int = 0
            while (i < len(lines)):
                if   (lines[i] == PHRASES_LOG): (phrases, skipLines) = extractor(lines, i + 1)
                elif (lines[i] == EMOJI_LOG):   (emoji,   skipLines) = extractor(lines, i + 1)
                elif (lines[i] == NICKS_LOG):   (nicks,   skipLines) = extractor(lines, i + 1)
                i += skipLines; skipLines = 0
    except FileNotFoundError as e:
        print(f"Error reading from file '{sourceFile}': {e}"); gnExit(exitCode.ERR_INV_FIL)
    if (len(phrases) == 0):
        print(f"No phrase was found in '{sourceFile}'."); gnExit(exitCode.ERR_INV_PHR)
    if (toggleEmoji and len(emoji) == 0):
        print(f"No emoji was found in '{sourceFile}'."); gnExit(exitCode.ERR_INV_EMO)
    return (phrases, emoji, nicks)