#!/usr/bin/env python3.10

from sys import argv as av

from Parameters import Parameters, drawParameters, defaultParameters

Goodnight = str

def addEmoji(gn: Goodnight) -> Goodnight:
    # TODO
    return gn

def goodnight(Parameters p) -> Goodnight:
    gn: Goodnight = ""
    if (p.toggleEmoji): gn = addEmoji(gn)
    return gn

def main(ac, av):
    # TODO
    if   (1): p = drawParameters(ac, av)
    elif (1): p = drawParameters()
    else    : p = defaultParameters()
    return goodnight(p)

if (__name__ == "__main__"): exit(main(len(av), av))
