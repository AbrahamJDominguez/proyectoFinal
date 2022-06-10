import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

#URL = "https://en.wikipedia.org/wiki/List_of_stars_in_Andromeda"
#URL = "https://en.wikipedia.org/wiki/14_And"
#page = requests.get(URL)

#Creamos una variable de tipo beatiful soup para poder manejar los datos como
#si se tratara de la pagina (nos facilita encontrar tablas o elementos de la pagina)
#soup = BeautifulSoup(page.content, "lxml")


#Eliminamos las referencias
#for tag in soup.find_all(class_="reference"):
#        tag.decompose()
#print(soup)

#Caso en que se busca de forma especifica un objeto 
#Se busca una caja de informacion
#tabla=soup.find("table", class_="infobox")

#Caso general para tablas con muchos objetos
#tab=pd.read_html(str(tabla))[0][0:-2]

#convertimos a un arreglo de numpy para optimizar el tiempo
#tab=pd.read_html(str(tabla))[0].to_numpy()
#print(type(pd.read_html(str(tabla))[0]))
#Caso en que se busca de forma especifica
#ar=np.where(tab == "Right ascension")
#dec=np.where(tab == "Declination")

#Caso en que se usan las tablas, en este caso podemos acceder a los datos con llaves
#print(tab["RA"].to_numpy())
#print(tab["Dec"].to_numpy())


#print(ar)
#print(f"{ar[0][0]} {ar[1][0]+1}")

#print(tab[ar[0][0]][ar[1][0]+1])
#print(soup)

def obtenerEstrellaE(nombre):
    
    """
    Obtiene datos de ubicacion de una estrella especifica, su utilidad esta 
    enfocada a ubicar las estrellas de sistemas planetarios
    """
    
    #Reemplazamos algunos caracteres que pueden causar problemas y
    #obtenemos el html de la pagina
    nombre=nombre.replace(" ", "_").replace(u"\xa0",u" ")
    URL = "https://en.wikipedia.org/wiki/"+nombre
    pag = requests.get(URL)
    
    try:
        soup=BeautifulSoup(pag.content,"lxml")
        
    except:
        print("Se recomienda instalar el paquete lxml con el comando pip install lxml")
        soup=BeautifulSoup(pag.content,"html.parser")
    
    for tag in soup.find_all(class_="reference"):
            tag.decompose()
            
    # Ponemos una captura de errores en caso de que en la pagina no se encuentren los
    # datos solicitados, hacemos que regrese un valor de 25 60 60 para poder reconocerlo
    # facilmente a la hora de obtener el error
    
    try:     
        tabla=soup.find("table", class_="infobox")
        tab=pd.read_html(str(tabla))[0].to_numpy()
        
    except ValueError:
        return False
    
    ar=np.where(tab == "Right ascension")
    dec=np.where(tab == "Declination")
    temptidx=np.where(tab == "Temperature")
    radidx=np.where(tab == "Radius")  
    
    rad=0
    tempt=0
    
    if temptidx[0].size > 0:
        if "±" in tab[temptidx[0][0]][temptidx[1][0]+1]:
            idx=tab[temptidx[0][0]][temptidx[1][0]+1].index("±")
            tempt=tab[temptidx[0][0]][temptidx[1][0]+1][0:idx].replace(u"\xa0",u" ").replace(u",","")
            
    if radidx[0].size > 0:
        if "±" in tab[radidx[0][0]][radidx[1][0]+1]:
            idx=tab[radidx[0][0]][radidx[1][0]+1].index("±")
            rad=tab[radidx[0][0]][radidx[1][0]+1][0:idx].replace(u"\xa0",u" ").replace(u",","")
        
    
    
    return tab[ar[0][0]][ar[1][0]+1]\
            .replace(u"\xa0",u" "), tab[dec[0][0]][dec[1][0]+1]\
                .replace(u"\xa0",u" "), tempt, rad
    
    

def obtenerConstelaciones():
    
    """
    Funcion para recuperar la tabla de constelaciones de wikipedia
    la cual contiene datos importantes, entre ellos la posicion y 
    el nombre
    """
    
    
    url="https://en.wikipedia.org/wiki/IAU_designated_constellations_by_area"
    pag=requests.get(url)
    
    print(pag.apparent_encoding)

    #contenido=BeautifulSoup(pag.content, "lxml")
    
    try:
        contenido=BeautifulSoup(pag.content,"lxml")

    except:
        print("Se recomienda instalar el paquete lxml con el comando pip install lxml")
        contenido=BeautifulSoup(pag.content, "html.parser")
    #contenido.encode("utf-8")
    
    pag.close()
    

    for tag in contenido.find_all(class_="reference"):
        tag.decompose()

    leg=contenido.find_all("tfoot")

    if leg:
        leg.decompose()
        
    tabla=contenido.find("table", class_="wikitable sortable")
    tab=pd.read_html(str(tabla))[0]

    return tab

def obtenerEstrellasConstelacion(constelacion):
    
    """
    Funcion para recuperar la tabla de estrellas de una constelacion
    de wikipedia la cual contiene datos importantes, entre ellos la 
    posicion y la distancia
    """
    
    
    #Reemplazamos los espacios por guiones bajos
    constelacion=constelacion.replace(" ", "_")
    
    #Por la forma organizada de wikipedia, podemos usar los nombres de las
    #constelaciones para acceder a su lista de estrellas
    url="https://en.wikipedia.org/wiki/List_of_stars_in_"+constelacion
    pag=requests.get(url)

    try:
        contenido=BeautifulSoup(pag.content,"lxml")
    except:
        print("Se recomienda instalar el paquete lxml con el comando pip install lxml")
        contenido=BeautifulSoup(pag.content, "html.parser")
        
    print(pag.apparent_encoding)
    #contenido.encode("utf-8")
    
    pag.close()
    

    for tag in contenido.find_all(class_="reference"):
        tag.decompose()

        
    tabla=contenido.find("table", class_="wikitable sortable")
    
    #Eliminamos la tabla con la leyenda
    for leg in tabla.find_all("tr", class_="sortbottom"):
        leg.decompose()
        
    tab=pd.read_html(str(tabla))[0]

    #Eliminamos la columna de notas que aparece en algunas tablas
    if "Notes" in tab.keys():
        tab.pop("Notes")
        

    return tab

def creaArchivoWikiTabla(tabla, nombre="constelaciones", ruta=""):
    
    llaves=list(tabla.keys())
    
    
    #Ya que otras codificaciones fallaron, fue mejor optar por utf-16 que fue el
    #unico formato que pudo manejar adecuadamente los caracteres especiales. Por 
    #alguna razon, excel no toma como separador a las comas en esa codificacion
    #pero si las tabulaciones
    
    cadena="\t".join(llaves)+"\n"
    
    forma=tabla.shape
    
    for i in range(forma[0]):
        for j in range(forma[1]):
            cadena+=f"{tabla[llaves[j]][i]}\t"
            
        cadena=cadena[:-1]
        cadena+="\n"
        
    cadena=cadena.replace("−","-")
        
    cadena=cadena.encode("utf-16")
    
    #cadena=cadena.encode("utf-8")
        
    if ruta and ruta[-1] != "/":
        ruta=ruta+"/"
        
    with open(ruta+nombre+".csv", "wb") as archivo:
        archivo.write(cadena)
        
def tablaClaseEspc():
    URL="http://www.isthe.com/chongo/tech/astro/HR-temp-mass-table-byhrclass.html"
    pag=requests.get(URL)
    
    try:
        contenido=BeautifulSoup(pag.content,"lxml")
    except:
        print("Se recomienda instalar el paquete lxml con el comando pip install lxml")
        contenido=BeautifulSoup(pag.content, "html.parser")
        
    tabla=contenido.find_all("table")[2]
    tab=pd.read_html(str(tabla))[0]
    #tab.pop(0)
    tab_t=tab.T
    
    for i in tab_t:
        if str(tab_t[i][1]) == "nan":
            tab_t.pop(i)
            
    tab=tab_t.T
    tab.to_csv(r"datosTipoEspectral.csv", index=False)


if __name__ == "__main__":
    
    #Ejecutar para crear la base de datos de constelaciones de forma local
    
    ruta="constelaciones"
    
    if not os.path.isdir(ruta):
        os.makedirs(ruta)
    
    const=obtenerConstelaciones()["Constellation"]
    
    ruta+="/"
    
    for c in const:
        if not os.path.isfile(ruta+c+".csv"):
            creaArchivoWikiTabla(obtenerEstrellasConstelacion(c),c,ruta)
    
    const=obtenerConstelaciones()
    
    creaArchivoWikiTabla(const)
    

    
    tablaClaseEspc()
    
    
    
    
    
    
    
    