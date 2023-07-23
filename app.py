import pymongo
from flask import Flask, render_template, request, redirect

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']
print(myclient.list_database_names())
mycol = mydb['ArtGallery']
print(mydb.list_collection_names())
db = mydb

app = Flask(__name__)

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        password1 = request.form['password-reenter']
        if password == password1 :
            if db['users'].find_one({'email': username}):
                return render_template('register.html', error='Username already exists')
                # Insert the new user into the MongoDB collection
            else:
                db['users'].insert_one({'username': username, 'password': password1})
                return redirect('/login')
        return render_template('register.html',error='passwords should match')
    return render_template('register.html')


if __name__ == '__main__':
    app.debug =  True
    app.run(host='0.0.0.0', port=5000, threaded=True)