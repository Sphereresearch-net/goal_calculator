#!/usr/bin/env python
# coding: utf-8

# In[159]:


import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# In[ ]:


st.title('Pianificatore per obiettivi')
image = Image.open(r'C:\Users\user\Downloads\Mauro_app\Goal.png')
st.sidebar.image(image, use_column_width=True)


# In[62]:





# In[ ]:


st.write('''###  ''')
st.write('''### Portafogli predefiniti''')


# In[157]:


portafogli = pd.read_excel(r'C:\Users\user\Downloads\Mauro_app\portafogli.xlsx')
portafogli = portafogli.set_index('ASSET ',1)
# portafogli = portafogli.drop('Unnamed: 2',1)
portafogli


# In[ ]:


st.write('''###  ''')
st.write('''### Seleziona i tuoi parametri''')


# In[ ]:


a1 = st.selectbox('Seleziona il portafoglio', list(portafogli.index))
a0 = st.number_input('Capitale iniziale', 10000) 
a3 = st.number_input('Obiettivo', 10000)
a2 = st.slider('Orizzonte temporale in mesi', 0,200, 36)


# In[128]:


## 
scelta = a1
mu = portafogli['REND.ATTESO'][scelta]
mu = (mu+1)**(1/12)

sigma = portafogli['''VOL.ATTESA'''][scelta]
sigma = sigma/(12**(1/2))


# In[151]:



def montecarlo(start, mu, sigma):
    lista_serie = []

    for i1 in range(300):
        lista = [start]
        for i in range (a2):
            rend = random.normalvariate(mu, sigma)
            lista.append(rend)
        lista_serie.append(lista)

    df = pd.DataFrame(lista_serie)
    df = df.transpose()
    df = df.cumprod()
    return df


# In[154]:


df = montecarlo(a0,mu, sigma)


# In[156]:


st.write('''###  ''')
st.write('''### Rappresentazione grafica di 300 simulazioni''')


df['index']= df.index
df = df.set_index('index')
df_ = np.log(df)
st.line_chart(df)


# ## Calcolo le probabilità ad un dato orizzonte

# In[148]:


obiettivo = a3
rilevazione = a2

campionamento = df.head(rilevazione).tail(1)


campionamento_ = np.array(campionamento)


proba = len(np.where(campionamento_>obiettivo)[0])/300
st.write('''###  ''')
st.write('''### La probabilità calcolata di ragiungere il tuo obiettivo è: ''', round(proba*100,2), ''' %''')


# # Ad ora le variabili da modificare sono: 
# - media e varianza
# - orizzonte temporale (rilevazione)
# - importo iniziale 
# 

# In[138]:


st.write('''###  ''')
st.write('''### Statistiche sull' orizzonte selezionato ''')

statistiche = campionamento.transpose().describe()
statistiche = statistiche.drop(['count', 'std', 'min', 'max'],0)
statistiche['statistiche'] = statistiche.values
statistiche = statistiche[['statistiche']]
statistiche


# In[ ]:



