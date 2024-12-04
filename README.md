# 📚 Marks Management System 2.0

A web-based system for managing student marks and attendance at Dr. B.B. Hegde First Grade College Kundapura.

[![GitHub](https://img.shields.io/badge/GitHub-redmoon0x-blue?style=flat&logo=github)](https://github.com/redmoon0x)
![Python](https://img.shields.io/badge/Python-Flask-green?style=flat&logo=python)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat&logo=sqlite)
![ReportLab](https://img.shields.io/badge/PDF-ReportLab-red?style=flat&logo=adobe)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat)

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Technologies Used](#️-technologies-used)
- [Setup and Installation](#️-setup-and-installation)
- [Usage](#-usage)
- [Database Structure](#-database-structure)
- [Security Features](#-security-features)
- [API Endpoints](#-api-endpoints)
- [Future Enhancements](#-future-enhancements)
- [Troubleshooting](#-troubleshooting)
- [Author](#-author)

## 🚀 Features

- **Student Management**
  - Add and manage student records
  - Track attendance and academic performance
  - Generate student reports
  - Bulk import student data from Excel

- **Attendance Tracking**
  - Record and monitor student attendance
  - Calculate attendance percentages
  - View monthly attendance breakdown
  - Export attendance reports

- **Report Generation**
  - Generate PDF reports with student details
  - Include attendance summaries
  - Professional formatting with college branding
  - Downloadable in multiple formats

## 📁 Project Structure

```
marksmasnagment2.0/
├── flask_app.py          # Main Flask application
├── reportgenerate.py     # PDF report generation logic
├── addstudent.py        # Student management functionality
├── templates/           # HTML templates
│   ├── login.html       # Login page
│   ├── dashboard.html   # Main dashboard
│   ├── report.html      # Report generation
│   └── student.html     # Student management
├── static/             # Static files
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   └── images/        # Image assets
├── batch_data/         # Student batch information
└── users.db            # SQLite database
```

## 🛠️ Technologies Used

- **Backend**: 
  - Python 3.x
  - Flask Framework
  - SQLite Database
  - Pandas for data processing

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap for responsive design

- **Report Generation**:
  - ReportLab for PDF generation
  - Excel export functionality

- **Development Tools**:
  - Visual Studio Code
  - Git for version control
  - SQLite Browser for database management

## ⚙️ Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/redmoon0x/marksmasnagment2.0.git
   cd marksmasnagment2.0
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**
   ```bash
   python setup_database.py
   ```

4. **Run the Application**
   ```bash
   python flask_app.py
   ```

5. **Access the System**
   - Open your browser
   - Navigate to: http://localhost:5000
   - Default admin credentials:
     - Username: admin
     - Password: admin123

## 💡 Usage

1. **Login to the System**
   - Use your assigned credentials
   - Access the dashboard
   - Reset password if needed

2. **View Student Records**
   - Access student attendance
   - Check academic performance
   - Generate reports
   - Export data to Excel

3. **Generate Reports**
   - Select student details
   - Choose report type
   - Download PDF report
   - Print or save digitally

## 📊 Database Structure

- **Users Table**:
  ```sql
  CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      username TEXT UNIQUE,
      password_hash TEXT,
      role TEXT
  )
  ```

- **Students Table**:
  ```sql
  CREATE TABLE students (
      roll_no TEXT PRIMARY KEY,
      name TEXT,
      reg_no TEXT UNIQUE,
      batch TEXT
  )
  ```

- **Attendance Table**:
  ```sql
  CREATE TABLE attendance (
      id INTEGER PRIMARY KEY,
      roll_no TEXT,
      date TEXT,
      subject TEXT,
      status TEXT
  )
  ```

## 🔐 Security Features

- Password hashing using Werkzeug
- Session management with Flask-Login
- Input validation and sanitization
- CSRF protection
- Secure password reset mechanism

## 🔄 API Endpoints

- **/login** - User authentication
- **/dashboard** - Main dashboard
- **/student/add** - Add new student
- **/attendance/record** - Record attendance
- **/report/generate** - Generate reports
- **/api/students** - Student data API
- **/api/attendance** - Attendance data API

## 🚀 Future Enhancements

1. **Mobile Application**
   - Android/iOS app for attendance marking
   - Real-time notifications

2. **Advanced Analytics**
   - Attendance patterns analysis
   - Performance predictions
   - Graphical representations

3. **Additional Features**
   - SMS notifications
   - Email reports
   - Parent portal

## ❗ Troubleshooting

1. **Database Connection Issues**
   - Verify database file exists
   - Check file permissions
   - Ensure correct path in configuration

2. **Report Generation Errors**
   - Check ReportLab installation
   - Verify template files exist
   - Ensure sufficient disk space

3. **Login Issues**
   - Clear browser cache
   - Reset password if needed
   - Contact administrator

## 👤 Author

**redmoon0x** - [GitHub Profile](https://github.com/redmoon0x)

## 📞 Support

For support, email your queries to [your-email@example.com]

---
Made with ❤️ for Dr. B.B. Hegde First Grade College Kundapura

© 2024 Marks Management System 2.0. All Rights Reserved.
