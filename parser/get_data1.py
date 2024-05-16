
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
driver = webdriver.Chrome(options=options)
driver.get("https://baikal-1.ru/tourism/routes-and-maps/")

ways_names = driver.find_elements(By.CLASS_NAME, "h3-link") # все названия маршрутов
kmls = driver.find_elements(By.XPATH, '//a[text()=".kml"]') # все ссылки на треки 
print(len(kmls))

# проход по всем маршрутам где трек доступен для скачивания
with open('./Ways_information.csv', 'a', encoding='utf-8') as f:
    for i, kml in enumerate(kmls):
        print(kml.get_attribute("href"))
        #скачивает только первый, пока не понимаю как поправить, скачала руками
        #driver.execute_script("arguments[0].click();", kml) # загрузка трека

        way_text = ways_names[i].text

        # переход на страницу маршрута
        link = driver.find_element(By.XPATH, f'//a[text()="{way_text}"]')
        driver.execute_script("arguments[0].click();", link)
        driver.switch_to.window(driver.window_handles[1]) 
        driver.implicitly_wait(15)

        # берём описание маршрута
        description = driver.find_elements(By.CLASS_NAME, "wpb_text_column")[11]
        description = description.find_element(By.CLASS_NAME, "wpb_wrapper")
        description = description.find_element(By.TAG_NAME, "p")
        print(driver.current_url)
        print(description.text)

        f.write(f'{way_text},"{description.text}",{kml.get_attribute("href")}\n')  

        #обратно на главную страницу
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(5)
    
    driver.quit()

