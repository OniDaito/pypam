# PyPAM

A python interface to [PAMGuard](https://www.pamguard.org/), covering the Gemini AAM module. 

Documentation is available at [https://onidaito.github.io/pypam](https://onidaito.github.io/pypam)

## Installation

At present, PyPAM is not part of Pip or any other distribution mechanism. To use this library in your own python program we recommend including it as part of a python virtual environment. You can install pypam inside such an environment as follows:

    pip install git+https://github.com/onidaito/pypam.git

or locally
    
    pip install <path to pypam>

## Getting started

Once installed, you can begin to read PAMGuard pgdf files as follows:

    from pypam.pgdf import PGDF 
    import os
 
    def test_glf():
        pgdf_path = "pamguard.pgdf"
        assert os.path.exists(pgdf_path)
  
        pgdf = PGDF(pgdf_path)
        print("PGDF Summary")

## Documentation

The documentation can be generated using mkdocs as follows:

    mkdocs build

Documentation is available at [https://onidaito.github.io/pypam](https://onidaito.github.io/pypam)

## Tests
In order to run the various tests you will need the test data files, which are held in a separate repository - [https://github.com/OniDaito/pypam_testdata](https://github.com/OniDaito/pypam_testdata).

With the submodule updated, run the following from the pypam directory:

    pytest

## Support
For support, please email Benjamin Blundell - bjb8@st-andrews.ac.uk

## Licence
Licenced under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
