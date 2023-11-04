#!/usr/bin/env python3.10

from pyperclip import copy # for copying the result to the clipboard

from sys import argv as av
from random import randint as rand

from SourceExtractor import sourceExtractor as extractor
from Parameters import Parameters, getParameters
from Types import Goodnight, Contents, WeightedList as Wlist
from CtrlC import handler as CtrlCHandler

def addEmoji(gn: Goodnight, emoji: Wlist) -> Goodnight:
    # TODO pick a random emoji (sequence) and add it to the end of the string
    return gn

def goodnight(p: Parameters) -> Goodnight:
    gn: Goodnight = ""
    contents: Contents = extractor(p.source, p)
    nbPhrases = int(p.nbPhrases)
    usedPhrases: list[int] = [] # stores indices of phrases already used to avoid repetition
    nickIdx: int = rand(0, nbPhrases - 1)

    if (p.verboseMode): print(f"Starting with parameters: \n{p}\n")
    # TODO --for-whom = nickname ?? for-whom
    for x in range(nbPhrases):
        # TODO pick a (weighted) phrase and blend it in
        if (x == nickIdx) : gn += p.forWhom
        if (p.toggleEmoji): gn = addEmoji(gn, contents.emoji)
        else:               gn += ","
        if (len(usedPhrases) == len(contents.phrases)): usedPhrases = [] # TODO depend upon --allow-repetition, if false then exit with error before execution
    return gn.strip().replace("  ", " ")

def main(ac: int, av: list[str]):
    CtrlCHandler() # binding Ctrl+C to a graceful program exit

    p: Parameters = getParameters(ac, av)

    result: Goodnight = goodnight(p)
    print(f"Result: \"{result}\"")
    print(f"for parameters: {p}")
    copy(result); print("Copied the result to your clipboard!")
    return 0

if (__name__ == "__main__"): exit(main(len(av), av))
