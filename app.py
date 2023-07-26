import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, render_template, request, redirect

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['MyArtGalleryDB'] 
print(myclient.list_database_names())
mycol = mydb['ArtCollection'] 
print(mydb.list_collection_names())
mycol.delete_many({})
mydict = { "email": "psreddy102@gmail.com", "password": "123456" }
mycol.create_index("email", unique=True)
x = mycol.insert_one(mydict)
print(x.inserted_id)


# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


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

@app.route('/register', methods=['GET', 'POST', 'PUT', 'DELETE'])
def register():
    error_message = None  # Initialize the error message variable
    sucess_message = None # Initialize the success message variable
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        password1 = request.form['password-reenter']
        print(username)
        print(password)
        if password != password1:
            error_message = 'Passwords do not match.'
            print(error_message)
        elif not is_valid_password(password):
            error_message = PASSWORD_REQUIREMENTS
            print(error_message)
        else:
            try:
                # Insert the document into the collection
                mycol.insert_one({'email': username, 'password': password})
                print("Document inserted successfully!")
                return redirect('/login')
            except DuplicateKeyError as e:
                print("Error: The 'email' field must be unique.")
                return redirect('/register')
            # mycol.insert_one({'email': username, 'password': password})
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the MongoDB collection for the username and password
        
        if user:
            # Successful login
            return redirect('home')
        else:
            # Invalid credentials
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


if __name__ == '__main__':
    app.debug =  True
    app.run()