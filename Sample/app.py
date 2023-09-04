from flask import Flask,render_template,request,session 

#database connection
import mysql.connector
conn = mysql.connector.connect(host='localhost',user='root',password='',database='SAMPLE')
mycursor=conn.cursor()

#create a flask application
app = Flask(__name__)

app.secret_key="sample"

#Define the route 
@app.route('/')
def index():
    return render_template('index.html')

#Load Login Page
@app.route('/login')
def login():
    return render_template('index.html')

#Load Register Page
@app.route('/register')
def register():
    return render_template('register.html')

#Registration Process
@app.route('/signup',methods=['POST'])
def signup():
    name = request.form['fullName']
    dob = request.form['dob']
    phone = request.form['phone']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    query = "INSERT INTO USER(NAME,DOB,PHONE,EMAIL,USERNAME,PASSWORD) VALUES(%s,%s,%s,%s,%s,%s)"
    data = (name,dob,phone,email,username,password)
    mycursor.execute(query,data)
    conn.commit()
    return render_template('index.html')

#Login Process
@app.route('/dashboard',methods=['POST'])
def dashboard():
    username=request.form['username']
    password=request.form['password']
    query="SELECT * FROM USER WHERE USERNAME = %s AND PASSWORD = %s"
    values=username,password
    mycursor.execute(query,values)
    account=mycursor.fetchall()
    if account:
        session['loggedin']=True
        session['id']=account[0]
        query = "SELECT * FROM USER"
        mycursor.execute(query)
        data=mycursor.fetchall()
        return render_template('dashboard.html',sqldata=data)
    else:
        msg = 'Incorrect Username or Password!'
        return render_template('index.html',msg=msg)

#Logout
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    return render_template('index.html')
#Run the flask app
if __name__=='__main__':
    app.run(debug = True)