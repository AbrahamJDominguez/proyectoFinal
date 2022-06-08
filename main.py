# coding: latin1
# Modulo principal
import sys
#sys.path.append("C:/Users/cimen/Documents/POOE/proyectoFinal-main/")
import seleccionObjeto as SO
import lecturaArchivos as Lec
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

#ruta = "C:/Users/cimen/Documents/POOE/proyectoFinal-main/"
ruta=""

lectura = Lec.lecturaArchivos(ruta)
name, sep, enc = lectura.inicializar()

seleccionO = SO.coordenadas('', '', '')

# =============================================== Búsqueda ====================================================
def busqueda(archivo, nombreArchivo): # Busca todos los objetos cercanos a las coordenadas escritas
    nombres, lista_index, coord = [], [], []
    
    for index in range(len(archivo)):
        
        
        if nombreArchivo == 'constelaciones':
            radio = 60
            if ((archivo[index][0] - float(seleccionO.ar))**2 + (archivo[index][1] - float(seleccionO.dec))**2) <= float(radio)**2:
                nombre_aux = [archivo[index][-2], archivo[index][-1]]
                nombres.append(nombre_aux)
                lista_index.append(index)
                coord.append([archivo[index][0], archivo[index][1]])
                
        elif nombreArchivo == 'MessierCatalogo':
            distancia = ((archivo[index][0] - float(seleccionO.ar))**2 + (archivo[index][1] - float(seleccionO.dec))**2)**(1/2)
            if distancia < float(seleccionO.radio) + float(archivo[index][2]):
                print(distancia, float(seleccionO.radio) + float(archivo[index][2]))
                nombres.append(archivo[index][-1])
                lista_index.append(index)
                coord.append([archivo[index][0], archivo[index][1]])
                
        elif ((archivo[index][0] - float(seleccionO.ar))**2 + (archivo[index][1] - float(seleccionO.dec))**2) <= float(seleccionO.radio)**2:
            nombres.append(archivo[index][-1])
            lista_index.append(index) 
            """ Agregué una lista para guardar las coordenadas de cada objeto dentro del radio """
            coord.append([archivo[index][0], archivo[index][1]])        
    
    return nombres, lista_index, coord

# ================================================ Inicio =====================================================
def datosIniciales():    
    global name, sep, enc
    
    # Usamos el modulo para preguntar los datos principales al usuario
    seleccionO.entradaC()
    ####### Try: (254.457, 35.3420) or (16 57 49.8110126616 +35 20 32.486555472) [Her X-1]
    ####### Try: (05 40 45.52666 -01 56 33.2649) [* zet Ori/ Altinak]
    
    # Obtenemos los datos de cada catálogo (creamos objetos de la clase lecturaArchivos)
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


    # Buscamos objetos dentro del radio 
    """ A cada objeto le corresponde una lista de coordenadas """
    nombresM, listaIndM, coordM = busqueda(messierCat, "MessierCatalogo")       # objetos Messier
    nombresP, listaIndP, coordP = busqueda(planetas, "planetas")                # planetas
    nombresC, listaIndC, coordC = busqueda(constelaciones, "constelaciones")    # constelaciones
    # estrellas (por medio de Messier de Gaia)
    
    if nombresC and len(nombresC) == 1:
        print('\nLas coordenadas ingresadas se ubican en la constelación de ' + str(nombresC[0][0]) + ' ('+ str(nombresC[0][1]) + ').')
    
    elif nombresC and len(nombresC) >= 2:
        print("""\nNo se identificó con presición la posición de las coordenadas ingresadas,
pero el objeto podría estar en alguna de las siguientes constelaciones:""")
        for i in range(len(nombresC)):
            print(str(i+1) + '. ' + str(nombresC[i][0]))
        
    else: 
        print("\nNo se localizaron las coordenadas ingresadas en ninguna constelación conocida.")
        
        
        
    
    """ Construí una lista concatenada con las tres listas de objetos para usarla al momento de que el usuario elija el objeto """
    listaC = []
    listaC = coordM + coordP + coordC
    indexAux = 0
    
    cont1 = 0
    print("\nSe encontraron los siguientes objetos cercanos a las coordenadas ingresadas:\n")
    if nombresM:
        print("============== Estrellas cercanas a los Messier ==============")
        indiceEM={}
        for nom in range(len(nombresM)):
            print(str(cont1+1) + '. ' + "Estrellas cercanas a " + str(nombresM[nom]))
            cont1 += 1    
            indiceEM[cont1]=nombresM[nom]
    else:
        print("============== Estrellas cercanas a los Messier ==============")
        print("* No se encontraron objetos Messier cercanos a las coordenadas ingresadas.")
            
    if nombresP:
        print("========================== Planetas ==========================")
        for nom in range(len(nombresP)):
            print(str(cont1 + 1) + '. ' + str(nombresP[nom]))
            cont1 += 1
            
    else:
        print("========================== Planetas ==========================")
        print("* No se encontraron planetas cercanos a las coordenadas ingresadas.\n")
        
    if nombresC:
        print("=============== Estrellas en las constelaciones ==============")
        indiceC = {}
        for nom in range(len(nombresC)):
            print(str(cont1 + 1) + '. ' + str(nombresC[nom][0]))
            cont1 += 1
            indiceC[cont1] = nombresC[nom][0]

    mapa = {}
    print("======================= Otras opciones =======================")
    print(str(cont1 + 1) + '. Mapa estelar')
    cont1+= 1
    mapa[cont1] = "mapa"
    
    #if not nombresM and not nombresP and not nombresE:
    if not nombresM and not nombresP:
        print("No se encontraron objetos cerca de las coordenadas ingresadas. \nLe recomendamos ampliar el radio de búsqueda.")
    #if nombresM or nombresP or nombresE:
    if nombresM or nombresP:
        opcion = int(input("\nSeleccione los elementos con los que desea trabajar (p.ej. 1,6,8): "))
        """ Cuando el usuario elija un objeto, el código va a buscar las coordenadas de ese objeto en la lista concatenada """
        num = opcion - 1
        
        if opcion in indiceEM:
            messier = SO.messier("ar", "dec", "radio", 'tipo', 'Mabsoluta', 'tamaño', 'dist')
            messier.estrella(indiceEM[opcion])
            
        elif opcion in indiceC:
            constelacion = SO.constelacion("ar", 'dec', 'radio', 'abrev', 'solidAA', 'solidAM', 'perc', 'quad')
            constelacion.const(indiceC[opcion])
            
        elif opcion in mapa:
            print("""
=====================================================
                Gráficas de Gaia Archive
1. Mapa estelar de pulsares.
2. Mapa estelar de constelaciones.
3. Mapa estelar de messier.
=====================================================""")
            opcion = int(input("Seleccione una opcion: "))
            if opcion == 1:
                objeto = SO.objetoEstelar(pulsaresAr, pulsaresDec, [])
                objeto.crearMapaEstelar([],[])
            elif opcion == 2:
                objeto = SO.objetoEstelar(constAr, constDec, [])
                objeto.crearMapaEstelar([],[])
            elif opcion == 3:
                objeto = SO.objetoEstelar(messAr, messDec, [])
                objeto.crearMapaEstelar([],[])
            else: 
                print("Opción no válida")
            
        else:
            coord = listaC[num]
            if coord in coordM:
                messier =SO.messier(coord[0], coord[1], seleccionO.radio, "tipo", "Mabsoluta", "tamaño", "dist")
                messier.cumulos()
                
            elif coord in coordP:
                index = coordP.index(coord)
                index = (np.array(planetas).transpose().tolist())[-1].index(nombresP[index])
                
                Nnom = []
                planeta = SO.Planeta(coord[0], coord[1], seleccionO.radio, planetas[index][3], planetas[index][4], planetas[index][5], planetas[index][6], planetas[index][7], planetas[index][8], planetas[index][9], planetas[index][10], planetas[index][2])
                planeta.pl()
                fig, func= planeta.sistemaPlanetario()
                
                def anim(i):
                    return func(i)
                
                ani = FuncAnimation(fig, anim , repeat=True)
                
                plt.show()
                #print(planetas[index][4])
                #if planetas[index][4] >= 2:
                #    for nom in nombresP:
                #        if nom[0:5] == nombresP[index][0:5]:
                #            Nnom.append(nom)
                #    print(Nnom)
                    
                #elif planetas[index][4] == 1:
                #else:
                #    planeta = SO.Planeta(coord[0], coord[1], seleccionO.radio, planetas[index][3], planetas[index][4], planetas[index][5], planetas[index][6], planetas[index][7], planetas[index][8], planetas[index][9], planetas[index][10], planetas[index][2])
                #    planeta.pl()
                #    planeta.sistemaPlanetario()
                
            else:
                conste = SO.constelacion(coord[0], coord[1], seleccionO.radio, "abrev", 'solidAA', 'solidAM', 'perc', 'quad')
                conste.const()
            
    
# ================================================= Main ======================================================
# Mandamos llamar funciones
datosIniciales()