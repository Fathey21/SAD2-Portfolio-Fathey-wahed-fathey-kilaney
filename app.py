"""
Course Management Web Application
Demonstrates Software Engineering Principles and Design Patterns
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os
import csv

app = Flask(__name__)

# Design Pattern: Singleton for Configuration
class Config:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Config._initialized:
            self.courses_file = 'courses.csv'
            self.students_file = 'students.csv'
            self.max_courses = 1000
            self.testing = False  # For tests, avoid file I/O
            Config._initialized = True
    
    def get_courses_file(self):
        return self.courses_file
    
    def get_students_file(self):
        return self.students_file
    
    def set_testing_mode(self, testing):
        self.testing = testing

# Design Pattern: Factory for Course Creation
class CourseFactory:
    @staticmethod
    def create_course(title, description, instructor='Unknown', credits=3):
        return {
            'id': CourseService.get_next_id(),
            'title': title,
            'description': description,
            'instructor': instructor,
            'credits': credits,
            'students': [],  # List of enrolled students
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_student(name, email, student_id):
        return {
            'id': student_id,
            'name': name,
            'email': email,
            'enrolled_at': datetime.now().isoformat(),
            'grade': None
        }

# Design Pattern: Observer Pattern for Course Notifications
class CourseObserver:
    def update(self, course, event_type):
        pass

class EmailNotifier(CourseObserver):
    def update(self, course, event_type):
        print(f"[Email] Course '{course['title']}' - Event: {event_type}")

class LogNotifier(CourseObserver):
    def update(self, course, event_type):
        print(f"[Log] Course '{course['title']}' - Event: {event_type}")

# Design Pattern: Repository for Data Access
class CourseRepository:
    def __init__(self, config):
        self.config = config
    
    def load_courses(self):
        """Load courses from CSV files"""
        if self.config.testing:
            return []  # Return empty list in tests
        courses = []
        course_dict = {}
        
        # Load courses
        if os.path.exists(self.config.get_courses_file()):
            try:
                with open(self.config.get_courses_file(), 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        course = {
                            'id': int(row['id']),
                            'title': row['title'],
                            'description': row['description'],
                            'instructor': row['instructor'],
                            'credits': int(row['credits']),
                            'students': [],
                            'created_at': row['created_at'],
                            'updated_at': row['updated_at']
                        }
                        courses.append(course)
                        course_dict[course['id']] = course
            except:
                pass
        
        # Load students
        if os.path.exists(self.config.get_students_file()):
            try:
                with open(self.config.get_students_file(), 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        student = {
                            'id': row['student_id'],
                            'name': row['name'],
                            'email': row['email'],
                            'enrolled_at': row['enrolled_at'],
                            'grade': row.get('grade') if row.get('grade') else None
                        }
                        course_id = int(row['course_id'])
                        if course_id in course_dict:
                            course_dict[course_id]['students'].append(student)
            except:
                pass
        
        return courses
    
    def save_courses(self, courses):
        """Save courses to CSV files"""
        if self.config.testing:
            return  # Skip file I/O in tests
        # Save courses
        if courses:
            with open(self.config.get_courses_file(), 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'title', 'description', 'instructor', 'credits', 'created_at', 'updated_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for course in courses:
                    writer.writerow({
                        'id': course['id'],
                        'title': course['title'],
                        'description': course['description'],
                        'instructor': course['instructor'],
                        'credits': course['credits'],
                        'created_at': course['created_at'],
                        'updated_at': course['updated_at']
                    })
        
        # Save students
        with open(self.config.get_students_file(), 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['course_id', 'student_id', 'name', 'email', 'grade', 'enrolled_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for course in courses:
                for student in course['students']:
                    writer.writerow({
                        'course_id': course['id'],
                        'student_id': student['id'],
                        'name': student['name'],
                        'email': student['email'],
                        'grade': student.get('grade'),
                        'enrolled_at': student['enrolled_at']
                    })

# Design Pattern: Service for Business Logic
class CourseService:
    def __init__(self, repository, observers=None):
        self.repository = repository
        self.observers = observers or []
        self.courses = self.repository.load_courses()
        self._update_next_id()
    
    @staticmethod
    def get_next_id():
        """Get next available ID"""
        if not hasattr(CourseService, '_next_id'):
            CourseService._next_id = 1
        current_id = CourseService._next_id
        CourseService._next_id += 1
        return current_id
    
    def _update_next_id(self):
        """Update next available ID"""
        if self.courses:
            max_id = max(course.get('id', 0) for course in self.courses)
            CourseService._next_id = max_id + 1
    
    def add_observer(self, observer):
        """Add observer for notifications"""
        self.observers.append(observer)
    
    def _notify_observers(self, course, event_type):
        """Notify all observers"""
        for observer in self.observers:
            observer.update(course, event_type)
    
    def add_course(self, title, description, instructor='Unknown', credits=3):
        """Add a new course"""
        course = CourseFactory.create_course(title, description, instructor, credits)
        self.courses.append(course)
        self.repository.save_courses(self.courses)
        self._notify_observers(course, 'created')
        return course
    
    def get_course(self, course_id):
        """Get course by ID"""
        for course in self.courses:
            if course['id'] == course_id:
                return course
        return None
    
    def update_course(self, course_id, **kwargs):
        """Update course"""
        course = self.get_course(course_id)
        if course:
            for key, value in kwargs.items():
                if key in course:
                    course[key] = value
            course['updated_at'] = datetime.now().isoformat()
            self.repository.save_courses(self.courses)
            self._notify_observers(course, 'updated')
            return course
        return None
    
    def delete_course(self, course_id):
        """Delete course"""
        course = self.get_course(course_id)
        if course:
            self.courses = [c for c in self.courses if c['id'] != course_id]
            self.repository.save_courses(self.courses)
            self._notify_observers(course, 'deleted')
            return True
        return False
    
    def get_all_courses(self):
        """Get all courses"""
        return self.courses
    
    def filter_courses(self, instructor=None):
        """Filter courses by instructor"""
        filtered = self.courses
        if instructor:
            filtered = [c for c in filtered if c['instructor'] == instructor]
        return filtered

# Design Pattern: Service for Student Management
class StudentService:
    def __init__(self, course_service):
        self.course_service = course_service
    
    def enroll_student(self, course_id, name, email, student_id):
        """Enroll a student in a course"""
        course = self.course_service.get_course(course_id)
        if course:
            student = CourseFactory.create_student(name, email, student_id)
            course['students'].append(student)
            course['updated_at'] = datetime.now().isoformat()
            self.course_service.repository.save_courses(self.course_service.courses)
            self.course_service._notify_observers(course, 'student_enrolled')
            return student
        return None
    
    def update_student_grade(self, course_id, student_id, grade):
        """Update student grade"""
        course = self.course_service.get_course(course_id)
        if course:
            for student in course['students']:
                if student['id'] == student_id:
                    student['grade'] = grade
                    course['updated_at'] = datetime.now().isoformat()
                    self.course_service.repository.save_courses(self.course_service.courses)
                    return student
        return None
    
    def remove_student(self, course_id, student_id):
        """Remove student from course"""
        course = self.course_service.get_course(course_id)
        if course:
            course['students'] = [s for s in course['students'] if s['id'] != student_id]
            course['updated_at'] = datetime.now().isoformat()
            self.course_service.repository.save_courses(self.course_service.courses)
            self.course_service._notify_observers(course, 'student_removed')
            return True
# Initialize services
config = Config()
repository = CourseRepository(config)
course_service = CourseService(repository)
course_service.add_observer(EmailNotifier())
course_service.add_observer(LogNotifier())
student_service = StudentService(course_service)
# Flask Routes
@app.route('/')
def index():
    """Home page"""
    courses = course_service.get_all_courses()
    return render_template('index.html', courses=courses)

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Get all courses API"""
    instructor = request.args.get('instructor')
    
    if instructor:
        courses = course_service.filter_courses(instructor=instructor)
    else:
        courses = course_service.get_all_courses()
    return jsonify(courses)

@app.route('/api/courses', methods=['POST'])
def create_course():
    """Create new course API"""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    instructor = data.get('instructor', 'Unknown')
    credits = data.get('credits', 3)
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    course = course_service.add_course(title, description, instructor, credits)
    return jsonify(course), 201

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get course by ID API"""
    course = course_service.get_course(course_id)
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Update course API"""
    data = request.get_json()
    course = course_service.update_course(course_id, **data)
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Delete course API"""
    if course_service.delete_course(course_id):
        return jsonify({'message': 'Course deleted successfully'})
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/<int:course_id>/students', methods=['POST'])
def enroll_student(course_id):
    """Enroll student in course API"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    student_id = data.get('student_id')
    
    if not all([name, email, student_id]):
        return jsonify({'error': 'Name, email, and student_id are required'}), 400
    
    student = student_service.enroll_student(course_id, name, email, student_id)
    if student:
        return jsonify(student), 201
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/<int:course_id>/students/<student_id>', methods=['PUT'])
def update_student_grade(course_id, student_id):
    """Update student grade API"""
    data = request.get_json()
    grade = data.get('grade')
    
    student = student_service.update_student_grade(course_id, student_id, grade)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Course or student not found'}), 404

@app.route('/api/courses/<int:course_id>/students/<student_id>', methods=['DELETE'])
def remove_student(course_id, student_id):
    """Remove student from course API"""
    if student_service.remove_student(course_id, student_id):
        return jsonify({'message': 'Student removed successfully'})
    return jsonify({'error': 'Course or student not found'}), 404

@app.route('/course/<int:course_id>')
def view_course(course_id):
    """View course page"""
    course = course_service.get_course(course_id)
    if course:
        return render_template('course.html', course=course)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

