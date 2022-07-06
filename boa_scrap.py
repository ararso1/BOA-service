from ctypes import resize
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton,KeyboardButton
from xml.sax.xmlreader import Locator
from requests import *
import requests
import types
from bs4 import BeautifulSoup
from telebot import *
from api import API_KEY
import telebot
import telegram

bot = telebot.TeleBot(API_KEY, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, 'Welcome, use the menu to get a BOA service')    

@bot.message_handler(commands=['exchangerate'])
def exchange_rate(msg):
    res=requests.get("https://www.bankofabyssinia.com/exchange-rate/").text
    soup = BeautifulSoup(res,'lxml')
    currency = soup.find("tbody", class_="row-hover")

    val = currency.find_all('tr')
    raw = val[0]
    raw1 = raw.find_all('td')
    
    l=[raw1[0].text,raw1[1].text,raw1[2].text]
    response = 'Today Currency Exchange Rate at BOA\n' 
    response +=f"{l[0]: <10}{l[1]: <10}{l[2]: >10}\n"

    for i in range(1,len(val)):
        val1 = val[i]
        val2 = val1.find_all('td')
        for i in range(len(val2)):
            response+=f"{val2[i].text}       "
        response +='\n'
    response += '\nUse menu for other service'

    bot.send_message(msg.chat.id, response)   

@bot.message_handler(commands=['atm_locator'])
def loca(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text="Share Location", request_location=True)

    markup.add(btn1)
    bot.send_message(msg.chat.id, 'Share your location to get BOA branch around you', reply_markup=markup)

@bot.message_handler(func = lambda m : True)
def atm_locator(msg):

    res1=requests.get("https://www.bankofabyssinia.com/branch-atm-locations/").text
    #res = requests.get("https://www.bankofabyssinia.com/loan-calculator/")
    soup = BeautifulSoup(res1, 'lxml')
    locator = soup.find('div', class_="cmsmasters_tab_inner") 
    atm_locator = locator.find('tbody', class_="row-hover")
    branch_name = atm_locator.find_all('tr')
    num=0
    bot.send_message(chat_id=msg.chat.id,text=msg.text)
    x = msg.text.upper()
    response =[ "Based on your laction, The following Branch are near to you\n"]
    for i in range(len(branch_name)):       
        branch_and_location = branch_name[i]
        location = branch_and_location.find_all('td')
        loc = location[2].text
        
        if x in loc:
            num=num+1
            response.append(f"{num: <5}{location[1].text},   {location[2].text: <10}\n")
            
        else:
            continue
    response.append('\nUse menu for other service')
    result = ""
    #print("my reespon",response)

    x= len(response)
    y=50
    if x > 2:
        for i in range(0,x,50):
            l1=[]
            result=""
            l1.extend(response[i:y])
            y+=50
            for j in l1:
                result+=j
            bot.send_message(msg.chat.id, result)
            
    else:
        bot.send_message(msg.chat.id, 'Please enter correct location!')

    return 0

bot.infinity_polling()

