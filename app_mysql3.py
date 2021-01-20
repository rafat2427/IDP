from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import os.path
import pickle


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)




col_names = ['Time', 'Heartrate', 'Alphalow', 'AlphaHigh', 'Betalow', 'Betahigh', 'Attention', 'Mediation',
             'Blinkstrength', 'Status']

user_data='M/model_input.csv'
dataset = pd.read_csv(user_data, header=None, names=col_names)

dataset = dataset.iloc[1:]
print(dataset.head())

#split dataset in features and target variable
feature_cols = ['Time', 'Heartrate', 'Alphalow', 'AlphaHigh', 'Betalow', 'Betahigh', 'Attention', 'Mediation',
             'Blinkstrength']
df = pd.DataFrame(dataset)

for x in range(len(feature_cols)):
    df[feature_cols[x]] = pd.to_numeric(df[feature_cols[x]],errors='coerce')


X_test = df[feature_cols] # Features

Updated_Status=[]

def update_status(s):
    length=len(s)
    for x in range(length):
        col=[]
        if(s[x]== 0):
            col.append(dataset.Time[x+1])
            col.append('No')
        else:
            col.append(dataset.Time[x+1])
            col.append('Yes')
        #print(s[x])
        Updated_Status.append(col)
    return Updated_Status
#Predict the response for test dataset
model = pickle.load(open('M/model_2.pkl','rb'))
#print(model.predict([[2, 19, 6]]))
y_pred_user = model.predict(X_test)
user_status=update_status(y_pred_user)
print(user_status)




@app.route('/', methods=['GET', 'POST'])
def index():
    cur_id = mysql.connection.cursor()
    mem_id = cur_id.execute("SELECT persno, name from members")
    if mem_id > 0:
        mem_val = cur_id.fetchall()
    return render_template('index2.php', mem_val = mem_val, us_st=user_status)


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
