# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:10:32 2022

@author: Abrah
"""
import pandas as pd

dh=15
dm=1/60
ds=1/3600

conv={"h":dh,"m":dm,"s":ds}

def tiempoaGrados(cadena, tipo = "hms"):
    cadena=cadena.replace("°", "h").replace("''","s").replace("′", "m").replace("″", "s").replace("'", "m")
    
    cadena=cadena.replace(u"\xa0",u" ")
    cadena=cadena.split(" ")
    
    h,m,s=[0],[0],[0]
    vals={"h":h,"m":m,"s":s}
    i=0
    
    for val in cadena:
        llaves=list(vals.keys())
        if val[-1].lower() in conv.keys():
            
            vals[val[-1].lower()][0]=float(val[0:-1])
            
        elif tipo == "hms":
            vals[llaves[i]][0]=float(val[0:])
            
        else:
            vals[tipo[i]][0]=float(val[0:])
            
        i+=1  
            
    d=h[0]*dh+m[0]*dm+s[0]*ds
    
    return d
        
        
if __name__=="__main__":
    #print(tiempoaGrados())
    
    h, m, s = [0],0,0
    
    #with open("constelaciones/Hydra.csv", "r", encoding="utf-16") as archivo:
    datos=pd.read_csv("constelaciones/Andromeda.csv", sep="\t", encoding="utf-16")
    #datos.close()
    print(tiempoaGrados(datos["RA"][0]))
        # llaves=next(datos)
        # print(llaves)