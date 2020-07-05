# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:16:06 2020

@author: Mahi
"""

from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

import pandas as pd

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.get("https://www.bigbasket.com/cl/gourmet-world-food/?nc=nb")
sleep(10)
main=[]
for i in range(1,20):
    try:
        ele=driver.find_element_by_xpath('//*[@id="filterbar"]/div[2]/div/div/div/div/div/div['+str(i)+']')
        elem=ele.find_element_by_tag_name("a")
        main.append(str(elem.get_attribute("href")))
    except:
        break
    
name=[]
listing_price=[]
price=[]
weight=[]
category=[]
for link in main:
    
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(link)
    sleep(10)
    driver.maximize_window()
    url=[]
    for i in range(1,20):
        try:
            ele=driver.find_element_by_xpath('//*[@id="filterbar"]/div[2]/div/div/div/div/div/div/div['+str(i)+']')
            elem=ele.find_element_by_tag_name("a")
            url.append(str(elem.get_attribute("href")))
        except:
            break
    driver.quit()

    for i in url:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        driver.get(i)
        sleep(10)
        c=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div')
        cat=c.find_elements_by_tag_name("a")
        cate=''
        for k in cat:
            k1=k.text
            if("HOME"not in k1):
                cate+=k1.strip()+"///"
        category_name=cate[:len(cate)-3]            
                
        for j in range(1,20):
            try:
                n=driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div/div[2]/div/div['+str(j)+']/product-template/div/div[4]/div[1]/a')
                lp=driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div/div[2]/div/div['+str(j)+']/product-template/div/div[4]/div[3]/div/div[1]/h4/span[1]/span')
                p=driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div/div[2]/div/div['+str(j)+']/product-template/div/div[4]/div[3]/div/div[1]/h4/span[2]/span')
                
                try:
                    q=driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div/div[2]/div/div['+str(j)+']/product-template/div/div[4]/div[2]/div/span/button/span/span[1]')
                except:
                    q=driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div/div[2]/div/div['+str(j)+']/product-template/div/div[4]/div[2]/div[1]/span/span[1]')
                name+=[n.text]
                listing_price+=[lp.text]
                price+=[p.text]
                weight+=[q.text]
                category+=[category_name]
            except:
                break
        driver.quit()
    

df = pd.DataFrame() 
df['Product name'] = name
df['List price'] = listing_price
df['Price'] = price
df['Weight'] = weight
df['Category'] = category

df.to_excel('temp.xlsx', index = False) 