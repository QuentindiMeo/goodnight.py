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
        print(f"Exit: {switch.get(code, 'Unknown error')}")
    exit(code.value)

def gnUsage():
    print("Usage: goodnight [OPTIONS]" \
        "\n" \
        "\nOptions:" \
        "\n-n, --nb-fragments <int>  (def: 2..4)    Number of fragments to draw" \
        "\n-e, --emoji        <bool> (def: false)   Add emoji between fragments" \
        "\n-w, --for-whom     <str>  (def: \"\")      For whom the goodnight is" \
        "\n-h, --help         Display this help and exit")
