#!/usr/bin/env python3.10

from Exit import exitCode, gnExit

def askConfirmation(s: str, e: exitCode = exitCode.SUCCESS) -> bool:
    while (True):
        ans: str = input(f"{s} (y/n) ")
        if (ans == "y"): return True
        if (ans == "n"):
            if (e != exitCode.SUCCESS): gnExit(e)
            return False
    return False

def isIn(chars: list[str], s: str) -> bool:
    for c in chars:
        if (c in s): return True
    return False

def rreplace(s: str, old: str, new: str) -> str:
    while (old in s): s = s.replace(old, new)
    return s
