# GOODNIGHT.PY #

from pyperclip import copy as copyToClipboard

from random import randint as rand
from time import sleep

from Utils import rreplace
from Exit import exitCode, gnExit
from ContentsExtractor import contentsExtractor
from Parameters import getParameters
from Types import Goodnight, Contents, Parameters
from CtrlHandlers import handler as CtrlHandler

def pickJunction(nth: int, nbPhrases: int, step: bool) -> str:
    if (nth >= nbPhrases - 1): return ""
    return " and" if ((nth + 1) % 2 == step) else ","

def goodnight(p: Parameters) -> Goodnight:
    gn = Goodnight("")
    contents: Contents = contentsExtractor(p)
    nbPhrases = int(p.nbPhrases)

    usedPhrases: list[int] = [] # stores indices of phrases already used to avoid repetition
    usedEmoji:   list[int] = [] # stores indices of  emoji  already used to avoid repetition
    nickIdx: int = rand(0, nbPhrases - 1) if int(p.nickNth) == 0 else int(p.nickNth) - 1 # index of the phrase that will be followed by the nickname

    if (not p.allowRep and nbPhrases > len(contents.phrases)): gnExit(exitCode.ERR_PAR_REP)
    p.forWhom = contents.pickNick(p)

    if (p.verbose): print(f"VVVV: Starting with parameters: \n{p}\n")
    for x in range(nbPhrases):
        usedPhrases = contents.pickPhrase(gn, usedPhrases)
        if (x == nickIdx) : gn.txt += (" " + p.forWhom)
        if (p.emoji):
            if (p.alternate and gn.step): gn.txt += pickJunction(x, nbPhrases, p.step)
            else: usedEmoji = contents.pickEmoji(gn, usedEmoji)
        else: gn.txt += pickJunction(x, nbPhrases, p.step)
        gn.txt += " "
        gn.step = not gn.step
        if (len(usedPhrases) == len(contents.phrases)): usedPhrases = []
        if (len(usedEmoji)   == len(contents.emoji))  : usedEmoji   = []
    gn.txt = rreplace(gn.txt.strip(), "  ", " ")
    gn.txt = gn.txt[0].upper() + gn.txt[1:]
    return gn

def main(ac: int, av: list[str]) -> int:
    CtrlHandler() # binding Ctrl+C/D to a graceful program exit

    p: Parameters = getParameters(ac, av)
    times = int(p.times)
    delay = (float(p.delay) / 1000) if (not p.delay.isalpha()) else -1

    while (times > 0 or p.infinite):
        result: Goodnight = goodnight(p)
        print(f"Result: \"{result.txt}\"")
        if (p.verbose): print(f"\nVVVV: for parameters: {p.toString()}")
        if (p.copy):
            copyToClipboard(result.txt)
            print("\nCopied the result to your clipboard!")
        times -= 1
        if (times > 0 or p.infinite):
            sleep(delay if (delay >= 0) else 0)
            if (delay == -1): input("\tPress Enter to proceed...")
    return 0
