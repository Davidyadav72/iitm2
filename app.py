from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table in the database
def create_tables():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS contact_entries (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        subject TEXT NOT NULL,
                        message TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Home page route
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page route with form handling
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        # Insert data into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO contact_entries (name, email, phone, subject, message) VALUES (?, ?, ?, ?, ?)',
                     (name, email, phone, subject, message))
        conn.commit()
        conn.close()

        return redirect(url_for('contact'))  # Redirect to avoid form resubmission

    return render_template('contact.html')

if __name__ == '__main__':
    create_tables()  # Ensure the table is created before running the app
    app.run(debug