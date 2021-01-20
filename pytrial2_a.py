from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY__DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

mysql = MySQL(app)




@app.route('/')
def index():
    return render_template("about.php")

if __name__ == "__main__":
    app.run(debug=True)
