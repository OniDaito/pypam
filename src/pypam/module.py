""" The module headers and footers for the
PAMGuard binary files."""

__all__ = ["ModuleHeader", "ModuleFooter", "PGModule", "PGObject"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import struct
from .pamdata import PAMData


class PGObject:
    """Each module has a number of objects - records - in the
    data block. The data will be a particular object such as
    tritech data, or sound data and will differ. The PamData is
    always a PAMData object."""

    def __init__(self, pam_data: PAMData, data):
        self.pam = pam_data
        self.data = data

    def __str__(self):
        return "pgobject:" + str(self.pam)


class PGModule:
    """The binary file has a module inside it (maybe more than one?)
    containing a header, footer and a number of objects."""

    def __init__(self, header):
        self.header = header
        self.objects = []
        self.footer = None

    def add_footer(self, footer):
        self.footer = footer

    def add_object(self, obj: PGObject):
        self.objects.append(obj)

    def __len__(self):
        return len(self.objects)

    def __str__(self):
        return str(self.header) + "," + str(self.footer)


class ModuleHeader:
    """The header for each PAMGuard module inside the pgdf."""

    def __init__(self, dat: bytes, offset: int):
        ds = offset
        # There is a module header first
        self.length = struct.unpack(">i", dat[ds : ds + 4])[0]
        self.identifier = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        self.version = struct.unpack(">i", dat[ds + 8 : ds + 12])[0]
        self.binary_length = struct.unpack(">i", dat[ds + 12 : ds + 16])[0]
        ds += 16
        self.length = ds - offset

    def __len__(self):
        return self.length

    def __str__(self):
        return (
            str(self.length)
            + ","
            + str(self.identifier)
            + ","
            + str(self.version)
            + ","
            + str(self.binary_length)
        )


class ModuleFooter:
    """The footer for each PAMGuard module inside the pgdf."""

    def __init__(self, dat: bytes, offset: int):
        ds = offset
        # There is a module header first
        self.length = struct.unpack(">i", dat[ds : ds + 4])[0]
        self.identifier = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        self.binary_length = struct.unpack(">i", dat[ds + 8 : ds + 12])[0]

    def __len__(self):
        return self.length

    def __str__(self):
        return (
            str(self.length)
            + ","
            + str(self.identifier)
            + ","
            + str(self.binary_length)
        )
