#!/usr/bin/env python3.10

from pyperclip import copy

from sys import argv as av
from random import randint as rand

from Parameters import Parameters, getParameters

Goodnight = str

phrases: list[str] = [
    "have a good night",
]
emoji: list[str] = [
    "🌙",
]

def addEmoji(gn: Goodnight) -> Goodnight:
    nbEmoji = rand(2, 3)
    gn += " "
    for _ in range(nbEmoji):
        gn += emoji[rand(0, len(emoji) - 1)]
    return gn + " "

def goodnight(p: Parameters) -> Goodnight:
    gn: Goodnight = ""
    for _ in range(p.nbFragments):
        # TODO pick a phrase and blend it in
        if (p.toggleEmoji): gn = addEmoji(gn)
    return gn.strip().replace("  ", " ")

def main(ac: int, av: list[str]):
    p: Parameters = getParameters(ac, av)
    result: Goodnight = goodnight(p)
    print(f"Result: \"{result}\"")
    print(f"for parameters: {p}")
    copy(result); print("Copied to clipboard!")
    return 0

if (__name__ == "__main__"): exit(main(len(av), av))
