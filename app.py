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
        if val:
            return redirect(url_for('login', message = "Registration Successful"))
        else:
            return redirect(url_for('login', message = "Registration Unsuccessful"))
    else:
        return redirect(url_for( 'root' ) )

@app.route("/home/")
def home():
    return render_template("homepage.html")

@app.route("/add/")
def add():
    return render_template("add.html")

@app.route("/create/")
def create():
    return render_template("create.html")



if __name__ == "__main__":
    app.debug = True
    app.run()

