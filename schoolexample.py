from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Extract MySQL credentials from environment variables
creds = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/showStudents', methods=['GET'])
def showStudents():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    sectionID = request.args.get('section_id')
    if sectionID:
        mycursor.execute("""SELECT student.id, first_name, last_name
                            FROM student
                            JOIN section_student ON student.id = section_student.student_id
                            WHERE section_student.section_id = %s""", (sectionID,))
        students = mycursor.fetchall()
        pageTitle = f"Students in Section {sectionID}"
    else:
        mycursor.execute("SELECT id, first_name, last_name FROM student")
        students = mycursor.fetchall()
        pageTitle = "All Students"

    mycursor.close()
    connection.close()
    return render_template('students.html', studentList=students, pageTitle=pageTitle)

@app.route('/showSections', methods=['GET', 'POST'])
def showSections():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    studentID = request.args.get('student_id')
    if studentID:
        # Handle new section registration if form is submitted
        if request.method == 'POST' and 'register_section_id' in request.form:
            new_section_id = request.form.get('register_section_id')
            if new_section_id:
                mycursor.execute("""INSERT INTO section_student (student_id, section_id) VALUES (%s, %s)""",
                                 (studentID, new_section_id))
                connection.commit()

        # Show sections the student is registered in
        mycursor.execute("""SELECT section.id, course.course_name, course.course_code
                            FROM section
                            JOIN section_student ON section.id = section_student.section_id
                            JOIN course ON course.id = section.course_id
                            WHERE section_student.student_id = %s""", (studentID,))
        registered_sections = mycursor.fetchall()

        # Show sections the student is not registered in
        mycursor.execute("""SELECT section.id, course.course_name, course.course_code
                            FROM section
                            JOIN course ON section.course_id = course.id
                            WHERE section.id NOT IN (
                                SELECT section_id FROM section_student WHERE student_id = %s
                            )""", (studentID,))
        available_sections = mycursor.fetchall()

        pageTitle = f"Sections for Student {studentID}"
    else:
        mycursor.execute("""SELECT section.id, course.course_name, course.course_code FROM section
                            JOIN course ON section.course_id = course.id""")
        registered_sections = mycursor.fetchall()
        available_sections = None
        pageTitle = "All Sections"

    mycursor.close()
    connection.close()
    return render_template('sections.html', registeredSections=registered_sections, 
                           availableSections=available_sections, pageTitle=pageTitle, studentId=studentID)

# New route to handle unenrollment
@app.route('/unenroll', methods=['POST'])
def unenroll():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    student_id = request.form.get('student_id')
    section_id = request.form.get('section_id')

    if student_id and section_id:
        # Remove the student from the section
        mycursor.execute("DELETE FROM section_student WHERE student_id = %s AND section_id = %s", (student_id, section_id))
        connection.commit()

    mycursor.close()
    connection.close()

    # Redirect back to the student's sections page
    return redirect(url_for('showSections', student_id=student_id))

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
