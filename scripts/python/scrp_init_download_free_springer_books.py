# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 08:36:28 2020

@author: Ashish
 Download Free Spring text books related to Python
"""

import requests
import wget
import pandas as pd
import os
# filePath = os.getcwd()
# print(filePath)
# # change working directory
os.chdir('C:\\Users\\Ashoo\\Documents\\playground_python\\scrapers\\')
filePath = os.getcwd()
print(filePath)

df = pd.read_excel("scripts\\python\\Free+English+textbooks.xlsx")
print(df.head(10))

for index, row in df.iterrows():
        # loop through the excel list
        file_name = f"{row.loc['Book Title']}_{row.loc['Edition']}".replace('/','-').replace(':','-')
        url = f"{row.loc['OpenURL']}"
        r = requests.get(url) 
        download_url = f"{r.url.replace('book','content/pdf')}.pdf"
        wget.download(download_url, f"data/free_springer_books/{file_name}.pdf") 
        print(f"downloading {file_name}.pdf Complete ....")
