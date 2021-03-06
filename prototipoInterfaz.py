# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:31:56 2022

@author: Abrah
"""

import tkinter as tk
from tkinter import ttk
from utilidades import tiempoaGrados, isfloat, creacionBases
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from datosGaia import solicitaDatosGaia
import numpy as np
import seleccionObjeto as SO
from tkinter import messagebox


#heredamos de la clase tk para poder crear una ventana principal y configurarla desde afuera
#de la misma forma que se haría con el Tk normal
class ventanaPrincipal(tk.Tk):
    FONDO="#0b0b0b"
    ventana=0
    
    def __init__(self, titulo="Estrellitas",tam=(1200,600)):
        super().__init__()
        self.iniciarVentana(titulo,tam)
        self.xlim=(-10,10)
        self.ylim=(-10,10)
        self.rad=0
        self.centro=(0,0)
        
        self.pal_est=tk.IntVar()
        self.pal_plnt=tk.IntVar()
        self.pal_psr=tk.IntVar()
        self.pal_est.set(0)
        self.pal_plnt.set(0)
        self.pal_psr.set(0)
        
        self.ent_ar=tk.StringVar()
        self.ent_dec=tk.StringVar()
        self.ent_rad=tk.StringVar()
        self.ent_tamx=tk.StringVar()
        self.ent_tamy=tk.StringVar()
        
        self._interfaz=tk.BooleanVar()
        self._interfaz.set(True)
        
        self.elec_const=tk.StringVar()
        self.elec_messier=tk.StringVar()
        
        self.__cambio=False
        
        self.iniciarElementos()
        
    def iniciarVentana(self, titulo, tam):
        self.minsize(*tam)
        self.title(titulo)
        self["bg"]=self.FONDO
    
    def iniciarElementos(self):
        self.iniciarFramePrincipal()
        self.iniciarFrameHerramientas()
    
    def iniciarFramePrincipal(self):
        self.fp=tk.Frame(self, bg=self.FONDO)
        self.fp.place(relx=0, rely=0, relheight=1, relwidth=0.75)
        self.canvasP=tk.Canvas(self.fp, bg="#0b0b0b")
        self.canvasP.place(relx=0, rely=0,relheight=1, relwidth=1)
    
    def iniciarFrameHerramientas(self):
        self.fh=tk.Frame(self, bg="#bbbbbb")
        self.fh.place(relx=0.75, rely=0, relheight=1, relwidth=0.25)
        self.entradas()
        self.checks()
        self.botones()
        self.listasDesplegables()
        
    def entradas(self):
        frame_entrys=tk.Frame(self.fh, bg="#b9b9b9")
        frame_entrys.place(relx=0, rely=0.02, relheight=0.21, relwidth=1)
        
        frameSepEl=tk.Frame(frame_entrys, bg="#bbbbbb")
        frameSepEl.place(relx=0.1,rely=0.045, height=20, relwidth=0.8)
        ttk.Separator(frameSepEl, orient="horizontal")\
            .place(relx=0, rely=0.4, relwidth=1)
        tk.Label(frameSepEl, text="Coordenadas", bg="#bbbbbb")\
        .pack()
        
        tk.Entry(frame_entrys, textvariable=self.ent_ar, justify="right")\
            .place(relx=0.15, rely=0.3, width=82, height=20)   
        tk.Entry(frame_entrys, textvariable=self.ent_dec, justify="right")\
            .place(relx=0.6, rely=0.3, width=82, height=20)
            
        frame_caja=tk.Frame(frame_entrys, bg="#a7a7a7")
        frame_caja.place(relx=0.10, rely=0.55, relwidth=0.7, relheight=0.4)
        
        frame_caja2=tk.Frame(frame_caja, bg="#a7a7a7")
        frame_caja2.place(relx=0, rely=0.55, relwidth=1, relheight=0.45)
        
        tamx=tk.Entry(frame_caja2, textvariable=self.ent_tamx)
        tamy=tk.Entry(frame_caja2, textvariable=self.ent_tamy)
        rad=tk.Entry(frame_caja2, textvariable=self.ent_rad)
        tamx.place(relx=0.07, width=82, height=20)
        tamy.place(relx=0.57, width=82, height=20)
        
        self.tipo=tk.IntVar()
        self.tipo.set(1)
        
        def cambioTipo():
            
            if self.tipo.get() == 1:
                rad.place_forget()
                tamx.place(relx=0.07, width=82, height=20)
                tamy.place(relx=0.57, width=82, height=20)
                
            elif self.tipo.get() == 2:
                tamx.place_forget()
                tamy.place_forget()
                rad.place(relx=0.3, width=82, height=20)
        
        tk.Radiobutton(frame_caja, text="Caja",bg="#a7a7a7", value=1, variable=self.tipo,
                       command= cambioTipo)\
            .place(relx=0.03, width=70)   
        tk.Radiobutton(frame_caja, text="Circulo",bg="#a7a7a7", value=2, variable=self.tipo, 
                       command=cambioTipo)\
            .place(relx=0.33, width=70)
        
        ttk.Separator(frame_entrys, orient="horizontal")\
            .place(relx=0, rely=1, relwidth=1)
            
                
        tk.Button(frame_entrys, text="Ingresar", command=self.revisar)\
            .place(relx=0.82, rely=0.75,width=52)
            
    def revisar(self):
        ra=self.ent_ar.get()
        dec=self.ent_dec.get()
        
        limx=self.ent_tamx.get()
        limy=self.ent_tamy.get()
        
        rad=self.ent_rad.get()
        
        try:
            x=tiempoaGrados(ra)
            y=tiempoaGrados(dec)
            self.centro=(x,y)
            
            if not isfloat(limx) and not isfloat(rad):
                xlim=tiempoaGrados(limx)
                self.xlim=(min(x-xlim/2, x+xlim/2),max(x-xlim/2, x+xlim/2))
                
            elif isfloat(limx) and not isfloat(rad):
                xlim=float(limx)
                self.xlim=(min(x-xlim/2, x+xlim/2),max(x-xlim/2, x+xlim/2))      
                
            if not isfloat(limy) and not isfloat(rad):
                ylim=tiempoaGrados(limy)
                self.ylim=(min(y-ylim/2, y+ylim/2),max(y-ylim/2, y+ylim/2))
                
            elif isfloat(limy) and not isfloat(rad):
                ylim=float(limy)
                self.ylim=(min(y-ylim/2, y+ylim/2),max(y-ylim/2, y+ylim/2))
                
            if isfloat(rad):
                rad=float(rad)
                self.rad=rad
                self.xlim=(min(x-rad, x+rad),max(x-rad, x+rad))
                self.ylim=(min(y-rad, y+rad),max(y-rad, y+rad))
                
            self.elec_const.set("")
            self.elec_messier.set("")
                
            self.cambio("mapad")
            
        except ValueError:
            print("Los datos ingresados no son validos")
            
        except IndexError:
            print("Los cuadros no fueron llenados")
        
    def checks(self):
        estilo=ttk.Style()
        estilo.configure("P.TCheckbutton", background="#bbbbbb")
        
        frame_checks=tk.Frame(self.fh, bg="#b9b9b9")
        frame_checks.place(relx=0,rely=0.23, relheight=0.17, relwidth=1)
        
        frameSepEl=tk.Frame(frame_checks, bg="#bbbbbb")
        frameSepEl.place(relx=0.1,rely=0.045, height=20, relwidth=0.8)
        ttk.Separator(frameSepEl, orient="horizontal")\
            .place(relx=0, rely=0.4, relwidth=1)
        tk.Label(frameSepEl, text="Elementos en mapa", bg="#bbbbbb")\
        .pack()
        # ttk.Separator(frame_checks, orient="horizontal")\
        #     .place(relx=0, rely=0.9, relwidth=1)
        
        ttk.Checkbutton(frame_checks, text="Estrellas",
                        variable=self.pal_est,
                        onvalue=1,
                        offvalue=0, style="P.TCheckbutton",
                        command=lambda: self.cambio("mapad")).place(relx=0.15, rely=0.3)
        
        # ttk.Checkbutton(frame_checks, text="Planetas",
        #                 variable=self.pal_plnt,
        #                 onvalue=1,
        #                 offvalue=0, style="P.TCheckbutton",
        #                 command=lambda: self.cambio("mapad")).place(relx=0.15, rely=0.5)
        
        ttk.Checkbutton(frame_checks, text="Pulsares",
                        variable=self.pal_psr,
                        onvalue=1,
                        offvalue=0, style="P.TCheckbutton",
                        command=lambda: self.cambio("mapad")).place(relx=0.15, rely=0.7)
        
        def desplegarAviso():
            self.cambio("mapad")
            if not self._interfaz.get():
                messagebox.showinfo(message="Al activar esta casilla se desplegarán ventanas\n "\
                                    "emergentes que detienen al programa hasta ser cerradas",
                                    title="Aviso")
            
        ttk.Checkbutton(frame_checks, text="Mostrar posibles incidencias",
                        variable=self._interfaz,
                        onvalue=False,
                        offvalue=True, style="P.TCheckbutton",
                        command= desplegarAviso).place(relx=0.15, rely=0.5)
        
    def botones(self):
        frame_botones=tk.Frame(self.fh, bg="#b9b9b9")
        frame_botones.place(relx=0, rely=0.4, relwidth=1, relheight=0.2)
        
        frameSepEl=tk.Frame(frame_botones, bg="#bbbbbb")
        frameSepEl.place(relx=0.1,rely=0, height=20, relwidth=0.8)
        ttk.Separator(frameSepEl, orient="horizontal")\
            .place(relx=0, rely=0.4, relwidth=1)
        tk.Label(frameSepEl, text="Diagramas de Messier elegido", bg="#bbbbbb")\
        .pack()
        ttk.Separator(frame_botones, orient="horizontal")\
            .place(relx=0, rely=0.9, relwidth=1)
        
        tk.Button(frame_botones, text="Diagrama H-R", command=lambda: self.diagramasMessier(3)).place(relx=0.15, rely=0.15)
        tk.Button(frame_botones, text="Radiacion de cuerpo negro", command=lambda: self.diagramasMessier(2)).place(relx=0.15, rely=0.40)
        #tk.Button(frame_botones, text="Orbitas").place(relx=0.15, rely=0.65)
        
    def listasDesplegables(self):
        self.listaConstelaciones()
        self.listaMessiers()
    
    def listaConstelaciones(self):
        frame_listas=tk.Frame(self.fh, bg= "#b9b9b9")
        frame_listas.place(relx=0, rely=0.60, relwidth=1, relheight=0.17)
        
        frameSepEl=tk.Frame(frame_listas, bg="#bbbbbb")
        frameSepEl.place(relx=0.1,rely=0.045, height=20, relwidth=0.8)
        ttk.Separator(frameSepEl, orient="horizontal")\
            .place(relx=0, rely=0.4, relwidth=1)
        tk.Label(frameSepEl, text="Constelaciones", bg="#bbbbbb")\
        .pack()
        ttk.Separator(frame_listas, orient="horizontal")\
            .place(relx=0, rely=0.9, relwidth=1)
            
        nombres=()
        
        if os.path.isfile("constelaciones.csv") and os.path.isdir("constelaciones"):
            nombres=pd.read_csv("constelaciones.csv", sep="\t", encoding="utf-16")["Constellation"]
            
        caja_m=ttk.Combobox(frame_listas, textvariable=self.elec_const)
            
        caja_m["values"]=tuple(list(nombres))
        caja_m["state"]="readonly"
        caja_m.place(relx=0.35, rely=0.3, height=20, width=82)
        
        tk.Button(frame_listas, text="Mostrar elección", command=lambda: self.cambio("espC"))\
            .place(relx=0.33, rely=0.6)
        
    def listaMessiers(self):
        frame_listas=tk.Frame(self.fh, bg= "#b9b9b9")
        frame_listas.place(relx=0, rely=0.77, relwidth=1, relheight=0.17)
        
        frameSepEl=tk.Frame(frame_listas, bg="#bbbbbb")
        frameSepEl.place(relx=0.1,rely=0.045, height=20, relwidth=0.8)
        ttk.Separator(frameSepEl, orient="horizontal")\
            .place(relx=0, rely=0.4, relwidth=1)
        tk.Label(frameSepEl, text="Messier", bg="#bbbbbb")\
        .pack()
        ttk.Separator(frame_listas, orient="horizontal")\
            .place(relx=0, rely=0.9, relwidth=1)
            
        nombres=()
        
        if os.path.isfile("MessierCatalogList.csv") and os.path.isdir("messiersGaia"):
            nombres=pd.read_csv("MessierCatalogList.csv", sep=",", encoding="utf-8")["M"]
            
        caja_m=ttk.Combobox(frame_listas, textvariable=self.elec_messier)
            
        caja_m["values"]=tuple(list(nombres))
        caja_m["state"]="readonly"
        caja_m.place(relx=0.35, rely=0.3, height=20, width=82)
        
        tk.Button(frame_listas, text="Mostrar elección", command=lambda: self.cambio("espM"))\
            .place(relx=0.33, rely=0.6)
            
    def busqueda(self, archivo, nombreArchivo, tipo="circ"): # Busca todos los objetos cercanos a las coordenadas escritas

        nombres, lista_index, coord = [], [], []
        
        for index in range(len(archivo)):
            
            if tipo == "circ":
                if nombreArchivo == 'constelaciones':

                    if ((archivo[index][0] - float(self.centro[0]))**2 + (archivo[index][1] - float(self.centro[1]))**2) <= float(self.rad)**2:
                        nombre_aux = [archivo[index][-2], archivo[index][-1]]
                        nombres.append(nombre_aux)
                        lista_index.append(index)
                        coord.append([archivo[index][0], archivo[index][1]])
                        
                elif nombreArchivo == 'MessierCatalogo':
                    distancia = ((archivo[index][0] - float(self.centro[0]))**2 + (archivo[index][1] - float(self.centro[1]))**2)**(1/2)
                    if distancia < float(self.rad) + float(archivo[index][2]):
                        nombres.append(archivo[index][-1])
                        lista_index.append(index)
                        coord.append([archivo[index][0], archivo[index][1]])
                        
                elif ((archivo[index][0] - float(self.centro[0]))**2 + (archivo[index][1] - float(self.centro[1]))**2) <= float(self.rad)**2:
                    nombres.append(archivo[index][-1])
                    lista_index.append(index) 
                    """ Agregué una lista para guardar las coordenadas de cada objeto dentro del radio """
                    coord.append([archivo[index][0], archivo[index][1]])        
        
            elif tipo == "rec":
                if nombreArchivo == 'constelaciones':
                    if (float(self.xlim[0]) < (archivo[index][0]) and float(self.xlim[1]) > (archivo[index][0])) and \
                    (archivo[index][1] > float(self.ylim[0]) and archivo[index][1] < float(self.ylim[1])) :
                        nombre_aux = [archivo[index][-2], archivo[index][-1]]
                        nombres.append(nombre_aux)
                        lista_index.append(index)
                        coord.append([archivo[index][0], archivo[index][1]])
                        
                elif nombreArchivo == 'MessierCatalogo':
                    distancia = ((archivo[index][0] - float(self.centro[0]))**2 + (archivo[index][1] - float(self.centro[1]))**2)**(1/2)
                    if max(float(archivo[index][2])+self.centro[0],float(archivo[index][2])+self.centro[1]) > distancia:

                        nombres.append(archivo[index][-1])
                        lista_index.append(index)
                        coord.append([archivo[index][0], archivo[index][1]])
                        
                elif (float(self.xlim[0]) < (archivo[index][0]) and float(self.xlim[1]) > (archivo[index][0])) and \
                (archivo[index][1] > float(self.ylim[0]) and archivo[index][1] < float(self.ylim[1])):
                    nombres.append(archivo[index][-1])
                    lista_index.append(index) 
                    """ Agregué una lista para guardar las coordenadas de cada objeto dentro del radio """
                    coord.append([archivo[index][0], archivo[index][1]])        
            
        return nombres, lista_index, coord
            
    def cambio(self, tipo):
        #if tipo == "mapad":
        self.__accion=tipo
        self.__cambio=True
        
    def diagramasMessier(self, tipo):
        mess=self.elec_messier.get()
        if mess:
            messier = SO.messier("ar", "dec", "radio", 'tipo', 'Mabsoluta', 'tamaño', 'dist')
            
            fig=messier.estrella(mess, tipo=tipo, interfaz=True)
            
            if tipo == 2:
                titulo=f"Radiacion de cuerpo negro de estrellas en {mess}"
                tipov="rcn"
                
            elif tipo == 3:
                titulo=f"Radiacion de cuerpo negro de estrellas en {mess}"
                tipov="hr"
                
            ventanaDiagrama(titulo, fig, tipo=tipov)
            
            
        
    def dibujar(self):
        #print(self.__cambio, self.tipo)
        if self.__cambio:
            #solicitaDatosGaia(self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1])
            import lecturaArchivos as Lec
            import seleccionObjeto as SO
            puntos=[]
            colores=[]
            if self.__accion == "mapad":
                self.revisar()
            
            ruta=""

            lectura = Lec.lecturaArchivos(ruta)
            name, sep, enc = lectura.inicializar()
            messierCat = lectura.lecturaCatalogoM(name[0], sep[0], enc[0])
            pulsares = lectura.lecturaPulsar(name[1], sep[1], enc[1]) 
            planetas = lectura.lecturaPlaneta(name[2], sep[2], enc[2])
            constelaciones = lectura.lecturaConstelacion(name[3], sep[3], enc[3])
            #estrellasM = lectura.lecturaMessier(name[4], sep[4], enc[4])
            
            messAr = []
            messDec = []
            for i in messierCat:
                messAr.append(i[0])
                messDec.append(i[1])

            constAr = []
            constDec = []
            for i in constelaciones:
                constAr.append(i[0])
                constDec.append(i[1])
            
            pulsaresAr = []
            pulsaresDec = []
            for i in pulsares:
                pulsaresAr.append(i[0])
                pulsaresDec.append(i[1])
                
            if self.__accion == "mapad":
                    
                if self.tipo.get() == 1:
        
                    """ A cada objeto le corresponde una lista de coordenadas """
                    nombresM, listaIndM, coordM = self.busqueda(messierCat, "MessierCatalogo", tipo="rec")       # objetos Messier
                    nombresP, listaIndP, coordP = self.busqueda(planetas, "planetas", tipo="rec")                # planetas
                    nombresC, listaIndC, coordC = self.busqueda(constelaciones, "constelaciones", tipo="rec")    # constelaciones
                    nombresPu, listaIndPu, coordPu = self.busqueda(pulsares, "pulsares", tipo ="rec")
                    
                elif self.tipo.get() == 2:
                    
                    """ A cada objeto le corresponde una lista de coordenadas """
                    nombresM, listaIndM, coordM = self.busqueda(messierCat, "MessierCatalogo")       # objetos Messier
                    nombresP, listaIndP, coordP = self.busqueda(planetas, "planetas")                # planetas
                    nombresC, listaIndC, coordC = self.busqueda(constelaciones, "constelaciones")    # constelaciones
                    nombresPu, listaIndPu, coordPu = self.busqueda(pulsares, "pulsares")
                    
                if self.pal_est.get() == 1:
                    if len(nombresM) > 0:
                        messier = SO.messier("ar", "dec", "radio", 'tipo', 'Mabsoluta', 'tamaño', 'dist')
                        
                        for m in nombresM:
                            puntosM=messier.estrella(m, interfaz=self._interfaz.get(), limpiar=True)[0]
                            puntos.append(puntosM[0])
                            colores.append(puntosM[1])
                            
                        
                    if len(nombresC) > 0: 
    
                        constelacion = SO.constelacion("ar", 'dec', 'radio', 'abrev', 'solidAA', 'solidAM', 'perc', 'quad')
                        for c in nombresC:
                            puntosC=constelacion.const(c[0], interfaz=self._interfaz.get(),limpiar=True)[0]
                            puntos.append(puntosC[0])
                            colores.append(puntosC[1])
                        
                if self.pal_psr.get() == 1:
                    #for p in nombresP:
                    objeto = SO.objetoEstelar(pulsaresAr, pulsaresDec, [])
                    puntosPlnt=objeto.crearMapaEstelar([],[], interfaz=self._interfaz.get())[0]
                    puntos.append(puntosPlnt[0])
                    colores.append(puntosPlnt[1])
                        
                if puntos:
                    
                    fig, ax = plt.subplots()
                    ax.set_facecolor((0,0,0))
    
                    i=0
                    for con in puntos:
                        try:
                            x=[el[0][0] for el in con]
                            y=[el[0][1] for el in con]
                            col = colores[i]
                            ax.scatter(x,y, s=2,color=col)
                            i+=1
                        except IndexError:
                            i+=1
                            continue
                    if self.tipo.get() == 2:
                        t = np.linspace(0,360,360)
                        x = self.rad*np.cos(np.radians(t)) + self.centro[0]  #a es el eje mayor de la elipse
                        y = self.rad*np.sin(np.radians(t)) + self.centro[1] #b es el eje menor de la elipse
                        ax.plot(x,y, linewidth=0.5)
                    ax.set_xlim(self.xlim)
                    ax.set_ylim(self.ylim)
                        
     
                    figuracanvas=FigureCanvasTkAgg(fig, master=self.canvasP)
                    figuracanvas.draw()
                    
                    figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
                    
            elif self.__accion == "espM":
                
                messier = SO.messier("ar", "dec", "radio", 'tipo', 'Mabsoluta', 'tamaño', 'dist')
                if self.elec_messier.get():
                    fig=messier.estrella(self.elec_messier.get(), interfaz=self._interfaz.get(), limpiar=True)[1]
                    figuracanvas=FigureCanvasTkAgg(fig, master=self.canvasP)
                    figuracanvas.draw()
                    figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
                
                
            
            elif self.__accion == "espC":
                constelacion = SO.constelacion("ar", 'dec', 'radio', 'abrev', 'solidAA', 'solidAM', 'perc', 'quad')
                if self.elec_const.get():
                    fig=constelacion.const(self.elec_const.get(), interfaz=self._interfaz.get(),limpiar=True)[1]
                    figuracanvas=FigureCanvasTkAgg(fig, master=self.canvasP)
                    figuracanvas.draw()
                    figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9) 
                
        self.__cambio = False
            
            
        
class ventanaDiagrama(tk.Toplevel):
    def __init__(self, titulo, datos, tammin=(800,500), tipo=""):
        super().__init__()
        self.iniciarVentana(titulo, tammin)
        self.figura=Figure(figsize=(5,4), dpi=50)
        
        if tipo == "rcn":
            self.graficaRCN(datos)
        
        elif tipo == "hr":
            self.graficaHR(datos)
            
        elif tipo == "orbitas":
            self.orbitas(datos)
        
    def iniciarVentana(self, titulo, tammin):
        self.title(titulo)
        self.minsize(*tammin)
        self.configure(bg="black")
        
    def graficaRCN(self, datos):
        self.canvasP=tk.Canvas(self, bg="#0b0b0b")
        self.canvasP.place(relx=0, rely=0,relheight=1, relwidth=1)
        
        figuracanvas=FigureCanvasTkAgg(datos, master=self)
        figuracanvas.draw()
        
        figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
        
    def graficaHR(self, messier):
        self.canvasP=tk.Canvas(self, bg="#0b0b0b")
        self.canvasP.place(relx=0, rely=0,relheight=1, relwidth=1)
        
        figuracanvas=FigureCanvasTkAgg(messier, master=self)
        figuracanvas.draw()
        
        figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
        
    def orbitas(self, datos):
        self.canvasP=tk.Canvas(self, bg="#0b0b0b")
        self.canvasP.place(relx=0, rely=0,relheight=1, relwidth=1)
        
        figuracanvas=FigureCanvasTkAgg(self.figura, master=self)
        figuracanvas.draw()
        
        figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
        
class main_():
    def __init__(self):
        self._iniciarInterfaz()
        self._actualizarPantalla()
        
        if self._gui:
            self._gui.mainloop()
            

    def _iniciarInterfaz(self):
        self._gui=ventanaPrincipal()

    def _actualizarPantalla(self):
        if self._gui:
            self._gui.dibujar()
            self._gui.after(100, self._actualizarPantalla)
    
        
        
    
if __name__ == "__main__":
    
    import sys
    creacionBases()      
    
    main_()
    
    print("Cerrando")
    sys.exit()
    
    # raiz=ventanaPrincipal()
    # raiz.mainloop()
    