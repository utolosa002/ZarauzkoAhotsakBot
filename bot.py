import os
import requests
from telegram import Bot
import asyncio
import hmac
import base64
import time
import urllib.parse
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import * 
import random

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_hizlaria():
    url = f'https://ahotsak.eus/zarautz/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find("table")
    hizlariak = results.find_all("tr")
    hizlaria=[]

    randoma=round(random.uniform(1, len(hizlariak)-1))

    url_element   = hizlariak[randoma].find(href=True)
    hizlari_datuak = hizlariak[randoma].find_all("td")[1]
    hizlari_izena   = hizlari_datuak.find("a").text
    #print('https://ahotsak.eus/zarautz/'+ url_element['href'])
    
####

    url_hizlaria = f'https://ahotsak.eus/zarautz/'+ url_element['href']
    response_hizlaria = requests.get(url_hizlaria)
    soup_hizlaria = BeautifulSoup(response_hizlaria.content, "html.parser")
    results_hizlaria = soup_hizlaria.find_all("table")

    pasarteak = results_hizlaria[1].find_all("tr")

    randoma=round(random.uniform(1, len(pasarteak)-1))
    url_pasartea_osoa = pasarteak[randoma].find(href=True)
    url_pasartea ='https://ahotsak.eus'+ url_pasartea_osoa['href']

####

    response_pasartea = requests.get(url_pasartea)
    soup_pasartea = BeautifulSoup(response_pasartea.content, "html.parser")
    results_pasartea = soup_pasartea.find("div", class_="laburpena")

    laburpena = results_pasartea.text
    hizlaria=[]
    hizlaria.append(hizlari_izena.strip())
    hizlaria.append(laburpena.strip())
    hizlaria.append(url_pasartea)

    return hizlaria

    

async def send_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_photo(photo, caption):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption=caption)

async def main():
    hizlaria = get_hizlaria()
    gaur = datetime.strftime(datetime.today(), '%Y/%m/%d')
    izena=hizlaria[0]
    laburpena=hizlaria[1]
    url=hizlaria[2]
    await send_message('Hizlaria: ' + izena + '\n\n' + laburpena + '\n\n' + url)
   
if __name__ == '__main__':
    asyncio.run(main())
