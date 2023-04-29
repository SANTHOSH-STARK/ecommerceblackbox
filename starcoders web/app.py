from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase
import sqlite3




app = Flask(__name__)
incdbli=[0,"uname"]

config = {
  'apiKey': "AIzaSyAmHhBKHbU_zxsRQqiWcD1t159ZFq1dUQI",
  'authDomain': "automated-ray-380216.firebaseapp.com",
  'projectId': "automated-ray-380216",
  'storageBucket': "automated-ray-380216.appspot.com",
  'messagingSenderId': "271666645379",
  'appId': "1:271666645379:web:922c2df33cc6c1e774ceb6",
  'measurementId': "G-7BJ7YSPF1Q",
  'databaseURL':'https://automated-ray-380216-default-rtdb.firebaseio.com/'
 
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/nav2log")
def log():
    return render_template("login.html")

@app.route("/nav2aiprod")
def aiprod():
    return render_template("ai_products.html")

@app.route("/nav2sos")
def sos():
    return render_template("sos.html")

@app.route("/nav2elec")
def elec():
    return render_template("electrical.html")

@app.route("/navfr")
def fr():
    return render_template("drowsy.html")

@app.route("/navgas")
def gas():
    return render_template("gas.html")
@app.route("/navalc")
def alc():
    return render_template("alcohol.html")
@app.route("/navfire")
def fire():
    return render_template("fire.html")
@app.route("/log", methods=["GET", "POST"])
def login():
    email = request.form["em_log"]
    password = request.form["pw_log"]    
    data = db.child("Users").get()
    valn=data.val()
    print(valn)
    n=len(valn)
    emli=[]
    nameli=[]
    pwli=[]
    for i in range(1,n):

        emli.append(list(valn[i].values())[0])
        nameli.append(list(valn[i].values())[1])    
        pwli.append(list(valn[i].values())[2])

    if email in emli:
        n=emli.index(email)
        if pwli[n] == password:
            incdbli[1]=nameli[n] #name of the logged user

            return render_template("products.html")
            #return "'{}'successfully logged address : {} pn_no : {}  ".format(incdbli[1],incdbli[2],incdbli[3])
        else:
            return "incorrect password"
    else:  
        return "no users found"

@app.route('/confirmorder',methods=['POST','GET'])
def confirmorder():
    conn=sqlite3.connect('starcoders.db')
    c=conn.cursor()      
    li=c.execute("select thing from thing")
    thing=li.fetchone()[0]    
    name=request.form['name']
    address=request.form['address']
    phone_no=request.form['pn_no']
    data = {"name": name, "address": address, "phoneno": phone_no,"item":thing}
    db.child('Orders').push(data)
    return render_template("order_placement.html")

@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["nm_reg"]
        email = request.form["em_reg"]
        password = request.form["pw_reg"]

        incdbli[0]+=1
        incdb=incdbli[0]
        data = {"name": name, "email": email, "password": password}
        try:
            db.child("Users").child(incdb).set(data)

            alert = "Registration successful. Please login to continue."
            return render_template("login.html", alert=alert)
        except:
            alert = "Registration failed. Please try again."
            return render_template("login.html", alert=alert)

    return render_template("login.html")
@app.route('/drowsyplaceorder')
def drowsyoreder():
    conn=sqlite3.connect('starcoders.db')
    c=conn.cursor()    
    c.execute('update thing set thing="Drowsy detection system"')
    conn.commit()
    return render_template("shop.html",thing="Drowsiness detection system")
@app.route('/fireplaceorder')
def fireorder():
    conn=sqlite3.connect('starcoders.db')
    c=conn.cursor()    
    c.execute('update thing set thing="Fire detection system"')
    conn.commit()
    return render_template("shop.html",thing="Fire detection system")
@app.route('/sosplaceorder')
def sosoreder():
    conn=sqlite3.connect('starcoders.db')
    c=conn.cursor()    
    c.execute('update thing set thing="SOS emergency system"')
    conn.commit()
    return render_template("shop.html",thing="SOS emergency system")
@app.route('/gasplaceorder')
def gasoreder():
    conn=sqlite3.connect('starcoders.db')
    c=conn.cursor()    
    c.execute('update thing set thing="Gas leakage detection system"')
    conn.commit()
    return render_template("shop.html",thing="Gas leakage detection system")
@app.route('/alcoholplaceorder')
def alcoholoreder():
    conn=sqlite3.connect('starcoders.db')
    c=conn.cursor()    
    c.execute('update thing set thing="alcohol detection system"')
    conn.commit()
    return render_template("shop.html",thing="alcohol detection system")





@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
