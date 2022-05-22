# -*- coding: utf-8 -*-
"""
Created on Sat May 21 20:45:28 2022

@author: Abrah
"""
import pandas as pd

def lecturaCatalogoM(ruta):
    datos=pd.read_csv("MessierCatalogList.csv", sep=",", encoding="utf-8")
    
    Ms=[]
    for i,j,k in zip(datos["RA"], datos["DEC"], datos["SIZE"]):
        Ms.append((i,j,k))
        
    return Ms
    
    
if __name__=="__main__":
    print(len(lecturaCatalogoM("")))