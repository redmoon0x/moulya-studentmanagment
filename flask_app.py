from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, current_app
import pandas as pd
from datetime import datetime
import os
import json
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
from reportgenerate import StudentReportGenerator

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Path to the directory where the attendance data is stored
data_dir = "batch_data"
credentials_file = "credentials.csv"

# Function to load sheet URLs from the JSON file
def load_sheet_urls():
    sheet_urls_file = os.path.join(data_dir, "sheet_urls.json")
    if os.path.exists(sheet_urls_file):
        with open(sheet_urls_file, 'r') as f:
            return json.load(f)
    else:
        return {}

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        return user[3]  # Return roll_no
    return None

def get_subject_wise_attendance(attendance_data):
    if attendance_data.empty:
        return pd.DataFrame()
    
    subject_wise = defaultdict(lambda: {
        'total_held': 0,
        'total_attended': 0,
        'monthly_data': defaultdict(lambda: {
            'held': 0,
            'attended': 0,
            'percentage': 0
        })
    })

    # Process attendance data for each subject
    for _, row in attendance_data.iterrows():
        subject = row['Subject']
        subject_wise[subject]['total_held'] += row['Classes Held']
        subject_wise[subject]['total_attended'] += row['Classes Attended']
        
        month = row['Month']
        subject_wise[subject]['monthly_data'][month] = {
            'held': row['Classes Held'],
            'attended': row['Classes Attended'],
            'percentage': row['Attendance Percentage']
        }

    # Convert to DataFrame format
    subject_summary = []
    for subject, data in subject_wise.items():
        total_percentage = (data['total_attended'] / data['total_held'] * 100) if data['total_held'] > 0 else 0
        monthly_breakdown = data['monthly_data']
        
        subject_summary.append({
            'Subject': subject,
            'Total Classes': data['total_held'],
            'Classes Attended': data['total_attended'],
            'Overall Percentage': round(total_percentage, 2),
            'Monthly Breakdown': monthly_breakdown
        })

    return pd.DataFrame(subject_summary)

def search_student_attendance(roll_no):
    student_data = []
    sheet_urls = load_sheet_urls()
    
    for sheet_url, info in sheet_urls.items():
        file_name = f"{info['batch_name']}_{info['subject_name']}.xlsx"
        file_path = os.path.join(data_dir, file_name)
        
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, index_col=0)
            df.index = df.index.astype(str)
            
            if str(roll_no).strip() in df.index:
                student_name = df.loc[str(roll_no).strip(), 'Name'] if 'Name' in df.columns else "Unknown"
                reg_no = df.loc[str(roll_no).strip(), 'Reg No'] if 'Reg No' in df.columns else "Unknown"
                
                months = [col for col in df.columns if '-Held' not in col and '-Percentage' not in col 
                          and col not in ['Name', 'Reg No', 'Internal 1', 'Internal 2']]
                
                for month in months:
                    held_col = f'{month}-Held'
                    percentage_col = f'{month}-Percentage'
                    
                    if held_col in df.columns and month in df.columns:
                        student_row = pd.DataFrame({
                            'Roll Number': [roll_no],
                            'Name': [student_name],
                            'Reg No': [reg_no],
                            'Subject': [info['subject_name']],
                            'Month': [month],
                            'Classes Held': [df.loc[str(roll_no).strip(), held_col]],
                            'Classes Attended': [df.loc[str(roll_no).strip(), month]],
                            'Attendance Percentage': [df.loc[str(roll_no).strip(), percentage_col]]
                        })
                        student_data.append(student_row)
    
    if student_data:
        return pd.concat(student_data, ignore_index=True)
    else:
        return pd.DataFrame()

def search_student_marks(roll_no):
    student_data = []
    sheet_urls = load_sheet_urls()
    
    for sheet_url, info in sheet_urls.items():
        file_name = f"{info['batch_name']}_{info['subject_name']}.xlsx"
        file_path = os.path.join(data_dir, file_name)
        
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, index_col=0)
            df.index = df.index.astype(str)
            
            if str(roll_no).strip() in df.index:
                student_row = df.loc[str(roll_no).strip()].to_frame().T
                student_row['Name'] = df.loc[str(roll_no).strip(), 'Name'] if 'Name' in df.columns else 'Unknown'
                student_row['Reg No'] = df.loc[str(roll_no).strip(), 'Reg No'] if 'Reg No' in df.columns else 'Unknown'
                student_row['Subject'] = info['subject_name']
                student_row['Roll Number'] = roll_no
                student_row['Internal 1'] = student_row['Internal 1'] if 'Internal 1' in student_row.columns else pd.NA
                student_row['Internal 2'] = student_row['Internal 2'] if 'Internal 2' in student_row.columns else pd.NA
                student_data.append(student_row)
    
    if student_data:
        return pd.concat(student_data, ignore_index=True)
    else:
        return pd.DataFrame()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        roll_no = authenticate(username, password)
        
        if roll_no:
            session['roll_no'] = roll_no
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    roll_no = session.get('roll_no')
    if not roll_no:
        return redirect(url_for('login'))
    
    # Get attendance and marks data
    attendance_data = search_student_attendance(roll_no)
    marks_data = search_student_marks(roll_no)
    
    # Get subject-wise attendance summary
    subject_wise_attendance = get_subject_wise_attendance(attendance_data)
    
    # Get student details
    student_name = "Unknown"
    reg_no = "Unknown"
    
    # Initialize totals
    total_classes_held = 0
    total_classes_attended = 0
    
    if not attendance_data.empty:
        student_name = attendance_data['Name'].iloc[0]
        reg_no = attendance_data['Reg No'].iloc[0]
        total_classes_held = attendance_data['Classes Held'].sum()
        total_classes_attended = attendance_data['Classes Attended'].sum()
    elif not marks_data.empty:
        student_name = marks_data['Name'].iloc[0]
        reg_no = marks_data['Reg No'].iloc[0]
    
    overall_attendance_percentage = round(total_classes_attended / total_classes_held * 100) if total_classes_held > 0 else 0

    return render_template('dashboard.html', 
                         attendance_data=attendance_data,
                         subject_wise_attendance=subject_wise_attendance,
                         marks_data=marks_data,
                         student_name=student_name,
                         reg_no=reg_no,
                         roll_no=roll_no,
                         total_classes_held=total_classes_held,
                         total_classes_attended=total_classes_attended,
                         overall_attendance_percentage=overall_attendance_percentage)

@app.route('/download_report')
def download_report():
    roll_no = session.get('roll_no')
    if not roll_no:
        return redirect(url_for('login'))
    
    try:
        # Get attendance and marks data
        attendance_data = search_student_attendance(roll_no)
        marks_data = search_student_marks(roll_no)
        
        # Get subject-wise attendance summary
        subject_wise_attendance = get_subject_wise_attendance(attendance_data)
        
        # Get student details
        student_name = "Unknown"
        reg_no = "Unknown"
        
        if not attendance_data.empty:
            student_name = attendance_data['Name'].iloc[0]
            reg_no = attendance_data['Reg No'].iloc[0]
        elif not marks_data.empty:
            student_name = marks_data['Name'].iloc[0]
            reg_no = marks_data['Reg No'].iloc[0]
        
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'report_{roll_no}_{timestamp}.pdf'
        output_path = os.path.join(reports_dir, filename)
        
        # Generate PDF report
        report_generator = StudentReportGenerator()
        report_generator.generate_report(
            student_name=student_name,
            reg_no=reg_no,
            roll_no=roll_no,
            subject_wise_attendance=subject_wise_attendance,
            marks_data=marks_data,
            output_path=output_path,
            logo_path="logo.png" 
        )
        
        # Send file and handle cleanup
        try:
            return send_file(
                output_path,
                as_attachment=True,
                download_name=f'academic_report_{roll_no}.pdf',
                mimetype='application/pdf'
            )
        finally:
            # Clean up the file after sending
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
                    
    except Exception as e:
        print(f"Error generating report: {str(e)}")  # For debugging
        flash("Error generating report. Please try again.")
        return redirect(url_for('dashboard'))
    
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))  # Redirect to login page
if __name__ == "__main__":
    app.run(debug=True)