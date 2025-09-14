import mysql.connector
import datetime

def connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='IwbiA@2008',
        database='rwa_db'
    )

def create_tables():
    db = connect()
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Residents (
            resident_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            apartment_no VARCHAR(10),
            phone_no VARCHAR(15)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Complaints (
            complain_id INT AUTO_INCREMENT PRIMARY KEY,
            resident_id INT,
            issue_type varchar(20),
            description VARCHAR(255),
            status VARCHAR(20),
            date_filed DATE,
            FOREIGN KEY (resident_id) REFERENCES Residents(resident_id)
        )
    ''')

    db.commit()
    cursor.close()
    db.close()

def add_resident(name, apartment_no, phone_no):
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO Residents (name, apartment_no, phone_no) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, apartment_no, phone_no))
    db.commit()
    cursor.close()
    db.close()

def file_complaint(resident_id, issue_type, description, status):
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO Complaints (resident_id, issue_type, description, status, date_filed) VALUES (%s, %s, %s, %s, CURDATE())"
    cursor.execute(sql, (resident_id, issue_type, description, status))
    db.commit()
    cursor.close()
    db.close()
    
def view_residents():
    db = connect()
    cursor = db.cursor()
    sql = 'SELECT * FROM Residents'
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Apartment: {row[2]}, Phone: {row[3]}")
    else:
        print('No residents found.')
    cursor.close()
    db.close()

def view_complaints():
    db = connect()
    cursor = db.cursor()
    sql = 'SELECT * FROM Complaints'
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"Complaint ID: {row[0]}, Resident ID: {row[1]}, Issue Type: {row[2]}, Description: {row[3]}, Status: {row[4]}, Date Filed: {row[5]}")
    else:
        print('No complaints found.')
    cursor.close()
    db.close()

def delete_tables():
    db = connect()
    cursor = db.cursor()
    sql1 = 'DROP TABLE Residents'
    sql2 = 'DROP TABLE Complaints'
    cursor.execute(sql1,sql2)
    db.commit()
    cursor.close()
    db.close()

while True:
    print("\n--- RWA Complaint Management ---")
    choice = int(input('1 = Create tables\n2 = Add resident\n3 = File complaint\n4 = View complaints\n5 = View residents\n6 = Delete Tables\n7 = Exit Module\nEnter choice: '))
    
    try:
        if choice == 1:
            create_tables()
            print('Tables created!')
        elif choice == 2:
            name = input("Enter resident name: ")
            apartment_no = input("Enter apartment no: ")
            phone_no = input("Enter phone no: ")
            add_resident(name, apartment_no, phone_no)
            print('Resident info added successfully.')
        elif choice == 3:
            resident_id = input("Enter resident ID: ")
            issue_type = input("Enter complaint type: ")
            description = input("Enter description of complaint: ")
            status = input("Enter complaint status: ")
            file_complaint(resident_id, issue_type, description, status)
            print('Complaint info added successfully.')
        elif choice == 4:
            view_complaints()
        elif choice == 5:
            view_residents()
        elif choice == 6:
            delete_tables()
            print("Tables deleted successfully!")
        elif choice == 7:
            print('TOGETHER FOR A BETTER COMMUNITY!\nDeveloped by Aashutosh Tandon.')
            break
        else:
            print('Invalid response. Please choose from 1-6.')
    except ValueError:
        print('Please select a number between 1-6.')