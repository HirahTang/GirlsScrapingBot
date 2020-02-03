#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:09:29 2020

@author: TH
"""

from scraper import *
from telegram.ext import Updater, CommandHandler

#url_ = 'https://www.legendadult.net/search?updated-max=2020-01-30T02:40:00%2B08:00&max-results=40&start=0&by-date=false'
#open_link(url_)



def plus_token():
    tk = '916581787:AAGZPZPzV80HnhtBKmu2yHBl49Ekn0adkHU'
    return tk
    

def bop(bot, update):
#    url = 'https://4.bp.blogspot.com/-DT3ZM3WS6X0/Wj9Sa6OaPRI/AAAAAAAABqU/rHWimJMvKGw1XTd4Q3UBfoSm7Og3rujYgCLcBGAs/s1600/1.jpg'
    url = 'https://4.bp.blogspot.com/-DOEGhZBSFko/XjPp7qprduI/AAAAAAABTjE/uyP420R-toABjojL1PDW34-GhPim6hItwCLcBGAsYHQ/s1600/Legendadult.blogspot.com%2B-%2B1.webp'
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)



def main():
    token = plus_token()
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('girlsphoto',present_image))
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
    
   
