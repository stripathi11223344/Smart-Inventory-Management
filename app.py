from flask import Flask, render_template, request, redirect, url_for, flash
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
    "port": os.getenv("PORT")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home page — show all items
@app.route('/')
def index():
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

if __name__ == "__main__":
    app.run(debug=True)

