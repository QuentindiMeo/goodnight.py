#!/usr/bin/env python3.10

def isIn(chars: list[str], s: str) -> bool:
    for c in chars:
        if (c in s): return True
    return False

def rreplace(s: str, old: str, new: str) -> str:
    while (old in s): s = s.replace(old, new)
    return s