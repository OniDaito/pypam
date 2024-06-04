""" The Gemini Data - tracks recorded by the Tritech sonar and 
subsequently annotated.

"""

__all__ = ["GeminiData"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"

import struct
import datetime
from pypam.util.time import epoch


class TrackPoint:
    """A point in the track."""

    def __init__(
        self,
        tmillis: int,
        sonar_id: int,
        minb: float,
        maxb: float,
        peakb: float,
        minr: float,
        maxr: float,
        peakr: float,
        objsize: float,
        occ: float,
        avgv: int,
        totalv: int,
        maxv: int,
    ):
        self.time = epoch(zone="UTC") + datetime.timedelta(milliseconds=tmillis)
        self.sonar_id = sonar_id
        self.min_bearing = minb
        self.max_bearing = maxb
        self.peak_bearing = peakb
        self.min_range = minr
        self.max_range = maxr
        self.peak_range = peakr
        self.obj_size = objsize
        self.occupancy = occ
        self.average_value = avgv
        self.total_value = totalv
        self.max_value = maxv

    def __str__(self):
        return (
            str(self.time)
            + ","
            + str(self.sonar_id)
            + ","
            + str(self.min_bearing)
            + ","
            + str(self.max_bearing)
            + ","
            + str(self.peak_bearing)
            + ","
            + str(self.min_range)
            + ","
            + str(self.max_range)
            + ","
            + str(self.peak_range)
            + ","
            + str(self.obj_size)
            + ","
            + str(self.occupancy)
            + ","
            + str(self.average_value)
            + ","
            + str(self.total_value)
            + ","
            + str(self.max_value)
        )


class Track:
    """A class that holds all the points of a track."""

    def __init__(self):
        self.points = []
        self.time_start = epoch(zone="UTC")
        self.time_end = epoch(zone="UTC")

    def add_point_from_dat(self, dat, offset) -> int:
        # TODO - possibly set this with underscore for internal function
        ds = offset
        time_millis = struct.unpack(">q", dat[ds : ds + 8])[0]
        sonar_id = struct.unpack(">h", dat[ds + 8 : ds + 10])[0]
        min_bearing = struct.unpack(">f", dat[ds + 10 : ds + 14])[0]
        max_bearing = struct.unpack(">f", dat[ds + 14 : ds + 18])[0]
        peak_bearing = struct.unpack(">f", dat[ds + 18 : ds + 22])[0]
        min_range = struct.unpack(">f", dat[ds + 22 : ds + 26])[0]
        max_range = struct.unpack(">f", dat[ds + 26 : ds + 30])[0]
        peak_range = struct.unpack(">f", dat[ds + 30 : ds + 34])[0]
        obj_size = struct.unpack(">f", dat[ds + 34 : ds + 38])[0]
        occupancy = struct.unpack(">f", dat[ds + 38 : ds + 42])[0]
        average_value = struct.unpack(">h", dat[ds + 42 : ds + 44])[0]
        total_value = struct.unpack(">i", dat[ds + 44 : ds + 48])[0]
        max_value = struct.unpack(">h", dat[ds + 48 : ds + 50])[0]

        if len(self.points) == 0:
            self.time_start += datetime.timedelta(milliseconds=time_millis)
            self.time_end += datetime.timedelta(milliseconds=time_millis)
        else:
            self.time_end = epoch(zone="UTC") + datetime.timedelta(
                milliseconds=time_millis
            )

        self.points.append(
            TrackPoint(
                time_millis,
                sonar_id,
                min_bearing,
                max_bearing,
                peak_bearing,
                min_range,
                max_range,
                peak_range,
                obj_size,
                occupancy,
                average_value,
                total_value,
                max_value,
            )
        )

        # Sort points by time going forward. Useful later
        self.points = sorted(self.points, key=lambda point: point.time)

        return 50

    def __len__(self):
        return self.track_length

    def __str__(self):
        s = "["

        for p in self.points:
            s += "(" + str(p) + "),"

        s = s[:-1]
        s += "]"
        return s


class GeminiData:
    """A class representing a track from the Tritech Gemini sonar
    that has been annoted by the user."""

    def __init__(self, dat, offset):
        ds = offset
        self.data_length = struct.unpack(">i", dat[ds : ds + 4])[0]
        self.num_points = struct.unpack(">i", dat[ds + 4 : ds + 8])[0]
        self.num_sonar = struct.unpack(">b", dat[ds + 8 : ds + 9])[0]
        self.sonar_ids = []
        ds += 9

        for i in range(self.num_sonar):
            self.sonar_ids.append(struct.unpack(">h", dat[ds : ds + 2])[0])
            ds += 2

        self.straight_length = struct.unpack(">f", dat[ds : ds + 4])[0]
        self.wobbly_length = struct.unpack(">f", dat[ds + 4 : ds + 8])[0]
        self.mean_occupancy = struct.unpack(">f", dat[ds + 8 : ds + 12])[0]
        ds += 12

        # print("Nums",self.data_length, self.num_points, self.num_sonar, self.sonar_ids, self.straight_length, self.wobbly_length, self.mean_occupancy)

        self.track = Track()

        for i in range(self.num_points):
            rec_size = self.track.add_point_from_dat(dat, ds)
            ds += rec_size

        self.length = ds - offset

    def __len__(self):
        return self.length

    def __str__(self):
        return (
            str(self.length)
            + ","
            + str(self.data_length)
            + ","
            + str(self.num_points)
            + ","
            + str(self.num_sonar)
            + ","
            + str(self.sonar_ids)
            + ","
            + str(self.straight_length)
            + ","
            + str(self.wobbly_length)
        )
