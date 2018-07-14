"""
Trivia game module for rikka.
The format for the leaderbaord is as follows:
    ServerID, UserID, Score
Carlos Saucedo, 2018
"""
from random import randint
from Mods.triviaSet import triviaSet
from Mods.triviaScore import triviaScore
from Mods import trivia
import re, pymysql
from array import array
import Mods.cmdUtils as utils

class triviaGame:
    def __init__(self, questionPath, answerPath):
        questionFile = open(questionPath, "r", encoding="utf8")
        self.questionList = questionFile.read().encode("ascii", "ignore").splitlines()
        self.questionCount = len(self.questionList)
        questionFile.close()
        
        answerFile = open(answerPath, "r", encoding="utf8")
        self.answerList = answerFile.read().encode("ascii", "ignore").splitlines()
        answerFile.close()
        
        self.setList = []
        
    def getQuestionCount(self):
        return self.questionCount
        
    def getQuestion(self, serverID):
        #Returns a randomly selected question.
        inList = False
        for x in self.setList:
            if x.getServer() == serverID:
                #If the server has already started a question instance.
                inList = True
                self.questionNumber = randint(0, self.questionCount -1)
                question = self.questionList[self.questionNumber]
                question = question.decode("utf-8")
                answer = self.answerList[self.questionNumber]
                answer = answer.decode("utf-8")
                x.setQuestion(question, answer)
                return x.getQuestion()
        if inList == False:
            #The server has not initated a trivia game.
            self.questionNumber = randint(0, self.questionCount -1)
            question = self.questionList[self.questionNumber]
            question = question.decode("utf-8")
            answer = self.answerList[self.questionNumber]
            answer = answer.decode("utf-8")
            x = triviaSet(serverID)
            x.setQuestion(question, answer)
            self.setList.append(x)
            return x.getQuestion()
            
    def getAnswer(self, serverID):
        #Returns the answer to the given question.
        for x in self.setList:
            if x.getServer() == serverID:
                return x.getAnswer()
    
    def getScore(self, userID, connection):
            with connection.cursor() as cursor:
                cursor.execute(utils.concat(("SELECT intScore FROM tblUser WHERE userID = ",userID,";")))
                return cursor.fetchone()

    def getSent(self, serverID):
        inList = False
        for x in self.setList:
            if x.getServer() == serverID:
                inList = True
                return x.getSent()
        if inList == False:
            return False
        
    def setSent(self, serverID, state):
        for x in self.setList:
            if x.getServer() == serverID:
                x.setSent(state)
        
    def addPoint(self, serverID, userID, connection):
        #Adds a point to the given user's score.
            if utils.userInDB(userID,connection):
                with connection.cursor() as cursor:
                    cursor.execute(utils.concat(("SELECT intScore FROM tblUser WHERE userID = ",userID,";")))
                    oldScore = cursor.fetchone()
                    cursor.execute(utils.concat(("UPDATE tblUser SET intScore = ",(oldScore + 1)," WHERE userID = ",userID,";")))
            else:
                with connection.cursor() as cursor:
                    cursor.execute(utils.concat(("INSERT INTO tblUser (userID,intCollectionDate,intScore) VALUES (",userID,",",None,",",1,");")))
            if not utils.guildInDB(serverID,connection):
                cursor.execute(utils.concat(("INSERT INTO tblServerPrefixes (serverID) VALUES (",serverID,");")))
                cursor.execute(utils.concat(("INSERT INTO tblServerPrefixesUser (serverID,userID) VALUES (",serverID,",",userID,");")))
            connection.commit()
            
    
    def addPoints(self, serverID, userID, amount, connection):
        if utils.userInDB(userID,connection):
            with connection.cursor() as cursor:
                cursor.execute(utils.concat(("SELECT intScore FROM tblUser WHERE userID = ",userID,";")))
                oldScore = cursor.fetchone()
                cursor.execute(utils.concat(("UPDATE tblUser SET intScore = ",oldScore + amount," WHERE userID = ",userID,";")))
        else:
            with connection.cursor() as cursor:
                cursor.execute(utils.concat(("INSERT INTO tblUser (userID,intCollectionDate,intScore) VALUES (",userID,",",None,",",amount,");")))
        if not utils.guildInDB(serverID,connection):
            cursor.execute(utils.concat(("INSERT INTO tblServerPrefixes (serverID) VALUES (",serverID,");")))
            cursor.execute(utils.concat(("INSERT INTO tblServerPrefixesUser (serverID,userID) VALUES (",serverID,",",userID,");")))
        connection.commit()
            
    def subtractPoints(self, serverID, userID, amount, connection):
        if utils.userInDB(userID,connection):
            with connection.cursor() as cursor:
                cursor.execute(utils.concat(("SELECT intScore FROM tblUser WHERE userID = ",userID,";")))
                oldScore = cursor.fetchone()
                cursor.execute(utils.concat(("UPDATE tblUser SET intScore = ",(oldScore - amount)," WHERE userID = ",userID,";")))
        if not utils.guildInDB(serverID,connection):
            cursor.execute(utils.concat(("INSERT INTO tblServerPrefixes (serverID) VALUES (",serverID,");")))
            cursor.execute(utils.concat(("INSERT INTO tblServerPrefixesUser (serverID,userID) VALUES (",serverID,",",userID,");")))
        connection.commit()
            
    def format(self, attempt):
        #Formats an attempt to make it easier to guess.
        #Removes "the", "a", "an", and any parenthetical words.
        formatted = attempt.lower()
        if attempt.startswith("a "):
            formatted = formatted.replace("a ", "")
        if attempt.startswith("the "):
            formatted = formatted.replace("the ","")
        if attempt.startswith("an "):
            formatted = formatted.replace("an ", "")
        formatted = re.sub("[\(\[].*?[\)\]]", "", formatted)
        return formatted
    
    def flag(self):
        #Adds the current question to the list of flagged questions.
        flaggedFile = open("flagged_questions.list", "a+")
        flaggedFile.write(str(self.questionNumber))
        flaggedFile.close()
        
    def getGlobalLeaderboard(self,connection):
        globalScores = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT userID, intScore FROM tblUser ORDER BY intScore DESC;")
            globalScores.append(triviaScore(cursor["userID"],cursor["serverID"]))
        return globalScores
    
    def getLocalLeaderboard(self, serverID, connection):
        localScores = []
        with connection.cursor() as cursor:
            cursor.execute(utils.concat(("SELECT tblUser.userID, tblUser.intScore FROM tblUser, tblServerUser WHERE tblServerUser.serverID = ",serverID," ORDER BY tblUser.intScore DESC;")))
            localScores.append(triviaScore(cursor["userID"],cursor["serverID"]))
        return localScores
        










