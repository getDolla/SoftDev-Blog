import sqlite3

#Adds a story id to a list of story ids
def insertID(story_ids, newstory):
    l = story_ids.split(",")
    l.append(str(newstory))
    retstr=""
    for story in l:
        retstr+=story
        retstr+=","
    retstr=retstr[0:-1]
    return retstr

def touchStory(user, story):
    db = sqlite3.connect("../data/database.db")
    c = db.cursor()
    q = "SELECT story_ids FROM users WHERE username=%s"(user)
    stories=c.execute(q)
    print stories


if __name__=='__main__':
    insertID("1,2,3",4)
