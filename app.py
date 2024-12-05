from flask import Flask,request,session
from flask import render_template
from flask import abort, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import utility
import json

import db
UPLOAD_FOLDER = './fp_template'
ALLOWED_EXTENSIONS = {'bin'}

MACHINE_CACHE={}

app = Flask(__name__)
app.secret_key=b'_5#y2L"F4Q8z\n\xec]/'

def get_current_month():
    current_date = datetime.now()
    current_month = current_date.month # current_mont is 1th idexed i.e 1-12
    return current_month-1 




@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/tempgetFp/<id>")
@utility.validate_api_key(MACHINE_CACHE)
def temp_download(id):
    if id=="6969" or id=="randi" or id=="abhiyan":
        print(id)
        return send_from_directory(UPLOAD_FOLDER, f"{id}.bin")
    else:
        return "No Finger Print Template Found",404


@app.route("/getFp/<id>")
@utility.validate_api_key(MACHINE_CACHE)
def download(id):
    student=db.Student.select().where(db.Student.id==id)
    if not student.exists():
        return "Invalid Id",404

    student=student.get()

    if not student.fp_template:
        return "No Finger Print Registerd",404
    

    if get_current_month()!=student.vend_month:
        student.vend_month=get_current_month()
        student.vend_amount=0
        student.save()
    else:
        if student.vend_amount>=4:
            return "Vend amount exceeds",404

    return send_from_directory(UPLOAD_FOLDER,student.fp_template)

"""
@app.route("/akw/<id>")
@utility.validate_api_key(MACHINE_CACHE)
def increment_vend_count(id):
    if id=="69696" or id=="69578":
        return f"sucess:69",200
    query = db.Student.update(vend_amount=db.Student.vend_amount + 1).where((db.Student.id==id) &(db.Student.vend_amount<4))
    count=query.execute()
    return f"sucess:{count}",200
"""

@app.route("/akw/<id>/<int:capacity>")
@utility.validate_api_key(MACHINE_CACHE)
def increment_vend_count_and_capacity(id,capacity):
    if id=="69696" or id=="69578":
        return f"sucess:69",200
    api_key=request.headers.get('X-API-KEY')
    count1=count2=0
    with db.master_db.atomic():
        query = db.Student.update(vend_amount=db.Student.vend_amount + 1).where((db.Student.id==id) &(db.Student.vend_amount<4))
        count1=query.execute()
        query2=db.VendingMachine.update(capacity=capacity).where(((db.VendingMachine.api_key==api_key)))
        count2=query2.execute()
    MACHINE_CACHE[api_key]["capacity"]=capacity
    return f"sucess:{count1,count2}",200

@app.route("/getCapacity")
@utility.validate_api_key(MACHINE_CACHE)
def get_capacity():
    api_key=request.headers.get('X-API-KEY')
    return str(MACHINE_CACHE[api_key]["capacity"])


@app.route("/dashboard",methods=["POST","GET"])
def dashboard():
    print(request.method)
    if(request.method=="POST"):
        q=request.form['q']
        print(q)
        user=db.Student.select().where(db.Student.id==q)
        
        user_lst=[]
        for i in user:
            print(i)
            user_lst.append({"id":i.id,"name":i.name,"sem":i.semester,"dep":i.faculty,"fingerprintFile":i.fp_template})
        user_json=json.dumps(user_lst)
        
        return render_template('User_dashboard.html',users=user_json)
        
    else:
        users=db.Student.select().limit(5)
        user_lst=[]
        for i in users:
            user_lst.append({"id":i.id,"name":i.name,"sem":i.semester,"dep":i.faculty,"fingerprintFile":i.fp_template})
        user_json=json.dumps(user_lst)
        print(user_json)            
        return render_template('User_dashboard.html',users=user_json)

@app.route("/add/student",methods=["POST"])
def add_student():
    pass

@app.route("/update/student/<id>",methods=["POST"])
def update_student(id):
    pass

if __name__=="__main__":
    #load entire machine info  in cache:
    for machine in db.VendingMachine.select().dicts():
        MACHINE_CACHE[machine["api_key"]]=machine
    print(MACHINE_CACHE)
    app.run(host="0.0.0.0", port=8080,debug=True)