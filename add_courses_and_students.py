#!/usr/bin/env python3
"""
Script to add 10 sample courses with one student each for testing purposes.
"""

import sys
import os
sys.path.append('.')

from app import course_manager

def add_10_courses_with_students():
    """Add 10 sample courses, each with one enrolled student"""

    course_data = [
        {"title": "Mathematics 101", "description": "Basic mathematics course", "instructor": "Dr. Ahmed", "credits": 3},
        {"title": "Physics Fundamentals", "description": "Introduction to physics", "instructor": "Dr. Fatima", "credits": 4},
        {"title": "Chemistry Basics", "description": "Fundamental chemistry concepts", "instructor": "Dr. Omar", "credits": 3},
        {"title": "Biology Essentials", "description": "Core biology principles", "instructor": "Dr. Layla", "credits": 4},
        {"title": "Computer Science Intro", "description": "Programming fundamentals", "instructor": "Dr. Karim", "credits": 3},
        {"title": "History of Science", "description": "Scientific discoveries timeline", "instructor": "Dr. Nour", "credits": 2},
        {"title": "English Literature", "description": "Classic literature analysis", "instructor": "Dr. Sara", "credits": 3},
        {"title": "Statistics 101", "description": "Basic statistical methods", "instructor": "Dr. Youssef", "credits": 3},
        {"title": "Art Appreciation", "description": "Understanding visual arts", "instructor": "Dr. Mona", "credits": 2},
        {"title": "Economics Principles", "description": "Introduction to economics", "instructor": "Dr. Hassan", "credits": 3}
    ]

    print("Adding 10 courses with one student each...")

    for i, data in enumerate(course_data, 1):
        # Create course
        course = course_manager.add_course(
            title=data["title"],
            description=data["description"],
            instructor=data["instructor"],
            credits=data["credits"]
        )

        if course:
            print(f"Created course: {course['title']} (ID: {course['id']})")

            # Enroll one student
            student_id = f"STD{i:03d}"
            name = f"Student {i}"
            email = f"student{i}@university.edu"

            student = course_manager.enroll_student(course['id'], name, email, student_id)
            if student:
                print(f"Enrolled student: {student['name']} ({student['id']}) in course {course['title']}")
            else:
                print(f"Failed to enroll student in course {course['title']}")
        else:
            print(f"Failed to create course: {data['title']}")

    print("Finished adding 10 courses with students.")

if __name__ == "__main__":
    add_10_courses_with_students()