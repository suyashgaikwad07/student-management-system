Student Management System
A console-based student management application written in Python 3 with role-based access control. All data is stored in plain-text files — no external databases or libraries required.
Quick Start
python main.py
That's it. No installation or dependencies needed — runs on any standard Python 3 interpreter.
Files
File	Purpose
main.py	Main application — login, menus, CRUD operations
credentials.txt	Login credentials (username, password, role)
students.txt	Student records (roll number, name, class, marks)
Sample Credentials
Username	Password	Role	Notes
admin1	admin123	Admin	Full access
teacher1	teach123	Teacher	View, search, update only
student1	stud123	Student	Views own record (Roll 101)
student2	stud456	Student	Views own record (Roll 102)
student3	stud789	Student	Views own record (Roll 103)
Role Permissions
Operation	Admin	Teacher	Student
Add Student	Yes	No	No
View All Students	Yes	Yes	No
Search by Roll Number	Yes	Yes	No
Update Marks	Yes	Yes	No
Delete Student	Yes	No	No
View Own Record	N/A	N/A	Yes
File Formats
credentials.txt
Each line contains one user account:
username,password,role
username,password,Student,roll_number
•	Admin and Teacher accounts have 3 fields.
•	Student accounts have a 4th field: the roll number that links them to their student record.
Example:
admin1,admin123,Admin
teacher1,teach123,Teacher
student1,stud123,Student,101
students.txt
Each line contains one student record:
roll_number,name,class,marks
Example:
101,Rahul Sharma,10A,85
102,Priya Patel,10B,92
How to Extend
Add a new user
Append a line to credentials.txt following the format above.
Add a new role
1.	Add a credential entry with your new role name.
2.	Create a new <role>_menu() function in main.py.
3.	Add an elif branch in the main() function to route the new role to its menu.
Add a new field to student records
1.	Update the load_students() and save_students() functions to handle the extra field.
2.	Update add_student() to prompt for the new field.
3.	Update display functions (view_all_students, search_student, view_own_record) to show it.
Switch to a different data format
Replace the file I/O in load_students() / save_students() with your preferred format (JSON, CSV module, SQLite, etc.). The rest of the application will work without changes.

