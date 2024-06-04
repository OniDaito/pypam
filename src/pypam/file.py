""" The file headers and footers for the
PAMGuard binary files.

This module contains the following:
    - FileHeader - A class that represents the Header of the PGDF File
    - FileFooter - A class that represents the Footer of the PGDF File
"""

__all__ = ["FileHeader", "FileFooter"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import struct
import datetime
from pypam.util.time import epoch


class FileHeader:
    """Appears at the beginning of the pgdf file. Should be the
    very first thing."""

    def __init__(self, dat: bytes, offset: int):
        ds = offset
        # There is a module header first
        self.length = struct.unpack(">i", dat[ds : ds + 4])[0]
        self.identifier = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        self.file_version = struct.unpack(">i", dat[ds + 8 : ds + 12])[0]
        self.pamguard = str(dat[ds + 12 : ds + 24], "utf-8")
        ds += 24
        dt = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2

        if dt > 0:
            self.pamguard_version = str(dat[ds : ds + dt], "utf-8")
            ds += dt
        else:
            self.pamguard_version = ""

        dt = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2

        if dt > 0:
            self.branch = str(dat[ds : ds + dt], "utf-8")
            ds += dt
        else:
            self.branch = ""

        # TODO - maybe round off milliseconds here as well
        dm = struct.unpack(">q", dat[ds : ds + 8])[0]
        self.data_date = epoch() + datetime.timedelta(milliseconds=dm)
        dm = struct.unpack(">q", dat[ds + 8 : ds + 16])[0]
        self.analysis_date = epoch() + datetime.timedelta(milliseconds=dm)
        dm = struct.unpack(">q", dat[ds + 16 : ds + 24])[0]
        self.start_sample = epoch() + datetime.timedelta(milliseconds=dm)
        ds += 24

        dt = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2

        if dt > 0:
            self.module_type = str(dat[ds : ds + dt], "utf-8")
            ds += dt
        else:
            self.module_type = ""

        dt = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2

        if dt > 0:
            self.module_name = str(dat[ds : ds + dt], "utf-8")
            ds += dt
        else:
            self.module_name = ""

        dt = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2

        if ds > 0:
            self.stream_name = str(dat[ds : ds + dt], "utf-8")
            ds += dt
        else:
            self.stream_name = ""

        self.extra_info_len = struct.unpack(">i", dat[ds : ds + 4])[0]
        ds += 4

        # TODO - There is an extra info bit but for now, we skip it
        ds += self.extra_info_len
        self.length = ds

    def __len__(self):
        return self.length

    def __str__(self):
        return (
            str(self.length)
            + ","
            + str(self.identifier)
            + ","
            + str(self.file_version)
            + ","
            + str(self.pamguard)
            + ","
            + str(self.pamguard_version)
            + ","
            + str(self.branch)
            + ","
            + str(self.data_date)
            + ","
            + str(self.analysis_date)
            + ","
            + str(self.start_sample)
            + ","
            + str(self.module_type)
            + ","
            + str(self.module_name)
            + ","
            + str(self.stream_name)
            + ","
            + str(self.extra_info_len)
            + ","
            + str(self.length)
        )


class FileFooter:
    def __init__(self, version, dat, offset):
        ds = offset
        self.length = struct.unpack(">i", dat[ds : ds + 4])[0]
        self.identifier = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        self.num_objects = struct.unpack(">i", dat[ds + 8 : ds + 12])[0]
        dm = struct.unpack(">q", dat[ds + 12 : ds + 20])[0]
        self.data_date = epoch() + datetime.timedelta(milliseconds=dm)
        dm = struct.unpack(">q", dat[ds + 20 : ds + 28])[0]
        self.analysis_date = epoch() + datetime.timedelta(milliseconds=dm)
        self.end_sample = struct.unpack(">q", dat[ds + 28 : ds + 36])[0]
        ds += 36

        self.lowest_UID = -1
        self.highest_UID = -1

        if version >= 3:
            self.lowest_UID = struct.unpack(">q", dat[ds : ds + 8])[0]
            self.highest_UID = struct.unpack(">q", dat[ds + 8 : ds + 16])[0]
            ds += 16

        self.file_length = struct.unpack(">q", dat[ds : ds + 8])[0]
        self.end_reason = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        ds += 8
        # self.length = ds

    def __str__(self):
        return (
            str(self.length)
            + ","
            + str(self.identifier)
            + ","
            + str(self.num_objects)
            + ","
            + str(self.data_date)
            + ","
            + str(self.end_sample)
            + ","
            + str(self.data_date)
            + ","
            + str(self.analysis_date)
            + ","
            + str(self.end_sample)
            + ","
            + str(self.lowest_UID)
            + ","
            + str(self.highest_UID)
            + ","
            + str(self.file_length)
            + ","
            + str(self.end_reason)
        )

    def __len__(self):
        return self.length
