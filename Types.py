#!/usr/bin/env python3.10

from types import TypeAlias

WeightedElement: TypeAlias = (str, int) # a phrase/emoji/nickname and its weight
WeightedList: TypeAlias = (list[str], int) # a list of phrases/emoji/nicknames and its weight

Goodnight: TypeAlias = str # the result
