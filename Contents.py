#!/usr/bin/env python3.10

from copy import deepcopy as duplicate
from random import randint as rand

from Parameters import Parameters
from Types import WeightedList as Wlist

class Contents:
    def pickNick(self, p: Parameters) -> str :
        if (self.nicks == []):
            if (p.verboseMode): print(f"No nicknames found, using default: {p.forWhom}")
            return p.forWhom

        randWeight: int = rand(0, sum([n[1] for n in self.nicks]))
        for n in self.nicks:
            randWeight -= n[1]
            if (randWeight <= 0): return n[0]
        return ""

    def pickEmoji(self, gn: str, usedEmoji: list[int]) -> (str, list[int]):
        unpickedEmoji: Wlist = duplicate(self.emoji)
        for i in usedEmoji:
            unpickedEmoji.pop(i)
        randWeight: int = rand(0, sum([e[1] for e in unpickedEmoji]))
        for e in unpickedEmoji:
            randWeight -= e[1]
            newUsedEmoji: list[int] = sorted(usedEmoji + [self.emoji.index(e)], reverse=True)
            if (randWeight <= 0): return (gn + " " + e[0], newUsedEmoji)
        return (gn, 999)

    def pickPhrase(self, gn: str, usedPhrases: list[int]) -> (str, list[int]):
        unpickedPhrases: Wlist = duplicate(self.phrases)
        for i in usedPhrases:
            unpickedPhrases.pop(i)
        randWeight: int = rand(0, sum([p[1] for p in unpickedPhrases]))
        for p in unpickedPhrases:
            randWeight -= p[1]
            newUsedPhrases: list[int] = sorted(usedPhrases + [self.phrases.index(p)], reverse=True)
            if (randWeight <= 0): return (" " + gn + p[0], newUsedPhrases)
        return (" " + gn, 999)

    def __str__(self) -> str:
        s = "Source file–extracted contents:\n"
        s += f"\tPhrases:\t(sum of weights {sum([n[1] for n in self.phrases])})\n"
        for p in self.phrases: s += f"\t\t{p[0]} (weighted {p[1]})\n"
        s += f"\tEmoji:\t(sum of weights {sum([n[1] for n in self.emoji])})\n"
        for e in self.emoji:   s += f"\t\t{e[0]} (weighted {e[1]})\n"
        s += f"\tNicknames:\t(sum of weights {sum([n[1] for n in self.nicks])})\n"
        for n in self.nicks:   s += f"\t\t{n[0]} (weighted {n[1]})\n"
        return s

    def __init__(self, p: Wlist, e: Wlist, n: Wlist):
        # I have a peeeeeeen
        self.phrases = p
        self.emoji   = e
        self.nicks   = n