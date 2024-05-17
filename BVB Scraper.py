#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
from bs4 import BeautifulSoup


# In[9]:


def get_info(string):
    # returns the current value, the daily variation in % and the min value and max value
    values = []
    
    URL = string
    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text,'lxml')
    
    price = soup.find('div', { 'class' : 'col-lg-5 col-xs-5 text-left pLeft0 tooltip-value' } ).find('b', class_='value').text
    values.append(price)
    
    variation_poz = soup.find('div', { 'class' : 'col-lg-3 col-xs-4 pRight0 pLeft0 text-left' } ).find('span', class_='text-center tooltip-trigger large w100p positive dropup text-shadow-d')
    variation_neg = soup.find('div', { 'class' : 'col-lg-3 col-xs-4 pRight0 pLeft0 text-left' } ).find('span', class_='text-center tooltip-trigger large w100p red text-shadow-d')
    
    if(variation_poz is None and variation_neg is None):
            variation = "0.00%"
            MinMax_value_search = " "
            
    elif(variation_poz is None):
        variation = variation_neg.text
        
    elif(variation_neg is None):
        variation = variation_poz.text
       
    values.append(variation)
    
    MinMaxList = []
    Min_Max_table = soup.find('div', { 'class' : 'col-lg-3 col-xs-3 pRight0' } ).find_all("tr")
    for row in Min_Max_table :
        cells = row.find_all('td')
        cell_texts = [cell.get_text(strip=True) for cell in cells]
        MinMaxList.append(cell_texts[1])
    
    values.append(MinMaxList)
    
    return values


# In[10]:


# Test get_info

symbol = "TLV"
URL = "https://bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s="
URL = URL + symbol
values = get_info(URL)
print (f"Pretul actiunii   : {symbol} este {values[0]}")
print (f"Variatia actiunii : {symbol} este {values[1]}")
print (f"Pretul minim      : {symbol} este {values[2][0]}")
print (f"Pretul maxim      : {symbol} este {values[2][1]}")


# In[11]:


import os
import xml.etree.ElementTree as ET

def new_profile(username):
    # I want the user to load it's profile via a XML file
    # so this function creates a new profile for a user
    
    file_path = f'Profiles/{username}' + "'s_profile.xml"
    
    if os.path.exists(file_path):
        print("Portoflio already exists !")
    
    else :
        root = ET.Element("Profile")

        tree = ET.ElementTree(root)

        e_watchlist = ET.Element("Watchlist")
        root.append(e_watchlist)

        e_portfolio = ET.Element("Portfolio")
        root.append(e_portfolio)

        tree.write(file_path)


# In[12]:


# Test new_portfolio
new_profile("Mihai")


# In[13]:


# As profile has to have a watchlist and a  portfolio these functions add to the watchlist/portfolio a certain index

# buying a stock also requires a quantity 
def add_2_portfolio(username, symbol, quantity):
    file = f'Profiles/{username}' + "'s_profile.xml"
    
    et = ET.parse(file)
    root = et.getroot()
    
    where_2_append = root.find('.//Portfolio')
    
    new_symbol = ET.Element("Symbol")
    new_symbol.text = quantity
    new_symbol.set('symbol', symbol)
    
    where_2_append.append(new_symbol)
    
    et.write(file)
    
# while as adding it to your watchlist does not
def add_2_watchlist(username, symbol):
    file = f'Profiles/{username}' + "'s_profile.xml"
    
    et = ET.parse(file)
    root = et.getroot()
    
    where_2_append = root.find('.//Watchlist')
    
    new_symbol = ET.Element("Symbol")
    new_symbol.text = symbol
    
    where_2_append.append(new_symbol)
    
    et.write(file)

   


# In[14]:


add_2_portfolio("Mihai","TLV",str(10))


# In[15]:


add_2_watchlist("Mihai","TLV")


# In[ ]:




