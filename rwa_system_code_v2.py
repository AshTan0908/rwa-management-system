import mysql.connector
from datetime import datetime

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
            phone_no VARCHAR(150)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Complaints (
            complain_id INT AUTO_INCREMENT PRIMARY KEY,
            resident_id INT,
            issue_type VARCHAR(20),
            description VARCHAR(255),
            status VARCHAR(20),
            date_filed DATE,
            FOREIGN KEY (resident_id) REFERENCES Residents(resident_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(20)
        )
    ''')

    cursor.execute("INSERT IGNORE INTO Admin (username, password) VALUES (%s, %s)", ('admin', 'admin123'))
    
    db.commit()
    cursor.close()
    db.close()
    print("Tables created successfully!")

def add_resident(name, apartment_no, phone_no):
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO Residents (name, apartment_no, phone_no) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, apartment_no, phone_no))
    resident_id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    print(f"Resident added successfully! Resident ID: {resident_id}")
    return resident_id

def get_resident_id(apartment_no):
    db = connect()
    cursor = db.cursor()
    sql = "SELECT resident_id FROM Residents WHERE apartment_no = %s"
    cursor.execute(sql, (apartment_no,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result[0] if result else None

def file_complaint(apartment_no, name, phone_no, issue_type, description):
    db = connect()
    cursor = db.cursor()

    resident_id = get_resident_id(apartment_no)
    if not resident_id:
        resident_id = add_resident(name, apartment_no, phone_no)
    
    sql = "INSERT INTO Complaints (resident_id, issue_type, description, status, date_filed) VALUES (%s, %s, %s, %s, CURDATE())"
    cursor.execute(sql, (resident_id, issue_type, description, 'Pending'))
    db.commit()
    cursor.close()
    db.close()
    print("Complaint filed successfully!")

def view_complaint_status(complain_id):
    db = connect()
    cursor = db.cursor()
    sql = "SELECT complain_id, issue_type, description, status, date_filed FROM Complaints WHERE complain_id = %s"
    cursor.execute(sql, (complain_id,))
    result = cursor.fetchone()
    if result:
        print(f"\nComplaint ID: {result[0]}")
        print(f"Issue Type: {result[1]}")
        print(f"Description: {result[2]}")
        print(f"Status: {result[3]}")
        print(f"Date Filed: {result[4]}")
    else:
        print("Complaint not found.")
    cursor.close()
    db.close()

def view_past_complaints(apartment_no):
    db = connect()
    cursor = db.cursor()
    sql = '''
        SELECT c.complain_id, c.issue_type, c.description, c.status, c.date_filed
        FROM Complaints c
        JOIN Residents r ON c.resident_id = r.resident_id
        WHERE r.apartment_no = %s
    '''
    cursor.execute(sql, (apartment_no,))
    results = cursor.fetchall()
    if results:
        print("\nPAST COMPLAINTS:")
        for row in results:
            print(f"Complaint ID: {row[0]}, Issue Type: {row[1]}, Description: {row[2]}, Status: {row[3]}, Date Filed: {row[4]}")
    else:
        print("No past complaints found.")
    cursor.close()
    db.close()

def modify_complaint(complain_id, new_description, new_phone_no, new_issue_type):
    db = connect()
    cursor = db.cursor()
    
    sql = "SELECT status FROM Complaints WHERE complain_id = %s"
    cursor.execute(sql, (complain_id,))
    result = cursor.fetchone()
    
    if not result:
        print("Complaint not found.")
        cursor.close()
        db.close()
        return
    
    current_status = result[0]
    print(f"Current status of complaint {complain_id}: {current_status}")  # Debug output
    if current_status in ['In Progress', 'Resolved']:
        print(f"Cannot modify complaint {complain_id}: It is already {current_status}.")
        cursor.close()
        db.close()
        return
    
    if new_description:
        sql = "UPDATE Complaints SET description = %s WHERE complain_id = %s"
        cursor.execute(sql, (new_description, complain_id))
    
    if new_issue_type:
        sql = "UPDATE Complaints SET issue_type = %s WHERE complain_id = %s"
        cursor.execute(sql, (new_issue_type, complain_id))
    
    if new_phone_no:
        sql = "UPDATE Residents SET phone_no = %s WHERE resident_id = (SELECT resident_id FROM Complaints WHERE complain_id = %s)"
        cursor.execute(sql, (new_phone_no, complain_id))
    
    db.commit()
    cursor.close()
    db.close()
    print(f"Complaint {complain_id} modified successfully!")

def admin_login(username, password):
    db = connect()
    cursor = db.cursor()
    sql = "SELECT * FROM Admin WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result is not None

def view_pending_complaints():
    db = connect()
    cursor = db.cursor()
    sql = '''
        SELECT c.complain_id, r.apartment_no, r.name, c.issue_type, c.description, c.date_filed
        FROM Complaints c
        JOIN Residents r ON c.resident_id = r.resident_id
        WHERE c.status = 'Pending'
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        print("\nPENDING COMPLAINTS:")
        for row in results:
            print(f"Complaint ID: {row[0]}, Flat No: {row[1]}, Name: {row[2]}, Issue Type: {row[3]}, Description: {row[4]}, Date Filed: {row[5]}")
    else:
        print("No pending complaints found.")
    cursor.close()
    db.close()

def update_complaint_status(complain_id, new_status):
    if new_status not in ['Pending', 'In Progress', 'Resolved']:
        print("Invalid status. Use: Pending, In Progress, or Resolved.")
        return
    db = connect()
    cursor = db.cursor()
    sql = "UPDATE Complaints SET status = %s WHERE complain_id = %s"
    cursor.execute(sql, (new_status, complain_id))
    db.commit()
    cursor.close()
    db.close()
    print("Complaint status updated successfully!")

def search_complaints(search_by, value):
    db = connect()
    cursor = db.cursor()
    if search_by == 'apartment_no':
        sql = '''
            SELECT c.complain_id, r.apartment_no, r.name, c.issue_type, c.description, c.status, c.date_filed
            FROM Complaints c
            JOIN Residents r ON c.resident_id = r.resident_id
            WHERE r.apartment_no = %s
        '''
    elif search_by == 'date':
        sql = '''
            SELECT c.complain_id, r.apartment_no, r.name, c.issue_type, c.description, c.status, c.date_filed
            FROM Complaints c
            JOIN Residents r ON c.resident_id = r.resident_id
            WHERE c.date_filed = %s
        '''
    elif search_by == 'issue_type':
        sql = '''
            SELECT c.complain_id, r.apartment_no, r.name, c.issue_type, c.description, c.status, c.date_filed
            FROM Complaints c
            JOIN Residents r ON c.resident_id = r.resident_id
            WHERE c.issue_type = %s
        '''
    else:
        print("Invalid search criteria.")
        cursor.close()
        db.close()
        return
    
    cursor.execute(sql, (value,))
    results = cursor.fetchall()
    if results:
        print("\nSEARCH RESULTS:")
        for row in results:
            print(f"Complaint ID: {row[0]}, Flat No: {row[1]}, Name: {row[2]}, Issue Type: {row[3]}, Description: {row[4]}, Status: {row[5]}, Date Filed: {row[6]}")
    else:
        print("No complaints found.")
    cursor.close()
    db.close()

def monthly_complaint_report(month, year):
    db = connect()
    cursor = db.cursor()
    sql = '''
        SELECT status, COUNT(*) 
        FROM Complaints 
        WHERE MONTH(date_filed) = %s AND YEAR(date_filed) = %s
        GROUP BY status
    '''
    cursor.execute(sql, (month, year))
    results = cursor.fetchall()
    if results:
        print(f"\nMONTHLY REPORT ({month}/{year}):")
        for row in results:
            print(f"Status: {row[0]}, Count: {row[1]}")
    else:
        print(f"No complaints found for {month}/{year}.")
    cursor.close()
    db.close()

while True:
    print("\n--- RWA Complaint Management System ---")
    print("1. Resident Module")
    print("2. Admin Module")
    print("3. Create Tables")
    print("4. Exit")
    choice = input("Enter choice (1-4): ")

    try:
        choice = int(choice)
        if choice == 1:
            while True:
                print("\n--- Resident Module ---")
                print("1. Register Complaint")
                print("2. View Complaint Status")
                print("3. View All Past Complaints")
                print("4. Modify Complaint")
                print("5. Back to Main Menu")
                resident_choice = input("Enter choice (1-5): ")
                
                try:
                    resident_choice = int(resident_choice)
                    if resident_choice == 1:
                        apartment_no = input("Enter Flat No: ")
                        name = input("Enter Name: ")
                        phone_no = input("Enter Contact No: ")
                        issue_type = input("Enter Issue Type (e.g., Water Leakage, Electricity Issue, Cleaning): ")
                        description = input("Enter Description: ")
                        file_complaint(apartment_no, name, phone_no, issue_type, description)
                    elif resident_choice == 2:
                        apartment_no = input("Enter Apartment No: ")
                        print("\nRecent Complaints for Your Apartment:")
                        view_past_complaints(apartment_no)  
                        complain_id = input("Enter Complaint ID for complaint to view from the list above: ")
                        view_complaint_status(complain_id)
                    elif resident_choice == 3:
                        apartment_no = input("Enter Flat No: ")
                        view_past_complaints(apartment_no)
                    elif resident_choice == 4:
                        apartment_no = input("Enter Apartment No: ")
                        print("\nRecent Complaints for Your Apartment:")
                        view_past_complaints(apartment_no)  
                        complain_id = input("Enter Complaint ID for complaint to view from the list above: ")
                        new_issue_type = input("Enter New Issue Type (or press Enter to skip): ")
                        new_description = input("Enter New Description (or press Enter to skip): ")
                        new_phone_no = input("Enter New Contact No (or press Enter to skip): ")
                        modify_complaint(complain_id, new_issue_type, new_description, new_phone_no)
                    elif resident_choice == 5:
                        break
                    else:
                        print("Invalid choice. Please choose from 1-5.")
                except ValueError:
                    print("Please enter a valid number (1-5).")
        
        elif choice == 2:
            username = input("Enter Admin Username: ")
            password = input("Enter Admin Password: ")
            if admin_login(username, password):
                while True:
                    print("\n--- Admin Module ---")
                    print("1. View Pending Complaints")
                    print("2. Change Complaint Status")
                    print("3. Search Complaints")
                    print("4. Monthly Complaint Report")
                    print("5. Back to Main Menu")
                    admin_choice = input("Enter choice (1-5): ")
                    
                    try:
                        admin_choice = int(admin_choice)
                        if admin_choice == 1:
                            view_pending_complaints()
                        elif admin_choice == 2:
                            print("\nAll Complaints:")
                            db = connect()
                            cursor = db.cursor()
                            sql = '''
                                SELECT c.complain_id, r.apartment_no, r.name, c.issue_type, c.description, c.status, c.date_filed
                                FROM Complaints c
                                JOIN Residents r ON c.resident_id = r.resident_id
                            '''
                            cursor.execute(sql)
                            results = cursor.fetchall()
                            if results:
                                for row in results:
                                    print(f"Complaint ID: {row[0]}, Apartment No: {row[1]}, Name: {row[2]}, Issue Type: {row[3]}, Description: {row[4]}, Status: {row[5]}, Date Filed: {row[6]}")
                            else:
                                print("No complaints found.")
                            cursor.close()
                            db.close()
                            
                            complain_id = input("Enter Complaint ID from the list above: ")
                            new_status = input("Enter New Status (Pending, In Progress, Resolved): ")
                            update_complaint_status(complain_id, new_status)
                        elif admin_choice == 3:
                            search_by = input("Search by (apartment_no, date, issue_type): ")
                            if search_by == 'date':
                                value = input("Enter Date (YYYY-MM-DD): ")
                            else:
                                value = input(f"Enter {search_by}: ")
                            search_complaints(search_by, value)
                        elif admin_choice == 4:
                            month = input("Enter Month (1-12): ")
                            year = input("Enter Year (e.g., 2025): ")
                            monthly_complaint_report(month, year)
                        elif admin_choice == 5:
                            break
                        else:
                            print("Invalid choice. Please choose from 1-5.")
                    except ValueError:
                        print("Please enter a valid number (1-5).")
            else:
                print("Admin login failed.")
        
        elif choice == 3:
            create_tables()
        
        elif choice == 4:
            print("\nTHANK YOU!")
            print("TOGETHER FOR A BETTER COMMUNITY")
            print("Developed by: Aashutosh Tandon")
            break
        
        else:
            print("Invalid choice. Please choose from 1-4.")
    
    except ValueError:
        print("Please enter a valid number (1-4).")