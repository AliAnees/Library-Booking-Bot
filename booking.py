import time
import random
import os, sys
from datetime import date
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import calendar
from dotenv import load_dotenv

load_dotenv()

first_name_1 = os.getenv('fname1')
last_name_1 = os.getenv('lname1')
email_1 = os.getenv('email1')
first_name_2 = os.getenv('fname2')
last_name_2 = os.getenv('lname2')
email_2 = os.getenv('email2')
login_email = os.getenv('login_email')
login_pass = os.getenv('login_pass')
chat_link = os.getenv('chat_link')

website = "https://cal.lib.uoguelph.ca/spaces?lid=1536&gid=2753"
browser = webdriver.Chrome(executable_path=r'C:\Users\Ali\Documents\Programs\Booking\chromedriver.exe')
browser.get(website)
counter = 0
picCount = 1
weekday = 0
if((date).today().weekday() != 6):
    weekday = date.today().weekday() + 1
tomorrow = calendar.day_name[weekday]

rooms = [2, 3]
roomNum = random.choice(rooms)
rowRoom = '//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/div[1]/div/table/tbody/tr['+str(roomNum)+']/td/div/div/'

def switch(argument):
    switcher = {
        2: ": Room 033",
        3: ": Room 217",
    }
    return switcher.get(argument, "Invalid")

def findStartingBox():
    global counter
    for i in range(10):
        try:
            for x in range(60):
                counter+=1
                boxTitle = browser.find_element_by_xpath(rowRoom + 'a['+str(counter)+']').get_attribute("title")
                if (tomorrow in boxTitle) and ("10:00am" in boxTitle):
                    break
            break
        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
    else:
        raise e

def clickStuff(xpathText):
    for i in range(10):
        try:
            browser.find_element_by_xpath(xpathText).click()
            time.sleep(0.2)
            break
        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
    else:
        raise e

def enterText(xpathText, fieldText):
    for i in range(10):
        try:
            browser.find_element_by_xpath(xpathText).send_keys(fieldText)
            break
        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
    else:
        raise e

def bookSessions():
    global counter
    for x in range(6):
        clickStuff(rowRoom + 'a['+str(counter)+']')
        time.sleep(0.2)
        counter+=1

def finishBooking(fName, lName, email):
    global picCount
    clickStuff('//*[@id="submit_times"]')
    clickStuff('//*[@id="terms_accept"]')
    enterText('//*[@id="fname"]', fName)
    enterText('//*[@id="lname"]', lName)
    enterText('//*[@id="email"]', email)
    clickStuff('//*[@id="btn-form-submit"]')
    time.sleep(1)
    browser.save_screenshot(str(picCount)+'.png')
    picCount+=1

def executeOrder66(): #Sends booking images to group chat
    browser.get(chat_link)
    browser.find_element_by_xpath('//*[@id="email"]').send_keys(login_email)
    browser.find_element_by_xpath('//*[@id="pass"]').send_keys(login_pass)
    browser.find_element_by_xpath('//*[@id="loginbutton"]').click()
    browser.find_element_by_xpath('//*[@id="facebook"]/body').click()
    time.sleep(2)
    images = os.getcwd()+"/2.png"+"\n"+os.getcwd()+"/1.png"+"\n"+os.getcwd()+"/3.png"+"\n"+os.getcwd()+"/4.png"
    browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form/div/span/input').send_keys(images)
    browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div[2]/a').click()
    browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div').send_keys(tomorrow+switch(roomNum))
    browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div[2]/a').click()
    time.sleep(20)

findStartingBox()

counter+=6
bookSessions()
finishBooking(first_name_1, last_name_1, email_1)

counter-=12
browser.get(website)
bookSessions()
finishBooking(first_name_2, last_name_1, email_2)

executeOrder66()

browser.quit()
sys.exit()