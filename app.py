from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# -----------------------------------------
# Database setup (runs on startup)
# -----------------------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
              (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    #Insert a test user if the table is empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "supersecret"))
    conn.commit()
    conn.close()

init_db()

# --------------------------------------------
# Routes
# ---------------------------------------------------

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        #VULNERABLE QUERY - DO NOT USE IN REAL LIFE
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return "Login successful"
        else:
            return "Invalid credentials"
    else:
        # Render the login form
        with open('templates/login.html', 'r') as f:
            return render_template_string(f.read())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)