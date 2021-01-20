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

@app.route('/')
# @app.route('/', methods=['GET', 'POST'])
def index():
#     if request.method == 'POST':
#         # Fetch form data
#         userDetails = request.form
#         name = userDetails['name']
#         email = userDetails['email']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
#         mysql.connection.commit()
#         cur.close()
#         return redirect('/users')
#     return render_template('index.html')
#
# @app.route('/users')
# def users():
    cur_member = mysql.connection.cursor()
    cur_gp = mysql.connection.cursor()
    resultValue = cur_member.execute("SELECT * FROM members")
    groupValue = cur_gp.execute("SELECT * FROM gp")
    if resultValue > 0 or groupValue > 0:
        userDetails = cur_member.fetchall()
        groupDetails = cur_gp.fetchall()
        return render_template('members group.php',userDetails=userDetails, groupDetails=groupDetails)

@app.route('/show')
def show_data():
    csv1 = pd.read_csv("status_1.csv")
    print(csv1)
    val_list = csv1.values.tolist()
    c_yes=val_list.count('Yes')
    c_no=val_list.count('No')
    state=1
    if c_no > c_yes:
     state = 2

    return render_template('show_status.php',val_list=val_list,c_yes=c_yes,c_no=c_no)

@app.route('/status')
def show_status():
    csv1 = pd.read_csv("status_1.csv")
    print(csv1)
    val_list = csv1.values.tolist()
    c_yes=val_list.count('Yes')
    c_no=val_list.count('No')
    # state=1
    # if c_no > c_yes
    #     state = 2
    state = 2

    cur_state = mysql.connection.cursor()
    cur_member = mysql.connection.cursor()
    cur_gp = mysql.connection.cursor()
    cur_state.execute("UPDATE `status` SET `sta_id` = %s WHERE `status`.`persno` = 12345 ", state)
    resultValue = cur_member.execute("SELECT * FROM members")
    groupValue = cur_gp.execute("SELECT * FROM status")
    if resultValue > 0 or groupValue > 0:
        userDetails = cur_member.fetchall()
        groupDetails = cur_gp.fetchall()
        return render_template('members group.php',userDetails=userDetails, groupDetails=groupDetails)



if __name__ == '__main__':
 app.run(debug=True)
