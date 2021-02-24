import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import numpy as np
from datetime import datetime
import time

url = "https://globoplay.globo.com/programacao/"
SCROLL_PAUSE_TIME = 2
load_page_wait = 20

option = Options()
#option.headless = True
option.add_argument("--headless")
option.add_argument("--log-level=3")


while True:    
    now = datetime.now()
    if ( int(now.strftime('%M'))%15==0.0 ):
        try:
            #driver = webdriver.Firefox(options=option, executable_path=r'geckodriver.exe')
            driver = webdriver.Chrome(options=option)


            print('chama url')
            driver.get(url)
            driver.implicitly_wait(load_page_wait)  # in seconds

            #elemento para pagedown
            tabela = driver.find_element_by_xpath("//div[@class='ReactVirtualized__Collection BodyGrid']")

            programa = set()

            i=0
            while i < 4:

                html_completo = driver.page_source
                soup = BeautifulSoup(html_completo, "html.parser")
                slots = soup.find_all(class_="epgv__slot")
                #print(nomes)

                for slot in slots:
                            
                    props = slot['style'].split(';')
                    canal = props[3]

                    soupDetalhe = BeautifulSoup(str(slot), "html.parser")
                    
                    hora = soupDetalhe.find(class_="epgv__program-time")
                    titulo = soupDetalhe.find(class_="epgv__program-title")
                    descricao = soupDetalhe.find(class_="epgv__program-description")

                    info = canal+ ";" + hora.text + ";" + str(titulo.text) + ";" + str(descricao.text) 
            
                    programa.add(info)
                    #print(props[3] + " - " + str(titulo.text) + " - " + str(descricao.text) + " - " + str(hora.text))

                    #programa = {
                    #    'canal'     : canal,
                    #    'titulo'    : titulo.text,
                    #    'descricao' : descricao.text,
                    #    'hora'      : hora.text
                    #}

                # Scroll down to bottom
                tabela.send_keys(Keys.PAGE_DOWN)
                # Wait to load page    
                #driver.implicitly_wait(SCROLL_PAUSE_TIME)
                
                i=i+1

            file = open('progs.txt', mode='at+', newline=None, encoding="utf-8")
                            
            file.write(str(programa)+"\n")
            file.close()

            driver.quit()

            #print(str(programa))
            time.sleep(65)

        except Exception as e:
            print(e)
            driver.quit()
            print()
            time.sleep(10)
            continue



