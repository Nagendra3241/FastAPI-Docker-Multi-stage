import time
from datetime import datetime


def now(format: str = "%Y-%m-%d %H:%M:%S") -> str: return datetime.now().strftime(format)


def time_elapsed(end: float, start: float) -> str:
    diff = end - start
    if diff > 60:
        mins, secs = int(diff // 60) , int(diff % 60)
        return f"Time elapsed {mins} minutes and {secs} seconds"
    return f"Time elapsed {diff} seconds"