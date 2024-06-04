""" Print information from a PGDF
Example usage:
    
"""

import os
import sys
import math
from pypam.pgdf import PGDF


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="pgdfinfo",
        description="Print information from a PGDF file",
        epilog="SMRU St Andrews",
    )

    parser.add_argument("filename")
    args = parser.parse_args()
    assert os.path.exists(args.filename)
    p = PGDF(args.filename)

    print("PGDF Length:", p.length)
    print("Num Module Objects:", len(p.module.objects))

    for pamobj in p.module.objects:
        tdate = pamobj.pam.date
        assert(tdate is not None)
        print("Object Date:", tdate)

    print("Tracks")

    tracks = []
    assert p.header.module_type == "Gemini Threshold Detector"

    for obj in p.module.objects:
        tracks.append(obj)

    # Sort tracks in order of time if not already
    tracks = sorted(tracks, key=lambda track: track.data.track.time_start)
    
    ids = [1861000198, 1861000199, 1861000200, 1861000201, 1861000202]

    for track in tracks:
        if track.pam.UID in ids:
            print(track.pam.UID, track.data.track)
