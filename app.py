from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
from attendance_taker import face_recognizer
from get_faces_from_camera_tkinter import Face_Register
from features_extraction_to_csv import FaceFeaturesExtractor

app = Flask(__name__)

attendance_taker_instance = None
get_faces_instance = None
Face_FeaturesExtractor_instance = None

face_recognizer_instance = face_recognizer()
Face_Register_instance = Face_Register
Face_FeaturesExtractor_instance = FaceFeaturesExtractor


@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/get_faces', methods=['GET'])
def get_faces_route():
    get_faces_instance = Face_Register()
    get_faces_instance.run()
    return render_template('index.html')


@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    print(formatted_date,">>>>>>>>>>>>>>>>>>>>>>>>>>")

    conn = sqlite3.connect('attendance2.db')
    cursor = conn.cursor()

    #cursor.execute("SELECT students_id,date, time, present FROM attendance WHERE date = ?", (formatted_date,))
    #attendance_data = cursor.fetchall()
    #print(attendance_data, "=============================")

    cursor.execute("SELECT * FROM student JOIN attendance ON student.id = attendance.students_id WHERE attendance.date = ?", (formatted_date,))
    all_data = cursor.fetchall()

    conn.close()

    if not all_data:
        return render_template('index.html', selected_date=selected_date, no_data=True, all_data=all_data)
    
    return render_template('index.html', selected_date=selected_date, attendance_data=all_data, all_data=all_data)

@app.route('/start_attendance_taker', methods=['GET'])
def start_attendance_taker():
    face_recognizer_instance.run()
    return render_template('index.html')

@app.route('/features_extraction', methods=['GET'])
def features_extraction_route():
    face_extractor_instance = FaceFeaturesExtractor()
    face_extractor_instance.main()
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)