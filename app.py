from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="tech_institute"
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/courses')
def courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses)

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']
        cursor.execute("INSERT INTO students (name, email, course_id) VALUES (%s, %s, %s)", 
                       (name, email, course_id))
        conn.commit()
        conn.close()
        return redirect('/view-enrollments')
    conn.close()
    return render_template('enroll.html', courses=courses)

@app.route('/view-enrollments')
def view_enrollments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT students.name, students.email, courses.course_name 
                      FROM students JOIN courses ON students.course_id = courses.id""")
    enrollments = cursor.fetchall()
    conn.close()
    return render_template('view_enrollments.html', enrollments=enrollments)

if __name__ == '__main__':
    app.run(debug=True)
