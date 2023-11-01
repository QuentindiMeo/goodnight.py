#!/usr/bin/env python3.10

from pyperclip import copy # for copying the result to the clipboard

from sys import argv as av
from random import randint as rand

from SourceExtractor import sourceExtractor as extractor
from Parameters import Parameters, getParameters
from Types import Goodnight, WeightedList as Wlist
from CtrlC import handler as CtrlCHandler

def addEmoji(gn: Goodnight, emoji: list[Wlist]) -> Goodnight:
    return gn + " "

def goodnight(p: Parameters) -> Goodnight:
    gn: Goodnight = ""
    (phrases, emoji, nicks) = extractor(p.source, p.toggleEmoji)
    usedPhrases: list[int] = [] # stores indices of phrases already used to avoid repetition

    if (p.debugMode):
        print(f"phrases: {phrases}\n" \
              f"emoji: {emoji}\n" \
              f"nicks: {nicks}\n")
    for _ in range(p.nbFragments):
        # TODO pick a phrase and blend it in
        if (p.toggleEmoji): gn = addEmoji(gn, emoji)
    # TODO ignore --for-whom if nicks are given
    return gn.strip().replace("  ", " ")

def main(ac: int, av: list[str]):
    CtrlCHandler()

    p: Parameters = getParameters(ac, av)
    result: Goodnight = goodnight(p)
    print(f"Result: \"{result}\"")
    print(f"for parameters: {p}")
    copy(result); print("Copied the result to your clipboard!")
    return 0

if (__name__ == "__main__"): exit(main(len(av), av))
