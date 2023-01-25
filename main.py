from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
with open ("appPW.txt") as f:
    passW = f.readline()
    
app.config['SECRET_KEY'] = passW

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

@app.route('/register') #The main page route
def register():
    form = MyForm() #The MyForm object so that it will get routed
    ta_form = TAForm()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


#dont put app.route in the class damn