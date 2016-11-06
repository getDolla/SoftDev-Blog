import sqlite3
import time
def newDatabase():
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    q = "CREATE TABLE users (username TEXT, password TEXT, story_ids TEXT)"
    c.execute(q)
    q = "CREATE TABLE stories (id INTEGER, title TEXT, time REAL, last_submisson TEXT, story TEXT)"
    c.execute(q)
    names = ['ely','celine','kevin','yikai']
    i = 0
    while(i<4):
        q = "INSERT INTO users VALUES ('%s','%s','')"%(names[i],names[i])
        c.execute(q)
        i+=1
    i=0
    while(i<4):
        title = names[i]+"s story"
        submission = names[i] + " went for a walk in the park"
        q = "INSERT INTO stories VALUES (%d, '%s', %f, '%s', '%s')"%(i, title,time.time(),submission, "<h1>"+title+"</h1><br><br>"+submission)
        print q
        c.execute(q)
        i+=1
    db.commit()
    db.close()


if __name__ == '__main__':
    newDatabase()

