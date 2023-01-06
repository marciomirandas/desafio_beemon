from django.shortcuts import render, get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import IndexForm
from .models import Record, Tag

import time
import datetime
import pandas as pd
import logging
import json
import glob
import io
import sys
import os
import sched

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def process():

    """
    Função que realiza o web scraping no site 'https://quotes.toscrape.com/', salva os dados no banco e gera um json na variável global 'result'
    """
                
    logging.basicConfig(level=logging.INFO, filename='core/app.log', format='%(asctime)s - %(levelname)s - %(message)s')
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
            record = Record.objects.create(
                quote = quote,
                author = author,
                author_link = author_link,
                born = born_date,
                place = born_location,
                description = description,
                image = new_pic
                )


            # Pega todas os elementos com a classe 'tag'
            tags_div = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/div')
            tags = tags_div.find_elements(By.CLASS_NAME, 'tag')

            j = 1
            list_tags = []
            for tag in tags:
                
                tag_name = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/div/a[{j}]').text
                tag_link = driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[1]/div[{i}]/div/a[{j}]').get_attribute('href')

                list_tags.append({'tag_name' : tag_name, 'tag_link': tag_link})

                Tag.objects.create(
                    name = tag_name,
                    link = tag_link,
                    record = record
                )

                j += 1
            
            dictionary["tags"] = list_tags


            # Adiciona o dicionário a lista
            list.append(dictionary)
            i += 1

        
        # Tenta clicar no link da próxima página, se não existir, encerra o while
        try:
            nexts_pags_class = driver.find_elements(By.CLASS_NAME, 'next')
            nexts_pags_class[0].find_elements(By.TAG_NAME, 'a')[0].click()
            time.sleep(2)
                    
        except:
            break


    final = json.dumps(list, indent=4)
    jsonObj = json.loads(final)
    
    logging.info('Fim do programa')

    global result
    result = jsonObj


def sche(year, month, day, hour, minute):

    """
    Função que realiza o agendamento da função 'process'

    :param year: int
    :param month: int
    :param day: int
    :param hour: int
    :param minute: int
    """

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute).timestamp(), 1, process)
    scheduler.run()


def index(request):

    if str(request.method) == 'POST':
        form = IndexForm(request.POST)

        if form.is_valid():

            # Pega os dados do formulário
            date_form = str(form.cleaned_data.get('date')).split('-')
            time_form = str(form.cleaned_data.get('time')).split(':')

            # chama a função sche
            sche(int(date_form[0]), int(date_form[1]), int(date_form[2]), int(time_form[0]), int(time_form[1]))

            context = {
                'form': form,
                'json': result
            }

        else:

            context = {
                'form': form,  
            }

    else:
        form = IndexForm()
        context = {
            'form': form,
        }
    
    return render(request, 'index.html', context)


def data(request):

    # Pega todos os registros na ordem decrescente
    context = {
        'records': Record.objects.all().order_by('-id'),
        'tags': Tag.objects.all()  
        }
    
    return render(request, 'data.html', context)


def data_id(request, id):

    # Pega o registro a partir do id
    record = get_object_or_404(Record, id=id)
    
    context = {
        'record': record,
        'tags': Tag.objects.filter(record=record) 
        }
    
    return render(request, 'data_id.html', context)


def dataframe(request):

    # Cria um dataframe a partir de uma query
    record = Record.objects.all().values()

    if record:
        df = pd.DataFrame(list(record))
        df = df.drop('image', axis=1)
        df = df.drop('description', axis=1)

        # converte o dataframe em json
        json_records = df.reset_index().to_json(orient='records')
        list_json = []
        list_json = json.loads(json_records)

    else:
        list_json = None
    
    context = {
        'dataframe': list_json
        }
    
    return render(request, 'dataframe.html', context)


def log(request):

    # Verifica se existe algum dado no banco de dados
    record = Record.objects.all()

    if record:

        # Localiza o arquivo app.log
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'app.log')

        # Abre o arquivo
        with open(file_path) as file:
            file = file.readlines()
    
    else:
        file = None

    context = {
        'logs': file   
        }
    
    return render(request, 'log.html', context)

