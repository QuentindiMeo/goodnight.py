# CTRLHANDLERS.PY #

from os import name as osName
from signal import signal as bindSignal, SIGINT, SIGTERM

def getContext(frame: str) -> str:
    return   frame.f_code.co_filename.split("\\")[-1] + ":" + str(frame.f_lineno) if osName == 'nt' \
        else frame.f_code.co_filename.split("/")[-1]  + ":" + str(frame.f_lineno)

def CtrlDHandler(signal_received: int, frame: str) -> None:
    print(f"\n! SIGTERM ({signal_received}) interruption caught in {getContext(frame)} !", flush=True)
    exit(0)

def CtrlCHandler(signal_received: int, frame: str) -> None:
    print(f"\n! SIGINT ({signal_received}) interruption caught in {getContext(frame)} !", flush=True)
    exit(0)

def handler() -> None:
    bindSignal(SIGINT, CtrlCHandler)
    bindSignal(SIGTERM, CtrlDHandler)
