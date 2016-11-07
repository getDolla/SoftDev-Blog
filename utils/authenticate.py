import sqlite3
import hashlib
from os import path, remove

checkerList = [" "]

def authenticate( requestForm, userNames, passWords ):
    for i in checkerList:
        if( requestForm['user'].find(i) != -1 ):
            return "Username Cannot Contain Any Whitespace"
        if( requestForm['password'].find(i) != -1 ):
            return "Password Cannot Contain Any Whitespace"
        
    if( requestForm['user'] in userNames ):
        index = userNames.index(requestForm['user'])
        if passWords[index] == hashWord( requestForm['password'] ):
            return True
        else:
            return "Password Does Not Match"
    else:
        return "Username Not Found"

def register( requestForm, userNames, passWords ):
    for i in checkerList:
        if( requestForm['user'].find(i) != -1 ):
            return "Username Cannot Contain Any Whitespace"
        if( requestForm['password'].find(i) != -1 ):
            return "Password Cannot Contain Any Whitespace"

    if( requestForm['user'] in userNames ):
        return "Username Already Taken"
    else:
        #userNames.append( requestForm['user'] )
        #passWords.append( hashWord(requestForm['password']) )
        addToDB( requestForm['user'], hashWord(requestForm['password']))
        return True

def hashWord( strIn ):
    return hashlib.sha256(strIn).hexdigest()
    
def dbHandler( ):
    db = sqlite3.connect("./data/database.db")
    cursor = db.cursor()
    cmd = "SELECT username, password FROM users"
    databaseData =  cursor.execute(cmd)
    userNames = []
    passWords = []
    for row in databaseData:
        userNames.append( row[0] );
        passWords.append( row[1] );
    db.commit()
    db.close()
    return { 'usernames' : userNames, 'passwords' : passWords }

def addToDB( userName, passWord ):
    db = sqlite3.connect("./data/database.db")
    cursor = db.cursor()
    cmd = "INSERT INTO users VALUES ( '%s', '%s', '')"%(userName, passWord)
    cursor.execute(cmd)
    db.commit()
    db.close()

