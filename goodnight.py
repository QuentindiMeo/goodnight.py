#!/usr/bin/env python3

from os import getcwd
from sys import argv as av, path

path.append(getcwd() + "/src") # fetch src/ to get the main's module

from Goodnight import main

if (__name__ == "__main__"): exit(main(len(av), av))
