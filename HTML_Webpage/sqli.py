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

# HOME PAGE

@app.route('/')
def home():
    return render_template('home.html')

# HOME PAGE

@app.route('/vehicles')
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

# MANY TO MANY RELATIONSHIP BELOW

@app.route('/persons')
def list_persons():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Person")
    persons = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('persons.html', persons=persons)


@app.route('/person_business/<int:person_id>')
def person_business(person_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT businesses.BusinessID, businesses.BusinessName, businesses.BusinessType, personbusiness.AssociationDate
    FROM businesses
    JOIN personbusiness ON businesses.BusinessID = personbusiness.BusinessID
    WHERE personbusiness.PersonID = %s
    """

    cursor.execute(query, (person_id,))
    businesses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('person_business.html', businesses=businesses, person_id=person_id)

@app.route('/business_person/<int:business_id>')
def business_person(business_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT p.PersonID, p.FirstName, p.LastName, pb.AssociationDate 
    FROM Person p
    JOIN PersonBusiness pb ON p.PersonID = pb.PersonID
    WHERE pb.BusinessID = %s
    """
    cursor.execute(query, (business_id,))
    persons = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('business_person.html', persons=persons, business_id=business_id)

@app.route('/add_person_business', methods=['GET', 'POST'])
def add_person_business():
    if request.method == 'POST':
        person_id = request.form['person_id']
        business_id = request.form['business_id']
        association_date = request.form['association_date']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO PersonBusiness (PersonID, BusinessID, AssociationDate) VALUES (%s, %s, %s)",
            (person_id, business_id, association_date)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('list_persons'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT PersonID, FirstName, LastName FROM Person")
    persons = cursor.fetchall()

    cursor.execute("SELECT BusinessID, BusinessName FROM Businesses")
    businesses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('add_person_business.html', persons=persons, businesses=businesses)

@app.route('/remove_person_business/<int:person_id>/<int:business_id>', methods=['POST'])
def remove_person_business(person_id, business_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM PersonBusiness WHERE PersonID = %s AND BusinessID = %s",
        (person_id, business_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('person_business', person_id=person_id))

# BUSINESS TABLE

@app.route('/businesses')
def list_businesses():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Businesses")
    businesses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('manage_businesses.html', businesses=businesses)

@app.route('/add_business', methods=['GET', 'POST'])
def add_business():
    if request.method == 'POST':
        business_name = request.form['business_name']
        business_type = request.form['business_type']
        connection = get_db_connection()
        cursor = connection.cursor()
        # Insert into the correct table name
        cursor.execute("INSERT INTO Businesses (BusinessName, BusinessType) VALUES (%s, %s)", (business_name, business_type))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('list_businesses'))
    return render_template('add_business.html')

@app.route('/edit_business/<int:business_id>', methods=['GET', 'POST'])
def edit_business(business_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        business_name = request.form['business_name']
        business_type = request.form['business_type']
        
        cursor.execute("""
            UPDATE Businesses 
            SET BusinessName = %s, BusinessType = %s 
            WHERE BusinessID = %s
        """, (business_name, business_type, business_id))
        connection.commit()
        
        cursor.close()
        connection.close()
        return redirect(url_for('manage_businesses'))
    
    cursor.execute("SELECT * FROM Businesses WHERE BusinessID = %s", (business_id,))
    business = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return render_template('edit_business.html', business=business)

@app.route('/delete_business/<int:business_id>', methods=['POST'])
def delete_business(business_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM Businesses WHERE BusinessID = %s", (business_id,))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('manage_businesses'))

@app.route('/manage_businesses', methods=['GET', 'POST'])
def manage_businesses():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Businesses")  # Use correct table name
    businesses = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('manage_businesses.html', businesses=businesses)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")