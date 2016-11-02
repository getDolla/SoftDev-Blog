import sqlite3
import time, random

#insertID(story_ids, newstory)
#Params:
#    string story_ids - the list of ids
#    int newstory - the id to add to the list
#Returns the new list
def insertID(story_ids, newstory):
    l = story_ids.split(",")
    l.append(str(newstory))
    retstr=""
    for story in l:
        retstr+=story
        retstr+=","
    retstr=retstr[0:-1]
    return retstr

#createStory(user, title, submission)
#creates a new story record in stories
#Params:
#    user - username who created story
#    title - title of story
#    submission - the text submitted
#    note the story id is generated using the current time and random
#Returns True
def createStory(user, title, submission):
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    random.seed(time.time())
    q = "SELECT COUNT(*) FROM stories"
    q = "INSERT INTO stories VALUES (%d, '%s', %f, '%s', '%s')"%(random.randint(0,int(time.time())), title,time.time(),submission, submission)
    c.execute(q)
    db.commit()
    db.close()
    return True;


if __name__=='__main__':
    print createStory("ely2", "titletry2", "story2")
    
