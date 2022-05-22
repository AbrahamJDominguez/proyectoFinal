# -*- coding: utf-8 -*-

from astroquery.gaia import Gaia
from utilidades import tiempoaGrados
from lecturaArchivos import lecturaCatalogoM
import os


def solicitaDatosGaia(x1,x2,y1,y2, n=2000):
    if x1 != x2 and y1 != y2:
        job = Gaia.launch_job(f"SELECT Top {n} ra, dec, teff_val "
                          "from gaiadr2.gaia_source "
                          "WHERE ( "
                          f"(ra BETWEEN {x1} AND {x2} AND dec BETWEEN {y1} AND {y2} AND teff_val > 0) "
                          ")")
        
        #print(job.get_results().keys())
        
        return job.get_results()
    
def solicitaMessiersGaia(messier):
    print(messier)
    ra=tiempoaGrados(messier[0])
    dec=tiempoaGrados(messier[1])
    
    job="SELECT TOP 2000 "
    job+="gaia_source.source_id,gaia_source.ra, "
    job+="gaia_source.dec, gaia_source.parallax, gaia_source.radius_val, "
    job+="gaia_source.phot_g_mean_mag, "
    job+="gaia_source.bp_rp,gaia_source.radial_velocity, "
    job+="gaia_source.teff_val "
    job+="FROM gaiadr2.gaia_source "
    
    if "x" in messier[2]:
        datos=messier[2].split("x")
        alt=float(datos[0])/60
        anc=float(datos[1])/60

        job+="WHERE "
        job+="CONTAINS( "
        job+="POINT('ICRS',gaiadr2.gaia_source.ra,gaiadr2.gaia_source.dec), "
        job+=f"BOX('ICRS',{ra},{dec},{anc},{alt})"
        job+=" )=1"
        
    else:
        r=float(messier[2])/60
        
        job+="WHERE "
        job+="CONTAINS( "
        job+="POINT('ICRS',gaiadr2.gaia_source.ra,gaiadr2.gaia_source.dec), "
        job+=f"CIRCLE('ICRS',{ra},{dec},{r})"
        job+=" )=1"
        
    
    job=Gaia.launch_job(job)
    
    
    return job.get_results()

def trabajoaCsv():
    pass
        
    
if __name__=="__main__":
    solicitaDatosGaia(1,2,3,4)
    
    messiers=lecturaCatalogoM("")
    #print(messiers)
    
    ruta="messiersGaia"
    
    if not os.path.isdir(ruta):
        os.makedirs(ruta)
    
    for m in range(len(messiers)):
        if not os.path.isfile(f"messiersGaia/M{m+1}.csv"):
            tabla=solicitaMessiersGaia(messiers[m])
            tabla.write(f"messiersGaia/M{m+1}.csv", format="ascii.csv")
        
    # print(f"SELECT Top {n} ra, dec, teff_val "
    #                   "from gaiadr2.gaia_source "
    #                   "WHERE ( "
    #                   f"(ra BETWEEN {x1} AND {x2} AND dec BETWEEN {y1} AND {y2} AND teff_val > 0) "
    #                   ")")