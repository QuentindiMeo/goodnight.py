#!/usr/bin/env python3.10

from os import name as osName
from copy import deepcopy as duplicate
from random import randint as rand
from typing import TypeAlias

IdxList:         TypeAlias = list[int] # a list of indices of used P/Es
ElementList:     TypeAlias = list[str] # a list of P/E/N elements
WeightedElement: TypeAlias = (str, int) # a P/E/N and its weight
WeightedList:    TypeAlias = (ElementList, int) # a list of P/E/N elements and its weight
UnweightedList:  TypeAlias = list[ElementList] # an unweighted list of P/E/N elements

DEF_COPY:       bool = True
DEF_NB_PHRASES:  str = "?"
DEF_NB_DBOUND:   str = "2,5"
DEF_NB_UBOUND:   str = "999"
DEF_EMOJI:      bool = False
DEF_SOURCE:      str = "./assets/source.log " # same as below
DEF_FOR_WHOM:    str = " " # space to skip the CLI if the user used the default value as a parameter
DEF_REPETITION: bool = False
DEF_STEP:       bool = False
DEF_ALTERNATE:  bool = False
DEF_INFINITE:   bool = False
DEF_VERBOSITY:  bool = False
DEF_SAVE_PREF:  bool = False

class Goodnight:
    def __init__(self, txt: str) -> None:
        self.txt = txt
        self.step = False

class Parameters:
    def pickNbPhrases(self) -> None:
        if (',' in self.nbPhrases):
            (lowerBound, upperBound) = (int(self.nbPhrases.split(",")[0]), int(self.nbPhrases.split(",")[1]))
            self.nbPhrases = str(rand(lowerBound, upperBound))

    def toString(self) -> str:
        source = self.source.split("\\" if osName == 'nt' else "/")[-1]
        wEmoji = "with" if self.emoji else "without"
        repetition = "allowed" if self.allowRep else "not allowed"
        step = ("even" if self.step else "odd") + "-numbered gaps"
        alternate = "" if self.alternate else "not "
        return  f"{self.nbPhrases} phrases, " \
                f"{wEmoji} emoji, " \
                f"source: {source}, " \
                f"for {self.forWhom}, " \
                f"repetition {repetition}, " \
                f"step: {step}, " \
                f"{alternate}alternating"
    def __str__(self) -> str:
        return \
                f"\t{self.nbPhrases} phrases\n" \
                f"\temoji: {self.emoji}\n" \
                f"\tsource file: {self.source}\n" \
                f"\tfor: {self.forWhom}\n" \
                f"\trepetition: {self.allowRep}\n" \
                f"\tstep: {self.step}\n" \
                f"\talternate: {self.alternate}\n" \
                f"\tcopy: {self.copy}\n" \
                f"\tverbose mode: {self.verbose}\n" \
                f"\tsaving preferences: {self.saving}"

    def __init__(self, c: bool = DEF_COPY, n: str = DEF_NB_PHRASES, e: bool = DEF_EMOJI, s: str = DEF_SOURCE, w: str = DEF_FOR_WHOM, \
                 r: bool = DEF_REPETITION, o: bool = DEF_STEP, a: bool = DEF_ALTERNATE, i: bool = DEF_INFINITE, \
                 v: bool = DEF_VERBOSITY, sav: bool = DEF_SAVE_PREF) -> None:
        self.copy      = c

        self.nbPhrases = n
        self.emoji     = e
        self.source    = s
        self.forWhom   = w

        self.allowRep  = r
        self.step      = o
        self.alternate = a
        self.infinite  = i

        self.verbose   = v
        self.saving    = sav

        self.times     = 1
        self.delay     = 0

class Contents:
    def pickNick(self, p: Parameters) -> str:
        if (p.forWhom != ""): return p.forWhom

        if (self.nicks == []):
            if (p.verbose): print(f"No nicknames found, using default: {p.forWhom}")
            return p.forWhom

        randWeight: int = rand(0, sum([n[1] for n in self.nicks]))
        for n in self.nicks:
            randWeight -= n[1]
            if (randWeight <= 0): return n[0]
        return ""

    def pickEmoji(self, gn: Goodnight, usedEmoji: IdxList) -> IdxList:
        unpickedEmoji: WeightedList = duplicate(self.emoji)
        for i in usedEmoji: unpickedEmoji.pop(i)
        randWeight: int = rand(0, sum([e[1] for e in unpickedEmoji]))
        for e in unpickedEmoji:
            randWeight -= e[1]
            newUsedEmoji: IdxList = sorted(usedEmoji + [self.emoji.index(e)], reverse=True)
            if (randWeight <= 0):
                gn.txt += " " + e[0]
                return newUsedEmoji
        return [999]

    def pickPhrase(self, gn: Goodnight, usedPhrases: IdxList) -> IdxList:
        unpickedPhrases: WeightedList = duplicate(self.phrases)
        for i in usedPhrases: unpickedPhrases.pop(i)
        randWeight: int = rand(0, sum([p[1] for p in unpickedPhrases]))
        for p in unpickedPhrases:
            randWeight -= p[1]
            newUsedPhrases: IdxList = sorted(usedPhrases + [self.phrases.index(p)], reverse=True)
            if (randWeight <= 0):
                gn.txt += " " + p[0]
                return newUsedPhrases
        gn.txt = " " + gn.txt
        return [999]

    def __str__(self) -> str:
        s = "Source file–extracted contents:\n"
        s += f"\tPhrases:\t(sum of weights {sum([n[1] for n in self.phrases])})\n"
        for p in self.phrases: s += f"\t\t{p[0]} (weighted {p[1]})\n"
        s += f"\tEmoji:\t(sum of weights {sum([n[1] for n in self.emoji])})\n"
        for e in self.emoji:   s += f"\t\t{e[0]} (weighted {e[1]})\n"
        s += f"\tNicknames:\t(sum of weights {sum([n[1] for n in self.nicks])})\n"
        for n in self.nicks:   s += f"\t\t{n[0]} (weighted {n[1]})\n"
        return s

    def __init__(self, p: WeightedList, e: WeightedList, n: WeightedList) -> None:
        # I have a peeeeeeen
        self.phrases = p
        self.emoji   = e
        self.nicks   = n