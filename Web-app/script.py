from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key for production

# Database configuration
DATABASE = 'XRPL.db'

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hash_password(request.form['password'])

        conn = connect_db()
        try:
            conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.")
        finally:
            conn.close()
    return render_template('signup.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])

        conn = connect_db()
        cursor = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash("Login successful! Welcome back.")
            return redirect(url_for('index'))
        else:
            flash("Login failed. Please check your email and password.")
    return render_template('login.html')

# Initialize the database and create the users table if it does not exist
def init_db():
    conn = connect_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    address TEXT NULL,
                    seed TEXT NULL,
                    public_key TEXT NULL,
                    private_key TEXT NULL,
                    balance TEXT NULL
                    )''')
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
