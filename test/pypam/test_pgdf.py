""" Tests for the PGDF data."""

from pypam.pgdf import PGDF 
import os
from PIL import Image


def test_glf():
    pgdf_path = "./pypam_testdata/Gemini_Threshold_Detector_Gemini_Threshold_Detector_Sonar_Tracks_20220722_000004.pgdf"
    assert os.path.exists(pgdf_path)
  
    pgdf = PGDF(pgdf_path)
    print("PGDF Summary")
    print(pgdf)
    print("First Track Info")
    print(pgdf.module.objects[0].data)
    print("First Track Points")
    print(pgdf.module.objects[0].data.track)
    print("Identifier", pgdf.header.identifier)