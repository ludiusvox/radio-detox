from ast import Tuple
from calendar import c
import email
from logging import error
import mailbox
import profile
from flask import Blueprint, appcontext_pushed, request, redirect, url_for, flash, g
from flask_security import auth_required, login_required, logout_user, login_user, current_user,  SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password, verify_password,_login_user
from flask.templating import render_template
from regex import P
from code.user.models import User
from flask.cli import with_appcontext
from code.extensions import db
bp_user = Blueprint('users',__name__,static_folder='/static',template_folder="../templates")
import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd
import sys
from flask_security import auth_token_required
from ..doc_comparison import *
import sqlite3
from code.user.database import db_session, engine, Base
@bp_user.before_request
def before_request():
    g.user = current_user
@bp_user.route('/dashboard/')
@login_required
def account(): 
    return render_template('dashboard.html')
@bp_user.route('/blog', methods=['GET','POST'])
@login_required
#This is the method that inputs the profile information
def blog():
    if request.method == 'GET': 
        return render_template("blog.html") 
    if request.method=='POST':
        db_file_name = 'enferno/enferno.db'
        conn = sqlite3.connect(db_file_name)
        cursor = conn.cursor()
        profile_information = request.form.get('message')
         
        Userprofile = User(email=current_user.email, profile_information=str(profile_information))
        db_session.add(Userprofile)
        db_session.commit()
        conn.close()
        feed()
        return render_template("after_profile.html")  
@bp_user.route('/eventblog', methods=['GET','POST'])
@login_required
#This is the method that inputs the profile information
def eventblog():
    if request.method == 'GET': 
        return render_template("event.html") 
    if request.method=='POST':
        db_file_name = 'enferno/enferno.db'
        conn = sqlite3.connect(db_file_name)
        cursor = conn.cursor()
        event = request.form.get('message')
        location = request.form.get('location')
        print(location)
        date = request.form.get('date')
        print(date)
        Userprofile = User(email=current_user.email, event=str(event), location=location, eventtime=date)
        db_session.add(Userprofile)
        db_session.commit()
        conn.close()
        eventfeed()
        return render_template("eventblog.html")   
@login_required
@bp_user.route("/after_profile",methods=['GET','POST'])
def feed():
    if request.method == 'GET': #worry about later
        db_file_name = 'enferno/enferno.db'
        conn = sqlite3.connect(db_file_name)
        cursor = conn.cursor()
        sql3 = cursor.execute("SELECT profile_information FROM user WHERE email =?",(current_user.email,))
        dforiginala = pd.DataFrame(sql3.fetchall())
        dforiginala=dforiginala.dropna()
        dforiginalstring= str(dforiginala[0].tolist())
        tableofcosines= list()
        #SQL query on other users profiles
        try:
            with engine.connect().execution_options(autocommit=True) as conn:
                query = conn.execute(text("SELECT email, profile_information FROM user"))         
                df = pd.DataFrame(query.fetchall(), columns=['email','profile_information'])
                df = df.fillna("0")
                df = df[~(df == 0).all(axis=1)]
                df = df.drop(index=0)
                long = pd.Series(range(0,len(df)))
                df.reset_index(drop=True)
                attndeeemail = current_user.email
                tableofcosines= []
                print(df) 
                emails = df['email'].to_list()
                corpus = df['profile_information'].to_list()
                add = []
                hostcorpus = []
                for i, tuple in enumerate(corpus):
                    add.append(corpus[i]) 
                for i , x in enumerate(add, start=0):
                    cosine = doc_comparisons(dforiginalstring,x)
                    tableofcosines.append(cosine)   
                    hostcorpus.append(x)       
                newlist = zip(emails,tableofcosines,hostcorpus)
                df1 = pd.DataFrame(zip(emails,tableofcosines, hostcorpus), columns=['hostmail', 'cosine','event'])   
                df1= df1.dropna()
                print(df1)
                df1['cosine'] = df1['cosine'].astype(float)
                df1 = df1.sort_values(by= ['cosine'], ascending=False) 
                df1 = df1.drop(columns=['cosine'])
                df1 = pd.DataFrame(df1)     
                return render_template("after_profile.html",tables=[df1.to_html(classes='email')],titles=['index','email','profile_information'])
        
        finally: conn.close()
            #new_df.insert(loc=groupname,column=['accntemail'],value=str(current_user.email))
             #           new_df.insert(loc=groupname,column=['email'],value=col)
@bp_user.route('/settings/', methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form.get("name")
        if name:
            user = User.query.get(current_user.id)
            user.name = name
            flash('Save successful. ')
            user.save()
    return render_template('settings.html')


@bp_user.route('/change-password/', methods=['GET','POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user = User.query.get(session.get('user_id'))
        oldpass = request.form.get("oldpass")
        if not verify_password(oldpass, user.password):
            flash('Wrong password entered.')
        else:
            password = request.form.get('password')
            if password != '':
                user.password = hash_password(password)
                user.save()
                flash ('Password changed successfully. ')
    return render_template('change-password.html')
@login_required
@bp_user.route("/events",methods=['GET','POST'])
def eventfeed():
    if request.method == 'GET': #worry about later
        db_file_name = 'enferno/enferno.db'
        conn = sqlite3.connect(db_file_name)
        cursor = conn.cursor()
        sql3 = cursor.execute("SELECT profile_information FROM user WHERE email =?",(current_user.email,))
        dforiginala = pd.DataFrame(sql3.fetchall())
        dforiginala=dforiginala.dropna()
        dforiginalstring= str(dforiginala[0].tolist())
        tableofcosines= list()
        #SQL query on other users profiles
        try:
            with engine.connect().execution_options(autocommit=True) as conn:
                query = conn.execute(text("SELECT email, event, location, eventtime FROM user"))         
                df = pd.DataFrame(query.fetchall(), columns=['email','event','location','eventtime'])
                df = df.fillna("0")
                df = df[~(df == 0).all(axis=1)]
                df = df.drop(index=0)
                long = pd.Series(range(0,len(df)))
                df.reset_index(drop=True)
                attndeeemail = current_user.email
                tableofcosines= []
                print(df) 
                emails = df['email'].to_list()
                corpus = df['event'].to_list()
                add = []
                hostcorpus = []
                location = df['location'].to_list()
                EventTime = df['eventtime'].to_list()
                locationlist = []
                timelist = []
                for i, tuple in enumerate(corpus):
                    add.append(corpus[i]) 
                for i , x in enumerate(add, start=0):
                    cosine = doc_comparisons(dforiginalstring,x)
                    tableofcosines.append(cosine)   
                    hostcorpus.append(x)     
                    locationlist.append(location[i])
                    timelist.append(EventTime[i])
                newlist = zip(emails,tableofcosines,hostcorpus,locationlist,timelist)
                df1 = pd.DataFrame(zip(emails,tableofcosines, hostcorpus,locationlist,timelist), columns=['hostmail', 'cosine','event','location','time'])   
                df1= df1.dropna()
                print(df1)
                df1['cosine'] = df1['cosine'].astype(float)
                df1 = df1.sort_values(by= ['cosine'], ascending=False) 
                df1 = df1.drop(columns=['cosine'])
                df1 = pd.DataFrame(df1)     
                return render_template("eventblog.html",tables=[df1.to_html(classes='email')],titles=['index','email','event','location','time'])
        
        finally: conn.close()
@bp_user.route('/logout')
def log_out():
    logout_user()
    return redirect(request.args.get('next') or '/')
