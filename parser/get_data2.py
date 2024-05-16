import pandas as pd
import requests
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def save_images(folder_name, images):
    for i, image in enumerate(images):
        image_url = image.get_attribute("src")
        print("IMG_URL", image_url)
        img_data = requests.get(image_url).content
        with open(f'{folder_name}/{i}.jpeg', 'wb') as handler:
            handler.write(img_data)

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
# options.add_argument('log-level=2')

driver = webdriver.Chrome(options=options)
driver.get("https://tripmir.com/routes/region/irkutskaya_oblast/index.html?viewed=&term=&type[0]=1&type[1]=2&type[2]=4&type[3]=5&type[4]=10&type[5]=13&days_count[min]=1&days_count[max]=31")
#"https://tripmir.com/routes/region/irkutskaya_oblast/index.html?viewed=&term=&type[0]=1&type[1]=2&type[2]=4&type[3]=5&type[4]=10&type[5]=13&days_count[min]=1&days_count[max]=31&page=2&per-page=15"

elements = driver.find_elements(By.CLASS_NAME, "tape__slider_title")
print(len(elements))

with open('./Ways_information.csv', 'a', encoding='utf-8') as f:
    for i, elem in enumerate(elements):
        # переход на страницу маршрута
        #elem = elem.find_element(By.TAG_NAME, "a")
        print(elem.get_attribute("href"))
        driver.execute_script("arguments[0].click();", elem)
        driver.switch_to.window(driver.window_handles[1]) 
        driver.implicitly_wait(10)

        #сбор данных
        way_text = driver.find_element(By.TAG_NAME, "h1").text
        print(way_text)
        
        read_full = driver.find_element(By.XPATH, f'//a[text()="Читать полностью"]')
        driver.execute_script("arguments[0].click();", read_full)

        description = driver.find_element(By.CLASS_NAME, "set-header__text")
        description = description.find_element(By.TAG_NAME, "p").text
        print(description)
        try:
            way_points = driver.find_element(By.CLASS_NAME, "accord__text")
            f.write(f'{way_text},"{description}",{elem.get_attribute("href")},{way_points}\n')
        except(Exception):
            print(f"{way_text} dont have availabled way points")
        
        #обратно на главную страницу
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(5)
    driver.quit()


