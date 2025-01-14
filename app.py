from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import sqlite3
import os
import openpyxl, time

images=os.path.join('static','images')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['icons'] = images
fav_icon = os.path.join(app.config['icons'], 'onlylogo.png')
load_img = os.path.join(app.config['icons'], 'completelogo.gif')
year = ""
dept = ""
section = ""

def connect_db():
    connection = sqlite3.connect('users.db')
    return connection

@app.route('/')
def index():
    if 'username' in session:
        return render_template("dashboard.html", fav_icon=fav_icon, load_img=load_img, data="true")
    return render_template("dashboard.html", fav_icon=fav_icon, load_img=load_img, data="false")
   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['logname']
        password = request.form['logpass']
        email = request.form['logemail']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            return "User already exists"
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        connection.commit()
        connection.close()
        return redirect('/login')
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template("dashboard.html", fav_icon=fav_icon, load_img=load_img, data="true")
    if request.method == 'POST':
        useremail = request.form['logemail']
        password = request.form['logpass']
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (useremail, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = useremail
            return render_template("dashboard.html", fav_icon=fav_icon, load_img=load_img, data="true")
        return "Invalid username or password"
    return render_template('index.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        useremail = request.form['logemail']
        return "Email Sent"
    return render_template('forgot.html', fav_icon=fav_icon, load_img=load_img)

@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    # Get the username from the session
    useremail = session['username']
    conn = sqlite3.connect('users.db')
    
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE email=?",(useremail,))
    username=cursor.fetchone()
    print(username)
    # Close the connection
    conn.close()
    # Connect to the database

    # Render the dashboard template with the username and message
    return render_template('dashboard.html', fav_icon=fav_icon, load_img=load_img, data="true")

@app.route('/display',methods=['GET', 'POST'])
def display():
    conn=sqlite3.connect("users.db")
    cur=conn.cursor()
    cur.execute("select loc, id from timetable where year = ? and dept = ? and section = ?",(year,dept,section))
    data=cur.fetchone()
    # print(data[0])
    if(data == None):
        return "No timetable provided. Contact your administrator"
    elif(data[1] == "1"):
        df = pd.read_excel(data[0])
        return render_template("display.html",  tables=[df.to_html(classes='data')], titles=df.columns.values, data="1", fav_icon=fav_icon, load_img=load_img, true="true")
    else:
        return render_template("display.html", iframe=data[0], data="2", fav_icon=fav_icon, load_img=load_img, true="false")

@app.route("/upload-file", methods=["POST"])
def upload_file():
    file = request.files["file"]
    # if file and file.content_type == "application/pdf":
    if file:
        file.save(os.path.join("files", file.filename))
        os.rename(os.path.join("files", file.filename), os.path.join("files", year+dept+section+".xlsx"))
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TimeTable (Year, Dept, Section, loc, id) VALUES (?, ?, ?, ?, ?)", (year, dept, section, "files/"+ year+dept+section+".xlsx", "1"))
        conn.commit()
        conn.close()
        return "File uploaded successfully!"
    return "No file was provided."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route("/update", methods=['POST', 'GET'])
def update():
    global year, dept, section
    if 'username' not in session and request.method == 'POST':
        year = request.form.get("Year")
        dept = request.form['Dept']
        section = request.form['section']
        return redirect('/display')

    else:
        if request.method == 'POST':
            year = request.form.get("Year")
            dept = request.form['Dept']
            section = request.form['section']
            print(year)
            return render_template("upload.html")

def c2embed(link):
    # Replace "edit" with "pubhtml" in the link
    embedded_link = link.replace("edit", "pubhtml")
    
    return embedded_link
@app.route("/embed_upload", methods=['POST', 'GET'])
def embed_upload():
    if(request.method == "POST"):
        link = request.form.get("google-sheet-link")
        link = c2embed(link)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TimeTable (Year, Dept, Section, loc, id) VALUES (?, ?, ?, ?, ?)", (year, dept, section, link, "2"))
        conn.commit()
        conn.close()
        time.sleep(2)
        return redirect("/dashboard")
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
