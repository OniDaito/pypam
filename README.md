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
In order to run the various tests you will need the test data files, which are held in a separate repository - [https://gitlab.st-andrews.ac.uk/biology/smru/bjb8/pypam_testdata](https://gitlab.st-andrews.ac.uk/biology/smru/bjb8/pypam_testdata). These are a few megabytes in size.

You will need to install the git lfs extension for large data files first. Follow the instructions at [https://git-lfs.com/](https://git-lfs.com/).

To download these into an existing pypam directory, use git as follows:

    git submodule update --init --recursive

With the submodule updated, run the following from the pypam directory:

    pytest

## Support
For support, please email Benjamin Blundell - bjb8@st-andrews.ac.uk

## Roadmap

- Complete support for all data types and modules that PAMGuard supports.
- Improved documentation and test coverage.

## Authors
Benjamin Blundell

## Licence
Licenced under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
