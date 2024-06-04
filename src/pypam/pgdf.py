""" Reading data from the PAMGuard binary pgdf file.

This module contains the following:
    - PGDF - The PGDF class representing a PGDF file
    
Examples:

    >>> from pypam.pgdf import PGDF
    >>> pgdf_path = 'test.pgdf'
    >>> assert os.path.exists(pgdf_path)
    >>> pgdf = PGDF(pgdf_path)

"""

__all__ = ["PGDF"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import struct
from pypam.module import ModuleHeader, ModuleFooter, PGObject, PGModule
from pypam.gemini import GeminiData
from pypam.pamdata import PAMData
from pypam.file import FileHeader, FileFooter


class PGDF:
    """The top structure for the PAMGuard binary file. Contains
    a header, footer and a number of modules."""

    def __init__(self, pgdf_path):
        """Initialise our PGDF object. This will read the entire
        binary file into memory at initialisation time.

        Args:
            pgdf_path (str): full path and name of the pgdf file.
        """
        # TODO - can we have multiple modules or not?
        # TODO - potentially __enter__ and __exit__?
        self.module = None

        with open(pgdf_path, "rb") as f:
            dat = f.read()
            ds = 0

            while ds < len(dat):
                # Read the two integers, length and type
                # These two are common to all but we just want to check
                # the type and length first
                self.length = struct.unpack(">i", dat[ds : ds + 4])[0]
                rec_type = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]

                # The following are the datatypes we might have in this record
                if rec_type == -1:
                    # File Header
                    self.header = FileHeader(dat, ds)
                    ds += len(self.header)

                elif rec_type == -2:
                    # FileFooter
                    # Get the leading digit on the version number string.
                    self.footer = FileFooter(self.header.file_version, dat, ds)
                    ds += len(self.footer)

                elif rec_type == -3:
                    # Module Header - lets start a new module
                    # Get the leading digit on the version number string.
                    module_header = ModuleHeader(dat, ds)
                    self.module = PGModule(module_header)
                    ds += len(module_header)

                elif rec_type == -4:
                    # Module Footer
                    module_footer = ModuleFooter(dat, ds)
                    assert self.module is not None
                    self.module.add_footer(module_footer)
                    ds += len(module_footer)

                elif rec_type == -5:
                    # Data
                    print("Unsupported rec type -5")
                    assert False

                else:
                    file_version = self.header.file_version
                    PAM_data = PAMData(dat, ds, file_version)
                    ds += len(PAM_data)

                    if PAM_data.is_background:
                        # TODO - some module_types are background not data
                        print("Read Background not yet implemented")
                        return

                    # Now read the rest of the module
                    # Now make a decision based on what data is inside
                    # this particular file
                    if self.header.module_type == "AIS Processing":
                        print("Not yet implemented")
                        raise NotImplementedError
                        return
                    elif (
                        self.header.module_type == "Click Detector"
                        or self.header.module_type == "SoundTrap Click Detector"
                    ):
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "Clip Generator":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "Deep Learning Classifier":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "DbHt":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "DIFAR Processing":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "LTSA":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif (
                        self.header.module_type == "Noise Monitor"
                        or self.header.module_type == "Noise Band"
                    ):
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "NoiseBand":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "RW Edge Detector":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "WhistlesMoans":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "Ipi module":
                        print("Not yet implemented")
                        raise NotImplementedError
                    elif self.header.module_type == "Gemini Threshold Detector":
                        # print("Loading Gemini")
                        data = GeminiData(dat, ds)
                        # print ("Gemini Length", len(data))
                        ds += len(data)
                        # Create the object then add to the module
                        pam_object = PGObject(PAM_data, data)
                        assert self.module is not None
                        self.module.add_object(pam_object)

                    else:
                        print("Unknown module type", self.header.module_type)
                        raise NotImplementedError

                    # Now see if there are any binary annotations on PAMData
                    len_anno = PAM_data.read_annotations(dat, ds)
                    # ds += len_anno

                    ds = PAM_data._next_obj

    def __len__(self):
        """Return the length of our object in bytes

        Returns:
            int: the number of bytes long this object is.
        """
        return self.length

    def __str__(self):
        return (
            "Header:"
            + str(self.header)
            + ":Footer:"
            + str(self.footer)
            + ":Length:"
            + str(self.__len__())
        )
