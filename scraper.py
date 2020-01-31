#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 20:11:49 2020

@author: TH
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
import os
from telegram.ext import Updater, CommandHandler

def open_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.findAll('div', class_ = 'card-post')
        for i in images:
            image_url = i.find('a').get('href')
            download_images(image_url)
            #print (image_url)
            
    else:
        return 0

def download_images(image_link):
    image_res = requests.get(image_link)
    image_soup = BeautifulSoup(image_res.text, "html.parser")
    
    # Return the title of that page
    title_div = image_soup.findAll('div', class_ = 'post-title')
    title = title_div[0].find('h2').text
    
    # Download all the images
    
    Path("{}".format(title)).mkdir(parents=True, exist_ok=True)
    # The links of all the images
    jpg_links = image_soup.findAll('div', class_ = 'separator')
    link = []
    for i in jpg_links:
        link.append(i.find('a'))
#    print (link)
    
    for i in tqdm(range(0, len(link))):
        dl = link[i].get('href')
        sample_name = str(i+1)
        img_file = requests.get(dl, allow_redirects = True).content
        with open('{}/{}.jpg'.format(title, sample_name), 'wb') as handler:
            handler.write(img_file)
    print ('{} download finish'.format(title))

def present_image(bot, update):
    
    url = get_url()
    image_res = requests.get(url)
    image_soup = BeautifulSoup(image_res.text, "html.parser")
    
    # Return the title of that page
    title_div = image_soup.findAll('div', class_ = 'post-title')
    title = title_div[0].find('h2').text
    
    #title_present(title)
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text = title) # Send title of images
    
    # Send Photos
    jpg_links = image_soup.findAll('div', class_ = 'separator')
    link = []
    for i in jpg_links:
        link.append(i.find('a'))
    for photos in link:
        image_url = photos.get('href')
#        img_file = requests.get(image_url, allow_redirects = True).content
#        chat_id = update.message.chat_id
#        bot.send_photo(chat_id=chat_id, photo=img_file)
        
        chat_id = update.message.chat_id
        bot.send_photo(chat_id=chat_id, photo = image_url)
#        send_photos()
    
def get_url():
    url_ = 'https://www.legendadult.net/2020/01/graphis-gals-yua-mikami-valentine-2018.html'
    return url_
    
#def title_present(bot, update, content):
#    chat_id = update.message.chat_id
#    bot.send_message(chat_id=chat_id, text = content)
    

#def send_photos(bot, update, url):
#    chat_id = update.message.chat_id
#    img_file = requests.get(url, allow_redirects = True).content
    


token = 'TOKEN'


    
#url_ = 'https://www.legendadult.net/search?updated-max=2020-01-30T02:40:00%2B08:00&max-results=40&start=0&by-date=false'
#open_link(url_)
