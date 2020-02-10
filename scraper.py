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

global title_list
global main_list

title_list = []
#main_list = ['https://www.legendadult.net/2020/02/xiuren-no1784-shen-meng-yao.html', 'https://www.legendadult.net/2020/02/xiuren-no1783-meng-xin-yue.html', 'https://www.legendadult.net/2020/02/xiuren-no1782-alice.html', 'https://www.legendadult.net/2020/02/xiuren-no1781-arjun.html', 'https://www.legendadult.net/2020/02/xiuren-no1780-lu-xuan-xuan.html', 'https://www.legendadult.net/2020/02/xiuren-no1778-sugar.html', 'https://www.legendadult.net/2020/02/xiuren-no1777-xiao-jiu-yue.html', 'https://www.legendadult.net/2020/02/xiuren-no1776-lele.html', 'https://www.legendadult.net/2020/02/xiuren-no1774-sandy.html', 'https://www.legendadult.net/2020/02/xiuren-no1772-nn.html', 'https://www.legendadult.net/2020/02/xiuren-no1771-sugar.html']
main_list = []
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
    
    url = page_list()
    image_res = requests.get(url)
    image_soup = BeautifulSoup(image_res.text, "html.parser")
    
    # Return the title of that page
    title_div = image_soup.findAll('div', class_ = 'post-title')
    title = title_div[0].find('h2').text
    
    # title_present(title)
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text = title) # Send title of images
    print('\nTitle: {}\n'.format(title))
    # Send Photos
    jpg_links = image_soup.findAll('div', class_ = 'separator')
    link = []
    for i in jpg_links:
        link.append(i.find('a').get('href'))
    for photos in tqdm(link):
#        image_url = photos.get('href')
#        img_file = requests.get(image_url, allow_redirects = True).content
#        chat_id = update.message.chat_id
#        bot.send_photo(chat_id=chat_id, photo=img_file)
        
        chat_id = update.message.chat_id
        bot.send_photo(chat_id=chat_id, photo = photos)
    
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text = 'Finish, {} photos in total'.format(len(link)))
#    return title
#        send_photos()
    
def open_url():
    url_ = 'https://www.legendadult.net/2020/01/graphis-gals-yua-mikami-valentine-2018.html'
    return url_
    
#def title_present(bot, update, content):
#    chat_id = update.message.chat_id
#    bot.send_message(chat_id=chat_id, text = content)
    

#def send_photos(bot, update, url):
#    chat_id = update.message.chat_id
#    img_file = requests.get(url, allow_redirects = True).content
    

def title_of(url_):
    respond = requests.get(url_)
    soup = BeautifulSoup(respond.text, "html.parser")
    
    title_div = soup.findAll('div', class_ = 'post-title')
    title = title_div[0].find('h2').text
    return title

def load_more(url_):
    mainpageres = requests.get(url_)
    mainsoup = BeautifulSoup(mainpageres.text, "html.parser")
    loadmore = mainsoup.findAll('div', class_ = 'loadmore')
    return loadmore[0].find('a').get('href')



def page_list():
    
    
    url_ = 'http://legendadult.net'
    
    
    if len(main_list)/10 >= 1: # The 10 pages are loaded and it is not the first page
        n = int(len(main_list)/10) # Divided value is of float type, convert it to int type for loop
#        print ('triggerd\n, n=', n)
        for i in range(n):
            url_ = load_more(url_)
#    elif len(main_list) == 0:
#        url_ = 'http://legendadult.net'
        
#    print (url_)
    mainpageres = requests.get(url_)
    mainsoup = BeautifulSoup(mainpageres.text, "html.parser")
    
    main_wrap = mainsoup.findAll('div', class_ = 'card-post')
#    print (main_list, len(main_list))
#    main_list = [] # The list of url links in the page
    for i in main_wrap:
        lk = i.find('a').get('href') # Get the link to the page, there are 10 pages for each load
        if lk not in main_list:
            main_list.append(lk)
            title = title_of(lk)
            return lk
        else:
            continue
            
            
        
#    return main_list
#    for i in main_list:
#        title = title_of(i)
#        if title not in title_list:
#            title_list.append(title)
#            return i
##            break
#        else:
#            continue
#    
        
#        title_list.append(lk)
#    print (main_list)
        
    
    
    

    
    
#page_list()




    
#url_ = 'https://www.legendadult.net/search?updated-max=2020-01-30T02:40:00%2B08:00&max-results=40&start=0&by-date=false'
#open_link(url_)