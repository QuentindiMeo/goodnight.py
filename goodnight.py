#!/usr/bin/env python3.10

from pyperclip import copy # for copying the result to the clipboard

from sys import argv as av
from random import randint as rand

from Utils import rreplace
from Exit import exitCode, gnExit
from ContentsExtractor import contentsExtractor
from Parameters import getParameters
from Types import Goodnight, Contents, Parameters
from CtrlC import handler as CtrlCHandler

def pickJunction(nth: int, nbPhrases: int, step: bool) -> str:
    if (nth >= nbPhrases - 1): return ""
    return " and" if ((nth + 1) % 3 == step) else ","

def goodnight(p: Parameters) -> Goodnight:
    gn = Goodnight("")
    contents: Contents = contentsExtractor(p)
    nbPhrases = int(p.nbPhrases)

    usedPhrases: list[int] = [] # stores indices of phrases already used to avoid repetition
    usedEmoji:   list[int] = [] # stores indices of  emoji  already used to avoid repetition
    nickIdx: int = rand(0, nbPhrases - 1)

    if (not p.allowRep and nbPhrases > len(contents.phrases)): gnExit(exitCode.ERR_PAR_REP)
    p.forWhom = contents.pickNick(p)

    if (p.verbose): print(f"Starting with parameters: \n{p}\n")
    for x in range(nbPhrases):
        usedPhrases = contents.pickPhrase(gn, usedPhrases)
        if (x == nickIdx) : gn.txt += (" " + p.forWhom)
        if (p.emoji):
            if (p.alternate and gn.step): gn.txt += pickJunction(x, nbPhrases, p.step)
            else: usedEmoji = contents.pickEmoji(gn, usedEmoji)
            gn.step = not gn.step
        # TODO --alternate
        else: gn.txt += pickJunction(x, nbPhrases, p.step)
        gn.txt += " "
        if (len(usedPhrases) == len(contents.phrases)): usedPhrases = []
        if (len(usedEmoji)   == len(contents.emoji))  : usedEmoji   = []
    gn.txt = rreplace(gn.txt.strip(), "  ", " ")
    return gn

def main(ac: int, av: list[str]) -> int:
    CtrlCHandler() # binding Ctrl+C to a graceful program exit

    p: Parameters = getParameters(ac, av)

    result: Goodnight = goodnight(p)

    print(f"Result: \"{result.txt}\"")
    if (p.verbose): print(f"for parameters: {p.toString()}")
    if (p.copy):
        copy(result.txt)
        print("\nCopied the result to your clipboard!")
    return 0

if (__name__ == "__main__"): exit(main(len(av), av))
# TODO new demo gif