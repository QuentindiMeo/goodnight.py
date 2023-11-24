#!/usr/bin/env python3.10

from Exit import exitCode, gnExit

# FIXME use this in CLI
def askConfirmation(s: str, e: exitCode = exitCode.SUCCESS) -> bool:
    while (True):
        ans: str = input(f"{s} (y/n) ")
        if (ans.lower() == "y" or ans.lower().startwith("yes")): return True
        if (ans.lower() == "n" or ans.lower().startwith("no")):
            if (e != exitCode.SUCCESS): gnExit(e)
            return False
    return False

def isIn(chars: list[str], s: str) -> bool:
    for c in chars:
        if (c in s): return True
    return False

def rremove(a: list[str], s: str) -> list[str]:
    while (s in a): a.remove(s)
    return a

def rreplace(s: str, old: str, new: str) -> str:
    while (old in s): s = s.replace(old, new)
    return s
