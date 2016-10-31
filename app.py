from flask import Flask, session, request, url_for, redirect
from utils import authenticate, dbEditor

app = Flask(__name__)

@app.route("/")
def root():
    if( session.hasKey( 'username' ) ):
        #do something
    else:
        redirect(url_for( 'login' ))

@app.route("/login/")
def login():
    render_template('login.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

