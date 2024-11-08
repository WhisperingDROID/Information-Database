#!/usr/bin/python3

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get('SQL_HOST'),
        user=os.environ.get('SQL_USER'),
        password=os.environ.get('SQL_PWD'),
        db=os.environ.get('SQL_DB'),
        port=os.environ.get('SQL_PORT')
    )
    return connection

@app.route('/')
def showTable():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Vehicle")
    vehicles = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', vehicles=vehicles)

@app.route('/submit_add_vehicle', methods=['GET', 'POST'])
def submit_add_vehicle():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        vin_number = request.form['vin_number']
        license_plate = request.form['license_plate']
        person_id = request.form['person_id']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Vehicle (Make, Model, Year, VIN_Number, LicensePlate, PersonID) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (make, model, year, vin_number, license_plate, person_id))
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect(url_for('showTable'))
    
    return render_template('add_vehicle.html')

@app.route('/delete_vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Vehicle WHERE VehicleID = %s", (vehicle_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('showTable'))

@app.route('/update_vehicle/<int:vehicle_id>', methods=['GET'])
def update_vehicle(vehicle_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Vehicle WHERE VehicleID = %s", (vehicle_id,))
    vehicle = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('update_vehicle.html', vehicle=vehicle)

@app.route('/submit_update/<int:vehicle_id>', methods=['POST'])
def submit_update(vehicle_id):
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    vin_number = request.form['vin_number']
    license_plate = request.form['license_plate']
    person_id = request.form['person_id']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Vehicle 
        SET Make = %s, Model = %s, Year = %s, VIN_Number = %s, LicensePlate = %s, PersonID = %s
        WHERE VehicleID = %s
    """, (make, model, year, vin_number, license_plate, person_id, vehicle_id))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('showTable'))

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")