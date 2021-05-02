from flask import Flask, render_template,request,json,jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="mental_health"

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * from student')
    
    userDetails=cur.fetchall()
    print(userDetails)
    return render_template('users.html',users=userDetails)

@app.route('/login',methods=['GET','POST'])
@cross_origin()
def login():
    if request.method=='POST':
        data=json.loads(request.data)
        print(data['email'])
        email=data['email']
        name=data['name']
        googleid=data['googleid']
        cur=mysql.connection.cursor()
        cur.execute('SELECT * from login_with_google')
        result=cur.fetchall()
        print("result-----",result)
        if len(result)>0:
            response = jsonify(message="Already email exists")
        else:
            cur.execute('INSERT into login_with_google (email,name,google_id) values(%s,%s,%s)',(email,name,googleid))
            mysql.connection.commit()
            response = jsonify(message="success")
        
        return response
    return "success"

if __name__=='__main__':
    app.run(debug=True)