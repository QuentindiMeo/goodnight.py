# CTRLHANDLERS.PY #

from os import name as osName
from signal import signal as bindSignal, SIGINT, SIGTERM
from types import FrameType

def getContext(frame: FrameType | None) -> str:
    try:
        if (osName == 'nt'): # Windows path type
            return frame.f_code.co_filename.split("\\")[-1] + ":" + str(frame.f_lineno) # type: ignore
        return frame.f_code.co_filename.split("/")[-1] + ":" + str(frame.f_lineno) # type: ignore
    except AttributeError | NameError:
        return "unknown context"

def CtrlDHandler(signalReceived: int, frame: FrameType | None) -> None:
    print(f"\n! SIGTERM ({signalReceived}) interruption caught in {getContext(frame)} !", flush=True)
    exit(0)

def CtrlCHandler(signalReceived: int, frame: FrameType | None) -> None:
    print(f"\n! SIGINT ({signalReceived}) interruption caught in {getContext(frame)} !", flush=True)
    exit(0)

def handler() -> None:
    bindSignal(SIGINT, CtrlCHandler)
    bindSignal(SIGTERM, CtrlDHandler)
