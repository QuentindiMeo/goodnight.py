#!/usr/bin/env python3.10

from enum import Enum

class exitCode(Enum):
    SUCCESS = 0x00
    HELP    = 0x01

    ERR_INV_ARG = 0x11
    ERR_INV_FIL = 0x12
    ERR_INV_PHR = 0x13
    ERR_INV_EMO = 0x14
    ERR_INV_WEI = 0x15
    ERR_DUP_ENT = 0x16
    ERR_DUP_PHR = 0x17
    ERR_DUP_EMO = 0x18
    ERR_DUP_NIC = 0x19

    ERR_PAR_REP = 0x21

def gnExit(code: exitCode) -> None:
    switch: dict() = {
        0x00: "Success",
        0x01: "Help",

        0x11: "Invalid parameters",
        0x12: "Invalid file",
        0x13: "Invalid phrases",
        0x14: "Invalid emoji",
        0x15: "Invalid weighting",
        0x16: "Duplicate entries",
        0x17: "Duplicate phrases header",
        0x18: "Duplicate emoji header",
        0x19: "Duplicate nicknames header",

        0x21: "Insufficient number of phrases to draw without repetition",
    }
    if (code == exitCode.HELP):
        gnUsage(); code = exitCode.SUCCESS
    if (code.value > 0x10):
        print(f"Exit: {switch.get(code.value, 'Unknown error')}.")
    exit(code.value)

def gnUsage() -> None:
    print("Usage: python Goodnight.py [OPTIONS]" \
        "\n" \
        "\nOptions:" \
        "\n  --default               Launch once with default values (ignores other parameters)" \
        "\n  --no-copy               Do not copy the result to clipboard" \
        "\n" \
        "\n  -b, --bounds     (x,y)  Bounds for the random range of how many phrases to draw (def: 2,5)" \
        "\n  -n, --nb-phrases <int>  Number of phrases to draw" \
        "\n  -e, --emoji             Add emoji between phrases (from source file)" \
        "\n  -s, --source     <str>  Source file to pull contents (phrases...) from (def: ./assets/source.log)" \
        "\n  -w, --for-whom   <str>  For whom the goodnight is (def: \"\" [no name used])" \
        "\n" \
        "\n  -r, --allow-repetition  Allow repetition of phrases if you ask for more than there are in the source file" \
        "\n  -o, --other-step        Use the even-numbered phrase gaps as \"and\"s instead of commas (def: [odd-])" \
        "\n  -a, --alternate         Alternate between \"and\"s, and emoji instead of commas (requires -e, def: False)" \
        "\n  -i, --ignore            Ignore preferences (preferences.sav)" \
        "\n  -S, --save              Save preferences to file (preferences.sav)" \
        "\n" \
        "\n  --verbose               Toggle verbose mode" \
        "\n  -h, --help              Display this help and exit" \
        "\n" \
        "\nExit the program at any time using Ctrl+C."
        )
