#!/usr/bin/env python3.10

from Parameters import Parameters

WeightedElement = (str, int) # type alias for a phrase/emoji/nickname and its weight
WeightedList = (list[str], int) # type alias for a list of phrases/emoji/nicknames and its weight
class Contents:
    def __str__(self) -> str:
        s = "Contents:\n"
        s += "\tPhrases:\n"
        for p in self.phrases: s += f"\t\t{p[0]} (weighted {p[1]})\n"
        s += "\tEmoji:\n"
        for e in self.emoji:   s += f"\t\t{e[0]} (weighted {e[1]})\n"
        s += "\tNicknames:\n"
        for n in self.nicks:   s += f"\t\t{n[0]} (weighted {n[1]})\n"
        # I have a peeeeeeeeeeeeen
        return s

    def __init__(self, phrases: WeightedList, emoji: WeightedList, nicks: WeightedList):
        self.phrases = phrases
        self.emoji   = emoji
        self.nicks   = nicks

Goodnight = str # type alias for the result