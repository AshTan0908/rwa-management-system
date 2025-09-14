while True:
    choice = int(input('What would you like to do? (1 = create tables, 2 = add residents, 3 = file complaints, 4 = exit)'))
    if choice == 1:
        create_tables()
    elif choice == 2:
        name = input("Enter resident name: ")
        apartment_no = input("Enter apartment no: ")
        phone_no = input("Enter phone no: ")
        add_residents(name, apartment_no, phone_no)
    elif choice == 3
        resident_id = input("Enter resident ID: ")
        description = input("Enter description of complaint: ")
        status = input("Enter complaint status: ")
        file_complaint(resident_id, description, status)
    elif choice == 4:
        print('TOGETHER FOR A BETTER COMMUNITY')
        break
    else:
        print('Invalid response. Please choose from 1-4.')
