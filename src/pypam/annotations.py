""" Called when reading the PAMData from the pgdf file.
If annotations exist, we read them from the binary file 
and add them to the end of the pgdf.

This module contains the following:

    - BeamAnglesAnno
    - BearingAnno
    - TDBLAnno
    - ClickClasssifier1Anno
    - MatchedClkClsfrAnno
    - BasicClassificationAnno
    - DLClassificationAnno
    - UserFormAnno
    - TargetMotionAnno
    - Annotations

"""

__all__ = [
    "BeamAnglesAnno",
    "BearingAnno",
    "TDBLAnno",
    "ClickClasssifier1Anno",
    "MatchedClkClsfrAnno",
    "BasicClassificationAnno",
    "DLClassificationAnno",
    "UserFormAnno",
    "TargetMotionAnno",
    "Annotations",
]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import struct
from pypam.util.read import read_java_string


class Location:
    """Held inside the Target motion annotation."""

    def __init__(self, lat, lon, height, error):
        self.latitude = lat
        self.longitude = lon
        self.height = height
        self.error = error


class BeamAnglesAnno:
    def __init__(self, dat: bytes, offset: int):
        ds = offset
        self.hydrophones = struct.unpack(">I", dat[ds : ds + 4])[0]
        self.array_type = struct.unpack(">h", dat[ds + 4 : ds + 6])[0]
        self.localisation_content = struct.unpack(">I", dat[ds + 6 : ds + 10])[0]
        self.num_angles = struct.unpack(">h", dat[ds + 10 : ds + 12])[0]
        ds += 12
        self.angles = []

        for i in range(self.num_angles):
            self.angles.append(struct.unpack(">f", dat[ds : ds + 4])[0])
            ds += 4

        self.length = ds - offset

    def __len__(self):
        return self.length


class BearingAnno:
    def __init__(self, dat: bytes, offset: int, anno_ver: int):
        ds = offset
        name, dv = read_java_string(dat, ds)
        ds += dv
        self.algorithm_name = name
        self.version = anno_ver
        self.hydrophones = struct.unpack(">I", dat[ds : ds + 4])[0]
        self.array_type = struct.unpack(">h", dat[ds + 4 : ds + 6])[0]
        self.localisation_content = struct.unpack(">I", dat[ds + 6 : ds + 10])[0]
        self.num_angles = struct.unpack(">h", dat[ds + 10 : ds + 12])[0]
        self.angles = []
        ds += 12

        for i in range(self.num_angles):
            self.angles.append(struct.unpack(">f", dat[ds : ds + 4])[0])
            ds += 4

        self.errors = []
        self.num_errors = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2

        for i in range(self.num_errors):
            self.errors.append(struct.unpack(">f", dat[ds : ds + 4])[0])
            ds += 4

        if anno_ver >= 2:
            self.ref_angles = []
            self.num_ref_angles = struct.unpack(">h", dat[ds : ds + 2])[0]
            ds += 2

            for i in range(self.num_ref_angles):
                self.ref_angles.append(struct.unpack(">f", dat[ds : ds + 4])[0])
                ds += 4

        self.length = ds - offset

    def __len__(self):
        return self.length


class TDBLAnno:
    def __init__(self, dat: bytes, offset: int):
        ds = offset
        self.num_angles = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2
        self.angles = []

        for i in range(self.num_angles):
            self.angles.append(struct.unpack(">f", dat[ds : ds + 4])[0])
            ds += 4

        self.num_errors = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2
        self.angle_errors = []

        for i in range(self.num_errors):
            self.angle_errors.append(struct.unpack(">f", dat[ds : ds + 4])[0])
            ds += 4

        self.length = ds - offset

    def __len__(self):
        return self.length


class ClickClasssifier1Anno:
    def __init__(self, dat: bytes, offset: int):
        ds = offset
        self.num_classifications = struct.unpack(">h", dat[ds : ds + 2])[0]
        ds += 2
        self.classifications = []

        for i in range(self.num_errors):
            self.classifications.append(struct.unpack(">h", dat[ds : ds + 2])[0])
            ds += 2

        self.length = ds - offset

    def __len__(self):
        return self.length


class MatchedClkClsfrAnno:
    def __init__(self, dat: bytes, offset: int, anno_ver: int):
        ds = offset

        if anno_ver == 1:
            self.threshold = struct.unpack(">d", dat[ds : ds + 8])[0]
            self.match_corr = struct.unpack(">d", dat[ds + 8 : ds + 16])[0]
            self.reject_corr = struct.unpack(">d", dat[ds + 16 : ds + 24])[0]
            ds += 24

        elif anno_ver == 2:
            self.num_templates = struct.unpack(">h", dat[ds : ds + 2])[0]
            ds += 2

            # Tuple of threshold, match_corr and reject_corr
            self.templates = []

            for i in range(self.num_templates):
                threshold = struct.unpack(">d", dat[ds : ds + 8])[0]
                match_corr = struct.unpack(">d", dat[ds + 8 : ds + 16])[0]
                reject_corr = struct.unpack(">d", dat[ds + 16 : ds + 24])[0]
                ds += 24
                self.templates.append((threshold, match_corr, reject_corr))

        self.length = ds - offset

    def __len__(self):
        return self.length


class BasicClassificationAnno:
    def __init__(self, dat: bytes, offset: int):
        ds = offset
        self.label, dv = read_java_string(dat, ds)
        ds += dv
        self.method, dv = read_java_string(dat, ds)
        ds += dv
        self.score = struct.unpack(">f", dat[ds : ds + 4])[0]
        self.length = ds - offset

    def __len__(self):
        return self.length


class DLClassificationAnno:
    def __init__(self, dat: bytes, offset: int):
        ds = offset
        self.num_models = struct.unpack(">h", dat[ds : ds + 2])[0]
        self.models = []

        for i in range(self.num_models):
            model = {}
            model_type = dat[ds : ds + 1]
            is_binary = struct.unpack("?", dat[ds + 1 : ds + 2])[0]
            scale = struct.unpack(">f", dat[ds + 2 : ds + 6])[0]
            num_species = struct.unpack(">h", dat[ds + 6 : ds + 8])[0]
            species = []
            ds += 8

            for i in range(num_species):
                s = struct.unpack(">h", dat[ds : ds + 2])[0] / scale
                species.append(s)
                ds += 2

            num_classes = struct.unpack(">h", dat[ds : ds + 2])[0]
            classnames = []

            for i in range(num_classes):
                s = struct.unpack(">h", dat[ds : ds + 2])[0]
                classnames.append(s)
                ds += 2

            # Dummy result
            model["predictions"] = []
            model["type"] = "dummy"
            model["class_id"] = 0
            model["is_binary"] = False

            if model_type == 0 or model_type == 1:
                model["predictions"] = species
                model["type"] = model_type
                model["class_id"] = classnames
                model["is_binary"] = is_binary

            self.models.append(model)

        self.length = ds - offset

    def __len__(self):
        return self.length


class UserFormAnno:
    def __init__(self, dat: bytes, offset: int, anno_id_len: int, an_len: int):
        ds = offset
        txt_length = an_len - anno_id_len - 4
        self.form_data = str(dat[ds : ds + txt_length], "utf-8")
        self.length = txt_length

    def __len__(self):
        return self.length


class TargetMotionAnno:
    def __init__(self, dat: bytes, offset: int):
        ds = offset
        self.name, dv = read_java_string(dat, ds)
        ds += dv
        self.num_locations = struct.unpack(">h", dat[ds : ds + 2])[0]
        self.hydrophones = struct.unpack(">I", dat[ds + 2 : ds + 6])[0]
        self.locations = []

        for i in range(self.num_locations):
            lat = struct.unpack(">d", dat[ds : ds + 8])[0]
            lon = struct.unpack(">d", dat[ds + 8 : ds + 16])[0]
            h = struct.unpack(">f", dat[ds + 16 : ds + 20])[0]
            ds += 20

            error_str, dv = read_java_string(dat, ds)
            ds += dv

            loc = Location(lat, lon, h, error_str)
            self.locations.append(loc)

        self.length = ds - offset

    def __len__(self):
        return self.length


class Annotations:
    """The Annotations section of the PAMData. This part comes
    at the end of the file before the footer and may or may not
    be filled in."""

    def __init__(self, dat: bytes, offset: int):
        self.beam_angles = None
        self.bearing = None
        self.target_motion = None
        self.toad_angles = None
        self.classification = None
        self.m_classification = None
        self.basic_classification = None
        self.dl_classification = None
        self.user_form_data = None
        self.length = 0
        ds = offset
        self.anno_length = struct.unpack(">h", dat[ds : ds + 2])[0]
        num_anno = struct.unpack(">h", dat[ds + 2 : ds + 4])[0]
        ds += 4

        for i in range(num_anno):
            anno_length = (
                struct.unpack(">h", dat[ds : ds + 2])[0] - 2
            )  # does not include the length field
            ds += 2

            # Read in a string
            anno_id, dv = read_java_string(dat, ds)
            ds += dv

            anno_ver = struct.unpack(">h", dat[ds : ds + 2])[0]
            ds += 2

            # Decide on the annotation type
            if anno_id == "Beer":
                self.beam_angles = BeamAnglesAnno(dat, ds)
                ds += len(self.beam_angles)

            elif anno_id == "Bearing":
                self.bearing = BearingAnno(dat, ds, anno_ver)
                ds += len(self.bearing)

            elif anno_id == "TMAN":
                self.target_motion = TargetMotionAnno(dat, ds)
                ds += len(self.target_motion)

            elif anno_id == "TDBL":
                self.TDBL = TDBLAnno(dat, ds)
                ds += len(self.TDBL)

            elif anno_id == "ClickClasssifier_1":
                self.click_classsifier_1 = ClickClasssifier1Anno(dat, ds)
                ds += len(self.click_classsifier_1)

            elif anno_id == "Matched_Clk_Clsfr":
                self.matched_clk_clsfr = MatchedClkClsfrAnno(dat, ds)
                ds += len(self.matched_clk_clsfr)

            elif anno_id == "BCLS":
                self.basic_classification = BasicClassificationAnno(dat, ds)
                ds += len(self.basic_classification)

            elif anno_id == "DLRE" or anno_id == "Delt":
                self.dl_classification = DLClassificationAnno(dat, ds)
                ds += len(self.dl_classification)

            elif anno_id == "Uson" or anno_id == "USON":
                self.dl_classification = UserFormAnno(
                    dat, ds, len(anno_id), anno_length
                )
                ds += len(self.dl_classification)

    def __len__(self):
        return self.length
