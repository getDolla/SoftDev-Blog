from flask import Flask, session, request, url_for, redirect, render_template
from utils import authenticate, dbEditor
app = Flask(__name__)
app.secret_key = "Celine Yan for President"

@app.route("/")
def root():
    if( 'username' in session.keys() ):
        return redirect(url_for( 'home' ))
    else:
        return redirect(url_for( 'login' ))

@app.route("/login/")
def login( **keyword_parameters ):
    message = ""
    if( 'message' in keyword_parameters):
        message = keyword_parameters['message']
    elif( 'message' in request.args ):
        message = request.args.get('message')
    return render_template('login.html', message = message)

@app.route("/authenticate/", methods = ["POST"] )
def authen():
    dbData = authenticate.dbHandler( )
    userNames = dbData['usernames']
    passWords = dbData['passwords']
    if request.form['account'] == 'Login':
        val = authenticate.authenticate(request.form, userNames, passWords )
        if val == True :
            session['username'] = request.form['user']
            return redirect(url_for('root'))
        else:
            return redirect(url_for('login', message = val))
    elif request.form['account'] == 'Register':
        val = authenticate.register(request.form, userNames, passWords)
        if val == True :
            return redirect(url_for('login', message = "Registration Successful"))
        else:
            return redirect(url_for('login', message = val))
    else:
        return redirect(url_for( 'root' ) )

@app.route("/home/")
def home():
    if dbEditor.allStories(session['username']) == []:
        message = "Looks like you didn't add to any stories yet!"
        message2 = "Get started by clicking the Add Story or Create Story button!"
        content = dbEditor.allStories(session['username'])
    else:
        message = "Here are the stories you've contributed to, in full length:"
        message2 = ""
        content = dbEditor.allStories(session['username'])
    return render_template("homepage.html", user = session['username'], message = message, message2 = message2, content = content)

@app.route("/add/")
def add():
    L = dbEditor.randomStory(session['username']);
    if L == []:
        return render_template("addfailure.html")
    return render_template("add.html", storyID = L[0], story = L[1], title = L[2])

@app.route("/addInput/", methods = ["POST"])
def addInput():
    dbEditor.addStory(session['username'], int(request.form['storyID']), request.form['story'])
    return redirect(url_for( 'home' ) );
    
@app.route("/createInput/", methods = ["POST"])
def createInput():
    dbEditor.createStory(session['username'], request.form['title'], request.form['story']);
    return redirect(url_for( 'home' ) );

@app.route("/create/")
def create():
    return render_template("create.html")

@app.route("/logout/")
def logout():
    session.pop('username')
    return redirect(url_for('root'))

if __name__ == "__main__":
    app.debug = True
    app.run()

