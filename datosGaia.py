# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:53:03 2022

@author: Abrah
"""

from astroquery.gaia import Gaia


def solicitaDatosGaia(x1,x2,y1,y2, n=2000):
    if x1 != x2 and y1 != y2:
        job = Gaia.launch_job(f"SELECT Top {n} ra, dec, teff_val "
                          "from gaiadr2.gaia_source "
                          "WHERE ( "
                          f"(ra BETWEEN {x1} AND {x2} AND dec BETWEEN {y1} AND {y2} AND teff_val > 0) "
                          ")")
        
        print(job.get_results())
        
        return job.get_results()
        
    
if __name__=="__main__":
    solicitaDatosGaia(1,2,3,4)