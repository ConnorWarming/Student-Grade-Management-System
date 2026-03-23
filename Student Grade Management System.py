"""
Student Grade Management System
Connor Warming

Features:
- Add/search students
- Add/update grades
- GPA calculation
- Transcript generation
- Course statistics
- Study group generation
- Data persistence (JSON)
- CLI menu interface

Run:
    python student_grade_system_improved.py
"""

import json
from typing import Dict, List

DATA_FILE = "student_data.json"


# =========================
# Data Structures
# =========================

student_db: Dict[str, dict] = {}
grades_db: Dict[str, Dict[str, int]] = {}


# =========================
# File Persistence
# =========================

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"students": student_db, "grades": grades_db}, f, indent=4)


def load_data():
    global student_db, grades_db
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            student_db = data.get("students", {})
            grades_db = data.get("grades", {})
    except FileNotFoundError:
        student_db = {}
        grades_db = {}


# =========================
# GPA Functions
# =========================

def numeric_to_points(grade: int) -> float:
    if grade >= 90: return 4.0
    if grade >= 80: return 3.0
    if grade >= 70: return 2.0
    if grade >= 60: return 1.0
    return 0.0


def calculate_gpa(student_id: str) -> float:
    grades = grades_db.get(student_id, {})
    if not grades:
        return 0.0
    points = [numeric_to_points(g) for g in grades.values()]
    return round(sum(points) / len(points), 2)


# =========================
# Core Functions
# =========================

def add_student():
    student_id = input("Enter Student ID: ").strip()
    if student_id in student_db:
        print("Student already exists.")
        return

    name = input("Enter Name: ")
    major = input("Enter Major: ")
    year = input("Enter Year: ")
    email = input("Enter Email: ")

    if "@" not in email:
        print("Invalid email.")
        return

    student_db[student_id] = {
        "name": name,
        "major": major,
        "year": year,
        "email": email
    }

    print("Student added successfully.")


def add_grade():
    student_id = input("Student ID: ")
    if student_id not in student_db:
        print("Student not found.")
        return

    course = input("Course Code: ")
    grade = int(input("Grade (0-100): "))
    grade = max(0, min(100, grade))

    grades_db.setdefault(student_id, {})
    grades_db[student_id][course] = grade

    print("Grade added/updated.")


def search_student():
    query = input("Enter student name or ID: ").lower()

    found = False
    for sid, data in student_db.items():
        if query in sid.lower() or query in data["name"].lower():
            print(f"{sid} - {data['name']} ({data['major']})")
            found = True

    if not found:
        print("No student found.")


def generate_transcript():
    student_id = input("Enter Student ID: ")
    if student_id not in student_db:
        print("Student not found.")
        return

    student = student_db[student_id]
    grades = grades_db.get(student_id, {})

    print("\n--- TRANSCRIPT ---")
    print(f"{student['name']} ({student_id})")
    print(f"{student['major']} - {student['year']}")
    print(f"Email: {student['email']}\n")

    if not grades:
        print("No courses.")
    else:
        for course, grade in grades.items():
            print(f"{course}: {grade}")

    print(f"\nGPA: {calculate_gpa(student_id)}")
    print("-------------------\n")


def course_statistics():
    course = input("Enter course code: ")
    grades = []

    for student_grades in grades_db.values():
        if course in student_grades:
            grades.append(student_grades[course])

    if not grades:
        print("No data.")
        return

    print(f"Students: {len(grades)}")
    print(f"Average: {round(sum(grades)/len(grades),2)}")
    print(f"Highest: {max(grades)}")
    print(f"Lowest: {min(grades)}")


def study_groups():
    course = input("Enter course code: ")

    groups = {
        "High Performers": [],
        "Average": [],
        "Needs Help": []
    }

    for sid, student_grades in grades_db.items():
        if course in student_grades:
            grade = student_grades[course]
            name = student_db[sid]["name"]

            if grade >= 85:
                groups["High Performers"].append(name)
            elif grade >= 70:
                groups["Average"].append(name)
            else:
                groups["Needs Help"].append(name)

    for group, students in groups.items():
        print(f"\n{group}:")
        for s in students:
            print(f" - {s}")


# =========================
# Menu System
# =========================

def menu():
    while True:
        print("""
====== STUDENT MANAGEMENT SYSTEM ======
1. Add Student
2. Add Grade
3. Search Student
4. Generate Transcript
5. Course Statistics
6. Study Groups
7. Save & Exit
""")

        choice = input("Select option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            search_student()
        elif choice == "4":
            generate_transcript()
        elif choice == "5":
            course_statistics()
        elif choice == "6":
            study_groups()
        elif choice == "7":
            save_data()
            print("Data saved. Exiting.")
            break
        else:
            print("Invalid option.")


# =========================
# Main
# =========================

if __name__ == "__main__":
    load_data()
    menu()