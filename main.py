"""
Student Management System
=========================
A console-based student management application with role-based access control.
All data is stored in plain-text files — no external databases or libraries required.

Files:
  - credentials.txt : Stores login credentials (username, password, role[, roll_number])
  - students.txt    : Stores student records (roll_number, name, class, marks)

Roles:
  - Admin   : Full access (Add, View All, Search, Update Marks, Delete)
  - Teacher : View All, Search, Update Marks
  - Student : View own record only (authenticated via roll number)

Usage:
  python main.py
"""

import os
import getpass

# ---------------------------------------------------------------------------
# File paths (same directory as main.py)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.txt")
STUDENTS_FILE = os.path.join(BASE_DIR, "students.txt")

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def clear_screen():
    """Clear the console screen (works on Windows and Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Wait for the user to press Enter before continuing."""
    input("\nPress Enter to continue...")


def ensure_file(filepath):
    """Create the file if it does not already exist."""
    if not os.path.exists(filepath):
        open(filepath, "w").close()

# ---------------------------------------------------------------------------
# Data I/O — students.txt
# ---------------------------------------------------------------------------

def load_students():
    """
    Read students.txt and return a list of dictionaries.
    Each line: roll_number,name,class,marks
    Blank lines and malformed rows are silently skipped.
    """
    ensure_file(STUDENTS_FILE)
    students = []
    with open(STUDENTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            students.append({
                "roll": parts[0].strip(),
                "name": parts[1].strip(),
                "class": parts[2].strip(),
                "marks": parts[3].strip(),
            })
    return students


def save_students(students):
    """
    Write the full student list back to students.txt.
    No blank lines are left in the file.
    """
    with open(STUDENTS_FILE, "w") as f:
        for s in students:
            f.write(f"{s['roll']},{s['name']},{s['class']},{s['marks']}\n")

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def load_credentials():
    """
    Read credentials.txt and return a list of credential dicts.
    Format: username,password,role[,roll_number]
    roll_number is only present for the Student role.
    """
    ensure_file(CREDENTIALS_FILE)
    creds = []
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 3:
                continue
            entry = {
                "username": parts[0].strip(),
                "password": parts[1].strip(),
                "role": parts[2].strip(),
            }
            # Student accounts carry an associated roll number
            if len(parts) >= 4:
                entry["roll"] = parts[3].strip()
            creds.append(entry)
    return creds


def login():
    """
    Prompt the user for credentials and authenticate.
    Returns a dict with 'username', 'role', and optionally 'roll' on success.
    Returns None after 3 failed attempts.
    """
    creds = load_credentials()
    if not creds:
        print("Error: No credentials found. Please set up credentials.txt first.")
        return None

    print("=" * 50)
    print("     STUDENT MANAGEMENT SYSTEM — LOGIN")
    print("=" * 50)

    attempts = 3
    while attempts > 0:
        username = input("\nUsername : ").strip()
        password = getpass.getpass("Password : ").strip()

        for c in creds:
            if c["username"] == username and c["password"] == password:
                print(f"\nLogin successful! Welcome, {username} ({c['role']})")
                result = {"username": username, "role": c["role"]}
                if "roll" in c:
                    result["roll"] = c["roll"]
                return result

        attempts -= 1
        if attempts > 0:
            print(f"Invalid credentials. {attempts} attempt(s) remaining.")
        else:
            print("Too many failed attempts. Access denied.")
    return None

# ---------------------------------------------------------------------------
# CRUD Operations
# ---------------------------------------------------------------------------

def add_student():
    """Add a new student record. Validates for duplicate roll numbers."""
    print("\n--- Add New Student ---")
    students = load_students()

    # Roll number
    roll = input("Roll Number : ").strip()
    if not roll:
        print("Error: Roll number cannot be empty.")
        return
    for s in students:
        if s["roll"] == roll:
            print(f"Error: Roll number {roll} already exists.")
            return

    # Name
    name = input("Name        : ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    # Class
    cls = input("Class       : ").strip()
    if not cls:
        print("Error: Class cannot be empty.")
        return

    # Marks
    marks_str = input("Marks       : ").strip()
    try:
        marks = int(marks_str)
        if marks < 0 or marks > 100:
            print("Error: Marks must be between 0 and 100.")
            return
    except ValueError:
        print("Error: Marks must be a whole number.")
        return

    students.append({"roll": roll, "name": name, "class": cls, "marks": str(marks)})
    save_students(students)
    print(f"Student '{name}' (Roll: {roll}) added successfully.")


def view_all_students():
    """Display every student record in a neat, column-aligned table."""
    print("\n--- All Student Records ---")
    students = load_students()
    if not students:
        print("No student records found.")
        return

    # Column headers
    header = f"{'Roll':<10} {'Name':<25} {'Class':<10} {'Marks':<6}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    for s in students:
        print(f"{s['roll']:<10} {s['name']:<25} {s['class']:<10} {s['marks']:<6}")
    print("-" * len(header))
    print(f"Total records: {len(students)}")


def search_student():
    """Search for a student by roll number and display the record."""
    print("\n--- Search Student ---")
    roll = input("Enter Roll Number to search: ").strip()
    if not roll:
        print("Error: Roll number cannot be empty.")
        return

    students = load_students()
    for s in students:
        if s["roll"] == roll:
            print(f"\n  Roll Number : {s['roll']}")
            print(f"  Name        : {s['name']}")
            print(f"  Class       : {s['class']}")
            print(f"  Marks       : {s['marks']}")
            return
    print(f"No student found with roll number '{roll}'.")


def update_marks():
    """Update the marks for an existing student without changing other fields."""
    print("\n--- Update Marks ---")
    roll = input("Enter Roll Number to update: ").strip()
    if not roll:
        print("Error: Roll number cannot be empty.")
        return

    students = load_students()
    for s in students:
        if s["roll"] == roll:
            print(f"  Current record — Name: {s['name']}, Class: {s['class']}, Marks: {s['marks']}")
            new_marks_str = input("  Enter new marks: ").strip()
            try:
                new_marks = int(new_marks_str)
                if new_marks < 0 or new_marks > 100:
                    print("Error: Marks must be between 0 and 100.")
                    return
            except ValueError:
                print("Error: Marks must be a whole number.")
                return
            s["marks"] = str(new_marks)
            save_students(students)
            print(f"Marks for roll number {roll} updated to {new_marks}.")
            return
    print(f"No student found with roll number '{roll}'.")


def delete_student():
    """Delete a student record by roll number; the file is rewritten cleanly."""
    print("\n--- Delete Student ---")
    roll = input("Enter Roll Number to delete: ").strip()
    if not roll:
        print("Error: Roll number cannot be empty.")
        return

    students = load_students()
    new_list = [s for s in students if s["roll"] != roll]

    if len(new_list) == len(students):
        print(f"No student found with roll number '{roll}'.")
        return

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete roll number {roll}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    save_students(new_list)
    print(f"Student with roll number {roll} deleted successfully.")


def view_own_record(roll):
    """Display the record for a single student (used by the Student role)."""
    print("\n--- Your Student Record ---")
    students = load_students()
    for s in students:
        if s["roll"] == roll:
            print(f"\n  Roll Number : {s['roll']}")
            print(f"  Name        : {s['name']}")
            print(f"  Class       : {s['class']}")
            print(f"  Marks       : {s['marks']}")
            return
    print("Your record was not found. Please contact an administrator.")

# ---------------------------------------------------------------------------
# Menus
# ---------------------------------------------------------------------------

def admin_menu():
    """Full-access menu for Admin users."""
    while True:
        print("\n" + "=" * 40)
        print("  ADMIN MENU")
        print("=" * 40)
        print("  1. Add Student")
        print("  2. View All Students")
        print("  3. Search Student by Roll Number")
        print("  4. Update Marks")
        print("  5. Delete Student")
        print("  6. Logout")
        print("=" * 40)
        choice = input("  Enter choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_marks()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        pause()


def teacher_menu():
    """Restricted menu for Teacher users: view, search, and update marks."""
    while True:
        print("\n" + "=" * 40)
        print("  TEACHER MENU")
        print("=" * 40)
        print("  1. View All Students")
        print("  2. Search Student by Roll Number")
        print("  3. Update Marks")
        print("  4. Logout")
        print("=" * 40)
        choice = input("  Enter choice (1-4): ").strip()

        if choice == "1":
            view_all_students()
        elif choice == "2":
            search_student()
        elif choice == "3":
            update_marks()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
        pause()


def student_menu(roll):
    """Minimal menu for Student users: view own record only."""
    while True:
        print("\n" + "=" * 40)
        print("  STUDENT MENU")
        print("=" * 40)
        print("  1. View My Record")
        print("  2. Logout")
        print("=" * 40)
        choice = input("  Enter choice (1-2): ").strip()

        if choice == "1":
            view_own_record(roll)
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
        pause()

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    """Launch the login prompt and route to the correct role-based menu."""
    ensure_file(STUDENTS_FILE)
    ensure_file(CREDENTIALS_FILE)

    while True:
        clear_screen()
        user = login()
        if user is None:
            # After 3 failed attempts, offer to retry or exit
            choice = input("\nTry again? (y/n): ").strip().lower()
            if choice != "y":
                print("Goodbye!")
                break
            continue

        role = user["role"]
        if role == "Admin":
            admin_menu()
        elif role == "Teacher":
            teacher_menu()
        elif role == "Student":
            if "roll" not in user:
                print("Error: No roll number linked to this student account.")
            else:
                student_menu(user["roll"])
        else:
            print(f"Unknown role: {role}")

        # After logout, offer to log in again or exit
        choice = input("\nLog in as another user? (y/n): ").strip().lower()
        if choice != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
