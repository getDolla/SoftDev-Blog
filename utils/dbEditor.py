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
        if(len(story)>0):
            retstr+=story
            retstr+=","
    retstr=retstr[0:-1]
    return retstr

#touchStory(user, story_id)
#adds a story id to the list of stories the user has edited
#Params:
#    string user - the user who edited a story
#    int story_id - the story id to add
#Returns True
def touchStory(user, story_id):
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    #Gets old story id list and adds to it
    q = "SELECT story_ids FROM users WHERE username='%s'"%(user)
    storyids = c.execute(q)
    for record in storyids:
        newstoryid = record[0] # Woohoo dynamic typing
    newstoryid=insertID(newstoryid, story_id)
    #updates record
    q = "UPDATE users SET story_ids = '%s' WHERE username = '%s'"%(newstoryid,user)
    c.execute(q)
    db.commit()
    db.close()

#createStory(user, title, submission)
#creates a new story record in stories
#Params:
#    string user - username who created story
#    string title - title of story
#    string submission - the text submitted
#    note the story id is generated using the current time and random
#Returns True
def createStory(user, title, submission):
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    random.seed(time.time())
    story_id=random.randint(0,int(time.time()))
    q = "INSERT INTO stories VALUES (%d, '%s', %f, '%s', '%s')"%(story_id, title,time.time(),submission, submission)
    c.execute(q)
    db.commit()
    db.close()
    touchStory(user, story_id)
    return True;

#addStory(user, title, submission)
#updates the record in stories, and updates the user's stories edited
#Params:
#    string user - username who added to the story
#    int story_id - the story that is edited
#    string text - the text added to the story
#Returns True
def addStory(user, story_id, text):
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    #Gets old story and adds new story
    q = "SELECT story FROM stories WHERE id=%d"%(story_id)
    stories = c.execute(q)
    for record in stories:
        story = record[0]
    story+=text
    #updates record
    q = "UPDATE stories SET time = %f, last_submission = '%s', story = '%s' WHERE id = %d"%(time.time(), text, story, story_id)
    c.execute(q)
    db.commit()
    db.close()
    touchStory(user, story_id)

if __name__=='__main__':
    addStory("dota", 0, "This is a test of stories")
