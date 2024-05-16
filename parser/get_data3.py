import pandas as pd
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
# options.add_argument('log-level=2')

driver = webdriver.Chrome(options=options)

urls = ["https://izi.travel/ru/43c2-irkutsk/ru",
        "https://izi.travel/ru/e7ec-animalisticheskie-skulptury-irkutska/ru",
        "https://izi.travel/ru/1dc4-marshruty-irkutska-stranicy-pobedy/ru",
        "https://www.izi.travel/ru/99b9-dostroprimechatelnosti-goroda-zima/ru",
        "https://www.izi.travel/ru/0335-kulturnyy-marshrut-po-gorodu-ust-ilimsku/ru",
        "https://www.izi.travel/ru/303e-istoriya-v-paru-shagov/ru",
        "https://www.izi.travel/ru/4297-cheremkhovo/ru",
        "https://www.izi.travel/ru/a3e4-lyudi-pamyatniki/ru",
        "https://www.izi.travel/ru/3e69-chto-posmotret-v-sayanske/ru",
        "https://www.izi.travel/ru/4810-khramy-slyudyanskogo-rayona/ru",
        "https://www.izi.travel/ru/4f6f-marshruty-baykala-slyudyanka/ru",
        "https://www.izi.travel/ru/7001-progulki-po-staromu-ust-kutu/ru",
        "https://www.izi.travel/ru/2579-zheleznogorsk-ilimskiy-pamyatnye-mesta/ru"]


with open('./Ways_information2.csv', 'a', encoding='utf-8') as f:
    for i in range(len(urls)):
        driver = webdriver.Chrome(options=options)
        driver.get(urls[i])

        city = driver.find_element(By.CLASS_NAME, "meta__item--city")
        city = city.find_element(By.TAG_NAME, "a").text
        print(city)
        way_points=""
        
        way_text = driver.find_element(By.CLASS_NAME, "masthead__title").text
        print(way_text[9:])

        # берём описание маршрута
        link = driver.find_element(By.CLASS_NAME, "tour__itinerary-link")
        driver.execute_script("arguments[0].click();", link)
        description = driver.find_element(By.CLASS_NAME, "tour__details")
        try:
            description = description.find_element(By.TAG_NAME, "p").text
            print(description)
        except:
             description="-"

        iterations = driver.find_elements(By.CLASS_NAME, "tour__itinerary-link")[1:]
        print("iterations------------------", len(iterations))
        for j in iterations:
            point_name = j.find_element(By.CLASS_NAME, "tour__itinerary-label").get_attribute("title")
            if point_name =="":
                point_name = j.find_element(By.CLASS_NAME, "tour__itinerary-label").text
            way_points+=point_name+"|"
        description = description.replace('"', "'")
        way_points = way_points.replace('"', "'")
        f.write(f'{way_text[9:]},{city},"{description}",{urls[i]},"{way_points[:-1]}"\n')
        driver.implicitly_wait(5)
        driver.close()

#собрать в таблицу маршрут, описание и картинки(?) и сохранить в отдельную таблицу

