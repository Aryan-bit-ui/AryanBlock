"""Built-in functions"""
import math
import random
import time

def _fmt(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f'"{k}": {_fmt(v)}' for k, v in v.items()) + "}"
    return str(v)

BUILTINS = {
    "print": lambda *args: print(*[_fmt(a) for a in args]),
    "input": input,
    "len": len,
    "type": lambda x: type(x).__name__,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "range": lambda *a: list(range(*a)),
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "sqrt": math.sqrt,
    "pow": pow,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "random": random.random,
    "random_int": random.randint,
    "time": time.time,
    "sleep": time.sleep,
    "push": lambda arr, x: arr.append(x) or arr,
    "pop": lambda arr: arr.pop(),
    "slice": lambda arr, *a: arr[slice(*a)],
    "reverse": lambda arr: arr.reverse() or arr,
    "sort": lambda arr: arr.sort() or arr,
    "join": lambda arr, sep="": sep.join(str(x) for x in arr),
    "split": lambda s, sep=" ": s.split(sep),
    "contains": lambda col, x: x in col,
    "keys": lambda d: list(d.keys()),
    "values": lambda d: list(d.values()),
    "upper": lambda s: s.upper(),
    "lower": lambda s: s.lower(),
    "trim": lambda s: s.strip(),
    "replace": lambda s, a, b: s.replace(a, b),
    "assert": lambda c, m="Assertion failed": None if c else (_ for _ in ()).throw(AssertionError(m)),
}

CONSTANTS = {"PI": math.pi, "E": math.e, "TAU": math.tau}
