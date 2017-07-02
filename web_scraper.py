# -*- coding: utf-8 -*-
"""
Created on Fri May 26 15:58:33 2017

@author: gbans6
"""

from lxml import html
import requests

'''page = requests.get('https://www.amazon.com/Sapiens-Humankind-Yuval-Noah-Harari/dp/0062316095/ref=sr_1_1?s=books&ie=UTF8&qid=1495828471&sr=1-1&keywords=homo+sapiens')
tree = html.fromstring(page.content)

hardcover_price = tree.xpath('//*[@id="a-autoid-6-announce"]/span[2]/span/text()')
test = tree.xpath('//*[@id="universal-detail-ilm"]')
print(test)
'''
page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)

#This will create a list of buyers:
buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

print(prices)