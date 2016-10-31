import sqlite3
import hashlib
from os import path, remove

def accessDB( ):
    db = sqlite3.connect("../data/database.db")
    cursor = db.cursor()
    cmd = "SELECT username, password FROM users"
    d =  cursor.execute(cmd)
    db.commit()
    db.close()
    return d

def authenticate( requestForm, userNames, passWords ):    
    if( requestForm['user'] in userNames ):
        index = userNames.index(requestForm['user'])
        if passWords[index] == hashWord( requestForm['password'] ):
            return True
        else:
            return "Bad Password"
    else:
        return "Bad Username"

def register( requestForm, userNames, passWords ):
    if( requestForm['user'] in userNames ):
        return False
    else:
        #userNames.append( requestForm['user'] )
        #passWords.append( hashWord(requestForm['password']) )
        addToDB( requestForm['user'], hashWord(requestForm['password']))
        return True

def hashWord( strIn ):
    return hashlib.sha256(strIn).hexdigest()
    
def dbHandler( databaseData ):
    userNames = []
    passWords = []
    for row in databaseData:
        userNames.append( row[0] );
        passWords.append( row[1] );
    return { 'usernames' : userNames, 'passwords' : passWords }

def commitToDB( userName, passWord ):
    db = sqlite3.connect("../data/database.db")
    cursor = db.cursor()
    cmd = "INSERT INTO users VALUES ( '%s', '%s', '')"%(userName, passWord)
    cursor.execute(cmd)
    db.commit()
    db.close()

