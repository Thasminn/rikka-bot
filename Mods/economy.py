"""
Economy module for Rikka.
Carlos Saucedo, 2018
"""

import datetime, pymysql
from random import randint
import Mods.trivia as  trivia

def getCurrentDay():
    now = datetime.datetime.now()
    return(str(now.day))

def hasCollectedToday(userID,connection):
        with connection.cursor() as cursor:
            cursor.execute("".join(("SELECT intCollectionDate FROM tblUser WHERE userID = ",str(userID))))
            collectDate = cursor.fetchone()
        if collectDate == getCurrentDay():
            return True
        else:
            return False

def setCollectionDate(userID,connection):
    if userInDB(userID,connection):
        with connection.cursor() as cursor:
            cursor.execute("".join(("UPDATE tblUser SET intCollectionDate = ", str(getCurrentDay()), " WHERE userID = ", str(userID),";")))
    else:
        with connection.cursor() as cursor:
            cursor.execute("".join(("INSERT INTO tblUser (userID,intCollectionDate) VALUES (", str(userID), ",", str(getCurrentDay()), ");")))
    connection.commit()

def userInDB(userID,connection):
    with connection.cursor() as cursor:
        cursor.execute("".join(("SELECT userID FROM tblUser WHERE userID = ", str(userID),";")))
        if cursor.fetchone() == None:
            return False
        else:
            return True

def guildInDB(serverID,connection):
    with connection.cursor() as cursor:
        cursor.execute("".join(("SELECT serverID FROM tblServerPrefixes WHERE serverID = '", str(serverID),"';")))
        if cursor.fetchone() == None:
            return False
        else:
            return True

def userExists(userID):
    if userID.getUser() == None:
        return False
    else:
        return True

        
        
        
        
        
