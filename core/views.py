from django.shortcuts import render, HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import IndexForm
from .models import Record

import time
import pandas as pd
import logging
import json
import glob
import io
import sys

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def index(request):
    
    if str(request.method) == 'POST':
        form = IndexForm(request.POST)

        if form.is_valid():

            logging.info('Inicio do programa')
            
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            driver.get("https://quotes.toscrape.com/")
            driver.set_window_size(1366, 768)
            time.sleep(2)

            list = []
            cont = 1

            while True:

                logging.info(f'Iteracao {cont}')
                cont +=1

                # Pega todas os elementos com a classe 'quote'
                div_principal = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]')
                divs = div_principal.find_elements(By.CLASS_NAME, 'quote')

                i = 1
                for div in divs:
                    dictionary = {}

                    # Pega os texto e os links da citação e do autor
                    quote = str(driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/span[1]').text)[1:-1]
                    dictionary["quote"] = quote

                    author = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/span[2]/small').text
                    author_link = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/span[2]/a').get_attribute('href')
                    dictionary["author"] = {"name" : author, "link": author_link}


                    # Pega todas os elementos com a classe 'tag'
                    tags_div = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/div')
                    tags = tags_div.find_elements(By.CLASS_NAME, 'tag')

                    j = 1
                    list_tags = []
                    for tag in tags:
                        
                        tag_name = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/div/a[{j}]').text
                        tag_link = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/div/a[{j}]').get_attribute('href')

                        list_tags.append({'tag_name' : tag_name, 'tag_link': tag_link})
                        
                        j += 1
                    
                    dictionary["tags"] = list_tags


                    # Entra na página do autor
                    driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/span[2]/a').click()
                    time.sleep(2)

                    # Pega o texto da página do autor
                    born_date = driver.find_element(By.XPATH, '/html/body/div/div[2]/p[1]/span[1]').text
                    born_location = driver.find_element(By.XPATH, '/html/body/div/div[2]/p[1]/span[2]').text
                    description = driver.find_element(By.XPATH, '/html/body/div/div[2]/div').text

                    # Salva a tela da página do autor
                    driver.save_screenshot('./media/temp/image.png')

                    # Converte a imagem salva para o formato a ser salvo no models
                    image = Image.open(glob.glob('media/temp/image.png')[0])
                    image = image.convert('RGB')
                    output = io.BytesIO()
                    image.save(output, format='png', quality=85)
                    output.seek(0)
                    new_pic= InMemoryUploadedFile(output, 'ImageField', 'field.png', 'image/jpeg', sys.getsizeof(output), None)

                    dictionary["page"] = {"date" : born_date, "location": born_location, "description": description}
                    
                    # Volta a página principal
                    driver.back()
                    time.sleep(2)


                    # Salva os dados no banco de dados
                    Record.objects.create(
                        quote = dictionary["quote"],
                        author = dictionary["author"],
                        tag = dictionary["tags"],
                        pag = dictionary["page"],
                        image = new_pic
                        )

                    # Adiciona o dicionário a lista
                    list.append(dictionary)
                    i += 1


                    # ----------- Povisório -----------
                    if i == 3:
                        break
                
                # Tenta clicar no link da próxima página, se não existir, encerra o while
                try:
                    break
                    nexts_pags_class = driver.find_elements(By.CLASS_NAME, 'next')
                    nexts_pags_class[0].find_elements(By.TAG_NAME, 'a')[0].click()
                    time.sleep(2)
                            
                except:
                    break

                
            final = json.dumps(list, indent=4)

            df = pd.read_json(final)
            df_html = df.to_html(index=False)
            
            direction = 1
            if direction == 0:
                return HttpResponse(df_html)

            elif direction == 1:
                jsonObj = json.loads(final)
            

            logging.info('Fim do programa')


            context = {
                'json': jsonObj,
                'df_html': df_html,
            }
    
    else:
        form = IndexForm()

        context = {
            'form': form,
        }
    
    return render(request, 'index.html', context)
