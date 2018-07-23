#Module for miscellaneous functions.

def concat(array,*args):
    if len(args) < 1:
        type = str
    else:
        type = args[0]
    convArray = map(type,array)
    concat = "".join(convArray)
    return concat

def userInDB(userID,connection):
    with connection.cursor() as cursor:
        cursor.execute(concat(("SELECT userID FROM tblUser WHERE userID = ",userID,";")))
        if cursor.fetchone() == None:
            return False
        else:
            return True

def guildInDB(serverID,connection):
    with connection.cursor() as cursor:
        cursor.execute(concat(("SELECT serverID FROM tblServerPrefixes WHERE serverID = '",serverID,"';")))
        if cursor.fetchone() == None:
            return False
        else:
            return True

def userExists(userID):
    if userID.getUser() == None:
        return False
    else:
        return True
















