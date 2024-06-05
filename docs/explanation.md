# Explanation

PyPAM contains a number of python functions for reading certain pieces of data generated by PAMGuard.

The functions are question are the ones required to extract data relating to the Tritech Gemini Sonars.

Only the *Gemini Threshold Detector* module is read from the PGDF file, along with the header and footer of said module.

The key elements we need from the PGDF include:

* The Tracks.
* The Points that make up the tracks.
* Annotations associated with tracks.


PyPAM is really just a small component of the much larger [sealhits](https://github.com/onidaito/sealhits) project.