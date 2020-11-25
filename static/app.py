from flask import Flask, session, render_template,request, url_for,redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from itsdangerous import URLSafeTimedSerializer
import smtplib
import math,random
from email.message import EmailMessage
from datetime import datetime

import os
app = Flask(__name__)


# Configure session to use filesystem

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://tlkbyctryyffkn:b0ab12cc98ffab444f5d1d07329271b38c4e253f6cf3d1368bed287623e3dda8@ec2-54-235-86-101.compute-1.amazonaws.com:5432/d4bmrsh5lptv18")
db = scoped_session(sessionmaker(bind=engine))

app.config["IMAGE_UPLOADS"] ="//home//rashi//elms//static//signature"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.config["MAX_IMAGE_FILESIZE"] = 50 * 1024

#notes.append(note)
# Python code to illustrate Sending mail from
# your Gmail account
def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/uploader", methods=["POST","GET"])
def uploader():
    message=(" ")
    if request.method == "POST" :
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    message=("File size exceeded")
                    return render_template("uploader.html",message=message)

                image = request.files["image"]

                if image.filename == "":
                    message=("No file name")
                    return render_template("uploader.html",message=message)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                    message=("Image Saved")

                    return render_template("uploader.html",message=message)

                else:
                    message=("That file extension is not allowed")
                    return render_template("uploader.html",message=message)

    return render_template("uploader.html",message=message)




def generateotp(n):
    digits = "0123456789"
    OTP =""
    for i in range(n):
        OTP+=digits[math.floor(random.random() *10)]
    return OTP


#flag = 0
def sendotp(sender,message):
    EMAIL_ADDRESS = "software.engwkze@gmail.com"
    EMAIL_PASSWORD = "April@2017"
    msg = EmailMessage()
    msg['Subject'] = 'IIITBH Employee Management System '
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = sender
    msg.set_content(message)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

@app.route("/mailcnfrm",methods=["POST","GET"])
def mailcnfrm():
    message=(" ")
    if request.method=="POST":
        chckmail= request.form.get("mailid")
        session["user1"] = chckmail
        session["category2"] = request.form.get("category")
        if session["category2"] == "faculty" :
            if(db.execute("SELECT *FROM faculty WHERE userid=:chckmail",{"chckmail":chckmail}).fetchone() is None):
                message = ("Email does not exits")
            else:
                message=generateotp(4)
                session["otp2"]=message
                sender=chckmail
                sendotp(sender,message)
                return render_template("otpp.html",message="Check Your Mail")

        elif session["category2"] == "admin" :
            if(db.execute("SELECT *FROM admin WHERE userid=:chckmail",{"chckmail":chckmail}).fetchone() is None):
                message = ("Email does not exits")
            else:
                message=generateotp(4)
                session["otp2"]=message
                sender=chckmail
                sendotp(sender,message)
                return render_template("otpp.html",message="Check Your Mail")

        elif session["category2"] == "others" :
            if(db.execute("SELECT *FROM others WHERE userid=:chckmail",{"chckmail":chckmail}).fetchone() is None):
                message = ("Email does not exits")
            else:
                message=generateotp(4)
                session["otp2"]=message
                sender=chckmail
                sendotp(sender,message)
                return render_template("otpp.html",message="Check Your Mail")

        elif session["category2"] == "staff" :
            if(db.execute("SELECT *FROM staff WHERE userid=:chckmail",{"chckmail":chckmail}).fetchone() is None):
                message = ("Email does not exits")
            else:
                message=generateotp(4)
                session["otp2"]=message
                sender=chckmail
                sendotp(sender,message)
                return render_template("otpp.html",message="Check Your Mail")



    return render_template("remail.html",message=message)

@app.route("/reset",methods=["POST","GET"])
def reset():
    if request.method =="POST":
        temp_otp= session["otp2"]
        entered_otp= request.form.get("otp")
        if temp_otp == entered_otp:
            return render_template("pswdreset.html")

        else:
            message=("Invalid OTP")
            return render_template("otpp.html", message=message)

@app.route("/pswdreset",methods=["POST"])
def pswdreset():
    if request.method =="POST":
        usr = session["user1"]
        newpassword = request.form.get("newpassword")
        category = session["category2"]
        if category == "faculty":
            db.execute("UPDATE faculty set password=:newpassword WHERE userid=:usr",{"usr":usr,"newpassword":newpassword})
            db.commit()
            message=("Successfully Password Reset")
            return render_template("login.html",message=message)
        elif category == "admin":
            db.execute("UPDATE admin set password=:newpassword WHERE userid=:usr",{"usr":usr,"newpassword":newpassword})
            db.commit()
            message=("Successfully Password Reset")
            return render_template("login.html",message=message)

        elif category == "others":
            db.execute("UPDATE others set password=:newpassword WHERE userid=:usr",{"usr":usr,"newpassword":newpassword})
            db.commit()
            message=("Successfully Password Reset")
            return render_template("login.html",message=message)

        elif category == "staff":
            db.execute("UPDATE staff set password=:newpassword WHERE userid=:usr",{"usr":usr,"newpassword":newpassword})
            db.commit()
            message=("Successfully Password Reset")
            return render_template("login.html",message=message)



@app.route("/otpcheck", methods=["POST"])
def otpcheck():
    userid = session["temp_userid"]
    entered_otp = request.form.get("otpverify")
    OTP = session["OTP"]
    print(OTP)
    if session["temp_category"] == "admin" :
        if OTP == entered_otp :
            message = "Successfully Registered"
            db.execute("UPDATE admin SET verify = 1 WHERE userid=:userid",{"userid":userid})
            db.commit()
            return render_template("login.html",message=message)
        else :
            message = "Incorrect OTP!!"
            return render_template("otp.html",messsage=message)
    elif session["temp_category"] == "faculty" :
        if OTP == entered_otp :
            message = "Successfully Registered Please Login Again!"
            db.execute("UPDATE faculty SET verify = 1 WHERE userid=:userid",{"userid":userid})
            db.commit()
            return render_template("login.html",message=message)
        else :
            message = "Incorrect OTP!!"
            return render_template("otp.html",message=message)
    elif session["temp_category"] == "others" :
        if OTP == entered_otp :
            message = "Successfully Registered Please Login Again!"
            db.execute("UPDATE others SET verify = 1 WHERE userid=:userid",{"userid":userid})
            db.commit()
            return render_template("login.html",message=message)
        else :
            message = "Incorrect OTP!!"
            return render_template("otp.html",message=message)
    elif session["temp_category"] == "staff" :
        if OTP == entered_otp :
            message = "Successfully Registered Please Login Again!"
            db.execute("UPDATE staff SET verify = 1 WHERE userid=:userid",{"userid":userid})
            db.commit()
            return render_template("login.html",message=message)
        else :
            message = "Incorrect OTP!!"
            return render_template("otp.html",message=message)




@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST" :
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        category = request.form.get('category')
        gender = request.form.get('gender')
        age = request.form.get('age')
        branch = request.form.get('branch')
        position = request.form.get("position")

        if category == "admin" :
            if (db.execute("SELECT * FROM admin WHERE userid=:username AND verify=1",{"username":username}).fetchone() is None) :
                db.execute("INSERT INTO admin (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                query = db.execute("SELECT * FROM admin WHERE userid=:username",{"username":username}).fetchone()
                id = query.id
                db.execute("INSERT INTO admin_info (id,name,age,gender) VALUES (:id,:name,:age,:gender)",{"name":name,"id":id,"age":age,"gender":gender})
                db.commit()
                OTP = generateotp(4)
                session["OTP"] = OTP
                sendotp(username,"Dear User, Your OTP for registration is :"+str(OTP))
                session["temp_userid"]=username;
                session["temp_category"] = "admin"
                return render_template("otp.html")
            else :
                message = ("Username Already exists")

        elif category == "faculty":
            if (db.execute("SELECT * FROM faculty WHERE userid=:username AND verify=1",{"username":username}).fetchone() is None) :
                if position == "HOD" :
                    h = db.execute("SELECT * FROM faculty_info WHERE position='HOD' AND department=:branch",{"branch":branch}).fetchone()
                    if h is None :
                        message=("HOD Already Exists")
                        return render_template("register.html",message=message)
                db.execute("INSERT INTO faculty (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                query = db.execute("SELECT * FROM faculty WHERE userid=:username",{"username":username}).fetchone()
                id = query.id
                db.execute("INSERT INTO faculty_info (id,name,age,department,gender,position) VALUES (:id,:name,:age,:branch,:gender,:position)",{"name":name,"id":id,"age":age,"branch":branch,"gender":gender,"position":position})
                db.commit()
                OTP = generateotp(4)
                session["OTP"] = OTP
                sendotp(username,"Dear User, Your OTP for registration is :"+str(OTP))
                session["temp_userid"]=username;
                session["temp_category"] = "faculty"
                return render_template("otp.html")
            else :
                message = ("Username Already exists")

        elif category == "others":
            if (db.execute("SELECT * FROM others WHERE userid=:username AND verify=1",{"username":username}).fetchone() is None) :
                db.execute("INSERT INTO others (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                query = db.execute("SELECT * FROM others WHERE userid=:username",{"username":username}).fetchone()
                id = query.id
                db.execute("INSERT INTO others_info (id,name,age,department,gender,position) VALUES (:id,:name,:age,:branch,:gender,:position)",{"name":name,"id":id,"age":age,"branch":branch,"gender":gender,"position":position})
                db.commit()
                OTP = generateotp(4)
                session["OTP"] = OTP
                sendotp(username,OTP)
                session["temp_userid"]=username;
                session["temp_category"] = "others"
                return render_template("otp.html")
            else :
                message = ("Username Already exists")

        elif category == "staff":
            if (db.execute("SELECT * FROM staff WHERE userid=:username AND verify=1",{"username":username}).fetchone() is None) :
                db.execute("INSERT INTO staff (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                query = db.execute("SELECT * FROM staff WHERE userid=:username",{"username":username}).fetchone()
                id = query.id
                db.execute("INSERT INTO staff_info (id,name,age,gender,position) VALUES (:id,:name,:age,:gender,:position)",{"name":name,"id":id,"age":age,"gender":gender,"position":position})
                db.commit()
                OTP = generateotp(4)
                session["OTP"] = OTP
                sendotp(username,OTP)
                session["temp_userid"]=username;
                session["temp_category"] = "staff"
                return render_template("otp.html")
            else :
                message = ("Username Already exists")

    else :
        message=(" ")

    return render_template("register.html",message=message)

@app.route("/")
def index():
    return render_template("slide.html")

@app.route("/login")
def login():
    message = ("")
    return render_template("login.html",message=message)

@app.route("/home",methods=["POST","GET"])
def home():
    if request.method == "POST":
        username =request.form.get("v_username")
        password = request.form.get("v_password")
        category = request.form.get("v_category")

        if category == "admin" :
            query=db.execute("SELECT * FROM admin WHERE userid=:username AND password=:password AND verify=1",{"username":username, "password":password}).fetchone()
            if (query is None):
                message = ("Incorrect Username or Password Admin")
                return render_template("login.html",message=message)
            else :
                session["logged_user"]=username
                session["category"]="admin"
                session["id"] = query.id
                id = query.id
                info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
                leave = db.execute("SELECT * FROM admin_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,admin=1)

        elif category == "faculty" :
            query = db.execute("SELECT * FROM faculty WHERE userid=:username AND password=:password AND verify=1",{"username":username, "password":password}).fetchone()
            if (query is None):
                message = ("Incorrect Username or Password faculty")
                return render_template("login.html",message=message)
            else :
                session["logged_user"]=username
                session["category"] = "faculty"
                id = query.id
                session["id"]=id
                info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
                session["department"] = info.department
                leave = db.execute("SELECT * FROM faculty_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                if db.execute("SELECT * FROM faculty_info WHERE id=:id AND position iLIKE '%hod%'  ",{"id":id}).fetchone() is None:
                    hod = 0;
                else :
                    hod = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,hod=hod,admin=0)

        elif category == "others" :
            query = db.execute("SELECT * FROM others WHERE userid=:username AND password=:password AND verify=1",{"username":username, "password":password}).fetchone()
            if (query is None):
                message = ("Incorrect Username or Password Others")
                return render_template("login.html",message=message)
            else :
                session["logged_user"]=username
                session["category"]="others"
                id = query.id
                session["id"] = query.id
                info = db.execute("SELECT * FROM others_info WHERE id=:id",{"id":id}).fetchone()
                session["department"] = info.department
                leave = db.execute("SELECT * FROM others_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,admin=0)
        elif category == "staff" :
            query = db.execute("SELECT * FROM staff WHERE userid=:username AND password=:password AND verify=1",{"username":username, "password":password}).fetchone()
            if (query is None):
                message = ("Incorrect Username or Password Others")
                return render_template("login.html",message=message)
            else :
                session["logged_user"]=username
                session["category"]="staff"
                id = query.id
                session["id"] = query.id
                info = db.execute("SELECT * FROM staff_info WHERE id=:id",{"id":id}).fetchone()
                leave = db.execute("SELECT * FROM staff_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,admin=0)
    elif request.method == "GET" :
        username = session["logged_user"]
        category = session["category"]
        id = session["id"]
        if category == "admin" :
            query = db.execute("SELECT * FROM admin WHERE id=:id",{"id":id}).fetchone()
            info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
            leave = db.execute("SELECT * FROM admin_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
            if (leave is None) :
                leaveapplied = 0;
            else :
                leaveapplied = 1;
            return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,admin=1)
        elif category == "faculty" :
                query = db.execute("SELECT * FROM faculty WHERE id=:id",{"id":id}).fetchone()
                info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
                leave = db.execute("SELECT * FROM faculty_leave WHERE id=:id  AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                if db.execute("SELECT * FROM faculty_info WHERE id=:id AND position iLIKE '%hod%'  ",{"id":id}).fetchone() is None:
                    hod = 0;
                else :
                    hod = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,hod=hod,admin=0)
        elif category == "others" :
                query = db.execute("SELECT * FROM others WHERE id=:id",{"id":id}).fetchone()
                info = db.execute("SELECT * FROM others_info WHERE id=:id",{"id":id}).fetchone()
                leave = db.execute("SELECT * FROM others_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,admin=0)
        elif category == "staff" :
                query = db.execute("SELECT * FROM staff WHERE id=:id",{"id":id}).fetchone()
                info = db.execute("SELECT * FROM staff_info WHERE id=:id",{"id":id}).fetchone()
                leave = db.execute("SELECT * FROM staff_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
                if (leave is None) :
                    leaveapplied = 0;
                else :
                    leaveapplied = 1;
                return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied,admin=0)

@app.route("/rejoin", methods=["POST","GET"])
def rejoin():
    user_id = session["id"]
    category = session["category"]
    db.execute("DELETE FROM station_leave WHERE id=:id AND category=:category",{"id":user_id,"category":category})
    if request.method == "POST" :
        rejoin_date = request.form.get("rejoin_date")
        if session["category"] == "faculty":
            db.execute("INSERT INTO faculty_rejoin (rejoin_date,id) VALUES (:rejoin_date,:user_id)",{"rejoin_date":rejoin_date,"user_id":user_id})
            db.commit()
            db.execute("UPDATE faculty_leave SET status=1 WHERE id=:id",{"id":user_id})
            db.commit()
            return redirect(url_for("home"))
        elif session["category"] == "admin" :
            db.execute("INSERT INTO admin_rejoin (rejoin_date,id) VALUES (:rejoin_date,:user_id)",{"rejoin_date":rejoin_date,"user_id":user_id})
            db.commit()
            db.execute("UPDATE admin_leave SET status=1 WHERE id=:id",{"id":user_id})
            db.commit()
            return redirect(url_for("home"))
        elif session["category"] == "others":
            db.execute("INSERT INTO others_rejoin (rejoin_date,id) VALUES (:rejoin_date,:user_id)",{"rejoin_date":rejoin_date,"user_id":user_id})
            db.commit()
            db.execute("UPDATE others_leave SET status=1 WHERE id=:id",{"id":user_id})
            db.commit()
            return redirect(url_for("home"))
        elif session["category"] == "staff":
            db.execute("INSERT INTO staff_rejoin (rejoin_date,id) VALUES (:rejoin_date,:user_id)",{"rejoin_date":rejoin_date,"user_id":user_id})
            db.commit()
            db.execute("UPDATE staff_leave SET status=1 WHERE id=:id",{"id":user_id})
            db.commit()
            return redirect(url_for("home"))
    if session["category"] == "faculty":
        leave_from = db.execute("SELECT leave_from FROM faculty_leave WHERE id =:id",{"id":user_id}).fetchone()
        leave_upto = db.execute("SELECT leave_upto FROM faculty_leave WHERE id =:id",{"id":user_id}).fetchone()
        query = db.execute("SELECT * FROM faculty_info WHERE id = :user_id",{"user_id":user_id}).fetchone()
    elif session["category"] == "admin":
        leave_from = db.execute("SELECT leave_from FROM admin_leave WHERE id =:id",{"id":user_id}).fetchone()
        leave_upto = db.execute("SELECT leave_upto FROM admin_leave WHERE id =:id",{"id":user_id}).fetchone()
        query = db.execute("SELECT * FROM admin_info WHERE id = :user_id",{"user_id":user_id}).fetchone()
    if session["category"] == "others":
        leave_from = db.execute("SELECT leave_from FROM others_leave WHERE id =:id",{"id":user_id}).fetchone()
        leave_upto = db.execute("SELECT leave_upto FROM others_leave WHERE id =:id",{"id":user_id}).fetchone()
        query = db.execute("SELECT * FROM others_info WHERE id = :user_id",{"user_id":user_id}).fetchone()
    if session["category"] == "staff":
        leave_from = db.execute("SELECT leave_from FROM staff_leave WHERE id =:id",{"id":user_id}).fetchone()
        leave_upto = db.execute("SELECT leave_upto FROM staff_leave WHERE id =:id",{"id":user_id}).fetchone()
        query = db.execute("SELECT * FROM staff_info WHERE id = :user_id",{"user_id":user_id}).fetchone()
    return render_template("rejoining.html",info=query,leave_from=leave_from,leave_upto=leave_upto)

@app.route("/leave", methods=["POST","GET"])
def leave():

    user = session["logged_user"]
    cat = session["category"]
    id = session["id"]
    now = datetime.now()
    cur_date = now.strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        idd = int(id)
        leave_from = request.form.get("leave_from")
        leave_upto = request.form.get("leave_upto")
        nature = request.form.get("nature")
        no_of_days = int(request.form.get("no_of_days"))
        reason = request.form.get("reason")
        prefix_from = request.form.get("prefix_from")
        prefix_upto = request.form.get("prefix_upto")
        suffix_from = request.form.get("suffix_from")
        suffix_upto = request.form.get("suffix_upto")
        prefix_days = request.form.get("prefix_days")
        suffix_days = request.form.get("suffix_days")
        travel_concession = request.form.get("travel_concession")
        station_leave_permission = request.form.get("station_leave_permission")
        position = request.form.get("position")
        missed_classes = request.form.get("missed_classes")
        address = request.form.get("address")
        district = request.form.get("district")
        phone_no = request.form.get("phone_no")
        pin = request.form.get("pin")
        name = request.form.get("name")
        if position == "yes" :
            assign_duty_to_name = request.form.get("assign_duty_to_name")
            assign_duty_to_email = request.form.get("assign_duty_to_email")
            assign_duty_to_contact_no = request.form.get("assign_duty_to_contact_no")
        if station_leave_permission == "yes":
            from_date = request.form.get("from_date")
            from_fnan = request.form.get("from_fnan")
            from_time = request.form.get("from_time")
            to_date = request.form.get("to_date")
            to_time = request.form.get("to_time")
            to_fnan = request.form.get("to_fnan")
            db.execute("INSERT INTO station_leave (id,from_date,to_date,from_time,to_time,from_type,to_type,category) VALUES (:id,:from_date,:to_date,:from_time,:to_time,:from_fnan,:to_fnan,:cat)",{"id":idd,"from_date":from_date,"from_fnan":from_fnan,"from_time":from_time,"to_date":to_date,"to_fnan":to_fnan,"to_time":to_time,"cat":cat})
            db.commit()
        if position == "yes":
            assign_duty_to_name = request.form.get("assign_duty_to_name")
            assign_duty_to_email = request.form.get("assign_duty_to_email")
            assign_duty_to_contact_no = request.form.get("assign_duty_to_contact_no")
            db.execute("INSERT INTO resposibility (id,assign_duty_to_name,assign_duty_to_email,assign_duty_to_contact_no,category) VALUES (:id,:assign_duty_to_name,:assign_duty_to_email,:assign_duty_to_contact_no,:cat)",{"id":idd,"assign_duty_to_name":assign_duty_to_name,"assign_duty_to_email":assign_duty_to_email,"assign_duty_to_contact_no":assign_duty_to_contact_no,"cat":cat})
            db.commit()


        application_no = generateotp(8)
        if(cat == "faculty"):
            department = session["department"]
            db.execute("INSERT INTO faculty_leave (id,leave_from,leave_upto,approved,no_of_days,reason,nature,application_no, prefix_upto, prefix_from,  suffix_upto, suffix_from, prefix_days, suffix_days, travel_conseesion, station_leave_permission, position, missed_classes, address, district, phone_no, pin, name, department, cur_date) VALUES (:idd, :leave_from, :leave_upto, 0,:no_of_days,:reason,:nature,:application_no,:prefix_from, :prefix_upto, :suffix_from, :suffix_upto, :prefix_days, :suffix_days, :travel_conseesion, :station_leave_permission, :position, :missed_classes, :address, :district, :phone_no, :pin, :name, :department, :cur_date)",{"idd":idd, "leave_from":leave_from,"leave_upto":leave_upto,"no_of_days":no_of_days,"nature":nature, "reason":reason, "application_no":application_no, "prefix_from":prefix_from, "prefix_upto":prefix_upto, "suffix_from":suffix_from, "suffix_upto":suffix_upto, "prefix_days":prefix_days, "suffix_days":suffix_days, "travel_conseesion":travel_concession, "station_leave_permission":station_leave_permission, "position":position, "missed_classes":missed_classes, "address":address, "district":district, "phone_no":phone_no, "pin":pin, "name":name,"department":department,"cur_date" :cur_date})
            db.commit()
            if nature == "CL" :
                db.execute("UPDATE faculty_info SET available_cl = available_cl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "VL" :
                db.execute("UPDATE faculty_info SET available_vl = available_vl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "PL" :
                db.execute("UPDATE faculty_info SET available_pl = available_pl - 1 WHERE id=:id",{"id":id})
                db.commit()
            if nature == "EL" :
                db.execute("UPDATE faculty_info SET available_el = available_el - 1 WHERE id=:id",{"id":id})
                db.commit()
            if position == "yes" :
                sendotp(assign_duty_to_email,"Due to leave applied by :"+str(name)+" \nYou have to take over his/her duty from : "+str(leave_from)+" To :"+str(leave_upto))
            message = "Dear User,\n You've Successfully Applied for Leave. \nYour Application no is : "+str(application_no)
            sendotp(user,message)
            hodq = db.execute("SELECT id FROM faculty_info WHERE position iLIKE '%HOD%' AND department=:department ",{"department":department}).fetchone()
            hodid = hodq.id
            hoduserid = db.execute("SELECT userid FROM faculty WHERE id=:hodid ",{"hodid":hodid}).fetchone()
            messagetohod = "\nNew leave Application Received. \nApplicant Name : " +str(name)+ "\nApplication No. :" +str(application_no)
            sendotp(hoduserid,messagetohod)
            return redirect(url_for('home'))
        elif(cat == "admin"):
            db.execute("INSERT INTO admin_leave (id,leave_from,leave_upto,approved,no_of_days,reason,nature,application_no, prefix_upto, prefix_from,  suffix_upto, suffix_from, prefix_days, suffix_days, travel_conseesion, station_leave_permission, position, missed_classes, address, district, phone_no, pin, name, cur_date) VALUES (:idd, :leave_from, :leave_upto, 0,:no_of_days,:reason,:nature,:application_no,:prefix_from, :prefix_upto, :suffix_from, :suffix_upto, :prefix_days, :suffix_days, :travel_conseesion, :station_leave_permission, :position, :missed_classes, :address, :district, :phone_no, :pin, :name,:cur_date)",{"idd":idd, "leave_from":leave_from,"leave_upto":leave_upto,"no_of_days":no_of_days,"nature":nature, "reason":reason, "application_no":application_no, "prefix_from":prefix_from, "prefix_upto":prefix_upto, "suffix_from":suffix_from, "suffix_upto":suffix_upto, "prefix_days":prefix_days, "suffix_days":suffix_days, "travel_conseesion":travel_concession, "station_leave_permission":station_leave_permission, "position":position, "missed_classes":missed_classes, "address":address, "district":district, "phone_no":phone_no, "pin":pin, "name":name,"cur_date":cur_date})
            db.commit()
            if nature == "CL" :
                db.execute("UPDATE admin_info SET available_cl = available_cl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "VL" :
                db.execute("UPDATE admin_info SET available_vl = available_vl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "PL" :
                db.execute("UPDATE admin_info SET available_pl = available_pl - 1 WHERE id=:id",{"id":id})
                db.commit()
            if nature == "EL" :
                db.execute("UPDATE admin_info SET available_el = available_el - 1 WHERE id=:id",{"id":id})
                db.commit()
            message = "Dear User, \nYour Application no is : "+str(application_no)+" \n Successfully Applied for Leave."
            sendotp(user,message)
            return redirect(url_for('home'))
        elif(cat == "others"):
            department = session["department"]
            db.execute("INSERT INTO others_leave (id,leave_from,leave_upto,approved,no_of_days,reason,nature,application_no, prefix_upto, prefix_from,  suffix_upto, suffix_from, prefix_days, suffix_days, travel_conseesion, station_leave_permission, position, missed_classes, address, district, phone_no, pin, name, department, cur_date) VALUES (:idd, :leave_from, :leave_upto, 0,:no_of_days,:reason,:nature,:application_no,:prefix_from, :prefix_upto, :suffix_from, :suffix_upto, :prefix_days, :suffix_days, :travel_conseesion, :station_leave_permission, :position, :missed_classes, :address, :district, :phone_no, :pin, :name, :department,:cur_date)",{"idd":idd, "leave_from":leave_from,"leave_upto":leave_upto,"no_of_days":no_of_days,"nature":nature, "reason":reason, "application_no":application_no, "prefix_from":prefix_from, "prefix_upto":prefix_upto, "suffix_from":suffix_from, "suffix_upto":suffix_upto, "prefix_days":prefix_days, "suffix_days":suffix_days, "travel_conseesion":travel_concession, "station_leave_permission":station_leave_permission, "position":position, "missed_classes":missed_classes, "address":address, "district":district, "phone_no":phone_no, "pin":pin, "name":name,"department":department,"cur_date":cur_date})
            db.commit()
            if nature == "CL" :
                db.execute("UPDATE others_info SET available_cl = available_cl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "VL" :
                db.execute("UPDATE others_info SET available_vl = available_vl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "PL" :
                db.execute("UPDATE others_info SET available_pl = available_pl - 1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "EL" :
                db.execute("UPDATE others_info SET available_el = available_el - 1 WHERE id=:id",{"id":id})
                db.commit()
            if position == "yes" :
                sendotp(assign_duty_to_email,"Due to leave applied by :"+str(name)+" You have to take over his/her duty from : "+str(leave_from)+" To :"+str(leave_upto))
            message = "Successfully Applied for Leave. Your Application no is "+str(application_no)
            sendotp(user,message)
            return redirect(url_for('home'))
        elif(cat == "staff"):
            db.execute("INSERT INTO staff_leave (id,leave_from,leave_upto,approved,no_of_days,reason,nature,application_no, prefix_upto, prefix_from,  suffix_upto, suffix_from, prefix_days, suffix_days, travel_conseesion, station_leave_permission, position, missed_classes, address, district, phone_no, pin, name, cur_date) VALUES (:idd, :leave_from, :leave_upto, 0,:no_of_days,:reason,:nature,:application_no,:prefix_from, :prefix_upto, :suffix_from, :suffix_upto, :prefix_days, :suffix_days, :travel_conseesion, :station_leave_permission, :position, :missed_classes, :address, :district, :phone_no, :pin, :name,:cur_date)",{"idd":idd, "leave_from":leave_from,"leave_upto":leave_upto,"no_of_days":no_of_days,"nature":nature, "reason":reason, "application_no":application_no, "prefix_from":prefix_from, "prefix_upto":prefix_upto, "suffix_from":suffix_from, "suffix_upto":suffix_upto, "prefix_days":prefix_days, "suffix_days":suffix_days, "travel_conseesion":travel_concession, "station_leave_permission":station_leave_permission, "position":position, "missed_classes":missed_classes, "address":address, "district":district, "phone_no":phone_no, "pin":pin, "name":name,"cur_date":cur_date})
            db.commit()
            if nature == "CL" :
                db.execute("UPDATE staff_info SET available_cL=available_cl-1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "VL" :
                db.execute("UPDATE staff_info SET available_vl= available_vl-1 WHERE id=:id",{"id":id})
                db.commit()
            elif nature == "PL" :
                db.execute("UPDATE staff_info SET available_pl=available_pl-1 WHERE id=:id ",{"id":id})
                db.commit()
            elif nature == "EL" :
                db.execute("UPDATE staff_info SET available_el=available_el-1 WHERE id=:id",{"id":id})
                db.commit()
            if position == "yes" :
                sendotp(assign_duty_to_email,"Due to leave applied by :"+str(name)+" You have to take over his/her duty from : "+str(leave_from)+" To :"+str(leave_upto))
            message = "Dear User, \nSuccessfully Applied for Leave.\nYour Application no is : "+str(application_no)
            sendotp(user,message)
            return redirect(url_for('home'))

    if(cat=="faculty"):
        query = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
    elif(cat=="admin"):
        query = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
    elif(cat=="others"):
        query = db.execute("SELECT * FROM others_info WHERE id=:id",{"id":id}).fetchone()
    elif(cat=="staff"):
        query = db.execute("SELECT * FROM staff_info WHERE id=:id",{"id":id}).fetchone()
    return render_template("leaveapplication.html",query=query)

@app.route("/stationleave")
def stationleave():
    return render_template("stationleave.html")

@app.route("/list")
def list():
    id = session["id"]
    if session["category"] == "faculty" :
        department = session["department"]
        info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
        leave = db.execute("SELECT * FROM faculty_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
        if (leave is None) :
            leaveapplied = 0;
        else :
            leaveapplied = 1;
        lists= db.execute("SELECT * FROM faculty_leave WHERE approved = 0   AND department=:department ",{"department":department}).fetchall()
        return render_template("list.html",leave=leave,info=info,lists=lists,hod=1)
    elif session["category"] == "admin" :
        admin = 1;
        info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
        leave = db.execute("SELECT * FROM faculty_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
        if (leave is None) :
            leaveapplied = 0;
        else :
            leaveapplied = 1;
        lists= db.execute("SELECT * FROM faculty_leave WHERE approved = 0").fetchall()
        lists_admin= db.execute("SELECT * FROM admin_leave WHERE approved = 0").fetchall()
        lists_others= db.execute("SELECT * FROM others_leave WHERE approved = 0").fetchall()
        lists_staff= db.execute("SELECT * FROM staff_leave WHERE approved = 0").fetchall()
        return render_template("list.html",leave=leave,info=info,lists=lists,admin=1,lists_admin=lists_admin,lists_others=lists_others,lists_staff=lists_staff)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/extend",methods=["GET","POST"])
def extend():
    if request.method == "POST" :
        cat = session["category"]
        id = session["id"]
        extend_to =request.form.get("extend_to")
        if cat == "admin" :
            db.execute("UPDATE admin_leave SET leave_upto=:extend_to WHERE id=:id",{"id":id,"extend_to":extend_to})
            db.commit()
        elif cat == "faculty" :
            db.execute("UPDATE faculty_leave SET leave_upto=:extend_to WHERE id=:id",{"id":id,"extend_to":extend_to})
            db.commit()
        if cat == "others" :
            db.execute("UPDATE others_leave SET leave_upto=:extend_to WHERE id=:id",{"id":id,"extend_to":extend_to})
            db.commit()
        if cat == "staff" :
            db.execute("UPDATE staff_leave SET leave_upto=:extend_to WHERE id=:id",{"id":id,"extend_to":extend_to})
            db.commit()
        return redirect(url_for('home'))
    return render_template("extend.html")

@app.route("/printleave")
def printleave():
    id = session["id"]
    category = session["category"]
    if session["category"] == "admin" :
        info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM admin_leave WHERE id=:id",{"id":id}).fetchone()
    elif session["category"] == "faculty" :
        info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM faculty_leave WHERE id=:id",{"id":id}).fetchone()
    elif session["category"] == "others" :
        info = db.execute("SELECT * FROM others_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM others_leave WHERE id=:id",{"id":id}).fetchone()
    elif session["category"] == "staff" :
        info = db.execute("SELECT * FROM staff_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM staff_leave WHERE id=:id",{"id":id}).fetchone()
    station = query.station_leave_permission
    station_info = db.execute("SELECT * FROM station_leave WHERE id=:id AND category=:category",{"id":id,"category":category}).fetchone()
    return render_template("printleave.html",info=info,query=query,station=station,station_info=station_info)

@app.route("/applicant/<id>/<category>")
def applicant(id,category):
    if category == "faculty" :
        info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM faculty_leave WHERE id=:id",{"id":id}).fetchone()
    elif category == "admin" :
        info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM admin_leave WHERE id=:id",{"id":id}).fetchone()
    elif category == "others" :
        info = db.execute("SELECT * FROM others_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM others_leave WHERE id=:id",{"id":id}).fetchone()
    elif category == "staff" :
        info = db.execute("SELECT * FROM staff_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM staff_leave WHERE id=:id",{"id":id}).fetchone()
    return render_template("applicant.html",query=query,info=info)

@app.route("/requestform")
def requestform():
    return render_template("requestform.html")


@app.route("/disapprove/<id>/<category>", methods=["POST","GET"])
def disapprove(id,category):
    comment = request.form.get("comment")
    if category == "faculty" :
        db.execute("UPDATE faculty_leave SET approved=2,comment=:comment WHERE id=:id",{"id":id,"comment":comment})
        db.commit()
        applicant = db.execute("SELECT * FROM faculty WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\n Your Application for leave has been disapproved!!")
        return "Done"
    if category == "admin" :
        db.execute("UPDATE admin_leave SET approved=2,comment=:comment WHERE id=:id",{"id":id,"comment":comment})
        db.commit()
        applicant = db.execute("SELECT * FROM admin WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\n Your Application for leave has been disapproved!!")
        return "Done"
    if category == "others" :
        db.execute("UPDATE others_leave SET approved=2,comment=:comment WHERE id=:id",{"id":id,"comment":comment})
        db.commit()
        applicant = db.execute("SELECT * FROM others WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\nYour Application for leave applied on 18-10-2019 has been disapproved.")
        return "Done"
    if category == "staff" :
        db.execute("UPDATE staff_leave SET approved=2,comment=:comment WHERE id=:id",{"id":id,"comment":comment})
        db.commit()
        applicant = db.execute("SELECT * FROM staff WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\nYour Application for leave has been disapproved.")
        return "Done"

@app.route("/approve/<id>/<category>", methods=["POST","GET"])
def approve(id,category):
    if category == "faculty" :
        db.execute("UPDATE faculty_leave SET approved=1 AND status=1 WHERE id=:id",{"id":id})
        db.commit()
        applicant = db.execute("SELECT * FROM faculty WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\n Your Application for leave has been approved!!")
        return "Done"
    if category == "admin" :
        db.execute("UPDATE admin_leave SET approved=1 AND status=1  WHERE id=:id",{"id":id})
        db.commit()
        applicant = db.execute("SELECT * FROM admin WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\n Your Application for leave has been approved!!")
        return "Done"
    if category == "others" :
        db.execute("UPDATE others_leave SET approved=1 AND status=1  WHERE id=:id",{"id":id})
        db.commit()
        applicant = db.execute("SELECT * FROM others WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\n Your Application for leave has been approved!!")
        return "Done"
    if category == "staff" :
        db.execute("UPDATE staff_leave SET approved=1 AND status=1  WHERE id=:id",{"id":id})
        db.commit()
        applicant = db.execute("SELECT * FROM staff WHERE id=:id",{"id":id}).fetchone()
        applicant_email = applicant.userid
        sendotp(applicant_email,"\n Your Application for leave has been approved!!")
        return "Done"

@app.route('/manage')
def manage():
    id = session["id"]
    info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
    leave = db.execute("SELECT * FROM faculty_leave WHERE id=:id AND status=0 AND approved!=2",{"id":id}).fetchone()
    if (leave is None) :
        leaveapplied = 0;
    else :
        leaveapplied = 1;
    lists = db.execute("SELECT * FROM faculty_info WHERE position!='None'").fetchall()
    return render_template("employee.html",lists=lists,leaveapplied=leaveapplied,info=info)

@app.route("/viewhistory")
def viewhistory():
    cat = session["category"]
    id = session["id"]
    if cat == "faculty" :
        info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM faculty_leave WHERE id=:id",{"id":id}).fetchall()
    elif cat == "admin" :
        info = db.execute("SELECT * FROM admin_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM admin_leave WHERE id=:id",{"id":id}).fetchall()
    elif cat == "staff" :
        info = db.execute("SELECT * FROM staff_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM staff_leave WHERE id=:id",{"id":id}).fetchall()
    elif cat == "others" :
        info = db.execute("SELECT * FROM others_info WHERE id=:id",{"id":id}).fetchone()
        query = db.execute("SELECT * FROM others_leave WHERE id=:id",{"id":id}).fetchall()
    return render_template("history.html",query=query,info=info)


@app.route("/remove/<id>",methods=["POST","GET"])
def remove(id):
    db.execute("UPDATE faculty_info SET position='None' WHERE id=:id",{"id":id})
    db.commit()
    return "Done"

@app.route("/developer_info")
def developer_info():
	return render_template("developer_info.html")

if __name__ =="__main__":
    app.run(port=5000)
