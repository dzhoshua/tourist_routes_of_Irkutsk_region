import pandas as pd
import time
import random
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


options = Options()
driver = webdriver.Chrome(options=options)

df = pd.read_csv("Ways_information2.csv") # маршруты которые будут геокодироваться
new_df = pd.DataFrame({"Наименование маршрута":[],
     "name":[],
     "query":[],
     "url":[],
     "short_name":[],
     "address":[],
     "coords":[],
     "lat":[],
     "lon":[],
     "source":[],
     "N_point":[]})
geolocator = Nominatim(user_agent="124.0.0.0")

hand_work = []
for i, points in enumerate(df["Пункты маршрута"]):
    way_name = df['Наименование маршрута'][i]
    source  = df['source'][i]
    city = df['Город'][i]
    points = points.split("|")
    for j in range(len(points)):
        # формируем и посылаем запрос
        search_string = f"{points[j]}, {city}"
        search_string = search_string.replace(' ', '+')
        search_string = search_string.replace(',', '%2C')

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com/search?q=" + search_string)

        address = None
        name = None
        # ищем адрес и имя пункта
        try:
            address = driver.find_element(By.CLASS_NAME, "LrzXr").text
            print(address)
        except:
            print(f"{way_name}, {points[j]}, Couldnt find address")
            print(search_string)
            hand_work.append(["searching",way_name, search_string])

        if address is not None:
            try:
                name = driver.find_element(By.CLASS_NAME, "DoxwDb")
                name = name.find_element(By.CLASS_NAME, "PZPZlf").text
                print(name)
            except:
                try:
                    name = driver.find_element(By.CLASS_NAME, "SPZz6b")
                    name = name.find_element(By.TAG_NAME, "span").text
                    print(name)
                except:
                    print(f"{way_name}, {points[j]}, Couldnt find name")
                    print(search_string)
                    hand_work.append(["searching",way_name, search_string])
                    
        # геокодируем найденный адрес
        if address is not None and name is not None:
            try:
                location = geolocator.geocode(address, language="ru")
                lat, lon = location.latitude, location.longitude
                coords = f"{lat}, {lon}"
                print(coords)
                
                # запись в датафрейм
                new_df.loc[ len(new_df.index )] = [way_name, f"{city}, {points[j]}", "","", name, address, coords, lat, lon, source, j+1]
            except:
                new_df.loc[ len(new_df.index )] = [way_name, f"{city}, {points[j]}", "","", name, address, "", "", "", source, j+1]
                hand_work.append(["geocode",way_name, name, address])
                print("---ERROR IN GEOCODE:", way_name, points[j])
        else:
            new_df.loc[ len(new_df.index )] = [way_name, f"{city}, {points[j]}", "","", "", "", "", "", "", source, j+1]
        
        time.sleep(random.randint(5, 15))

print("--SHAPE-- ", new_df.shape)
# запись датафрейма в файл с маршрутами
new_df.to_csv('WayPoint_coords.csv', mode='a', index= False , header= False )
print("Data was added successfuly.")
print(hand_work)


