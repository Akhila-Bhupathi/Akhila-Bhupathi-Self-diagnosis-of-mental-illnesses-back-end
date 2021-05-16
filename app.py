from flask import Flask, render_template,request,json,jsonify
from flask.wrappers import Response
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from questions import set1

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
    print(set1)
    return render_template('index.html')

@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * from student')
    
    userDetails=cur.fetchall()
    print(userDetails)
    return render_template('users.html',users=userDetails)

@app.route('/register',methods=['GET','POST'])
@cross_origin()
def register():
    if request.method=='POST':
        data=json.loads(request.data)
        email=data['email']
        password=data['password']
        cur=mysql.connection.cursor()
        cur.execute('select * from user_login where email = %s',[email])
        result=cur.fetchall()
        print(result)
        if len(result)>0:
            response = jsonify(message="Already email exists")
        else:
            cur.execute('INSERT into user_login (email,password) values(%s,%s)',(email,password))
            mysql.connection.commit()
            cur.execute('select user_id from user_login where email=%s',[email])
            result=cur.fetchone()
            print(result)
            res={
                "msg":"success",
                "id":result[0
                ]
            }
            response = jsonify(res)
        return response


@app.route('/loginuser',methods=['GET','POST'])
@cross_origin()
def loginuser():
    if request.method=='POST':
        data=json.loads(request.data)
        email=data['email']
        password=data['password']
        cur=mysql.connection.cursor()
        cur.execute('select * from user_login where email = %s',[email])
        result=cur.fetchall()
        print(result)
        if len(result)>0:
            cur.execute('select user_id from user_login where email=%s and password=%s',[email,password])
            result=cur.fetchone()
            print(result)
            if result==None:
                response = jsonify(message="incorrect password")
            else:
                r=result
                res={
                    "msg":"success",
                    "id":r[0]
                }
                response = jsonify(res)
        else:
            response = jsonify(message="please register to continue")
        return response


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
        cur.execute('SELECT * from login_with_google where email=%s',[email])
        result=cur.fetchall()
        print("result-----",result)
        if len(result)>0:
            #response = jsonify(message="Already email exists")
            cur.execute('select user_id from login_with_google where email=%s',[email])
            result=cur.fetchone()
            print(result)
            res={
                "msg":"success",
                "id":result[0
                ],
                "email":email,
            }
            response = jsonify(res)
        else:
            cur.execute('INSERT into login_with_google (email,name,google_id) values(%s,%s,%s)',(email,name,googleid))
            mysql.connection.commit()
            cur.execute('select user_id from login_with_google where email=%s',[email])
            result=cur.fetchone()
            print(result)
            res={
                "msg":"success",
                "id":result[0
                ],
                "email":email,
            }
            response = jsonify(res)
        return response
    return "success"

@app.route("/questions",methods=['GET','POST'])
def questions():
    if request.method=='GET':
        response=jsonify(set1)
    if request.method=='POST':
        data=json.loads(request.data)
        print(data)
        response=jsonify(message="success")
    return response

@app.route("/changepassword",methods=['POST'])
def changePassword():
    if request.method=='POST':
        data=json.loads(request.data)
        print(data)
        id=data['id']
        oldpassword=data['oldpassword']
        newpassword=data['newpassword']
        cur=mysql.connection.cursor()
        cur.execute('SELECT * from user_login where user_id=%s',[id])
        result=cur.fetchall()
        print("result-----",result[0][2])
        password=result[0][2]
        if password==oldpassword:
            cur.execute("UPDATE user_login set password=%s where user_id=%s",[newpassword,id])
            mysql.connection.commit()
            response=jsonify(message="successfully updated")
        else:
            response=jsonify(message="Wrong password")
    return response

if __name__=='__main__':
    app.run(debug=True)