import sqlite3
from werkzeug.security import generate_password_hash
import pandas as pd
import sys
import os

def setup_database():
    """Create the users table if it doesn't exist"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        roll_no TEXT UNIQUE NOT NULL
    )''')
    
    conn.commit()
    conn.close()

def generate_credentials(roll_no):
    """Generate username and password based on roll number"""
    username = f"student{roll_no}"
    password = f"{roll_no}@123"
    return username, password

def add_user(roll_no):
    """Add a new user to the database"""
    username, password = generate_credentials(roll_no)
    password_hash = generate_password_hash(password)
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, roll_no) VALUES (?, ?, ?)",
            (username, password_hash, roll_no)
        )
        conn.commit()
        print(f"Successfully created account for Roll No: {roll_no}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        return (roll_no, username, password)  # Return credentials for CSV

    except sqlite3.IntegrityError:
        print(f"Error: User already exists for Roll No: {roll_no}")
        return None
    
    finally:
        conn.close()

def bulk_add_users_from_csv(file_path):
    """Add multiple users from a CSV file containing roll numbers and generate a new CSV with credentials"""
    output_data = []

    try:
        df = pd.read_csv(file_path)
        if 'roll_no' not in df.columns:
            print("Error: CSV file must contain a 'roll_no' column")
            return
        
        for roll_no in df['roll_no']:
            credentials = add_user(str(roll_no))
            if credentials:
                output_data.append(credentials)
        
        # Create a new DataFrame for the output
        if output_data:
            output_df = pd.DataFrame(output_data, columns=['Roll No', 'Username', 'Password'])
            output_file_path = "generated_credentials.csv"
            output_df.to_csv(output_file_path, index=False)
            print(f"Credentials have been saved to {output_file_path}")
            
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")

def view_all_users():
    """View all users in the database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT roll_no, username FROM users")
    users = c.fetchall()
    
    if users:
        print("List of all users:")
        for roll_no, username in users:
            password = f"{roll_no}@123"
            print(f"Roll No: {roll_no}, Username: {username}, Password: {password}")
    else:
        print("No users found.")
    
    conn.close()

def export_all_credentials():
    """Export all user credentials to an Excel file"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT roll_no, username FROM users")
    users = c.fetchall()
    
    if users:
        output_data = []
        for roll_no, username in users:
            password = f"{roll_no}@123"
            output_data.append((roll_no, username, password))
        
        output_df = pd.DataFrame(output_data, columns=['Roll No', 'Username', 'Password'])
        output_file_path = "all_credentials.xlsx"
        output_df.to_excel(output_file_path, index=False)
        print(f"All credentials have been exported to {output_file_path}")
    else:
        print("No users found to export.")
    
    conn.close()

def main():
    setup_database()
    
    while True:
        print("\n--- User Management Menu ---")
        print("1. Add Single Student")
        print("2. Add Bulk Students from CSV")
        print("3. View All Users")
        print("4. Export All Credentials to Excel")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            roll_no = input("Enter Roll No: ")
            add_user(roll_no)
        
        elif choice == '2':
            
            
            csv_path = input("Enter the path to the CSV file: ")
            bulk_add_users_from_csv(csv_path)
        
        elif choice == '3':
            view_all_users()
        
        elif choice == '4':
            export_all_credentials()
        
        elif choice == '5':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()