#!/usr/bin/env python3.10

from pyperclip import copy # for copying the result to the clipboard

from sys import argv as av
from random import randint as rand

from Utils import rreplace
from Exit import exitCode, gnExit
from ContentsExtractor import contentsExtractor
from Contents import Contents
from Parameters import Parameters, getParameters
from Types import Goodnight, WeightedList as Wlist
from CtrlC import handler as CtrlCHandler

def goodnight(p: Parameters) -> Goodnight:
    gn: Goodnight = ""
    contents: Contents = contentsExtractor(p); nbPhrases = int(p.nbPhrases)

    usedPhrases: list[int] = [] # stores indices of phrases already used to avoid repetition
    usedEmoji:   list[int] = [] # stores indices of emoji already used to avoid repetition
    nickIdx: int = rand(0, nbPhrases - 1)

    if (not p.allowRep and nbPhrases > len(contents.phrases)): gnExit(exitCode.ERR_PAR_REP)
    p.forWhom = contents.pickNick(p)
    if (p.verboseMode): print(f"Starting with parameters: \n\t{p}\n")
    for x in range(nbPhrases):
        gn += " "
        # TODO pick a (weighted) phrase and blend it in
        if (x == nickIdx) : gn += p.forWhom
        if (p.toggleEmoji): gn += contents.pickEmoji(usedEmoji)
        else:               gn += "," if (x < nbPhrases - 1) else ""
        if (len(usedPhrases) == len(contents.phrases)): usedPhrases = []
        if (len(usedEmoji)   == len(contents.emoji))  : usedEmoji   = []
    return rreplace(gn.strip(), "  ", " ")

def main(ac: int, av: list[str]):
    CtrlCHandler() # binding Ctrl+C to a graceful program exit

    p: Parameters = getParameters(ac, av)

    result: Goodnight = goodnight(p)
    print(f"Result: \"{result}\"")
    print(f"for parameters: {p}")
    copy(result); print("Copied the result to your clipboard!")
    return 0

if (__name__ == "__main__"): exit(main(len(av), av))
