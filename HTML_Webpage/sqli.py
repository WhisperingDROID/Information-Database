#!/usr/bin/python3

# Credentials are sepererated using a .env file.

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os

load_dotenv()

app = Flask(__name__)

# Passwords are not hard coded
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get('SQL_HOST'),
        user=os.environ.get('SQL_USER'),
        password=os.environ.get('SQL_PWD'),
        db=os.environ.get('SQL_DB'),
        port=os.environ.get('SQL_PORT')
    )
    return connection

# Vehicle Table
@app.route('/')
def showTable():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Vehicle")
    vehicles = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('index.html', vehicles=vehicles)

# Connection to DB and Form Submission
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    vin_number = request.form['vin_number']
    license_plate = request.form['license_plate']
    person_id = request.form['person_id']

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check to see if PersonID is valid from the Person Table
    cursor.execute("SELECT * FROM person WHERE PersonID = %s", (person_id,))
    person = cursor.fetchone()

    # Error if PersonID is not found
    if not person:
        cursor.close()
        connection.close()
        return "Error: Please provide a valid PersonID. (1 or 2)", 400

    # Insert the new vehicle using the provided data (only if the PersonID exists)
    query = """
    INSERT INTO Vehicle (Make, Model, Year, VIN_Number, LicensePlate, PersonID)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (make, model, year, vin_number, license_plate, person_id))
    connection.commit()

    cursor.close()
    connection.close()

    # Redirection back to home page
    return redirect(url_for('showTable'))
    

# I added a delete function in case the user makes a mistake while entering the information. 
# It is also useful for updating the database later on if needed.

@app.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete the vehicle with the given VehicleID
    cursor.execute("DELETE FROM Vehicle WHERE VehicleID = %s", (vehicle_id,))
    connection.commit()

    cursor.close()
    connection.close()

    # Redirect back to the home page after deletion
    return redirect(url_for('showTable'))


    # SQL Injection Fix
    query = """
    INSERT INTO Vehicle (Make, Model, Year, VIN_Number, LicensePlate, PersonID)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (make, model, year, vin_number, license_plate, person_id))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('showTable'))

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
