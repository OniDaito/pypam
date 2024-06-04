""" Support functions and classes we need when reading the
various PAMGuard and related files. This one is about byte
and byte array operations. 
https://techoverflow.net/2020/09/27/how-to-fix-python3-typeerror-unsupported-operand-types-for-bytes-and-bytes/
"""

__all__ = ["bitwise_and_bytes", "bitwise_or_bytes", "bitwise_xor_bytes"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"


def bitwise_and_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") & int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")


def bitwise_or_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") | int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")


def bitwise_xor_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") ^ int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")
