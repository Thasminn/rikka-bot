"""
Economy module for Rikka.
Carlos Saucedo, 2018
"""

import datetime, pymysql, Mods.trivia
from random import randint
import Mods.cmdUtils as utils

def getCurrentDay():
    now = datetime.datetime.now()
    return(str(now.day))

def hasCollectedToday(userID,connection):
        with connection.cursor() as cursor:
            cursor.execute(utils.concat(("SELECT intCollectionDate FROM tblUser WHERE userID = ",userID,";")))
            collectDate = cursor.fetchone()
        if collectDate == getCurrentDay():
            return True
        else:
            return False

def setCollectionDate(userID,connection):
    if utils.userInDB(userID,connection):
        with connection.cursor() as cursor:
            cursor.execute(utils.concat(("UPDATE tblUser SET intCollectionDate = ",getCurrentDay(), " WHERE userID = ",userID,";")))
    else:
        with connection.cursor() as cursor:
            cursor.execute("".join(("INSERT INTO tblUser (userID,intCollectionDate) VALUES (", str(userID), ",", str(getCurrentDay()), ");")))
    connection.commit()

        
        
        
        
        
