# -*- coding: utf-8 -*-
"""
Created on Sat May 21 20:45:28 2022

@author: Abrah
"""
############ MODULO DE LECTURA DE ARCHIVOS ##############
import csv
import tkinter
from tkinter import filedialog
import pandas as pd
import os
import glob
import utilidades as Util

ruta="C:/Users/sandy/Documents/Pooye/proyectoFinal-main/"
#ruta = "C:/Users/cimen/Documents/POOE/proyectoFinal-main/"

""" Cambiar esta dirección a donde estén los archivos messiersGaia y constelaciones:"""
rutaMessiers="messiersGaia/"
rutaConste="constelaciones/"
#rutaMessiers = "C:/Users/cimen/Documents/POOE/proyectoFinal-main/messiersGaia/"
#rutaConste = "C:/Users/cimen/Documents/POOE/proyectoFinal-main/constelaciones/"


class lecturaArchivos:
    def __init__(self,ruta):
        self.ruta=ruta
        
    def inicializar(self):
        nombres=["MessierCatalogo", "pulsares", "planetas", "constelaciones", "estrellas_messier", "estrellasConste"]
        archivos={nombres[0]:["MessierCatalogList.csv",",","utf-8"], nombres[1]:["pulsar.csv","\t","utf-16"], 
                  nombres[2]:["Planetas.csv",",","utf-8"],nombres[3]:["constelaciones.csv","\t","utf-16"],
                  nombres[4]:["messiersGaia/",",","utf-8"],nombres[5]:["constelaciones/","\t","utf-16"]}
        name, sep, enc = [], [], []
        
        for arch in range(len(nombres)):
            name.append(archivos[nombres[arch]][0])
            sep.append(archivos[nombres[arch]][1])
            enc.append(archivos[nombres[arch]][2])
        
        return name, sep, enc
        
    def lecturaCatalogoM(self, name,sep,enc): # Objetos Messier
        cambioRA, cambioDEC, radio = [], [], []
        datos=pd.read_csv(name, sep=sep, encoding=enc)
        
        """ En caso de que el área del messier sea un cuadrado, toma la longitud del lado más pequeño como un radio """
        for value in datos['SIZE']:
            if "x" in value:
                split=value.split("x")
                if float(split[0])>float(split[1]):
                    radio.append(split[1])
                else:
                    radio.append(split[0])
            else:
                radio.append(value)
            
        for value in range(len(datos['RA'])):    
            cambioRA.append(Util.tiempoaGrados(datos['RA'][value], 'ra'))
            cambioDEC.append(Util.tiempoaGrados(datos['DEC'][value], 'dec'))
        
        Ms=[]
        #for i,j,k in zip(datos["RA"], datos["DEC"], datos["SIZE"]):
        for i,j,k,l in zip(cambioRA, cambioDEC, radio, datos["M"]):
            Ms.append((i,j,k,l))
            
            
        return Ms
    
    def lecturaPulsar(self,name,sep,enc): # Pulsares
        cambioRA, cambioDEC = [], []
        datos=pd.read_csv(name, sep=sep, encoding=enc)
        
        for value in range(len(datos['ra'])):    
            cambioRA.append(Util.tiempoaGrados(datos['ra'][value], 'ra'))
            cambioDEC.append(Util.tiempoaGrados(datos['dec'][value], 'dec'))
        
        Pu=[]
        for i,j in zip(cambioRA, cambioDEC):
            Pu.append((i,j))
            
        return Pu
    
    def lecturaPlaneta(self,name,sep,enc): # Planetas
        #datos=pd.read_csv(name, sep=sep, encoding=enc, skiprows=99)
        datos=pd.read_csv(name, sep=sep, encoding=enc, skiprows=1)
        
        Pl=[]
        # "ra" y "dec" ya están en grados, en lugar de "rastr" y "decstr" que están en h/m/s 
        for i,j,k,n,m,o,p,q,r,s,t in zip(datos["ra"], datos["dec"], datos["hostname"], datos["sy_snum"], datos["sy_pnum"], datos["pl_orbsmax"], datos["pl_rade"], datos["pl_bmasse"], datos["pl_orbeccen"], datos['st_rad'], datos['pl_name']):
            Pl.append((i,j,k,n,m,o,p,q,r,s,t))
            
        return Pl
    
    def lecturaConstelacion(self,name,sep,enc): # Constelaciones
        cambioRA, cambioDEC = [], []
        datos=pd.read_csv(name, sep=sep, encoding=enc)
        
        for value in range(len(datos['Right ascension(hours & mins)'])):    
            cambioRA.append(Util.tiempoaGrados(datos['Right ascension(hours & mins)'][value], 'ra'))
            cambioDEC.append(Util.tiempoaGrados(datos['Decli­nation(degs & mins)'][value], 'dec'))
        
        Cn=[]
        #for i,j,k in zip(datos["Right ascension(hours & mins)"], datos["Decli­nation(degs & mins)"], datos["Constellation"]):
        for i,j,k,n in zip(cambioRA, cambioDEC, datos["Constellation"], datos["Abbrev."]):
            Cn.append((i,j,k,n))
            
        return Cn
    
    def lecturaMessier(self, name,sep,enc): # Estrellas cercanas a objetos Messier
        listaMessier = []
        EM = {}
        
        with os.scandir(rutaMessiers) as ficheros: # Extraemos lista con nombres de archivos
            for fichero in ficheros:
                listaMessier.append(str(fichero.name))
        
        for num in listaMessier:
            datos=pd.read_csv(name+num, sep=sep, encoding=enc)
            M = []
            
            for i,j,k,l,n in zip(datos["ra"], datos["dec"], datos["parallax"], datos["bp_rp"], datos["teff_val"]):
                M.append((i,j,k,l,n))
                
            EM[num]=M
        
        return EM
    
    def estrellasXConstelacion(self,name,sep,enc): # Estrellas conocidas dentro de constelaciones
        listaConste = []
        EC = {}
        with os.scandir(rutaConste) as ficheros: # Extraemos lista con nombres de archivos
            for fichero in ficheros:
                listaConste.append(str(fichero.name))

        for num in listaConste:
            datos=pd.read_csv(name+num, sep=sep, encoding=enc)
            C = []
            
            # CONVERTIR COORDENADAS A GRADOS
            for i,j,k,l,n in zip(datos["RA"], datos["Dec"], datos["abs.mag."], datos["Sp. class"], datos["Name"]):
                C.append((i,j,k,l,n))
                
            EC[num] = C
        
        return EC
    
    def ventanaArchivo(self):
        root=tkinter.Tk()
        root.withdraw()
        ruta=filedialog.askopenfilename() 
    	
        return ruta
    
    def obtenerColoresCuerpoN(self, ruta = ""):
        try:
            if ruta == "":
                ruta = self.ventanaArchivo()
                
            colores = {}
            with open (ruta, "r") as archivo:
                for line in archivo:
                    line = line.strip()
                    col = line.split(" ")
                    if col[1] == "10deg":
                        col[0] = float(col[0].split(" ")[0])
                        colores[col[0]] = col[-1]
                    
            return colores
        except FileNotFoundError:
            return []
        
    def coloresCuerpoNegro(self, ruta=""):
        
        if not ruta:
            global colores
            
            return colores
        
        else:
            colores=self.obtenerColoresCuerpoN(ruta)
            return colores
        
if __name__=="__main__":
    lectura=lecturaArchivos(ruta)
    name, sep, enc = lectura.inicializar()
    #pulsares = lectura.lecturaPulsar(name[1], sep[1], enc[1])
    constelacion=lectura.lecturaCatalogoM(name[0], sep[0], enc[0])
    planetas=lectura.lecturaPlaneta(name[2], sep[2], enc[2])
    print(planetas)
    #print(constelacion['Hercules.csv'] """