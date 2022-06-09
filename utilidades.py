# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:10:32 2022

@author: Abrah
"""
import pandas as pd

dd=1
dh=15
dm=1/60
ds=1/3600

conv={"h":dh,"m":dm,"s":ds,"d":dd}

#def tiempoaGrados(cadena, tipo = "dec"):
def tiempoaGrados(cadena, tipo="dec"):
    neg=False
    esc=1
    
    cadena=str(cadena)
    
    cadena=cadena.replace(u"\xa0",u" ")
    
    if cadena[0] == "-":
        neg=True
        cadena=cadena.replace("-", "")
        
    #if " " not in cadena and (len(cadena.split("°")) >= 2 or len(cadena.split("h")) >= 2):
    if " " not in cadena:
        cadena=cadena.replace("°","° ").replace("m","m ").replace("h","h ").replace("'\"","m 30s").replace("'","' ")
        
    if "h" in cadena or tipo == "ra":
        esc=15

       
    cadena=cadena.replace("°", "d").replace("''","s").replace("′", "m").replace("″", "s").replace('"', "s").replace("'", "m")
    
    cadena=cadena.split(" ")
    
    while "" in cadena:
        cadena.remove("")
    
    h,m,s,d=[0],[0],[0],[0]
    vals={"h":h,"m":m,"s":s,"d":d}
    i=0
    
    for val in cadena:
        llaves=list(vals.keys())
        
        if val[-1].lower() in conv.keys():
            
            vals[val[-1].lower()][0]=float(val[0:-1])
            
            if i >= 1:
                vals[val[-1].lower()][0]*=esc
            
        elif tipo == "dec":
            
            if i == 0:
                vals["d"][0]=float(val[0:])
                
            else:
                vals[llaves[i]][0]=float(val[0:])*esc
                         
        else:
            esc=15
            vals[llaves[i]][0]=float(val[0:])
            
            if i >= 1:
                vals[llaves[i]][0]*=esc
            
        i+=1  
        
    
    d=h[0]*dh+m[0]*dm+s[0]*ds+d[0]
    
    if neg:
        d=-d
        
    return d

def isfloat(cadena):
    try:
        float(cadena)
        return True

    except:
        return False
        
        
if __name__=="__main__":
    #print(tiempoaGrados())
    
    h, m, s = [0],0,0
    
    #with open("constelaciones/Hydra.csv", "r", encoding="utf-16") as archivo:
    datos=pd.read_csv("constelaciones/Andromeda.csv", sep="\t", encoding="utf-16")
    #datos.close()
    print(tiempoaGrados("5h 34.5m", 'ra'))
    
    datos=pd.read_csv("MessierCatalogList.csv", sep=",", encoding="utf-8")
    
    print(datos["RA"])
        # llaves=next(datos)
        # print(llaves)