import os
import sqlite3
import logging
from logging.config import dictConfig
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'security.log',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS credit_cards
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  card_number TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if len(username) < 3 or len(password) < 8:
            app.logger.warning(f"Signup input validation violation: Username={username}")
            flash('Username must be at least 3 characters and password at least 8 characters long.')
            return redirect(url_for('signup'))
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, generate_password_hash(password)))
            conn.commit()
            app.logger.info(f"New user signed up: {username}")
            flash('Account created successfully!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            app.logger.warning(f"Signup attempt with existing username: {username}")
            flash('Username already exists.')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            app.logger.info(f"User logged in: {username}")
            return redirect(url_for('home'))
        else:
            app.logger.warning(f"Failed login attempt for username: {username}")
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/create_credit_card', methods=['GET', 'POST'])
def create_credit_card():
    if 'user_id' not in session:
        app.logger.warning(f"Unauthorized attempt to access create_credit_card")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        card_number = request.form['card_number']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO credit_cards (user_id, card_number) VALUES (?, ?)",
                  (session['user_id'], card_number))
        conn.commit()
        conn.close()
        app.logger.info(f"Credit card created for user_id: {session['user_id']}")
        flash('Credit card added successfully!')
        return redirect(url_for('home'))
    return render_template('create_credit_card.html')

@app.route('/view_credit_card/<int:card_id>')
def view_credit_card(card_id):
    if 'user_id' not in session:
        app.logger.warning(f"Unauthorized attempt to view credit card id: {card_id}")
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credit_cards WHERE id = ? AND user_id = ?", (card_id, session['user_id']))
    card = c.fetchone()
    conn.close()
    
    if card:
        app.logger.info(f"Credit card viewed - id: {card_id}, user_id: {session['user_id']}")
        return render_template('view_credit_card.html', card=card)
    else:
        app.logger.warning(f"Attempt to view non-existent or unauthorized credit card - id: {card_id}, user_id: {session['user_id']}")
        flash('Credit card not found or unauthorized.')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880)