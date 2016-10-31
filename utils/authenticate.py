import sqlite3
from os import path, remove

def accessDB( ):
    db = sqlite3.connect("../data/database.db")
    cursor = db.cursor()
    cmd = "SELECT username, password FROM users"
    d =  cursor.execute(cmd)
    db.commit()
    db.close()
    return d

def authenticate( requestForm, databaseData ):
    userNames = []
    passWords = []
    for row in databaseData:
        userNames.append( row[0] );
        passWords.append( row[1] );
    if( requestForm['user'] in userNames ):
        index = userNames.index(requestForm['user'])
        if passWords[index] == hashWord( requestForm['password'] ):
            #do something
        else:


