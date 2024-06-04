# Usage


## Reading the summary from a PGDF file

    from pypam.pgdf import PGDF 
    import os
 
    def test_glf():
        pgdf_path = "pamguard.pgdf"
        assert os.path.exists(pgdf_path)
  
        pgdf = PGDF(pgdf_path)
        print("PGDF Summary")
