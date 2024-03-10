# TYPES.PY #

from os import name as osName
from copy import deepcopy as duplicate
from random import randint as rand
from typing import TypeAlias

IdxList:         TypeAlias = list[int] # a list of indices of used P/Es
ElementsList:    TypeAlias = list[str] # a list of P/E/N elements
WeightedElement: TypeAlias = tuple[str, int] # a P/E/N and its weight
WeightedList:    TypeAlias = tuple[ElementsList, int] # a list of P/E/N elements and its weight
UnweightedList:  TypeAlias = list[ElementsList] # an unweighted list of P/E/N elements
SetParams:       TypeAlias = list[str] | None
ParamDict:       TypeAlias = dict[str, bool | str | float | SetParams]

DEF_PREFFPATH:   str = "./assets/preferences.sav"
DEF_COPY:       bool = True
DEF_NB_PHRASES:  str = "?"
DEF_NB_DBOUND:   str = "2,5"
DEF_NB_UBOUND:   str = "999"
DEF_EMOJI:      bool = False
DEF_SOURCE:      str = "./assets/source.log"
DEF_FOR_WHOM:    str = ""
DEF_NICK_NTH:    str = "0"
DEF_REPETITION: bool = False
DEF_STEP:       bool = False
DEF_ALTERNATE:  bool = False
DEF_TIMES:       str = "1"
DEF_INFINITE:   bool = False
DEF_DELAY:       str = "0"
DEF_VERBOSITY:  bool = False
DEF_SAVE_PREF:  bool = False

class Goodnight:
    def __init__(self, txt: str) -> None:
        self.txt:   str = txt
        self.step: bool = False

class Parameters:
    def pickNbPhrases(self) -> None:
        if (',' in self.nbPhrases):
            (lowerBound, upperBound) = (int(self.nbPhrases.split(",")[0]), int(self.nbPhrases.split(",")[1]))
            self.nbPhrases = str(rand(lowerBound, upperBound))

    def toString(self) -> str:
        copynating = "copying" if self.copy else "generating"
        source = self.source.split("\\" if osName == 'nt' else "/")[-1]
        wEmoji = "with" if self.emoji else "without"
        forWhom = "(no name)" if self.forWhom == "" else self.forWhom
        match self.nickNth:
            case "0":  nickNth = "at random"
            case "-1": nickNth = "nowhere"
            case _:    nickNth = "after phrase " + self.nickNth
        repetition = "allowed" if self.allowRep else "not allowed"
        step = ("even" if self.step else "odd") + "-numbered gaps"
        alternate = "" if self.alternate else "not "
        return \
                f"{copynating} {self.times} goodnight(s) with "\
                f"{self.nbPhrases} phrases, " \
                f"{wEmoji} emoji, " \
                f"using {source} as a source, " \
                f"for {forWhom}, " \
                f"placing nickname {nickNth}, " \
                f"repetition {repetition}, " \
                f"step: {step}, " \
                f"{alternate}alternating, " \
                f"with a {self.delay}ms delay"
    def __str__(self) -> str:
        return \
                f"\tcopy: {self.copy}\n" \
                f"\tnumber of phrases: {self.nbPhrases}\n" \
                f"\temoji: {self.emoji}\n" \
                f"\tsource file: {self.source}\n" \
                f"\tfor: {self.forWhom}\n" \
                f"\tnickname position: {self.nickNth}\n" \
                f"\trepetition: {self.allowRep}\n" \
                f"\tstep: {self.step}\n" \
                f"\talternate: {self.alternate}\n" \
                f"\ttimes: {self.times}\n" \
                f"\tdelay: {self.delay}\n" \
                f"\tverbose mode: {self.verbose}\n" \
                f"\tsaving preferences: {self.saving}"

    def __init__(self, p: ParamDict) -> None:
        self.copy:      bool = bool(p.get("copy"))

        self.nbPhrases:  str = str(p.get("nbPhrases"))
        self.emoji:     bool = bool(p.get("emoji"))
        self.source:     str = str(p.get("source"))
        self.forWhom:    str = str(p.get("forWhom"))
        self.nickNth:    str = str(p.get("nickNth"))

        self.allowRep:  bool = bool(p.get("allowRep"))
        self.step:      bool = bool(p.get("step"))
        self.alternate: bool = bool(p.get("alternate"))
        self.times:      str = str(p.get("times"))
        self.infinite:  bool = bool(p.get("infinite"))
        self.delay:    float = p.get("delay")

        self.verbose:   bool = bool(p.get("verbose"))
        self.saving:    bool = bool(p.get("saving"))

        self.prefFile:   str = str(p.get("prefFile", DEF_PREFFPATH))
        self.setParams: SetParams = p.get("setParams", [])

class Contents:
    def pickNick(self, p: Parameters) -> str:
        if (p.forWhom != ""): return p.forWhom

        if (self.nicks == []):
            if (p.verbose): print(f"VVVV: No nicknames found, using default: {p.forWhom}")
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
        unpickedPhrases = duplicate(self.phrases)
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
        self.phrases: WeightedList = p
        self.emoji:   WeightedList = e
        self.nicks:   WeightedList = n
