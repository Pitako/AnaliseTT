#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as py
import datetime as date

import numpy as np

from matplotlib import pyplot as plt

import seaborn as sns

import os

DIAS = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]


pd.options.display.float_format = '{:,.2f}'.format


# # Leitura dos arquivos com informações dos trendtopics

# In[3]:


source = "./"

dir_list = os.listdir(source)

os.chdir(source)

tt = pd.DataFrame()

for i in range(len(dir_list)):
    filename = dir_list[i]
    if filename.endswith('.txt'):
        print(filename)
        pdtt = pd.read_csv(filename, sep=";", header=None, names=['data','hashtag','qtd'], index_col=False, encoding='utf-8')
        pdtt.drop(pdtt[pdtt.qtd == 'None'].index, inplace=True)
        pdtt['qtd'] = pd.to_numeric(pdtt['qtd'])        
        tt = tt.append(pdtt,ignore_index=True)
           


# In[5]:


#https://www.dropbox.com/s/b9bhp4lhuhc2ja2/tt.txt?dl=0




# ## Quantidade de registros

# In[6]:


tt.count()


# In[7]:


tt.head()


# ## Tratamento dos dados

# A captura de dados aconteceu usando mais de uma máquina no começo e como existe a possibilidade de existir dados repetidos, foi feito um agrupamento para retirar a duplicidade nos horários.
# 
# E como não é possível garantir que exista informação em toda fração de 5 minutos, as quantidades de tweetts foram agrupados com valor médio

# In[ ]:





# In[8]:


tt_unique = tt.groupby(by=['data','hashtag'], as_index=False ).qtd.agg('max')


# #### Retirada de # da hashtag, padronização em caixa alta e soma dos iguais na mesma hora

# In[9]:


tt_unique['hashtag'] = tt_unique.apply(lambda row: row['hashtag'].upper().replace('#',''), axis=1)


# In[ ]:





# In[ ]:





# ### Tipo de dados Date 

# In[10]:


tt_unique['data'] = tt_unique.apply(lambda row: date.datetime.strptime(row.data,'%d/%m/%Y %H:%M:%S'), axis=1)


# ### Quantidade de registros únicos

# In[11]:


tt_unique.count()


# ### Período dos dados

# In[12]:


print('De {} até {}'.format(tt_unique.data.min(),tt_unique.data.max()))


# In[ ]:





# In[ ]:





# In[ ]:





# ### Criando colunas para separar horas e dia da semana

# In[13]:


# criando colunas com dia da semana em número (0-6) e texto
tt_unique['nDiaSemana'] = tt_unique.apply(lambda row: row.data.weekday(), axis=1)
tt_unique['diaSemana'] = tt_unique.apply(lambda row: DIAS[row.nDiaSemana], axis=1)
tt_unique['hora'] = tt_unique.apply(lambda row: row.data.hour, axis=1)
tt_unique['dma'] = tt_unique.apply(lambda row: row.data.date() , axis=1)


# In[14]:


# vendo o resultando
tt_unique.sort_values(by='dma')


# ### Agrupando por hora

# Agrupamento por hora será feito com média de ocorrências pra garantir que as hashtags tenham quantidades coerentes mesmo que algum período da hora não tenha capturado dados

# In[15]:


tt_unique_hora = tt_unique.groupby(by=['dma','hashtag','nDiaSemana','diaSemana','hora'], as_index=False ).qtd.agg('mean')


# In[16]:


tt_unique_hora = tt_unique_hora.sort_values(by=['dma','hora','hashtag'])
tt_unique_hora


# ### Preparar DataFrames

# #### Período completo

# Depois de calculada a média por hora, para exibir a informação durante todo o período decidi usar o somatório das quantidades pra ter uma noção mais próxima da quantidade de tweets que aconteceram

# In[17]:


diaMes = tt_unique_hora.groupby(by=['dma'], as_index=False).qtd.agg('sum')


# In[18]:


diaMes


# In[19]:


f, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x=diaMes.dma, y=diaMes.qtd, ci=None, ax=ax)


# In[ ]:





# #### Por hashtag por hora por dia da semana

# Soma de quantidades usado com mesmo raciocínio do gráfico anterior, de aproximar com a quantidade real

# In[20]:


#cálculo do valor total por hash, dia, hora
hashHora = tt_unique_hora.groupby(by=['hashtag','nDiaSemana','diaSemana','hora'], as_index=False).qtd.agg('sum')


# In[21]:


hashHora


# In[ ]:





# ### Agrupamentos para visualização

# Nos dataframes e gráficos seguintes, as quantidades foram calculadas com médias para que efeitos de outliers fossem diminuidos com o tempo

# #### Média por dia da semana

# In[25]:


diaQTD = tt_unique_hora.groupby(by=['nDiaSemana'], as_index=False).qtd.agg('mean')
diaQTD['diaSemana'] = diaQTD.apply(lambda row: DIAS[int(row.nDiaSemana)], axis=1)

fig, ax = plt.subplots(figsize=(15, 7))
#plt.bar(diaQTD.diaSemana,diaQTD.qtd)


# #### Média por hora

# In[27]:


#quantidade por hora
horaQTD = tt_unique_hora.groupby(by=['hora'], as_index=False).qtd.agg('mean')
#horaQTD
fig, ax = plt.subplots(figsize=(15, 7))
#plt.bar(horaQTD.hora,horaQTD.qtd)


# #### Média por hora por dia da semana

# In[28]:


#cálculo do valor médio por dia, hora
diaHora = tt_unique_hora.groupby(by=['nDiaSemana','diaSemana','hora'], as_index=False).qtd.agg('mean')
#diaHora


# In[29]:


diahoratabela = diaHora[['nDiaSemana','hora','qtd']].pivot(index='hora', columns='nDiaSemana', values='qtd')
fig, ax = plt.subplots(figsize=(15, 10))

#sns.heatmap(diahoratabela, cmap='YlGnBu', annot=True, fmt=".2f", vmin=diaHora.qtd.min(), vmax=diaHora.qtd.max(), linewidths=0.5, linecolor='white', cbar=False)

plt.xticks(np.arange(7) + .5, labels=DIAS)
ax.xaxis.tick_top()

#plt.show()


# In[ ]:





# ### Gravação de arquivo de dado analítico tratado

# In[22]:


tt_unique_hora.to_csv('trendsTratados.csv')


# In[ ]:




