# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:31:56 2022

@author: Abrah
"""

import tkinter as tk
from tkinter import ttk
from utilidades import tiempoaGrados, isfloat
import pandas as pd
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#heredamos de la clase tk para poder crear una ventana principal y configurarla desde afuera
#de la misma forma que se haría con el Tk normal
class ventanaPrincipal(tk.Tk):
    FONDO="#0b0b0b"
    ventana=0
    
    def __init__(self, titulo="Estrellitas",tam=(1200,600)):
        super().__init__()
        self.iniciarVentana(titulo,tam)
        
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
        
        tipo=tk.IntVar()
        tipo.set(1)
        
        def cambioTipo():
            
            if tipo.get() == 1:
                rad.place_forget()
                tamx.place(relx=0.07, width=82, height=20)
                tamy.place(relx=0.57, width=82, height=20)
                
            elif tipo.get() == 2:
                tamx.place_forget()
                tamy.place_forget()
                rad.place(relx=0.3, width=82, height=20)
        
        tk.Radiobutton(frame_caja, text="Caja",bg="#a7a7a7", value=1, variable=tipo,
                       command= cambioTipo)\
            .place(relx=0.03, width=70)   
        tk.Radiobutton(frame_caja, text="Circulo",bg="#a7a7a7", value=2, variable=tipo, 
                       command=cambioTipo)\
            .place(relx=0.33, width=70)
        
        ttk.Separator(frame_entrys, orient="horizontal")\
            .place(relx=0, rely=1, relwidth=1)
            
        def revisar():
            ra=self.ent_ar.get()
            dec=self.ent_dec.get()
            
            limx=self.ent_tamx.get()
            limy=self.ent_tamy.get()
            
            rad=self.ent_rad.get()
            
            try:
                tiempoaGrados(ra)
                tiempoaGrados(dec)
                if not isfloat(limx) and not isfloat(rad):
                    tiempoaGrados(limx)
                    
                if not isfloat(limy) and not isfloat(rad):
                    tiempoaGrados(limy)
                    
                self.elec_const.set("")
                self.elec_messier.set("")
                    
                self.cambio()
                
            except ValueError:
                print("Los datos ingresados no son validos")
                
            except IndexError:
                print("Los cuadros no fueron llenados")
                
        tk.Button(frame_entrys, text="Ingresar", command=revisar)\
            .place(relx=0.82, rely=0.75,width=52)
        
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
                        command=self.cambio).place(relx=0.15, rely=0.3)
        
        ttk.Checkbutton(frame_checks, text="Planetas",
                        variable=self.pal_plnt,
                        onvalue=1,
                        offvalue=0, style="P.TCheckbutton",
                        command=self.cambio).place(relx=0.15, rely=0.5)
        
        ttk.Checkbutton(frame_checks, text="Pulsares",
                        variable=self.pal_psr,
                        onvalue=1,
                        offvalue=0, style="P.TCheckbutton",
                        command=self.cambio).place(relx=0.15, rely=0.7)
        
    def botones(self):
        frame_botones=tk.Frame(self.fh, bg="#b9b9b9")
        frame_botones.place(relx=0, rely=0.4, relwidth=1, relheight=0.2)
        
        frameSepEl=tk.Frame(frame_botones, bg="#bbbbbb")
        frameSepEl.place(relx=0.1,rely=0, height=20, relwidth=0.8)
        ttk.Separator(frameSepEl, orient="horizontal")\
            .place(relx=0, rely=0.4, relwidth=1)
        tk.Label(frameSepEl, text="Diagramas de elementos en mapa", bg="#bbbbbb")\
        .pack()
        ttk.Separator(frame_botones, orient="horizontal")\
            .place(relx=0, rely=0.9, relwidth=1)
        
        tk.Button(frame_botones, text="Diagrama H-R").place(relx=0.15, rely=0.15)
        tk.Button(frame_botones, text="Radiacion de cuerpo negro").place(relx=0.15, rely=0.40)
        tk.Button(frame_botones, text="Orbitas").place(relx=0.15, rely=0.65)
        
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
        
        tk.Button(frame_listas, text="Mostrar elección", command=self.cambio)\
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
        
        tk.Button(frame_listas, text="Mostrar elección", command=self.cambio)\
            .place(relx=0.33, rely=0.6)
        
        
    def cambio(self):
        self.__cambio=True
        
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
        
        figuracanvas=FigureCanvasTkAgg(self.figura, master=self)
        figuracanvas.draw()
        
        figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
        
    def graficaHR(self, datos):
        self.canvasP=tk.Canvas(self, bg="#0b0b0b")
        self.canvasP.place(relx=0, rely=0,relheight=1, relwidth=1)
        
        figuracanvas=FigureCanvasTkAgg(self.figura, master=self)
        figuracanvas.draw()
        
        figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
        
    def orbitas(self, datos):
        self.canvasP=tk.Canvas(self, bg="#0b0b0b")
        self.canvasP.place(relx=0, rely=0,relheight=1, relwidth=1)
        
        figuracanvas=FigureCanvasTkAgg(self.figura, master=self)
        figuracanvas.draw()
        
        figuracanvas.get_tk_widget().place(relx=0.05, rely=0, relheight=1, relwidth=0.9)
        
        
        
    
if __name__ == "__main__":
    ventanaPrincipal().mainloop()
    
    