from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

Config = {
    "apiKey": "AIzaSyAt6FBViei_fTCcoNKcQOGQNHQYANBeC7E",

  "authDomain": "final-project-65575.firebaseapp.com",

  "databaseURL": "https://final-project-65575-default-rtdb.europe-west1.firebasedatabase.app",

  "projectId": "final-project-65575",

  "storageBucket": "final-project-65575.appspot.com",

  "messagingSenderId": "823719740861",

  "appId": "1:823719740861:web:e314e585e79a2143297ed4",

  "measurementId": "G-XQGLK7XF4Y"
  }

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("final.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = {'username':request.form["username"],'password':request.form['password'],'email':request.form["email"]}
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("user").child(login_session['user']['localId']).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    return render_template("signup.html")
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('home'))
    # except:
        error = "Authentication failed"
        return render_template("signin.html")
    return render_template("signin.html")
    
@app.route('/addnbch', methods=['GET', 'POST'])
def addnbch():
    if 'user' in login_session:
        if request.method == 'POST':
            nbch = {'name':request.form["name"],'location':request.form["location"],'des':request.form["des"] ,"uid": login_session['user']['localId']}
            db.child("nbch").push(nbch)
            return redirect(url_for("nbchlist"))
        else:
            return render_template("addnbch.html")
    return render_template("final.html")




@app.route('/allnbch', methods=['GET','POST'])
def nbchlist():
    return render_template("allnbch.html",nbch = db.child('nbch').get().val())



    return render_template("final.html")#####################################################

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template("Forgot.html")

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)