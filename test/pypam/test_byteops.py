""" Tests for the byteops."""

from pypam.util.byteops import bitwise_and_bytes

def test_byteops():
    res = bitwise_and_bytes(bytes(b'\x00\x8d'), bytes(b'\x00\x8d')) # noqa: F405
    assert res == b'\x00\x8d'
    
    res = bitwise_and_bytes(bytes(b'\x00\x8d'), bytes(b'\x00\x8d')) # noqa: F405
    assert res == b'\x00\x8d'
    
    TIMEMILLIS = bytes(b'\x00\x01')
    TIMENANOS = bytes(b'\x00\x02')
    CHANNELMAP =  bytes(b'\x00\x04')
    UID =  bytes(b'\x00\x08')
    MILLISDURATION =  bytes(b'\x00\x80')

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), TIMEMILLIS)  # noqa: F405
    assert res != b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), TIMENANOS) # noqa: F405
    assert res == b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), CHANNELMAP) # noqa: F405
    assert res != b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), UID) # noqa: F405
    assert res != b'\x00\x00'

    res = bitwise_and_bytes(bytes(b'\x00\x8d'), MILLISDURATION) # noqa: F405
    assert res != b'\x00\x00'