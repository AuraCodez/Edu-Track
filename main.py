from flask import Flask, redirect, render_template, request, url_for, flash 
from flask import get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import pandas as pd
import sqlite3


app = Flask(__name__)

with open ("appPW.txt") as f: #to hide and open the secret key
    passW = f.readline()
    
    
app.config['SECRET_KEY'] = passW
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


conn = sqlite3.connect("instance/db.db", check_same_thread=False) #Making a connection to the database

cursor = conn.cursor()
query = 'SELECT * FROM student'

cursor.execute(query) #Execute this query
conn.commit()
students = cursor.fetchall()  # fetches all (or all remaining) rows of a query result set and returns a list of tuples.




class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(80), nullable=False) #To make the colmun not contain a NULL value.
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
class TA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    

class MyForm(FlaskForm):
    fullName = StringField('Enter Name: ', validators=[DataRequired()])
    age = StringField('Enter age', validators=[DataRequired()])
    email = StringField('Enter email', validators=[DataRequired()])
    submit = SubmitField("Register Here")

    
class TAForm(FlaskForm):
    fullName = StringField('Enter Name: ', validators=[DataRequired()])
    age = StringField('Enter age', validators=[DataRequired()])
    email = StringField('Enter email', validators=[DataRequired()])
    submit = SubmitField("Register Here")
    
 
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/register', methods=["GET", "POST"]) #The main page route
def register():
    student_form = MyForm()
    ta_form = TAForm()
    if student_form.validate_on_submit():
        student_register()
    elif ta_form.validate_on_submit():
        ta_register()
    
    return render_template('register.html', student_form=student_form, ta_form=ta_form)


@app.route('/student_register', methods=["GET","POST"])
def student_register():
    form = MyForm() 
    if form.validate_on_submit():
        flash("Record successfully added.")
        new_student = Student(fullName=form.fullName.data, age=form.age.data, email = form.email.data)
        cursor.execute("INSERT INTO student (fullName, age, email) VALUES (?, ?, ?)", (new_student.fullName, new_student.age, new_student.email))
        conn.commit()
        return redirect(url_for('register'))
    
    
@app.route('/ta_register', methods=["GET","POST"])
def ta_register():
    ta_form = TAForm()
    if ta_form.validate_on_submit():
        flash("Record successfully added.")
        new_TA = TA(fullName=ta_form.fullName.data, age=ta_form.age.data, email=ta_form.email.data)
        cursor.execute("INSERT INTO TA (fullName, age, email) VALUES (?, ?, ?)", (new_TA.fullName, new_TA.age, new_TA.email))
        conn.commit()
        return redirect(url_for('register'))
    
    
@app.route('/test')
def test():
     return render_template('test.html', students=students)
    
    
    

    
if __name__ == '__main__':
    app.run(debug=True)
