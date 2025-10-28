#!/usr/bin/env python3
"""
Student Management System
A comprehensive demonstration of CRUD operations, file I/O, and data management.

Features:
- Add new student records
- View all students or search by ID
- Update student information
- Delete student records
- Calculate GPA automatically
- Persistent storage using JSON files
- Input validation and error handling
"""

import json
import os
from datetime import datetime


class Student:
    """Represents a student with personal and academic information."""
    
    def __init__(self, student_id, name, age, email, grades=None):
        """
        Initialize a Student object.
        
        Args:
            student_id (str): Unique identifier for the student
            name (str): Student's full name
            age (int): Student's age
            email (str): Student's email address
            grades (list): List of numerical grades (0-100)
        """
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.grades = grades if grades else []
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
    
    def calculate_gpa(self):
        """Calculate GPA on a 4.0 scale based on grades."""
        if not self.grades:
            return 0.0
        
        # Convert percentage grades to GPA (simplified conversion)
        avg = sum(self.grades) / len(self.grades)
        if avg >= 90:
            return 4.0
        elif avg >= 80:
            return 3.0
        elif avg >= 70:
            return 2.0
        elif avg >= 60:
            return 1.0
        else:
            return 0.0
    
    def to_dict(self):
        """Convert student object to dictionary for JSON serialization."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'grades': self.grades,
            'enrollment_date': self.enrollment_date,
            'gpa': self.calculate_gpa()
        }
    
    def __str__(self):
        """String representation of student for display."""
        gpa = self.calculate_gpa()
        return f"ID: {self.student_id} | Name: {self.name} | Age: {self.age} | Email: {self.email} | GPA: {gpa:.2f}"


class StudentManagementSystem:
    """Manages student records with CRUD operations and file persistence."""
    
    def __init__(self, filename='students.json'):
        """
        Initialize the management system.
        
        Args:
            filename (str): Path to JSON file for data storage
        """
        self.filename = filename
        self.students = {}
        self.load_students()
    
    def load_students(self):
        """Load student data from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    # Reconstruct Student objects from dictionary data
                    for student_id, student_data in data.items():
                        student = Student(
                            student_data['student_id'],
                            student_data['name'],
                            student_data['age'],
                            student_data['email'],
                            student_data.get('grades', [])
                        )
                        self.students[student_id] = student
                print(f"✓ Loaded {len(self.students)} student(s) from {self.filename}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"✗ Error loading data: {e}. Starting with empty database.")
        else:
            print("No existing data file found. Starting fresh.")
    
    def save_students(self):
        """Save all student data to JSON file."""
        try:
            data = {sid: student.to_dict() for sid, student in self.students.items()}
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"✓ Data saved to {self.filename}")
        except IOError as e:
            print(f"✗ Error saving data: {e}")
    
    def add_student(self, student_id, name, age, email, grades=None):
        """Add a new student to the system."""
        # Input validation
        if student_id in self.students:
            print(f"✗ Student ID {student_id} already exists!")
            return False
        
        if age < 0 or age > 150:
            print("✗ Invalid age!")
            return False
        
        if '@' not in email:
            print("✗ Invalid email format!")
            return False
        
        # Create and add new student
        student = Student(student_id, name, age, email, grades)
        self.students[student_id] = student
        self.save_students()
        print(f"✓ Added student: {student}")
        return True
    
    def get_student(self, student_id):
        """Retrieve a student by ID."""
        student = self.students.get(student_id)
        if student:
            return student
        else:
            print(f"✗ Student ID {student_id} not found!")
            return None
    
    def update_student(self, student_id, name=None, age=None, email=None, grades=None):
        """Update existing student information."""
        student = self.get_student(student_id)
        if not student:
            return False
        
        # Update only provided fields
        if name:
            student.name = name
        if age is not None:
            if age < 0 or age > 150:
                print("✗ Invalid age!")
                return False
            student.age = age
        if email:
            if '@' not in email:
                print("✗ Invalid email format!")
                return False
            student.email = email
        if grades is not None:
            student.grades = grades
        
        self.save_students()
        print(f"✓ Updated student: {student}")
        return True
    
    def delete_student(self, student_id):
        """Remove a student from the system."""
        if student_id in self.students:
            student = self.students.pop(student_id)
            self.save_students()
            print(f"✓ Deleted student: {student.name} (ID: {student_id})")
            return True
        else:
            print(f"✗ Student ID {student_id} not found!")
            return False
    
    def list_all_students(self):
        """Display all students in the system."""
        if not self.students:
            print("No students in the system.")
            return
        
        print("\n" + "="*80)
        print(f"Total Students: {len(self.students)}")
        print("="*80)
        for student in self.students.values():
            print(student)
            print(f"  Grades: {student.grades}")
            print("-"*80)
    
    def search_by_name(self, name):
        """Search for students by name (partial match)."""
        results = [s for s in self.students.values() if name.lower() in s.name.lower()]
        if results:
            print(f"\nFound {len(results)} student(s):")
            for student in results:
                print(student)
        else:
            print(f"No students found with name containing '{name}'")
        return results


def main():
    """Main function demonstrating the Student Management System."""
    print("\n" + "="*80)
    print("STUDENT MANAGEMENT SYSTEM DEMO")
    print("="*80 + "\n")
    
    # Initialize the system
    sms = StudentManagementSystem()
    
    # Demo: Add students
    print("\n--- Adding Students ---")
    sms.add_student("S001", "Alice Johnson", 20, "alice@example.com", [85, 90, 88])
    sms.add_student("S002", "Bob Smith", 22, "bob@example.com", [78, 82, 80])
    sms.add_student("S003", "Charlie Brown", 21, "charlie@example.com", [92, 95, 93])
    
    # Demo: List all students
    print("\n--- All Students ---")
    sms.list_all_students()
    
    # Demo: Search for student
    print("\n--- Searching for 'Bob' ---")
    sms.search_by_name("Bob")
    
    # Demo: Update student
    print("\n--- Updating Student S002 ---")
    sms.update_student("S002", age=23, grades=[78, 82, 80, 85])
    
    # Demo: Get specific student
    print("\n--- Getting Student S003 ---")
    student = sms.get_student("S003")
    if student:
        print(f"Retrieved: {student}")
        print(f"GPA: {student.calculate_gpa():.2f}")
    
    # Demo: Try to add duplicate (should fail)
    print("\n--- Attempting to Add Duplicate ID ---")
    sms.add_student("S001", "David Lee", 19, "david@example.com")
    
    # Demo: Invalid input (should fail)
    print("\n--- Testing Input Validation ---")
    sms.add_student("S004", "Invalid Student", 200, "bademail")  # Invalid age and email
    
    # Demo: Delete student
    print("\n--- Deleting Student S002 ---")
    sms.delete_student("S002")
    
    # Demo: Final list
    print("\n--- Final Student List ---")
    sms.list_all_students()
    
    print("\n" + "="*80)
    print("DEMO COMPLETED")
    print("="*80)


if __name__ == "__main__":
    main()
