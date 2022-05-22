# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datosWiki import creaArchivoWikiTabla
import os

def creaBasePulsar():
    URL="http://www.johnstonsarchive.net/relativity/binpulstable.html"
    
    pag=requests.get(URL)
    
    soup=BeautifulSoup(pag.content,"lxml")
    
    tabla=soup.find("table")

    cambio=str(tabla).replace("right ascension<br/>declination", "ra</th><th>dec")
    cambio=cambio.replace("<colgroup><col/><col align=\"left\"/><col align=\"right\"/><col/><col align=\"left\"/><col align=\"left\"/><col align=\"right\"/><col align=\"right\"/></colgroup>",
                          "")
    
    cambio=re.sub(r"[^a-z]m<br/>","m</td><td>",cambio)
    cambio=re.sub(r"[^a-z]s<br/>","s</td><td>",cambio)
    
    tabla_i=pd.read_html(cambio)[0]
    
    return tabla_i
    
if __name__ == "__main__":
    creaBasePulsar()
    
    if not os.path.isfile("pulsar.csv"):
        creaArchivoWikiTabla(creaBasePulsar(),"pulsar","")