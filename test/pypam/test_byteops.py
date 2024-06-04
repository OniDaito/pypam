""" Tests for the byteops."""

from pypam.util.byteops import *

def test_byteops():
    res = bitwise_and_bytes(bytes(b'\x00\x8d'), bytes(b'\x00\x8d'))
    assert res == b'\x00\x8d'
    
    res = bitwise_and_bytes(bytes(b'\x00\x8d'), bytes(b'\x00\x8d'))
    assert res == b'\x00\x8d'
    
    TIMEMILLIS = bytes(b'\x00\x01')
    TIMENANOS = bytes(b'\x00\x02')
    CHANNELMAP =  bytes(b'\x00\x04')
    UID =  bytes(b'\x00\x08')
    MILLISDURATION =  bytes(b'\x00\x80')

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), TIMEMILLIS)
    assert res != b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), TIMENANOS)
    assert res == b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), CHANNELMAP)
    assert res != b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), UID)
    assert res != b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), MILLISDURATION)
    assert res != b'\x00\x00'