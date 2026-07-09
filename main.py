# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for, send_from_directory
from animation_generator import generate_animation  # Your function above
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from werkzeug.utils import secure_filename
from PIL import Image
import math
import urllib.request
import urllib.parse


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="delivery_share"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

        
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ds_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = "Admin"
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ds_user WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg)

@app.route('/login_d', methods=['GET', 'POST'])
def login_d():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ds_deliver_person WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('dp_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_d.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    if request.method=='POST':
        name=request.form['name']
        location=request.form['location']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT count(*) from ds_user where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
    
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM ds_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO ds_user(id,name,location,city,mobile,email,uname,pass,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,location,city,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="success"
            #if mycursor.rowcount==1:
            
        else:
            msg='fail'
    return render_template('register.html',msg=msg,act=act)

@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    
    act=request.args.get("act")
    if request.method=='POST':
        
        category=request.form['category']
      
        mycursor.execute("SELECT max(id)+1 FROM ds_category")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO ds_category(id,category) VALUES (%s, %s)"
        val = (maxid,category)
        mycursor.execute(sql, val)
        mydb.commit()           
        
        msg="success"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ds_category where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_cat'))
        
    mycursor.execute("SELECT * FROM ds_category")
    data = mycursor.fetchall()

        
        
    return render_template('web/add_cat.html',msg=msg,act=act,data=data)

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_category")
    dat = mycursor.fetchall()
    
    act=request.args.get("act")
    if request.method=='POST':
        
        category=request.form['category']
        food=request.form['food']
        price=request.form['price']
        file = request.files['file']
      
        mycursor.execute("SELECT max(id)+1 FROM ds_food")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        fn=file.filename
        fnn="F"+str(maxid)+fn  
        food_img = secure_filename(fnn)
        file.save(os.path.join("static/upload", food_img))
            
        sql = "INSERT INTO ds_food(id,category,food,price,food_img) VALUES (%s, %s,%s,%s,%s)"
        val = (maxid,category,food,price,food_img)
        mycursor.execute(sql, val)
        mydb.commit()
        
        
        msg="success"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ds_food where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_food'))
    
    mycursor.execute("SELECT * FROM ds_food")
    data = mycursor.fetchall()

        
        
    return render_template('web/add_food.html',msg=msg,act=act,data=data,dat=dat)


@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_category")
    dat = mycursor.fetchall()
    
    act=request.args.get("act")
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']

        glocation = request.form['glocation']             
     
        l1=glocation.split("),")
        l2=l1[0].split("(")
        l3=l2[1].split(",")

        lat=l3[0]
        lon=l3[1]

        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT max(id)+1 FROM ds_deliver_person")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        sql = "INSERT INTO ds_deliver_person(id,name,mobile,email,latitude,longitude,uname,pass) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,name,mobile,email,lat,lon,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()
        
        msg="success"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ds_deliver_person where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_person'))
    
    mycursor.execute("SELECT * FROM ds_deliver_person")
    data = mycursor.fetchall()

        
        
    return render_template('web/add_person.html',msg=msg,act=act,data=data,dat=dat)









@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg=""
    act=request.args.get("act")
    if request.method=='POST':
        name=request.form['name']   
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
   
        mycursor.execute("SELECT max(id)+1 FROM ds_contact")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO ds_contact(id,name,email,subject,message) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid,name,email,subject,message)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        msg="success"
        #if mycursor.rowcount==1:
        
    return render_template('contact.html',msg=msg,act=act)

#K-Means Clustering - consumer grouping
def cluster():
    customers = {
        'C1': (1.2, 2.3),
        'C2': (2.1, 3.0),
        'C3': (-1.5, 1.8),
        'C4': (-2.0, -2.5),
        'C5': (3.3, -0.7),
        'C6': (-3.5, 2.2),
        'C7': (1.5, -3.0),
        'C8': (-1.8, -1.0),
        'C9': (0.5, -2.5),
        'C10': (2.8, 1.5)
    }

    # --- Convert to NumPy array ---
    coords = np.array(list(customers.values()))
    labels = list(customers.keys())

    # --- Set number of delivery agents (clusters) ---
    k = 3

    # --- Apply K-Means Clustering ---
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(coords)

    # --- Retrieve Results ---
    cluster_labels = kmeans.labels_          
    centroids = kmeans.cluster_centers_          

    # --- Group customers per cluster ---
    grouped_customers = {i: [] for i in range(k)}
    for idx, label in enumerate(cluster_labels):
        grouped_customers[label].append(labels[idx])

    # --- Print Result ---
    print("Grouped Customers (per delivery agent):")
    for cluster_id, customer_list in grouped_customers.items():
        print(f"Agent {cluster_id + 1} → {customer_list}")
        
#Firefly Algorithm -route optimize
class Firefly:
    def __init__(self, pop_size=20, alpha=1.0, betamin=1.0, gamma=0.01, seed=None):
        self.pop_size = pop_size
        self.alpha = alpha
        self.betamin = betamin
        self.gamma = gamma
        self.rng = default_rng(seed)

    def route_distance(route):
        total = 0
        for i in range(len(route) - 1):
            total += euclidean_distance(route[i], route[i+1])
        return total

    def move_towards(firefly_i, firefly_j, β, α):
        # Apply partial order of j into i
        new_route = partial_crossover(firefly_i, firefly_j, β)
        # Random swap (diversity)
        if random.random() < α:
            new_route = random_swap(new_route)
        return new_route

    def run(self, function, dim, lb, ub, max_evals):
        fireflies = self.rng.uniform(lb, ub, (self.pop_size, dim))
        intensity = np.apply_along_axis(function, 1, fireflies)
        best = np.min(intensity)

        evaluations = self.pop_size
        new_alpha = self.alpha
        search_range = ub - lb

        while evaluations <= max_evals:
            new_alpha *= 0.97
            for i in range(self.pop_size):
                for j in range(self.pop_size):
                    if intensity[i] >= intensity[j]:
                        r = np.sum(np.square(fireflies[i] - fireflies[j]), axis=-1)
                        beta = self.betamin * np.exp(-self.gamma * r)
                        steps = new_alpha * (self.rng.random(dim) - 0.5) * search_range
                        fireflies[i] += beta * (fireflies[j] - fireflies[i]) + steps
                        fireflies[i] = np.clip(fireflies[i], lb, ub)
                        intensity[i] = function(fireflies[i])
                        evaluations += 1
                        best = min(intensity[i], best)
        return best
@app.route('/admin')
def admin():
    uname=""
    if 'username' in session:
        uname = session['username']
        
   
    return render_template('web/admin.html',uname=uname)

@app.route('/view_share')
def view_share():
    uname=""
    if 'username' in session:
        uname = session['username']
        
    generate_animation('static/animation.gif')
    return render_template('web/view_share.html',uname=uname)

@app.route('/view_query', methods=['GET', 'POST'])
def view_query():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor.execute("SELECT * from ds_contact order by id desc")
    data = mycursor.fetchall()
    
    return render_template('web/view_query.html',msg=msg,data=data,uname=uname)

@app.route('/view_feed', methods=['GET', 'POST'])
def view_feed():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor.execute("SELECT * from ds_feedback order by id desc")
    data = mycursor.fetchall()
    
    return render_template('web/view_feed.html',msg=msg,data=data,uname=uname)


@app.route('/userhome')
def userhome():
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_user where uname=%s",(uname,))
    usr = mycursor.fetchone()
    
    return render_template('web/userhome.html',uname=uname,usr=usr)



@app.route('/user_book', methods=['GET', 'POST'])
def user_book():
    data=[]
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_user where uname=%s",(uname,))
    usr = mycursor.fetchone()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    mycursor.execute("SELECT * FROM ds_category")
    dat = mycursor.fetchall()

    if request.method=='POST':
        
        cat=request.form['cat']
        mycursor.execute("SELECT * FROM ds_food where category=%s",(cat,))
        data = mycursor.fetchall()

    else:
        mycursor.execute("SELECT * FROM ds_food")
        data = mycursor.fetchall()

    if act=="book":
        fid=request.args.get("fid")
        mycursor.execute('SELECT count(*) FROM ds_cart WHERE uname=%s && food_id = %s && status=0', (uname, fid))
        num = mycursor.fetchone()[0]

        mycursor.execute("SELECT * FROM ds_food where id=%s",(fid,))
        pdata = mycursor.fetchone()
        prd=pdata[2]
        price=pdata[3]
        cat=pdata[1]
        
        if num==0:
            mycursor.execute("SELECT max(id)+1 FROM ds_cart")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                
            sql = "INSERT INTO ds_cart(id, uname, food_id, status, rdate, price,category,qty,amount,bill_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
            val = (maxid, uname, fid, '0', rdate, price, cat, '0', '0','0')
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('book_food'))
        else:
            return redirect(url_for('book_food'))


    return render_template('web/user_book.html', uname=uname,act=act,usr=usr,data=data,dat=dat)

###
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  

    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

@app.route('/assign_delivery/<int:bill_id>')
def assign_delivery(bill_id):

    
    cursor = mydb.cursor(dictionary=True)

    # Get customer location
    cursor.execute("SELECT * FROM ds_bill WHERE id=%s", (bill_id,))
    bill = cursor.fetchone()

    cust_lat = bill['lat']
    cust_lon = bill['lon']

    # Get all delivery persons
    cursor.execute("SELECT * FROM ds_deliver_person")
    dps = cursor.fetchall()

    nearest_dp = None
    min_dist = 999999

    for dp in dps:
        dist = calculate_distance(cust_lat, cust_lon, dp['latitude'], dp['longitude'])

        if dist < min_dist:
            min_dist = dist
            nearest_dp = dp

    # Update bill with nearest delivery person
    cursor.execute("UPDATE ds_bill SET dp_id=%s WHERE id=%s", (nearest_dp['uname'], bill_id))
    mydb.commit()

    #return "Delivery Person Assigned: " + nearest_dp['name']
    return redirect(url_for('user_pay',bill_id=bill_id))


@app.route('/book_food', methods=['GET', 'POST'])
def book_food():
    msg=""
    data=[]
    act=request.args.get("act")
    amt=0
    bill_id=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_user where uname=%s",(uname,))
    usr = mycursor.fetchone()


    mycursor.execute("SELECT * FROM ds_cart c,ds_food u where c.food_id=u.id && c.status=0 && c.uname=%s",(uname,))
    data = mycursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")

    if request.method=='POST':
        qty=request.form.getlist('qty[]')
        rid=request.form.getlist('rid[]')
        glocation = request.form['glocation']             
     
        l1=glocation.split("),")
        l2=l1[0].split("(")
        l3=l2[1].split(",")

        lat=l3[0]
        lon=l3[1]

        
        
        mycursor.execute('SELECT count(*) FROM ds_cart WHERE uname=%s && status=0', (uname, ))
        num = mycursor.fetchone()[0]
        if num>0:
            mycursor.execute("SELECT max(id)+1 FROM ds_bill")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            j=0
            for rr in rid:
                mycursor.execute("SELECT price FROM ds_cart where id=%s",(rr, ))
                prc = mycursor.fetchone()[0]
                
                qty1=int(qty[j])
                amt=prc*qty1
                mycursor.execute("update ds_cart set status=1,qty=%s,amount=%s,bill_id=%s where uname=%s",(qty1,amt,maxid,uname))
                mydb.commit()
                j+=1


            dp_id=""
            sql = "INSERT INTO ds_bill(id, uname, amount, lat,lon,dp_id, pay_st, rdate,deliver_st) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s)"
            val = (maxid, uname, amt,lat,lon,dp_id, '0', rdate,'0')
            mycursor.execute(sql,val)
            mydb.commit()
            bill_id=str(maxid)
            #return redirect(url_for('user_pay',bill_id=str(maxid)))
            msg="assign"

    if act=="rem":
        rid=request.args.get("rid")
        mycursor.execute("delete from ds_cart where id=%s",(rid,))
        mydb.commit()
        return redirect(url_for('book_food'))

    return render_template('web/book_food.html',msg=msg,uname=uname,act=act,usr=usr,data=data,bill_id=bill_id)

@app.route('/user_pay', methods=['GET', 'POST'])
def user_pay():
    msg=""
    data=[]
    act=request.args.get("act")
    bill_id=request.args.get("bill_id")
    amt=0
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_user where uname=%s",(uname,))
    usr = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ds_bill where id=%s",(bill_id,))
    data = mycursor.fetchone()

    if request.method=='POST':
        card=request.form['card']
        mycursor.execute("update ds_bill set pay_st=1 where id=%s",(bill_id,))
        mydb.commit()
        msg="success"

    return render_template('web/user_pay.html', msg=msg,uname=uname,act=act,usr=usr,data=data)

@app.route('/user_order', methods=['GET', 'POST'])
def user_order():
    data=[]
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']
        
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ds_user where uname=%s",(uname,))
    usr = cursor.fetchone()


    cursor.execute("""
        SELECT b.*, d.name as dp_name, d.mobile as dp_mobile
        FROM ds_bill b
        LEFT JOIN ds_deliver_person d ON b.dp_id = d.uname
        WHERE b.uname = %s
        ORDER BY b.id DESC
    """, (uname,))

    data = cursor.fetchall()


    return render_template('web/user_order.html', uname=uname,act=act,usr=usr,data=data)


@app.route('/dp_home', methods=['GET', 'POST'])
def dp_home():
    data=[]
    act=request.args.get("act")
    amt=0
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_deliver_person where uname=%s",(uname,))
    usr = mycursor.fetchone()

    return render_template('web/dp_home.html', uname=uname,act=act,usr=usr,data=data)


@app.route('/dp_order', methods=['GET', 'POST'])
def dp_order():
    data=[]
    act=request.args.get("act")
    amt=0
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM ds_deliver_person where uname=%s",(uname,))
    usr = mycursor.fetchone()

    mycursor.execute("""
        SELECT * FROM ds_bill
        WHERE dp_id = %s
        ORDER BY id DESC
    """, (uname,))

    data = mycursor.fetchall()

    return render_template('web/dp_order.html', uname=uname,act=act,usr=usr,data=data)

@app.route('/start_delivery/<int:id>')
def start_delivery(id):
    
    cursor = mydb.cursor()

    cursor.execute("UPDATE ds_bill SET deliver_st=1 WHERE id=%s", (id,))
    mydb.commit()

    return redirect('/dp_order')

@app.route('/complete_delivery/<int:id>')
def complete_delivery(id):
    
    cursor = mydb.cursor()

    cursor.execute("UPDATE ds_bill SET deliver_st=2 WHERE id=%s", (id,))
    mydb.commit()

    return redirect('/dp_order')

@app.route('/view_map/<int:bill_id>')
def view_map(bill_id):

    
    cursor = mydb.cursor(dictionary=True)

    # Bill (customer)
    cursor.execute("SELECT * FROM ds_bill WHERE id=%s", (bill_id,))
    bill = cursor.fetchone()

    # Delivery person
    cursor.execute("SELECT * FROM ds_deliver_person WHERE uname=%s", (bill['dp_id'],))
    dp = cursor.fetchone()

    return render_template("web/map.html", bill=bill, dp=dp)

@app.route('/share')
def share():
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_deliver_person where uname=%s",(uname,))
    usr = mycursor.fetchone()

    
    generate_animation('static/animation.gif')
    return render_template('web/share.html',uname=uname,usr=usr)

@app.route('/add_feed', methods=['GET', 'POST'])
def add_feed():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ds_user where uname=%s",(uname,))
    usr = mycursor.fetchone()
    
    act=request.args.get("act")
    if request.method=='POST':
        
        feedback=request.form['feedback']
      
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT max(id)+1 FROM ds_feedback")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO ds_feedback(id,uname,feedback) VALUES (%s, %s, %s)"
        val = (maxid,uname,feedback)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        msg="success"
        #if mycursor.rowcount==1:
        
    return render_template('web/add_feed.html',msg=msg,act=act,uname=uname,usr=usr)

@app.route('/view_order')
def view_order():
    
    cursor = mydb.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.*, 
               d.name AS dp_name, d.mobile AS dp_mobile
        FROM ds_bill b
        LEFT JOIN ds_deliver_person d ON b.dp_id = d.uname
        ORDER BY b.id DESC
    """)

    data = cursor.fetchall()

    return render_template('web/view_order.html', data=data)

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


