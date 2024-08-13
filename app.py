from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'Rohit@1122',
    'host': 'localhost',
    'database': 'owner_db'
}

# Establishing database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Route to display the form and list of owners
@app.route('/')
def index():
    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to database", 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM owners")
    owners = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', owners=owners)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    restaurant_name = request.form['restaurant_name']

    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to database", 500

    cursor = connection.cursor()

    try:
        # Insert data into the database
        cursor.execute('''
            INSERT INTO owners (name, age, gender, restaurant_name)
            VALUES (%s, %s, %s, %s)
        ''', (name, age, gender, restaurant_name))

        connection.commit()
        flash("Owner details added successfully!", "success")
    except Error as e:
        print("Error inserting data into MySQL", e)
        flash("Failed to add owner details.", "danger")

    cursor.close()
    connection.close()

    return redirect(url_for('index'))

# Route to handle owner deletion
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to database", 500

    cursor = connection.cursor()

    try:
        # Delete owner from the database by ID
        cursor.execute('DELETE FROM owners WHERE id = %s', (id,))
        connection.commit()
        flash("Owner details deleted successfully!", "success")
    except Error as e:
        print("Error deleting data from MySQL", e)
        flash("Failed to delete owner details.", "danger")

    cursor.close()
    connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
