#!/usr/bin/env python3
"""
Script to add all courses from courses_backup.csv to the main application.
"""

import sys
import csv
sys.path.append('.')

from app import course_manager

def add_backup_courses():
    """Add all courses from backup file to the main system"""

    added_count = 0

    try:
        with open('courses_backup.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip if course with this title already exists
                existing_courses = course_manager.get_all_courses()
                if any(course['title'] == row['title'] for course in existing_courses):
                    print(f"Skipping duplicate course: {row['title']}")
                    continue

                # Add the course
                course = course_manager.add_course(
                    title=row['title'],
                    description=row['description'] or '',
                    instructor=row['instructor'] or 'Unknown',
                    credits=int(row['credits']) if row['credits'] else 3
                )

                if course:
                    print(f"Added course: {course['title']} (ID: {course['id']})")
                    added_count += 1
                else:
                    print(f"Failed to add course: {row['title']}")

    except FileNotFoundError:
        print("courses_backup.csv not found")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"\nتم إضافة {added_count} دورة تدريبية إلى النظام")

if __name__ == "__main__":
    add_backup_courses()