""" Support functions and classes we need when reading the
various PAMGuard and related files. """

__all__ = ["read_java_string"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import struct
from typing import Tuple


def read_java_string(dat, offset) -> Tuple[str, int]:
    """Utility function for reading java strings"""
    ds = offset
    dt = struct.unpack(">h", dat[ds : ds + 2])[0]
    ds += 2
    java_str = ""

    if dt > 0:
        java_str = str(dat[ds : ds + dt], "utf-8")
        ds += dt

    return (java_str, dt + 2)
