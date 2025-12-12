from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
  # you already have, keep any value

import mysql.connector
import os   # <-- needed for environment variables

app = Flask(__name__)
app.secret_key = "12345"  # any random string

# Database connection (using environment variables)
db_config = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
    "port": os.getenv("DB_PORT")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home page — show all items
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items ORDER BY id DESC")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", items=items)

# Add new item
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    category = request.form['category']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, quantity, category) VALUES (%s, %s, %s)",
        (name, quantity, category)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash("Item added successfully!")
    return redirect(url_for('index'))
# GET ITEM TO UPDATE
@app.route('/update_quantity/<int:id>', methods=['GET'])
def update_quantity(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id=%s", (id,))
    item = cursor.fetchone()
    conn.close()
    return render_template('update_quantity.html', item=item)

# UPDATE LOADED ITEM
@app.route('/update_quantity/<int:id>', methods=['POST'])
def update_quantity_post(id):
    quantity = request.form['quantity']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET quantity=%s WHERE id=%s", (quantity, id))
    conn.commit()
    conn.close()

    return redirect('/')


# Delete item
@app.route('/delete/<int:id>')
def delete_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Item deleted successfully!")
    return redirect(url_for('index'))

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # SIMPLE LOGIN (you can change username/password)
        if username == "SWAPNIL" and password == "BBDGROUP123":
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')




if __name__ == "__main__":
    app.run(debug=True)

