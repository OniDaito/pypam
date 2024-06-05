""" Support functions and classes we need when reading the
various PAMGuard and related files. """

__all__ = ["is_float"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"


def is_float(v):
    try:
        _ = float(v)
    except ValueError:
        return False
    return True
