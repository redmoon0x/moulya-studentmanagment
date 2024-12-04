# 📚 Marks Management System 2.0

A web-based system for managing student marks and attendance at Dr. B.B. Hegde First Grade College Kundapura.

[![GitHub](https://img.shields.io/badge/GitHub-redmoon0x-blue?style=flat&logo=github)](https://github.com/redmoon0x)
![Python](https://img.shields.io/badge/Python-Flask-green?style=flat&logo=python)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat&logo=sqlite)

## 🚀 Features

- **Student Management**
  - Add and manage student records
  - Track attendance and academic performance
  - Generate student reports

- **Attendance Tracking**
  - Record and monitor student attendance
  - Calculate attendance percentages
  - View monthly attendance breakdown

- **Report Generation**
  - Generate PDF reports with student details
  - Include attendance summaries
  - Professional formatting with college branding

## 📁 Project Structure

```
marksmasnagment2.0/
├── flask_app.py          # Main Flask application
├── reportgenerate.py     # PDF report generation logic
├── addstudent.py        # Student management functionality
├── templates/           # HTML templates
├── static/             # Static files (CSS, JS)
├── batch_data/         # Student batch information
└── users.db            # SQLite database
```

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS
- **Report Generation**: ReportLab
- **Data Processing**: Pandas

## ⚙️ Setup and Installation

1. **Install Python Dependencies**
   ```bash
   pip install flask pandas reportlab
   ```

2. **Run the Application**
   ```bash
   python flask_app.py
   ```

3. **Access the System**
   - Open your browser
   - Navigate to: http://localhost:5000
   - Login with your credentials

## 💡 Usage

1. **Login to the System**
   - Use your assigned credentials
   - Access the dashboard

2. **View Student Records**
   - Access student attendance
   - Check academic performance
   - Generate reports

3. **Generate Reports**
   - Select student details
   - Choose report type
   - Download PDF report

## 📊 Database Structure

- **Users Table**: Stores login credentials
- **Student Records**: Maintains student information
- **Attendance Data**: Tracks student attendance

## 🔐 Security Features

- Password hashing for secure authentication
- Session management
- Input validation

## 👤 Author

**redmoon0x** - [GitHub Profile](https://github.com/redmoon0x)

---
Made with ❤️ for Dr. B.B. Hegde First Grade College Kundapura
