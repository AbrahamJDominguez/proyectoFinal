import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
from matplotlib.animation import FuncAnimation
import numpy as np
#import random as rd

c=3*10**8
h=6.63*10**-34
k=1.38*10**-23
# 1 AU = 1.5x10^11 m
radTierra = 6371000 / 1.5e11 # cambiamos a AU
radSol = 696340000 / 1.5e11

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name,
        a=minval, b=maxval),cmap(np.linspace(minval, maxval, n)))
    return new_cmap

class grafica:
    
    def __init__(self, interfaz=False):
        
        self.interfaz=interfaz
        
        if not interfaz:
            self.fig, self.ax = plt.subplots()
        
    
    def mapaEstelar(self, ar, dec, objeto=[], rgb=[], indice="", colores=[], teff=[], ob=False, guardar=False, limpiar = False, interfaz=False):
        
        #self.llamadaInterfaz()
        self.interfaz=interfaz
    
        for i in ar:
            if i > 360:
                ar[ar.index(i)]=i-360
                
            elif i < 0:
                ar[ar.index(i)]=i+360
                
        scat=[]
        clr=[]
                
        if limpiar:
            self.reiniciarFigura()
         #usuario ingresa coordenadas, elige objeto
        if len(colores) == 1:
            aux=self.ax.scatter(ar, dec, s=2, color=colores[0])
            scat.append(aux.get_offsets().data)
            clr.append(aux.get_facecolors())
        
        self.ax.set_facecolor((0,0,0))
        
        if indice and not ob:
            
            for i in indice:
                if teff and colores:
                    aux=self.ax.scatter(ar[i], dec[i], s=2, color=colores[round(teff[i]*0.01)*100])
                    scat.append(aux.get_offsets().data)
                    clr.append(aux.get_facecolors())
                    continue
                aux=self.ax.scatter(ar[i], dec[i], s=2, color='r')
                scat.append(aux.get_offsets().data)
                clr.append(aux.get_facecolors())
                
        elif ob:
            
            for i in range(len(teff)):
                if teff and colores:
                    aux=self.ax.scatter(ar[i], dec[i], s=2, color=colores[round(teff[i]*0.01)*100])
                    scat.append(aux.get_offsets().data)
                    clr.append(aux.get_facecolors())
                    continue
                aux=self.ax.scatter(ar[i], dec[i], s=2, color='r')
                scat.append(aux.get_offsets().data)
                clr.append(aux.get_facecolors())
                
        elif teff:
            for i in range(len(ar)):
                if teff and colores:
                    
                    aux=self.ax.scatter(ar[i], dec[i], s=2, color=colores[round(teff[i]*0.01)*100])
                    scat.append(aux.get_offsets().data)
                    clr.append(aux.get_facecolors())
                    continue
                
        else:
            aux=self.ax.scatter(ar, dec, s=2, color='r')
            scat.append(aux.get_offsets())
            clr.append(aux.get_facecolors())
        
        #self.ax.set_xlim(45,50)
        #self.ax.set_ylim(2,6)
            
        #self.ax.scatter(229.6375, 2.0811, s=20, color=(1,1,1))

        for ob in objeto:
            if ob:
                aux=self.ax.scatter(ob[0], ob[1], s=3, color='r')
                scat.append(aux.get_offsets().data)
                clr.append(aux.get_facecolors().to_list())
                #self.ax.axhline(y=objeto[1]-objeto[2], xmin=objeto[0]-objeto[2], xmax=objeto[0]+objeto[2],color="y")
                #self.ax.axhline(y=objeto[1]+objeto[2], xmin=objeto[0]-objeto[2], xmax=objeto[0]+objeto[2],color="y")
                theta=np.linspace(0, 2*np.pi, 100)
                a=ob[2]*np.cos(theta) + ob[0]
                b=ob[2]*np.sin(theta) + ob[1]
                self.ax.plot(a, b, color='g')
                
        
        self.ax.set_xlabel("Ascensi??n recta ($^o$)")
        self.ax.set_ylabel("Declinaci??n ($^o$)")
        self.ax.set_title("Mapa estelar")

        
        if guardar:
            self.fig.savefig("mapaEstelar.jpg")
            
        if not interfaz:   
            plt.show()
            
        if len(scat) != len(clr):
            for i in range(len(scat)):
                clr.append(clr[0])
            
        return ((scat, clr), self.fig)

        
    def radiacionCuerpoN(self, teff,tempMax=0, colores=[], interfaz=False,guardar=False):
        import numpy as np
        self.interfaz=interfaz
        
        self.reiniciarFigura()
        self.llamadaInterfaz()
        
        def f(x, teff):
            return (2*(c/x)**3)/(c**2)*h*1/(np.exp((h*(c/x))/(k*teff))-1)   
        
        x=np.linspace(0, 3*10**-6, 1000)
        
        for val in teff:
            if val==tempMax:
                self.ax.plot(x, f(x, val),color="r",label=r"TempMax=%d$^o$C"%tempMax)
                
            elif colores:
                self.ax.plot(x, f(x, val), color=colores[round(teff[teff.index(val)]*0.01)*100])
            else:
                self.ax.plot(x, f(x, val))
        
        self.ax.set_xlabel("Longitud de onda ($\mu m$)")
        self.ax.set_ylabel("Intensidad ($W/m^2Hz^2sterad$)")
        self.ax.set_title("Espectro de radiaci??n del cuerpo negro") 
        self.ax.legend()
        if guardar:
            self.fig.savefig("radiacionCuerpoNegro.jpg")
        
        if not self.interfaz:
            
            plt.show()
        
        return self.fig
        
        
    def diagramaHR(self, bp_rp, phot_g_mean_mag, radius, interfaz=False,guardar=False, tempt=False, zoom=False):

        self.reiniciarFigura()
        self.llamadaInterfaz()
        self.interfaz=interfaz
        
        vmin=35000
        vmax=2000
        
        self.ax.set_position([self.ax.get_position().x0,self.ax.get_position().y0+0.1
                                 ,self.ax.get_position().width,self.ax.get_position().height-0.1])
        
        if tempt:
        
            mapeo=self.ax.scatter(bp_rp, phot_g_mean_mag, c=bp_rp, s=radius, cmap="RdYlBu", vmin=vmin, vmax=vmax)
            #mapeo=self.ax.scatter(bp_rp, phot_g_mean_mag, c=bp_rp, s=2, cmap="RdYlBu", vmin=11000, vmax=2000)
            
        else:
            mapeo=self.ax.scatter(bp_rp, phot_g_mean_mag, c=bp_rp, s=radius, cmap="RdYlBu_r", vmin=-1, vmax=5)
            self.ax.set_xlabel("Color BP-RP ($G_{BP}-G_{RP}$)")
            self.ax.set_title("Diagrama de Hertzsprung-Russell")
        
        self.ax.set_facecolor((0,0,0))
        
        if tempt and zoom:
            temp_max=max(bp_rp)+500
            temp_min=min(bp_rp)-500
            
            cax = self.fig.add_axes([self.ax.get_position().x0,self.ax.get_position().y0-0.1
                                     ,self.ax.get_position().width,0.01], label="cbp")
            
            colb=self.fig.colorbar(mapeo, cax=cax, orientation="horizontal")
            colb.ax.invert_xaxis()
            
            cax2 = self.fig.add_axes([self.ax.get_position().x0,self.ax.get_position().y0
                                     ,self.ax.get_position().width,0.01], label="cbs")
            
            fracmin=(temp_min-vmin)/(vmax-vmin)
            fracmax=(temp_max-vmin)/(vmax-vmin)
            mapeo2=truncate_colormap(plt.get_cmap('jet'), minval=fracmin, maxval=fracmax)
            norm=colors.Normalize(vmin=temp_min, vmax=temp_max)
                
            colb2=colorbar.ColorbarBase(cax2, cmap=mapeo2, norm=norm , orientation="horizontal")
            
            colb2.ax.invert_xaxis()
            
            self.ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        
            self.ax.set_xlim(temp_min,temp_max)
        
            self.ax.invert_xaxis()
            
            self.ax.set_title("Diagrama de Hertzsprung-Russell ($T_{eff}$ [K])")
            
        elif tempt and not zoom:
            cax = self.fig.add_axes([self.ax.get_position().x0,self.ax.get_position().y0
                                     ,self.ax.get_position().width,0.01])
                
            colb=self.fig.colorbar(mapeo, cax=cax, orientation="horizontal")
            
            colb.ax.invert_xaxis()
            
            self.ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            self.ax.set_xlim(2000,5000)
        
            self.ax.invert_xaxis()
            
            self.ax.set_title("Diagrama de Hertzsprung-Russell ($T_{eff}$ [K])")
            
        else: 
            self.ax.set_xlim(min(bp_rp)-0.5, max(bp_rp)+0.5)
            #self.ax.set_xlim(-1,5)
        
        #colb.ax.invert_xaxis()
        
        #self.ax.set_ylim(-10,20)
        self.ax.set_ylim(min(phot_g_mean_mag) - 5, max(phot_g_mean_mag) + 5)
        self.ax.invert_yaxis()
        
        self.ax.set_ylabel("Magnitud absoluta ($M_G$)")
        
        if guardar:
            self.fig.savefig("diagramaHR.jpg")
            
        if not self.interfaz:
            
            plt.show()
        
        return self.fig
    
    def orbitas(self, numE, numP, ar, dec, a, e, radioE, radioP, nomE): # coord=[ra, dec]
        
        self.reiniciarFigura()
        self.llamadaInterfaz()
        
        circs=[]
        b=[]
        lineas=[]
        
        for val in range(len(a)):
            b.append(a[val] * np.sqrt(1-e[val]**2))
            c = a[val]**2 - b[-1]**2
            centroAux = ar - c
            
            t = np.linspace(0,360,360)
            x = a[val]*np.cos(np.radians(t)) + centroAux  #a es el eje mayor de la elipse
            y = b[-1]*np.sin(np.radians(t)) + dec #b es el eje menor de la elipse
        
            lineas.append(self.ax.plot(x, y, linewidth = 1, alpha=0.5)[0])
            
            x1,x2=self.ax.get_xlim()
            y1,y2=self.ax.get_ylim()
            
            if radioE >3:
            
                escala=min(x2-x1, y2-y1)/25
                
            else:
                escala=min(x2-x1, y2-y1)/10
        
            if str(radioP[val]) != "nan":
                circ = plt.Circle((x[0], y[0]), radius=escala*radioP[val]*radTierra, color="b", fill = True)
                circs.append(circ)
            
            else:
                circ = plt.Circle((x[0], y[0]), radius=escala*0.1, color="b", fill = True)
                circs.append(circ)
        
            self.ax.add_patch(circ)
            
        def update(i):
        
            t=i*5
            
            for j in range(len(circs)):
                x1 = a[j]*np.cos(np.radians(t)) + centroAux  #a es el eje mayor de la elipse
                y1 = b[j]*np.sin(np.radians(t)) + dec #b es el eje menor de la elipse
                
                xy=lineas[j].get_data()
                circs[j].center=(xy[0][t],xy[1][t])
                

        
            return circs
            
        if str(radioE) != "nan":
            
            self.ax.add_patch(plt.Circle((ar, dec), radius=radioE*radSol*escala,color="r", fill=True))
            #self.ax.scatter(coord[0], coord[1], s = radioE, color='red', label='')
        else:
            self.ax.add_patch(plt.Circle((ar, dec), radius=escala,color="r", fill=True))
    
    
        self.ax.set_xlabel("Ascensi??n recta ($^o$)")
        self.ax.set_ylabel("Declinaci??n ($^o$)")
        self.ax.set_title("Sistema planetario de " + str(nomE))
        #self.ax.legend()
        self.ax.set_facecolor('k')
        plt.axis('scaled')

        
        return self.fig, lambda i: update(i)
    
        
    def limpiarFigura(self):
        self.ax.cla()
        self.fig.clf()
        
    def llamadaInterfaz(self):
        if self.interfaz:
            self.fig, self.ax = plt.subplots() 
        
    def reiniciarFigura(self):
        try:
            if self.fig.get_axes() and (self.ax.collections or self.ax.lines):
                self.fig, self.ax = plt.subplots()
            #plt.close()
            
        except AttributeError:
            pass
            
    def __bool__(self):
        
        try:
            if self.fig.get_axes() and (self.ax.collections or self.ax.lines):
                return True
            
            return False
        
        except AttributeError:

            return False

    def __getitem__(self, item):
        if item == 0:
            return self.fig
        
        elif item == 1:
            return self.ax
        
        
if __name__=="__main__":
    grafica().radiacionCuerpoN(3000)
    cmap=plt.get_cmap("jet")
    #print(plt.get_cmap("jet"))
    #print(colors.LinearSegmentedColormap.from_list('trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=0.01, b=0.02),cmap(np.linspace(0.01, 0.02, 100))))
# -*- coding: utf-8 -*-
