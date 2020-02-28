#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:19:05 2020

@author: TH
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
#import os
import telegram
from telegram.ext import Updater, CommandHandler


    
    

def search(bot, update):
    code = update.message.text
    url = 'http://javbus.com/{}'.format(code)
    
    response = requests.get(url)
    content = BeautifulSoup(response.text, "html.parser")
#    print ('Search seccess')
    try:
        title_name = content.find("h3").text
        # Scrap the cover image
        bigImage = content.find_all('a', class_ = 'bigImage')
    
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text = title_name)
        bot.send_message(chat_id=chat_id, text = 'Headphoto:')# Send title of images
    
        for i in tqdm(bigImage):
            bigImage_s = i.get('href')
            bot.send_photo(chat_id=chat_id, photo = bigImage_s)
    
        print ('Head image download finish!')
    
        bot.send_message(chat_id=chat_id, text = 'Class:')
    
    
        genre = content.findAll('span', class_ = 'genre')
        for i in genre:
            txt = i.find('a').text
            lk = i.find('a').get('href')
#           bot.send_message(chat_id=chat_id,
#                         text = txt)
            bot.send_message(chat_id=chat_id, 
                         text = '<a href = "{}">{}</a>'.format(lk, txt),
                         parse_mode=telegram.ParseMode.HTML)
##        
##        bot.send_message(chat_id=chat_id, 
##                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', 
##                 parse_mode=telegram.ParseMode.HTML)
#    
        bot.send_message(chat_id=chat_id, text = 'Sample Images:')
    
        sample_image = content.find_all('a', class_ = 'sample-box')# Scrape the sample images
        for i in tqdm(sample_image):
            try:
                sample = i.get('href')
                bot.send_photo(chat_id = chat_id, photo = sample)
            except:
                continue
    
        bot.send_message(chat_id=chat_id, text = 'Finish, {} photos in total'.format(len(sample_image)))
    
        print ('Sample images download finish!')
    
        bot.send_message(chat_id=chat_id, text = 'Link: {}'.format(url))
    except:
        chat_id=update.message.chat_id
        bot.send_message(chat_id=chat_id, text = 'Wrong movie code! Try to change to another one.')
#    print (code)

#def search():
    