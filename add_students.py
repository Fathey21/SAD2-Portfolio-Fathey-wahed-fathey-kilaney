#!/usr/bin/env python3
"""
Script to add 50 sample students to the first course for testing purposes.
"""

import sys
import os
sys.path.append('.')

from app import course_manager

def add_50_students():
    """Add 50 sample students to the first course"""
    courses = course_manager.get_all_courses()
    if not courses:
        print("No courses found. Please create a course first.")
        return

    course_id = courses[0]['id']  # Use the first course

    print(f"Adding 50 students to course ID {course_id}...")

    for i in range(1, 51):
        student_id = f"STU{i:03d}"
        name = f"Student {i}"
        email = f"student{i}@example.com"

        student = course_manager.enroll_student(course_id, name, email, student_id)
        if student:
            print(f"Added: {student['name']} ({student['id']})")
        else:
            print(f"Failed to add student {i}")

    print("Finished adding 50 students.")

if __name__ == "__main__":
    add_50_students()