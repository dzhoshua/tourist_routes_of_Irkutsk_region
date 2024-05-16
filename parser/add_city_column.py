import pandas as pd
import numpy as np


df = pd.read_csv('WayPoint_coords.csv')
df2 = pd.read_csv('Ways_information2.csv')

for i in range(420, df.shape[0]):
    for j in range(df2.shape[0]):
        if df['Наименование маршрута'][i] == df2['Наименование маршрута'][j]:
            df['name'][i] = f"{df2['Город'][j]}, {df['name'][i]}"
            break
# print(df['name'][420:435])

df['city']=np.nan

df['name'][248]=f"Иркутск, {df['name'][248]}"
for i in range(df.shape[0]):
    first_part = df['name'][i].split(", ")[0]
    if first_part=="Иркутская область":
        tmp = df['name'][i].split(", ")[1].split(" ")
        if len(tmp)>1 and tmp[0]=="г.":
            df['city'][i] = tmp[1] 
        else:
            df['city'][i] = df['name'][i].split(", ")[1]
    else:
        df['city'][i] = first_part


categories = df['city'].unique()
print(list(categories))
df.to_csv('WayPoint_coords.csv', mode='w', index= False)