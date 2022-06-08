import numpy as np
import lecturaArchivos as lectura
import graficas as graf
#ruta = "C:/Users/cimen/Documents/POOE/proyectoFinal-main/"
ruta = ""#"C:/Users/sandy/Documents/Pooye/proyectoFinal-main"
lectura = lectura.lecturaArchivos(ruta)
name, sep, enc = lectura.inicializar()

class coordenadas():
    def __init__(self,ar,dec,radio):
        self.ar=ar
        self.dec=dec
    
    def entradaC(self):
        print("Indica las coordenadas y el radio de busqueda de objetos estelares. ")
        
        coord=int(input("Elija el tipo de coordenadas:\n   1. [h/m/s, °/'/'']\n   2. Grados\nSelección: "))
        
        if coord==1:
            ascension=input("Ascensión recta (h/m/s): ")
            declinacion=input("Declinación (°/'/''): ")
            self.radio=input("Radio de busqueda (en grados): ")
            ### conversion
            ascension=ascension.split("/")
            ascension[1]=float(ascension[1])/60
            ascension[2]=float(ascension[2])/3600
            self.ar=(float(ascension[0])+ascension[1]+ascension[2])*15
            declinacion=declinacion.split("/")
            declinacion[1]=float(declinacion[1])/60
            declinacion[2]=float(declinacion[2])/3600
            self.dec= float(declinacion[0])+declinacion[1]+declinacion[2]

        else:
            self.ar=input("Ascensión recta (en grados): ")
            self.dec=input("Declinación (en grados): ")
            self.radio=input("Radio de busqueda (en grados): ")
            
    
class objetoEstelar():                      # Clase padre
    def __init__(self,ar,dec,radio):
        self.ar=ar
        self.dec=dec
        self.radio=radio
        
    def coorObj(self, arObjeto, decObjeto):
        self.ar = arObjeto
        self.dec = decObjeto
        
    def crearMapaEstelar(self, teff, objeto):
        graficas = graf.grafica()        
        if teff: 
            graficas.mapaEstelar(self.ar, self.dec, [], indice = '', colores = [], teff=teff, ob = True, guardar = False )
            
        elif objeto: 
            graficas.mapaEstelar(self.ar, self.dec, objeto = objeto, indice = '', colores = [], teff=[], ob = False, guardar = False )
        else:
            graficas.mapaEstelar(self.ar, self.dec, [], indice = '', colores = [], teff=[], ob = False, guardar = False )
        
        
    
class objetoLuminoso(objetoEstelar): ## modulo para estrellas cercanas a messier
    def __init__(self,ar, dec, radio, temp_eff, m_absoluta):
        objetoEstelar.__init__(self,ar,dec,radio)
        self.temp_eff = temp_eff
        self.m_absoluta = m_absoluta
        
    def crearRadiacionCN():
        pass
    
    def crearDiagramaHR():
        pass
        


"""
class Estrella(): # Verificar si es conveniente dejarla como sub clase
    def __init__(self,ar,dec,radio,paralaje,Mrelativa,bp_rp,rad_vel,teff):
        objetoEstelar.__init__(self,ar,dec,radio)
        self.paralaje=paralaje          ## Paralaje
        self.Mrelativa=Mrelativa        ## Magnitud relativa
        self.bp_rp=bp_rp                ## Color bp-rp
        self.rad_vel=rad_vel            ## Velocidad radial
        self.teff=teff                  ## Temperatura efectiva
"""        
        # Mapa estelar
        # Diagrama H-R
        # Diagrama de cuerpo negro
        # Genera achivo con los datos de las estrellas en un radio dado (coordenadas, temp. eff., densidad de flujo...)

class Planeta(objetoEstelar):
    def __init__(self,ar,dec,radio,sy_snum,sy_pnum,pl_orbsmax,pl_rade,pl_bmasse,pl_orbeccen, st_rad, nom, nomE):
        objetoEstelar.__init__(self,ar,dec,radio)
        self.numE=sy_snum               ## no. de estrellas
        self.numP=sy_pnum               ## no. de planetas
        #self.pOrb=pl_orbper             ## periodo orbital
        self.orbSMeje=pl_orbsmax        ## orbita eje semi-mayor
        self.radioT=pl_rade             ## radio del planeta (en radio de la Tierra)
        #self.radioJ=pl_radj             ## radio del planeta (en radios de júpiter)
        self.masaT=pl_bmasse            ## masa (en masa terrestre)
        #self.masaJ=pl_bmassj            ## masa (en masas de júpiter)
        self.e=pl_orbeccen              ## excentricidad
        #self.eqTemp=pl_eq               ## temperatura de equilibrio
        self.radioE=st_rad              ## radio de la estrella principal
        self.nom=nom                    ## Nombre del planeta
        self.nomE=nomE                  ## Nombre de la estrella
        
        print("Este es el numero de estrellas", self.numE)
        print("Este es el numero de estrellas", self.nomE)
        
    def pl(self):
        print("\n\n*****Estás en el módulo planeta******")
        planetas = lectura.lecturaPlaneta(name[2], sep[2], enc[2])
        ar = []
        dec = []
        objeto = [self.ar, self.dec, self.radio]
        for i in planetas:
            ar.append(i[0])
            dec.append(i[1])
        print("¿Qué deseas hacer?\n1. Mapa Estelar de todos los planetas disponibles")
        opcion = int(input("Selección: "))
        if opcion == 1:
            objeto = objetoEstelar(ar,dec, [])
            #objeto.crearMapaEstelar([], objeto) ### no toma objeto como debería para graficar el punto rojo del planeta
            objeto.crearMapaEstelar([], [])
        
        # Gráfica que compare masas/ radios de planetas conocidos
        # Muestre los datos del sistema donde se encuentra (número de estrellas, planetas, nombres, etc.)
        # Genera gráfica de sistema planetario
        # Gráfica que compare masas/ radios de planetas conocidos
        # Muestre los datos del sistema donde se encuentra (número de estrellas, planetas, nombres, etc.)
    def sistemaPlanetario(self):
        plots = graf.grafica()
        fig, anim=plots.orbitas(self.numE, self.numP, [self.ar, self.dec], self.orbSMeje, self.e, self.radioE, self.radioT)
        return fig, anim
        # Genera gráfica de sistema planetario
""" 
class constelacion():
    def __init__(self,ar,dec,radio,abrev,solidAA,solidAM,perc,quad):
        objetoEstelar.__init__(self,ar,dec,radio)
        self.abrev=abrev
        self.solidAA=solidAA
        self.solidAM=solidAM
        self.perc=perc
        self.quad=quad
        
        # Graficar la posición de la constelación elegida con respecto a nosotros y las constelaciones que colindan con ella.
        # Sugerencia: preguntar al usuario si quiere ver un mapa con las contelaciones cercanas al objeto elegido
"""
class messier(objetoEstelar):
    def __init__(self,ar,dec,radio, tipo,Mabsoluta,tamaño,dist):
        objetoEstelar.__init__(self,ar,dec,radio)
        self.tipo=tipo
        self.Mabsoluta=Mabsoluta
        self.tamaño=tamaño
        self.dist=dist
        
    #def cumulos(self):
    #    print("Estás en el módulo messiers, qué deseas hacer?")
    #    print(self.ar,self.dec)
        
    def estrella(self,messier):
        print("\n\n*****Estás en el modulo de estrellas cercanas al messier****")
        estrellasM = lectura.lecturaMessier(name[4], sep[4], enc[4])
        #print(estrellasM[messier+".csv"])
        datos = estrellasM[messier+'.csv']
        ar = []
        dec = []
        teff = []
        for i in datos:
            ar.append(i[0])
            dec.append(i[1])
            teff.append(i[-1])
        print("¿Qué deseas hacer?\n1. Mapa Estelar de todas las estrellas disponibles dentro del messier")
        opcion = int(input("Selección: "))
        if opcion == 1:
            objeto = objetoEstelar(ar,dec, [])
            objeto.crearMapaEstelar(teff, [])
        

class constelacion(objetoEstelar):
    def __init__(self,ar,dec,radio,abrev,solidAA,solidAM,perc,quad):
        objetoEstelar.__init__(self,ar,dec,radio)
        self.abrev=abrev
        self.solidAA=solidAA
        self.solidAM=solidAM
        self.perc=perc
        self.quad=quad

        '''nombres=["MessierCatalogo", "pulsares", "planetas", "constelaciones", "estrellas_messier"]
        archivos={nombres[0]:["MessierCatalogList.csv","\t","utf-16"], nombres[1]:["pulsar.csv",",","utf-8"], nombres[2]:["PS_2022.05.20_12.28.05.csv",",","utf-8"],nombres[3]:["constelaciones.csv","\t","utf-16"],nombres[4]:["messiersGaia/M1.csv",",","utf-8" ]}
        
        
        name=archivos[nombres[3]][0]
        sep=archivos[nombres[3]][1]
        enc=archivos[nombres[3]][2]
        lec=lectura.lecturaArchivos("")
        Cn=lec.lecturaPlaneta(name,sep,enc)'''
        #print(Cn)
    def const(self, laConste):
        print("\n\n******Estás en el módulo constelacion******")
        constel = lectura.estrellasXConstelacion(name[5], sep[5], enc[5])
        #print(constel[laConste+".csv"])
        datos = constel[laConste+'.csv']
        ar = []
        dec = []
        for i in datos:
            ar.append(i[0])
            dec.append(i[1])
        print("¿Qué deseas hacer?\n1.Mapa Estelar de todas las estrellas disponibles dentro de la constelación")
        opcion = int(input("Elección: "))
        if opcion == 1:
            objeto = objetoEstelar(ar, dec, [])
            objeto.crearMapaEstelar([], [])
        # Graficar la posición de la constelación elegida con respecto a nosotros y las constelaciones que colindan con ella.
        # Sugerencia: preguntar al usuario si quiere ver un mapa con las contelaciones cercanas al objeto elegido

        
if __name__=="__seleccionObjeto__":
    constelacion=constelacion('ar', 'dec', 'radio', 'abrev', 'solidAA', 'solidAM', 'perc', 'quad')
    constelacion.const('Hercules')
    #objeto=objetoEstelar("2", "3", "")
    #mes = messier("2", "3", "radio", "tipo", "Mabsoluta", "tamaño", "dist")
    #mes.estrella('M13')
    #pulsares = lectura.lecturaPulsar(name[1], sep[1], enc[1])