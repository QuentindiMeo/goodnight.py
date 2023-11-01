#!/usr/bin/env python3.10

from enum import Enum

class exitCode(Enum):
    SUCCESS = 0x00
    HELP    = 0x01

    ERR_INV_ARG = 0x11
    ERR_INV_FIL = 0x12

def gnExit(code: exitCode):
    switch: dict = {
        0x00: "Success",
        0x01: "Help",
        0x11: "Invalid parameters",
        0x12: "Invalid file",
    }
    if (code.value == 0x01):
        gnUsage(); code = exitCode.SUCCESS
    if (code.value > 0x10):
        print(f"Exit: {switch.get(code.value, 'Unknown error')}")
    exit(code.value)

def gnUsage():
    print("Usage: python Goodnight.py [OPTIONS]" \
        "\n" \
        "\nOptions:" \
        "\n-n, --nb-fragments <int>  Number of fragments to draw (def: 2..4)" \
        "\n-e, --emoji        <bool> Add emoji between fragments (def: false)" \
        "\n-w, --for-whom     <str>  For whom the goodnight is (def: \"\")" \
        "\n-s, --source       <str>  Source file (def: \"source.log\")" \
        "\n-D                 Save used parameters as preferences (.sav file)" \
        "\n-i, --ignore       Ignore preferences (.sav file)" \
        "\n-h, --help         Display this help and exit")
