# RWA ISSUE LOGGER
It can be used by resident welfare associations to manage complaints by tenants. It primarily uses Python and SQL code written from MySQL Workbench.

My project is based on RWA COMPLAINT MANAGEMENT SYSTEM
The project consists of 3 modules:
    1.	RESIDENT
    2.	ADMIN
    3.	EXIT


1. RESIDENT MODULE
In the RESIDENT MODULE, there will be 5 options:
    1.	REGISTER COMPLAINT:
    In this option, a resident can register a complaint by entering their Apartment No., Name, Phone No., Issue Type (e.g., Water Leakage, Electricity Issue, Cleaning), and Description of the problem.
    2.	VIEW COMPLAINT STATUS:
    In this option, a resident can check the current status of their complaint (Pending / In Progress / Resolved) by entering their complaint ID.
    3.	VIEW ALL PAST COMPLAINTS:
    In this option, the resident can see a list of all complaints they have made along with their date and final status.
    4. 	MODIFY COMPLAINT:
    In this option, the resident can modify their complaint details (e.g., change description or contact number) before it is marked as In Progress or Resolved.`


2. ADMIN MODULE
In the ADMIN MODULE, the admin has to enter Admin ID and Password to log in.
Once logged in, the admin can:
    1.	View all Pending Complaints with complaint details.
    2.	Change the Status of complaints (Pending → In Progress / Resolved).
    3.	Search complaints by Flat No., Date, or Issue Type.
    4.	View Monthly Complaint Report with counts of resolved vs pending complaints.

3. EXIT MODULE
In the EXIT MODULE, the user can end the program.
At last, the program will display THANK YOU with a positive message such as:
“TOGETHER FOR A BETTER COMMUNITY”
“COMMUNICATION IS THE KEY TO RESOLUTION”
It will also display the Developer Name.
 
