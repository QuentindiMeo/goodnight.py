#!/usr/bin/env python3.10

from enum import Enum

class exitCode(Enum):
    SUCCESS = 0x00
    HELP    = 0x01

    ERR_INV_ARG = 0x11
    ERR_INV_FIL = 0x12
    ERR_INV_PHR = 0x13
    ERR_INV_EMO = 0x14

def gnExit(code: exitCode):
    switch: dict = {
        0x00: "Success",
        0x01: "Help",
        0x11: "Invalid parameters",
        0x12: "Invalid file",
        0x13: "Invalid phrases",
        0x14: "Invalid emoji",
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
        "\n-n, --nb-fragments <int>  Number of fragments to draw (def: 2..5)" \
        "\n-e, --emoji               Add emoji between fragments (def: False)" \
        "\n-s, --source       <str>  Source file to read fragments and emoji from (def: source.log)" \
        "\n-w, --for-whom     <str>  For whom the goodnight is (def: \"\" (no name used))" \
        "\n-i, --ignore       Ignore preferences (preferences.sav)" \
        "\n--debug            Debug mode (def: False)" \
        "\n-h, --help         Display this help and exit")
