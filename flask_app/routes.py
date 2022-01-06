from __future__ import print_function
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt
from flask_app import IDAgeValidator as ID
from flask_app import app, db
from flask_app.models import User, Post
from flask_app.forms import PostForm
from flask_restful import Resource, Api, reqparse
import os
import requests
import json
from werkzeug.utils import secure_filename
import webbrowser

 # In python 2.7
import sys
URL = "https://geocode.search.hereapi.com/v1/geocode"
location =  "Autryville"#taking user input
api_key = 'HCQ-VGfKxiIoy1CoOH4mCCRAv9Up8ruRs09NrZQ9Dd4' # Acquire from developer.here.com
PARAMS = {'apikey':api_key,'q':location}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
data = r.json()
print(data, file=sys.stderr)

#Acquiring the latitude and longitude from JSON
latitude = data['items'][0]['position']['lat']
#print(latitude)
longitude = data['items'][0]['position']['lng']
#print(longitude)

UPLOAD_FOLDER = 'ID'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 10
@app.route('/map/newmap')

def map_func():
	return render_template('map.html',apikey=api_key,latitude=latitude,longitude=longitude)#map.html is my HTML file name


@app.route("/")
def index():
    db.create_all()
    posts = Post.query.all()
    return render_template("index.html", posts=posts)
@app.route("/notlogin")
def notlogin():

    return render_template("notlogin.html")


def map_func():

    return render_template('map.html',apikey=api_key,latitude=latitude,longitude=longitude)





from flask import send_from_directory

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/about")
def about():
    return render_template("about.html")
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET','POST'])


def predict():

    if request.method == 'POST':
            # check if the post request has the file part

        file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fname = request.form.get('fname')
            mname = request.form.get('mname')
            lname = request.form.get('lname')
            street = request.form.get('street')
            city = request.form.get('city')
            state = request.form.get('state')
            Zipcode = request.form.get('zip')
            age = request.form.get('age')
            model = ID.readdl.readlicense(app.config['UPLOAD_FOLDER']+"/"+filename)
            Zipcode = str(Zipcode)
            x = ID.verify.validate(model,fname,mname,lname,street,city,state,Zipcode,age)
            if x == str("ID works"):
                return render_template("login.html")
            else:
                return render_template("failed.html")

@app.route('/login', methods=['POST','GET'])
def logon():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(username=username).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')

            return redirect(url_for('index2'))


        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')



    return render_template("login.html")

@app.route('/post',methods=['POST'])
def loggedin():
    if request.method =='POST':
        return render_template('create_post.html')





@app.route('/register',methods=['POST','GET'])
def register():
    if request.method =='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password1')

        new_user = User(email=email, username=username,password=sha256_crypt.hash(password))

    # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    else:
        return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('register.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(username=username).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')

            return redirect(url_for('index2'))


        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')
@app.route("/internal")
def index2():
    db.create_all()
    posts = Post.query.all()
    return render_template("index2.html", posts=posts)

@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return render_template("logout.html")


# Check if username or email are already taken
def user_exists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,  content=form.content.data,author=current_user,Longitude=longitude,Latitude=latitude)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        map_func()
        webbrowser.open_new_tab('templates/map.html')
        return redirect(url_for('index2'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
@app.route('/_get_post_json/', methods=['POST'])
def get_post_json():
    data = request.get_json()

    return jsonify(status="success", data=data)
@app.route("/post")
def posts():
    db.create_all()
    posts = Post.query.all()
    return render_template("index2.html", posts=posts)
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        longitude = longitude
        latitude = latitude
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
