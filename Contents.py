#!/usr/bin/env python3.10

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

    def __str__(self) -> str:
        s = "Source file–extracted contents:\n"
        s += "\tPhrases:\n"
        for p in self.phrases: s += f"\t\t{p[0]} (weighted {p[1]})\n"
        s += "\tEmoji:\n"
        for e in self.emoji:   s += f"\t\t{e[0]} (weighted {e[1]})\n"
        s += "\tNicknames:\n"
        for n in self.nicks:   s += f"\t\t{n[0]} (weighted {n[1]})\n"
        return s

    def __init__(self, p: Wlist, e: Wlist, n: Wlist):
        # I have a peeeeeeen
        self.phrases = p
        self.emoji   = e
        self.nicks   = n