#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 01:10:33 2020

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
import random
import telegram
import timeit

def open_url():
    page_num = random.randint(1, 147)
    javbus = 'https://www.javbus.com/page/{}'.format(page_num)
    response = requests.get(javbus)
    html = BeautifulSoup(response.text, "html.parser")
    first_page_links = []
    for link in html.findAll('a', class_="movie-box"):
#        print (link.get('href'))
        first_page_links.append(link.get('href'))
    mov_num = random.randint(0, 29)
    return first_page_links[mov_num]

    
def javpop(bot, update):
    
    url = open_url()
    start = timeit.default_timer()
    respond = requests.get(url)
    content = BeautifulSoup(respond.content, "html.parser")
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
    
    
    # For director, studio(producer), label(seller), series
    header_list = []
    name_list = []
    for i in content.findAll('p'):
        t = i.find('a')
        try :
            print (t.text)
            e = t.get('href')
        
            header_list.append(e)
            name_list.append(t.text)
        except:
            continue
    
    name_list = name_list[0:-3]
    header_list = header_list[0:-3]
    
    try:
        bot.send_message(chat_id=chat_id, 
                         text = '导演：<a href = "{}">{}</a>'.format(header_list[0], name_list[0]),
                         parse_mode=telegram.ParseMode.HTML)
                         
    except:
        bot.send_message(chat_id=chat_id,
                         text = '导演：未知')
    
    try:
        bot.send_message(chat_id=chat_id, 
                         text = '制作商：<a href = "{}">{}</a>'.format(header_list[1], name_list[1]),
                         parse_mode=telegram.ParseMode.HTML)
                         
    except:
        bot.send_message(chat_id=chat_id,
                         text = '制作商：未知')
        
    try:
        bot.send_message(chat_id=chat_id, 
                         text = '发行商：<a href = "{}">{}</a>'.format(header_list[2], name_list[2]),
                         parse_mode=telegram.ParseMode.HTML)
                         
    except:
        bot.send_message(chat_id=chat_id,
                         text = '发行商：未知')
        
    try:
        bot.send_message(chat_id=chat_id, 
                         text = '系列：<a href = "{}">{}</a>'.format(header_list[3], name_list[3]),
                         parse_mode=telegram.ParseMode.HTML)
                         
    except:
        bot.send_message(chat_id=chat_id,
                         text = '系列：暂无')
    
    bot.send_message(chat_id=chat_id, text = 'Class:')
    
    
    genre = content.findAll('span', class_ = 'genre')
    for i in genre:
        txt = i.find('a').text
        lk = i.find('a').get('href')
#        bot.send_message(chat_id=chat_id,
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
    stop = timeit.default_timer()
    bot.send_message(chat_id=chat_id, text = 'Finish in {} seconds, {} photos in total'.format(round(stop - start, 2), len(sample_image)))
    
    print ('Sample images download finish!')
    
    bot.send_message(chat_id=chat_id, text = 'Link: {}'.format(url))
    
    
    
    
    
    
    