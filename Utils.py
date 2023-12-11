#!/usr/bin/env python3.10

from re import search as matches

from Exit import exitCode, gnExit
from Types import UnweightedList as Ulist

DEF_MAX_UBOUND:    str = "999"
MAT_NUMBERS_INPUT: str = "^[0-9]+$"
MAT_INVALID_INPUT: str = "Invalid input: must be a positive number or 'y'."

def hasDuplicates(listOfLists: Ulist) -> bool:
    flatList = [item for sublist in listOfLists for item in sublist]
    return len(set(flatList)) != len(flatList)

def askConfirmationNumber(context: str) -> str:
    while (True):
        ans: str = input(f"{context}. Continue or change (y/?): ").strip().lower()
        if (ans == "y" or ans.startswith("yes")): break
        if (not matches(MAT_NUMBERS_INPUT, ans)):
            print(MAT_INVALID_INPUT); continue
        if (int(ans) > int(DEF_MAX_UBOUND)): ans = DEF_MAX_UBOUND
        return ans
    return "y"

def askConfirmation(context: str, e: exitCode = exitCode.SUCCESS) -> bool:
    while (True):
        ans: str = input(f"{context} (y/n): ").strip().lower()
        if (ans == "y" or ans.startswith("yes")): return True
        if (ans == "n" or ans.startswith("no")):
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
