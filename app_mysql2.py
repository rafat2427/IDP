from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import os.path
# import yaml


app = Flask(__name__)

# Configure db
# db = yaml.load(open('db.yaml'))
# app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
# app.config['MYSQL_DB'] = db['mysql_db']

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

# Start coding

# @app.route('/')
# def index():
#     return render_template("about.php")
#
#
# @app.route('/users')
# def users():
#     cur = mysql.connection.cursor()
#     resultValue = cur.execute("SELECT * FROM users")
#     if resultValue > 0:
#         userDetails = cur.fetchall()
#         return render_template('users.html',userDetails=userDetails)

# @app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    cur_id = mysql.connection.cursor()
    mem_id = cur_id.execute("SELECT persno, name from members")
    if mem_id > 0:
        mem_val = cur_id.fetchall()
    return render_template('index2.php', mem_val = mem_val)

# @app.route('/users')
# def users():
#     cur_member = mysql.connection.cursor()
#     cur_gp = mysql.connection.cursor()
#     resultValue = cur_member.execute("SELECT * FROM members")
#     groupValue = cur_gp.execute("SELECT * FROM gp")
#     if resultValue > 0 or groupValue > 0:
#         userDetails = cur_member.fetchall()
#         groupDetails = cur_gp.fetchall()
#         return render_template('members group.php',userDetails=userDetails, groupDetails=groupDetails)
#
# @app.route('/show')
# def show_data():
#     csv1 = pd.read_csv("status_1.csv")
#     print(csv1)
#     val_list = csv1.values.tolist()
#     c_yes=val_list.count('Yes')
#     c_no=val_list.count('No')
#     state=1
#     if c_no > c_yes:
#      state = 2
#
#     return render_template('show_status.php',val_list=val_list,c_yes=c_yes,c_no=c_no)

@app.route('/status', methods=['POST', 'GET'])
def show_status():
    if request.method == 'POST' or request.method == 'GET':
        # Fetch form data
        # val_pers = request.form.get('select_pers')
        val_pers = request.form['select_pers']
        print(val_pers)
        stable_status = str(1)
        wng_status = str(1)
        p_no = str(val_pers)

        cur = mysql.connection.cursor()
        # cur.execute("UPDATE status SET sta_id = 2 WHERE persno =  %s",  p_no )
        cur.execute("UPDATE status SET sta_id = %s WHERE persno = %s", (wng_status, p_no))
        mysql.connection.commit()
        cur.close()

    csv1 = pd.read_csv("status_1.csv")

    print(csv1)
    val_list = csv1.values.tolist()
    yes_count = val_list.count("Yes")
    # yes_count = 5
    print(val_list)

    stat_id = mysql.connection.cursor()
    stat_exec = stat_id.execute("SELECT m.name, st.sta_name from members m natural join status natural join status_name st")
    if stat_exec > 0:
        stat_val = stat_id.fetchall()
    return render_template('show_status.php', val_list = val_list, stat_val=stat_val, wng=wng_status, typeQ=type(val_list), num=val_pers, yes_count=yes_count)



if __name__ == '__main__':
 app.run(debug=True)
