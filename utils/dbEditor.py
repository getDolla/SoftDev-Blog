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
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    #Gets old story id list and adds to it
    q = "SELECT story_ids FROM users WHERE username='%s'"%(user)
    storyids = c.execute(q)
    for record in storyids:
        newstoryid = str(record[0]) # Woohoo dynamic typing
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
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    random.seed(time.time())
    story_id=random.randint(0,int(time.time()))
    q = "INSERT INTO stories VALUES (%d, '%s', %f, '%s', '%s')"%(story_id, title,time.time(),submission, submission)
    print q
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
    db = sqlite3.connect("data/database.db")
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

#randomStoryId(user)
#Returns a random story_id that the user has not touched
#Params:
#    string user - username who is accessing a story
#Returns story_id
def randomStoryId(user):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    q="SELECT story_ids FROM users WHERE username = '%s'"%(user)
    records = c.execute(q)
    temp=""
    for record in records:
        temp = str(record[0])
    story_ids=temp.split(",")
    q="SELECT id FROM stories"
    if((len(story_ids)>0) and story_ids[0]!=''):
        q+=" WHERE id != %d"%(int(story_ids[0]))
    i = 1
    while i<len(story_ids):
        q+=" AND id != %d"%(int(story_ids[i]))
        i+=1;
    records = c.execute(q)
    list=[]
    for record in records:
        list.append(record[0])
    db.commit()
    db.close()
    random.seed(time.time())
    return list[random.randint(0,len(list)-1)]

#randomStory(user)
#Returns a random story that the user has not touched
#Params:
#    string user - username who is accessing a story
#Returns story_id, last_submission
def randomStory(user):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    id = randomStoryId(user)
    q = "SELECT last_submission, title FROM stories WHERE id = %d"%(id)
    records = c.execute(q)
    for record in records:
        last_submission = record[0]
        title = record[1]
    db.commit()
    db.close()
    return id, last_submission, title


#allStories(user)
#Returns all of the stories that a user has contributed to in chronological order
#Params:
#    string user - username who is accessing a story
#Returns list of story texts
def allStories(user):
    #Gets all story ids
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    q="SELECT story_ids FROM users WHERE username = '%s'"%(user)
    records = c.execute(q)
    temp=""
    for record in records:
        temp = record[0]
    story_ids=temp.split(",")
    q="SELECT story, time FROM stories"
    if(len(story_ids)>0):
        q+=" WHERE id = %d"%(int(story_ids[0]))
    i = 1
    while i<len(story_ids):
        q+=" OR id = %d"%(int(story_ids[i]))
        i+=1;
    records = c.execute(q)
    #Uses an insertion sort to sort by recency
    list=[]
    times=[]
    i;
    for record in records:
        list.append("")
        times.append(0)
        i=0
        time = record[1]
        while i<len(list) and time<times[i]:
            i+=1
        ii=len(list)-1
        while ii>i:
            list[ii]=list[ii-1]
            times[ii]=times[ii-1]
            ii-=1;
        list[i]=record[0]
        times[i]=time
    db.commit()
    db.close()
    return list

def newDatabase():
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    q = "CREATE TABLE users (username TEXT, password TEXT, story_ids TEXT)"
    c.execute(q)
    q =	"CREATE TABLE stories (id INTEGER, title TEXT, time REAL, last_submission TEXT, story TEXT)"
    c.execute(q)
    db.commit()
    db.close()


if __name__ == '__main__':
    newDatabase()
        
