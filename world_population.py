#!/usr/bin/env python
# coding: utf-8



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as mp
import base64

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('World Population Count')

st.markdown("""
This app performs simple webscraping and visualisation of wikipidea world count data 
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, BeautifulSoup 
* **Data source:** [wikipidea.com](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population).
""")
choices=['Population By Region', 'Population By Country']
st.sidebar.header('Choose a Visualisation')
selected_choice = st.sidebar.selectbox('choose',choices)
@st.cache

def load(choice):
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    html = pd.read_html(url, header = 0, flavor = 'bs4')
    df = html[0]
    df = df.drop(['Notes'], axis = 1) # Deletes 'Notes' column 
    df = df.drop(['Source (official or from the United Nations)'], axis = 1) # Deletes 'Sources' column 

    df = df.iloc[1:]

    df['UN Region'] = df['UN Region'].str.replace('[[b]]', "")
    df['UN Region'] = df['UN Region'].str.replace('[[c]]', "")
    df['UN Region'] = df['UN Region'].str.replace('[[]', "")

    df['Percentage of the world'] = df['Percentage of the world'].str.replace("%", "")
    df['Percentage of the world'] = df['Percentage of the world'].astype(float)
    
    if choice == choices[0]:
        result = region(df)
        result.plot('UN Region', kind = "bar", figsize = (9, 8) )

    
    else:
        result = country(df)
        result.head(20).plot(x = "Country / Dependency", y = "Population", kind = "bar", figsize = (9, 8))

    return result
# Web scraping of wikipidea population count page
def country(df):
    return df.sort_values(by = ['Population'], ascending=False )
#group data by regions to count population by each region 
def region(df):
    return df.groupby('UN Region', as_index=False).agg({"Population": "sum"}).sort_values(by = ['Population'], ascending = False)
        
dataa = load(selected_choice)
        

st.header('World Population count')
st.write('Data Dimension: ' + str(dataa.shape[0]) + ' rows and ' + str(dataa.shape[1]) + ' columns.')
st.dataframe(dataa)

def filedownload(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href = "data:file/csv;base64,{b64}" download = "stats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(dataa), unsafe_allow_html = True)
st.pyplot()

