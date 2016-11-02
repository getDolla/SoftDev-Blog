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

#addStory(user, title, submission)
#updates the record in stories, and updates the user's stories edited
#Params:
#    user - username who added to the story
#    story_id - the story that is edited
#    text - the text added to the story
#Returns True
def addStory(user, story_id, text):
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    #Gets new story
    q = "SELECT story FROM stories WHERE id=%d"%(story_id)
    stories = c.execute(q)
    for record in stories:
        story = record[0] # Woohoo dynamic typing
    story+=text
    q = "UPDATE stories SET time = %f, last_submission = '%s', story = '%s' WHERE id = %d"%(time.time(), text, story, story_id)
    c.execute(q)
    db.commit()
    db.close()
if __name__=='__main__':
    addStory("ely", 1, " newtext")
    
