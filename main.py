from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import json
from datetime import datetime
import urllib.parse
import mysql.connector
import configparser


class DBConnection(object):

    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
        self.host = DB_HOST
        self.port = DB_PORT
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.con = None

    def connect_db(self):
        if self.con is None:
            self.con = mysql.connector.connect(host=self.host,
                                               port=self.port,
                                               db=self.name,
                                               user=self.user,
                                               passwd=self.password)
            # self.con.set_character_set("utf8")
        return self.con

    def fetch_db(self, query):
        self.query = query
        self.cursor = self.con.cursor()
      #   self.cursor.execute("SET NAMES utf8;")
      #   self.cursor.execute("SET CHARACTER SET utf8;")
      #   self.cursor.execute("SET character_set_connection=utf8;")
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()

        return self.result

    def insert_db(self, query):
        self.query = query
        self.cursor = self.con.cursor()
        self.cursor.execute("SET NAMES utf8;")
        self.cursor.execute("SET CHARACTER SET utf8;")
        self.cursor.execute("SET character_set_connection=utf8;")
        self.cursor.execute(self.query)
        self.con.commit()

        return

def getConfig(section, key):
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
    result = data[section][key]
    return result


# inisial MySQL

# fungsi select table

# search select DB without restart python
def getData(table, param):
    mydb = mysql.connector.connect(
        host=getConfig('DB', 'host'),
        user=getConfig('DB', 'user'),
        password=getConfig('DB', 'password'),
        database=getConfig('DB', 'database')
    )

    crs = mydb.cursor()
    crs.execute("SELECT * FROM "+table+param)
    results = crs.fetchall()
#   crs.close()
   #  mydb.close()
    for result in results:
      return result


def sendFinish(uuid):
    try:
        mydb = mysql.connector.connect(
        host=getConfig('DB', 'host'),
        user=getConfig('DB', 'user'),
        password=getConfig('DB', 'password'),
        database=getConfig('DB', 'database')
        )

        mydb.autocommit = False
        crs = mydb.cursor()
        query = "INSERT INTO kirim_whatsapp_riwayat SELECT NULL,tujuan,otp,response,uuid,waktu_started,waktu_expired,NOW() FROM kirim_whatsapp WHERE uuid='"+uuid+"'"
        crs.execute(query)
        query = "DELETE from kirim_whatsapp WHERE uuid='"+uuid+"'"
        crs.execute(query)
        mydb.commit()
    except mysql.connector.Error as error:
        print("GAGAL, otw rollback: {}".format(error))
        mydb.rollback()
    finally:
        if mydb.is_connected():
          # crs.close()
            mydb.close()


        # initial Variable
        # ATH
creator = getConfig('ATH', 'creator')
name = getConfig('ATH', 'name')
version = getConfig('ATH', 'version')
description = getConfig('ATH', 'description')
print(name)
print("version: "+version)
print(description)
print("Using for development only")
print("==========================================")

# classWebWA
msgBoxParrent = getConfig('CLS', 'msgBoxParrent')
msgBoxChild = getConfig('CLS', 'msgBoxChild')
msgBoxSubChild = getConfig('CLS', 'msgBoxSubChild')
buttonSend = getConfig('CLS', 'buttonSend')
formatPesan = getConfig('PRF', 'formatPesan')
_formatPesan = formatPesan.replace("{br}", os.linesep)


# profile
profileBrowserPath = getConfig('PRF', 'profileBrowserPath')
binDriverPath = getConfig('PRF', 'binDriverPath')
profile = webdriver.FirefoxProfile(profileBrowserPath)

# driver
driver = webdriver.Firefox(firefox_profile=profile,
                           executable_path=binDriverPath)

# fungsi sender


def WASender(_tujuan, _pesan):
    pesan = urllib.parse.quote(_pesan)
    driver.get("https://web.whatsapp.com/send?phone="+_tujuan+"&text="+pesan)
    wait = WebDriverWait(driver, 50)
    try:
        element = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, buttonSend))
        )
        time.sleep(2)
        button = driver.find_element_by_class_name(buttonSend)
        button.click()
    finally:
        print('x')
        # driver.quit()


# whiletrue disini
while(True):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    queue = getData("kirim_whatsapp", " where waktu_started<='" +
                    date+"' order by waktu_started asc limit 1")
    if queue is None:
        time.sleep(5)
    else:
        print(queue)
        tujuan = queue[1]
        otp = queue[2]
        waktu_started = queue[3]
        pesan = _formatPesan.replace("{otp}", otp)
        print("Tujuan: "+queue[1])
        print("Pesan:\n "+pesan)
        print("=============================================")
        WASender(tujuan, pesan)
        sendFinish(queue[4])
      #   if mydb.is_connected():
      #      # crs.close()
      #      mydb.close()
        time.sleep(3)

    # if(condition):
    #    break
