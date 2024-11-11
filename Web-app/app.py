from flask import Flask, render_template, request, jsonify, session, flash, redirect,url_for
from flask_cors import CORS
from predict import predict_activity
import numpy as np
import sqlite3
import hashlib
import xrpl
from xrplwallet import createwallet, getbalance,xrpTransfer,getseedToWallet

app = Flask(__name__)
app.secret_key = 'CWcLHp7HdBiAPIFMz8bFwwFp2S1KtnydjGLKDr4f3wdCpS2YjRxLv6OOQHLSqoJLCXsy0H9yvCS7UxlHFSfIkgrU7VSbwLL4CaaFtZAZ9Sf8s6MuPNjR7AFi2GP0SVBM'
# CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
db_name = 'XRPL.db'

def hash_password(password):
    """ Hash the password using SHA-256 """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Function to connect to the SQLite database
def connect_db(db_name):

    """ Connect to the SQLite database and return the connection object """
    conn = sqlite3.connect(db_name)
    return conn

# Function to execute a query (INSERT, UPDATE, DELETE, or SELECT)
def execute_query(conn, query, params=None):
    """ Execute a single query """
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()  # Commit the changes if the query modifies the database
    return cursor

# Function to fetch data from the database (for SELECT queries)
def fetch_data(conn, query, params=None):
    """ Fetch data from the database """
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()


# Function to close the connection to the database
def close_connection(conn):
    """ Close the SQLite database connection """
    conn.close()

def getloginUserData():
    conn = connect_db(db_name)
    # Generate a new wallet
    email = session['email']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    return user

conn = connect_db(db_name)
@app.route('/')
def home():
    return render_template('index.html', title="Home Page")

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = connect_db(db_name)
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email)
        # print(password)
        if not email or not password:
            flash('Both email and password are required!', 'error')
            return redirect(url_for('login'))
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user:
            # Compare hashed passwords
            hashed_password = str(user[3])
            if hashed_password == str(hash_password(password)):
                # Successful login: store user info in session
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['email'] = user[2]
                flash('Login successful!', 'success')
                return redirect(url_for('profile'))  # Redirect to the dashboard (or home page)

    return render_template('login.html',title="Registration")

@app.route('/register')
def signup():
    return render_template('signup.html',title="Registration")

@app.route('/register_save',methods=['POST'])
def reg():
    conn = connect_db(db_name)
    name = request.form['name']
    email = request.form['email']
    password = hash_password(request.form['password'])
    insert_data_query = "INSERT INTO users (name, email,password) VALUES (?, ?, ?)"
    execute_query(conn, insert_data_query, (name, email, password))
    return render_template('reg_success.html',title="Registration success")

@app.route('/profile')
def profile():
    if not session['email']:
        return redirect(url_for('login'))
    conn = connect_db(db_name)
    email = session['email']
    weather_data = weather_data = np.array([[24,48,25,50, 0, 2]]) # Indoor workout
    weather_data = np.array([[20, 55, 10, 0, 0, 1]]) # walking
    activity = predict_activity(weather_data)
    # Corrected query to retrieve a single row based on email
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    balance = getbalance(user[4])

    # Print the result
    # print(user["email"])
    return render_template('profile.html',title="Registration",activity=activity, user=user, balance=balance)

@app.route('/create_wallet')
def create_wallet():
    address, seed, balance = createwallet()

    query = """
        UPDATE users
        SET address = ?,
            seed = ?,
            balance = ?
        WHERE email = ?
        """
        
        # Connect to the database
    conn = connect_db(db_name)
    cursor = conn.cursor()
    email = session['email']
        # Execute the query with the provided values
    cursor.execute(query, (
            address,
            seed,
            balance,
            email
        ))

        # Commit the transaction
    conn.commit()

        # Close the connection
    conn.close()
    return redirect(url_for('profile')) 

@app.route('/xrp_payment', methods=['POST'])
def xrppayment():
    payment_wallet = request.form['token_receiver']
    amount = request.form['amount']
    user = getloginUserData()
    selfwallet = getseedToWallet(user[5])
    tr = xrpTransfer(selfwallet,user[4],payment_wallet,amount)
    return redirect(url_for('profile'))

if __name__ == '__main__':
    
    db_name = 'XRPL.db'
    # Connect to the database
    conn = connect_db(db_name)

    app.run(debug=True)
