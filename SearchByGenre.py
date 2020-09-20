#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 14:06:24 2020

@author: TH
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

def genre_valid(url, a1, a2): # Check if the page contains the idea genres
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")
    genre = []    
    for i in html.findAll('span', class_ = 'genre'): # Get all the genres
        genre.append(i.text)
#    print (genre)
    if a1 in genre and a2 in genre:
#        download_url(url)
        print ("Found: {}".format(url.split('/')[-1]))
        Image = html.find('a', class_ = 'bigImage').get('href')
        img_file = requests.get(Image, allow_redirects = True).content
        with open('{}.jpg'.format(url.split('/')[-1]), 'wb') as handler:
            handler.write(img_file)
        return (url, html.find('h3').text) # Title


def iterate_url(url, a1, a2): # Iterate all the films in the Menu Page
    
    print ("Page:{}\n".format(url.split('/')[-1]))
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")


    list_url = []
    link_l = html.findAll('a', class_ = 'movie-box')
    for i in link_l:
       list_url.append(i.get('href'))
    if len(list_url) > 0:
#        print (list_url)
        for i in tqdm(list_url):
            output = genre_valid(i, a1, a2)
            if output != None:
                film_l.append(output[0])
                f.write(output[0]+'\t'+ output[1]+ '\n'*2) # Write a txt file store the code and title of the fil,
                
#    url = "https://www.javbus.com/genre/5c/2"
        url = url[:-1] +  str(int(url[-1]) + 1)
#        print (url)
        iterate_url(url, a1, a2)
    else:
        print ('All films iterated')
        

def main():
    a = input("Title:") # Title
    a1 = input("Keyword1:") # Keyword1
    a2 = input("Keyword2:") # Keyword2
    web = input("Website:")
    os.chdir('/Users/TH/Desktop/Jav') # Wordking_D
    global f
    f = open("{}-{}+{}.txt".format(a, a1, a2),"w+") # Descriptive file
    global film_l
    film_l = []
    try:
        os.makedirs('{}-{}+{}'.format(a, a1, a2))
    except:
        os.chdir('/Users/TH/Desktop/Jav/{}-{}+{}'.format(a, a1, a2))
    os.chdir('/Users/TH/Desktop/Jav/{}-{}+{}'.format(a, a1, a2))
    iterate_url(web, a1, a2)
    f.close()
#    download_all(film_l)
if __name__  == "__main__":
    main()    