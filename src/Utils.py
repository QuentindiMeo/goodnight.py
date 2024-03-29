# UTILS.PY #

from os import kill, getpid

from re import search as matches

from Exit import exitCode, gnExit
from Types import UnweightedList as Ulist

DEF_NB_UBOUND:     str = "999"
MAT_INTEGER_INPUT: str = r"^[0-9]+$"
MAT_INVALID_INPUT: str = "Invalid input: must be a positive number or 'y'."

def runParameterDuplicateChecks(av: list[str]) -> None:
    parametersLong:  list[str] = [arg for arg in av if arg.startswith("--")]
    parametersShort: list[str] = [arg for arg in av if arg.startswith("-") and arg not in parametersLong]

    # if duplicate among parameters, raise error
    if (len(parametersLong)  != len(set(parametersLong)) or \
        len(parametersShort) != len(set(parametersShort))):
            print(f"Duplicate argument(s) in '{av}':")
            for par in parametersLong:
                if (parametersLong.count(par) != 1): print(f"\t'{par}' is present several times."); break
            for par in parametersShort:
                if (parametersShort.count(par) != 1): print(f"\t'{par}' is present several times."); break
            gnExit(exitCode.ERR_DUP_PAR)

def hasDuplicates(listOfLists: Ulist) -> bool:
    flatList = [item for sublist in listOfLists for item in sublist]
    return len(set(flatList)) != len(flatList)

def askConfirmationNumber(context: str) -> str:
    while (True):
        ans: str = input(f"{context}. Continue or change (y/?): ").strip().lower()
        if (ans == "y" or ans.startswith("yes")): break
        if (not matches(MAT_INTEGER_INPUT, ans)):
            print(MAT_INVALID_INPUT); continue
        if (int(ans) > int(DEF_NB_UBOUND)): ans = DEF_NB_UBOUND
        return ans
    return "y"

def askConfirmation(context: str, e: exitCode = exitCode.SUCCESS) -> bool:
    while (True):
        ans: str = input(f"{context} (y/n): ").strip().lower()
        if (ans == "y" or ans.startswith("yes")): return True
        if (ans == "n" or ans.startswith("no")):
            if (e != exitCode.SUCCESS): gnExit(e)
            break
    return False

def beval(value: str) -> bool: return eval(value.capitalize())

def sendSignal(sig: int) -> None:
    kill(getpid(), sig)

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
