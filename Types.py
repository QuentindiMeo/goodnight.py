#!/usr/bin/env python3.10

from types import TypeAlias

PickResponse: TypeAlias = (str, list[int]) # the picked P/E and the list of indices of used P/Es
WeightedElement: TypeAlias = (str, int) # a P/E/N and its weight
WeightedList: TypeAlias = (list[str], int) # a list of P/E/Ns and its weight

Goodnight: TypeAlias = str # the result
