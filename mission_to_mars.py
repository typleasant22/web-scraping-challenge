#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sysconfig import get_python_version


get_python_version().system(' pip install flask')


# In[2]:


import os
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import json


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[4]:


url = 'https://redplanetscience.com/'
browser.visit(url)


# In[5]:


browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[6]:


html = browser.html
html


# In[7]:


news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text') 
slide_elem


# In[8]:


news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Mars Space 

# In[10]:


url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[13]:


img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Pandas_Scrape

# In[15]:


url2='https://galaxyfacts-mars.com'
tables=pd.read_html(url2)
tables


# In[16]:


tables_df=tables[0]
tables_df


# In[17]:


mars_df= pd.DataFrame({'Mars Profile': tables_df[0],
                      'Measurements': tables_df[1]})
mars_df


# In[18]:


html_table=mars_df.to_html().replace('\n','')
html_table


# # Mars Hemispheres

# In[19]:


url3='https://marshemispheres.com'
browser.visit(url3)
html= browser.html
soup= soup(html,'html.parser')


# In[20]:


results= soup.find_all('div',class_='item')


# In[21]:


#create list for image URLs
hemisphere_image_urls=[]

for result in results:
    hemispheres= {}
    hemispheres['title']= result.find('h3').text
    hemispheres['image_url']= result.img['src']


# In[22]:


#append object
hemisphere_image_urls.append(hemispheres)


# In[23]:


print(json.dumps(hemisphere_image_urls, sort_keys=False, indent=4))


# In[ ]:




