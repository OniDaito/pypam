""" The part of the data common to all the PAM Data types.

"""

__all__ = ["PAMData"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import datetime
import struct
from pypam.annotations import Annotations
from pypam.util.time import epoch
from pypam.util.byteops import bitwise_and_bytes

TIMEMILLIS = bytes(b"\x00\x01")
TIMENANOS = bytes(b"\x00\x02")
CHANNELMAP = bytes(b"\x00\x04")
UID = bytes(b"\x00\x08")
STARTSAMPLE = bytes(b"\x00\x10")
SAMPLEDURATION = bytes(b"\x00\x20")
FREQUENCYLIMITS = bytes(b"\x00\x40")
MILLISDURATION = bytes(b"\x00\x80")
TIMEDELAYSECS = bytes(b"\x01\x00")
HASBINARYANNOTATIONS = bytes(b"\x02\x00")
HASSEQUENCEMAP = bytes(b"\x04\x00")
HASNOISE = bytes(b"\x08\x00")
HASSIGNAL = bytes(b"\x10\x00")
HASSIGNALEXCESS = bytes(b"\x20\x00")


class PAMData:
    def __init__(self, dat: bytes, offset: int, file_version: int):
        self.length = 0
        self.identifier = 0
        self.is_background = False
        self.millis = 0
        self.flag_bitmap = 0
        self.time_nanos = 0
        self.channel_map = 0
        self.UID = 0
        self.start_sample = 0
        self.sample_duration = 0
        self.freq_limits = [0, 0]
        self.duration_millis = 0
        self.num_time_delays = 0
        self.time_delays = []
        self.sequence_map = 0
        self.has_annotations = False
        self.anno_length = 0
        self.annotations = None
        self.noise = 0
        self.signal = 0
        self.signal_excess = 0
        self.date = epoch(zone="GMT")  # TODO - BST didn't work in Windows

        # We have to provide big endian here weirdly otherwise it doesn't work :/
        ds = offset
        binary_length = struct.unpack(">i", dat[ds : ds + 4])[0]
        self.identifier = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        self._next_obj = (
            offset + binary_length
        )  # Next object in case there is an error reading this one
        ds += 8

        self.is_background = self.identifier == -6
        self.millis = struct.unpack(">q", dat[ds : ds + 8])[0]
        self.date += datetime.timedelta(milliseconds=self.millis)
        ds += 8

        if file_version >= 3:
            self.flag_bitmap = dat[ds : ds + 2]
            ds += 2

        if (
            file_version == 2
            or bitwise_and_bytes(self.flag_bitmap, TIMENANOS) != b"\x00\x00"
        ):
            self.time_nanos = struct.unpack(">q", dat[ds : ds + 8])[0]
            ds += 8

        if (
            file_version == 2
            or bitwise_and_bytes(self.flag_bitmap, CHANNELMAP) != b"\x00\x00"
        ):
            self.channel_map = struct.unpack(">i", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, UID) != b"\x00\x00":
            self.UID = struct.unpack(">q", dat[ds : ds + 8])[0]
            ds += 8

        if bitwise_and_bytes(self.flag_bitmap, STARTSAMPLE) != b"\x00\x00":
            self.sample_duration = struct.unpack(">i", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, SAMPLEDURATION) != b"\x00\x00":
            self.sample_duration = struct.unpack(">i", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, FREQUENCYLIMITS) != b"\x00\x00":
            self.freq_limits[0] = struct.unpack(">f", dat[ds : ds + 4])[0]
            self.freq_limits[1] = struct.unpack(">f", dat[ds + 4 : ds + 8])[0]
            ds += 8

        if bitwise_and_bytes(self.flag_bitmap, MILLISDURATION) != b"\x00\x00":
            self.duration_millis = struct.unpack(">f", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, TIMEDELAYSECS) != b"\x00\x00":
            self.num_time_delays = struct.unpack(">h", dat[ds : ds + 2])[0]
            ds += 2

            for i in range(self.num_time_delays):
                self.time_delays.append(struct.unpack(">f", dat[ds : ds + 4])[0])
                ds += 4

        if bitwise_and_bytes(self.flag_bitmap, HASSEQUENCEMAP) != b"\x00\x00":
            self.sequence_map = struct.unpack(">i", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, HASNOISE) != b"\x00\x00":
            self.noise = struct.unpack(">f", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, HASSIGNAL) != b"\x00\x00":
            self.duration_millis = struct.unpack(">f", dat[ds : ds + 4])[0]
            ds += 4

        if bitwise_and_bytes(self.flag_bitmap, HASSIGNALEXCESS) != b"\x00\x00":
            self.signal_excess = struct.unpack(">f", dat[ds : ds + 4])[0]
            ds += 4

        self.length = ds - offset

    def read_annotations(self, dat, offset) -> int:
        """Called at the end of the Module - read any annotations
        we might have, return how far we've read along."""
        if bitwise_and_bytes(self.flag_bitmap, HASBINARYANNOTATIONS) != b"\x00\x00":
            self.has_annotations = True
            self.annotations = Annotations(dat, offset)
            return len(self.annotations)

        return 0

    def __len__(self):
        return self.length

    def __str__(self):
        return (
            str(self.length)
            + ","
            + str(self.identifier)
            + ","
            + str(self.is_background)
            + ","
            + str(self.millis)
            + ","
            + str(self.flag_bitmap)
            + ","
            + str(self.time_nanos)
            + ","
            + str(self.channel_map)
            + ","
            + str(self.UID)
            + ","
            + str(self.start_sample)
            + ","
            + str(self.sample_duration)
            + ",("
            + str(self.freq_limits[0])
            + ","
            + str(self.freq_limits[1])
            + "),"
            + str(self.duration_millis)
            + ","
            + str(self.num_time_delays)
            + ",["
            + ",".join([str(i) for i in self.time_delays])
            + "],"
            + str(self.sequence_map)
            + ","
            + str(self.noise)
            + ","
            + str(self.signal)
            + ","
            + str(self.signal_excess)
            + ","
            + str(self.has_annotations)
            + ","
            + str(self.date)
        )
