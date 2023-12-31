from collections import UserString
from functools import wraps
import pymongo
from cryptography.fernet import Fernet
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, render_template, request, redirect, session, url_for, flash



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['MyArtGalleryDB'] 
print(myclient.list_database_names())
mycol = mydb['ArtCollection'] 
myart = mydb['ArtistCollection']
myPhoto = mydb['PhotoCollection']
print(mydb.list_collection_names())
mycol.create_index("email", unique=True)
# x = mycol.insert_one(mydict)
# print(x.inserted_id)\

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

app.secret_key = '1809'

# Function to check if the user is logged in (you can modify this based on your authentication logic)
def is_user_logged_in():
    return 'logged_in' in session



def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')  
  return wrap

@app.route('/')
def home():
    if is_user_logged_in():
        return render_template('homeloggedin.html')
    else:
        return render_template('home.html')
    return render_template('home.html')

MIN_PASSWORD_LENGTH = 8
PASSWORD_REQUIREMENTS = "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."


def is_valid_password(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?\\/~`"\' ' for char in password):
        return False
    return True

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None  # Initialize the error message variable
    success_message = None # Initialize the success message variable
    success_message = None # Initialize the success message variable
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        password1 = request.form['password-reenter']
        key = Fernet.generate_key()
        # Instance the Fernet class with the key
        fernet = Fernet(key)
        encMessage = fernet.encrypt(password.encode())
        print("original string: ", password)
        print("encrypted string: ", encMessage)
        print(username)
        print(password)
        if password != password1:
            error_message = 'Passwords do not match.'
            print(error_message)
            return render_template('register.html',error_message=error_message)
        elif not is_valid_password(password):
            error_message = PASSWORD_REQUIREMENTS
            print(error_message)
            return render_template('register.html',error_message=error_message)
        else:
            try:
                # Insert the document into the collection
                mycol.insert_one({'username': None,'email': username, 'password': password, 'Bio':None})
                print("Document inserted successfully!")
                success_message="Registration successful! /n Please proceed to the login page"
                return render_template('register.html', success_message=success_message)
            except DuplicateKeyError as e:
                error_message="Email already exists"
                print("Error: The 'email' field must be unique.")
                return render_template('register.html',error_message=error_message)
            # mycol.insert_one({'email': username, 'password': password})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username)
        user = mycol.find_one({'email': username})
        print(user['email'])
        print(password)
        print(user['password'])
        if user['email']==username and user['password'] == password:
            # Successful login
            session['user_id'] = username
            print("valid username and password")
            return redirect(url_for('homeloggedin'))
        else:
            # Invalid credentials
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/home',methods=['GET', 'POST'])
def homeloggedin():
     return render_template('homeloggedin.html')

@app.route('/logout')
def logout():
    # Clear the session and log the user out
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    if request.method == 'GET': 
        user_id = session.get('user_id')
        print(user_id)
        user = mycol.find_one({'email': user_id})
        username = user['username']
        bio = user['Bio']
        if username and bio:
            return render_template('profile.html',username=username,bio=bio)
        else:
            a = user_id.find('@')
            bio = "Hey!"
            if a>0:
                user1 = user_id[:a]
                print(user1)
            return render_template('profile.html',username=user1,bio=bio)
    if request.method == 'POST': 
        b = request.form['']
        return render_template('profile.html')
    return render_template('profile.html')

@app.route('/updateprofile', methods=['GET', 'POST'])
def updateprofile():
    if request.method == 'GET': 
        user_id = session.get('user_id')
        print(user_id)
        user = mycol.find_one({'email': user_id})
        username = user['username']
        bio = user['Bio']
        if username and bio:
            print("Success")
        else:
            a = user_id.find('@')
            bio = "Hey!"
            if a>0:
                username = user_id[:a]
                print(username)
        if user_id:
            user = mycol.find_one({'email': user_id}) # Fetch user data from your data source
            return render_template('updateprofile.html', user=user,username=username,bio=bio)
    if request.method == 'POST':
        print("Yesssss")
        username = request.form['username']
        mail = request.form['email']
        account = request.form['account']
        password = mycol.find_one({'email': mail})
        if(account=='Artist'):
            # print(mycol.delete_one({'username':mail}))
            myart.insert_one({'username': username, 'email': mail,'password':password['password']})
            print('success')
        if(account=='Photographer'):
            myPhoto.insert_one({'username': username, 'email': mail,'password':password['password']})
            print('success')
        return render_template('profile.html', user=user)
    return render_template('updateprofile.html')

if __name__ == '__main__':
    app.debug =  True
    app.run()