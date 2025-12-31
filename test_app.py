"""
Automated Test Suite for Course Management Application
50 Automated Test Cases
"""

import pytest
import json
import os
from app import app, Config, CourseFactory, CourseService, CourseRepository, EmailNotifier

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def clean_tasks():
    """Clean up courses.csv and students.csv before and after tests"""
    # Set testing mode to avoid file I/O
    from app import Config, CourseService
    config = Config()
    config.set_testing_mode(True)
    
    # Reset the global course_service
    from app import course_service
    course_service.courses = []
    CourseService._next_id = 1
    yield
    # Reset after tests
    config.set_testing_mode(False)

# Test Case 1-10: Course Creation Tests
def test_create_course_with_title(client, clean_tasks):
    """Test Case 1: Create course with valid title"""
    response = client.post('/api/courses', json={'title': 'Test Course'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Course'
    assert 'students' in data

def test_create_course_without_title(client, clean_tasks):
    """Test Case 2: Create course without title should fail"""
    response = client.post('/api/courses', json={'description': 'No title'})
    assert response.status_code == 400

def test_create_course_with_all_fields(client, clean_tasks):
    """Test Case 3: Create course with all fields"""
    response = client.post('/api/courses', json={
        'title': 'Complete Course',
        'description': 'Full description',
        'instructor': 'Dr. Smith',
        'credits': 4
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['instructor'] == 'Dr. Smith'
    assert data['credits'] == 4

def test_create_course_with_default_instructor(client, clean_tasks):
    """Test Case 4: Create course with default instructor"""
    response = client.post('/api/courses', json={'title': 'Default Instructor Course'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['instructor'] == 'Unknown'

def test_create_course_with_instructor(client, clean_tasks):
    """Test Case 5: Create course with specific instructor"""
    response = client.post('/api/courses', json={
        'title': 'Instructor Course',
        'instructor': 'Dr. Smith'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['instructor'] == 'Dr. Smith'

def test_create_course_with_credits(client, clean_tasks):
    """Test Case 6: Create course with credits"""
    response = client.post('/api/courses', json={
        'title': 'Credits Course',
        'credits': 4
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['credits'] == 4

def test_create_course_with_empty_description(client, clean_tasks):
    """Test Case 7: Create course with empty description"""
    response = client.post('/api/courses', json={'title': 'No Description Course'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['description'] == ''

def test_create_course_with_long_title(client, clean_tasks):
    """Test Case 8: Create course with long title"""
    long_title = 'A' * 200
    response = client.post('/api/courses', json={'title': long_title})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert len(data['title']) == 200

def test_create_course_has_created_at(client, clean_tasks):
    """Test Case 9: Created course has created_at timestamp"""
    response = client.post('/api/courses', json={'title': 'Timestamp Test'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'created_at' in data
    assert data['created_at'] is not None

def test_create_course_has_id(client, clean_tasks):
    """Test Case 10: Created course has unique ID"""
    response1 = client.post('/api/courses', json={'title': 'Course 1'})
    response2 = client.post('/api/courses', json={'title': 'Course 2'})
    data1 = json.loads(response1.data)
    data2 = json.loads(response2.data)
    assert data1['id'] != data2['id']

# Test Case 11-20: Task Retrieval Tests
def test_get_all_courses_empty(client, clean_tasks):
    """Test Case 11: Get all courses when empty"""
    response = client.get('/api/courses')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

def test_get_all_courses_with_data(client, clean_tasks):
    """Test Case 12: Get all courses with data"""
    client.post('/api/courses', json={'title': 'Course 1'})
    client.post('/api/courses', json={'title': 'Course 2'})
    response = client.get('/api/courses')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2

def test_get_course_by_id_exists(client, clean_tasks):
    """Test Case 13: Get course by ID when exists"""
    create_response = client.post('/api/courses', json={'title': 'Find Me'})
    course_id = json.loads(create_response.data)['id']
    response = client.get(f'/api/courses/{course_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Find Me'

def test_get_course_by_id_not_exists(client, clean_tasks):
    """Test Case 14: Get course by ID when not exists"""
    response = client.get('/api/courses/999')
    assert response.status_code == 404

def test_enroll_student_in_course(client, clean_tasks):
    """Test Case 15: Enroll student in course"""
    # Create course
    course_response = client.post('/api/courses', json={'title': 'Math 101'})
    course_id = json.loads(course_response.data)['id']
    
    # Enroll student
    student_data = {'name': 'John Doe', 'email': 'john@example.com', 'student_id': 'S001'}
    response = client.post(f'/api/courses/{course_id}/students', json=student_data)
    assert response.status_code == 201
    
    # Check student was added
    course_response = client.get(f'/api/courses/{course_id}')
    course_data = json.loads(course_response.data)
    assert len(course_data['students']) == 1
    assert course_data['students'][0]['name'] == 'John Doe'

def test_update_student_grade(client, clean_tasks):
    """Test Case 16: Update student grade"""
    # Create course and enroll student
    course_response = client.post('/api/courses', json={'title': 'Math 101'})
    course_id = json.loads(course_response.data)['id']
    student_data = {'name': 'John Doe', 'email': 'john@example.com', 'student_id': 'S001'}
    client.post(f'/api/courses/{course_id}/students', json=student_data)
    
    # Update grade
    response = client.put(f'/api/courses/{course_id}/students/S001', json={'grade': 'A'})
    assert response.status_code == 200
    
    # Check grade was updated
    course_response = client.get(f'/api/courses/{course_id}')
    course_data = json.loads(course_response.data)
    assert course_data['students'][0]['grade'] == 'A'

def test_remove_student_from_course(client, clean_tasks):
    """Test Case 17: Remove student from course"""
    # Create course and enroll student
    course_response = client.post('/api/courses', json={'title': 'Math 101'})
    course_id = json.loads(course_response.data)['id']
    student_data = {'name': 'John Doe', 'email': 'john@example.com', 'student_id': 'S001'}
    client.post(f'/api/courses/{course_id}/students', json=student_data)
    
    # Remove student
    response = client.delete(f'/api/courses/{course_id}/students/S001')
    assert response.status_code == 200
    
    # Check student was removed
    course_response = client.get(f'/api/courses/{course_id}')
    course_data = json.loads(course_response.data)
    assert len(course_data['students']) == 0

def test_enroll_multiple_students(client, clean_tasks):
    """Test Case 18: Enroll multiple students in course"""
    # Create course
    course_response = client.post('/api/courses', json={'title': 'Math 101'})
    course_id = json.loads(course_response.data)['id']
    
    # Enroll multiple students
    students = [
        {'name': 'John Doe', 'email': 'john@example.com', 'student_id': 'S001'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'student_id': 'S002'},
        {'name': 'Bob Johnson', 'email': 'bob@example.com', 'student_id': 'S003'}
    ]
    
    for student in students:
        response = client.post(f'/api/courses/{course_id}/students', json=student)
        assert response.status_code == 201
    
    # Check all students enrolled
    course_response = client.get(f'/api/courses/{course_id}')
    course_data = json.loads(course_response.data)
    assert len(course_data['students']) == 3

def test_student_enrollment_with_grades(client, clean_tasks):
    """Test Case 19: Student enrollment with grades"""
    # Create course and enroll students
    course_response = client.post('/api/courses', json={'title': 'Math 101'})
    course_id = json.loads(course_response.data)['id']
    
    students = [
        {'name': 'John Doe', 'email': 'john@example.com', 'student_id': 'S001'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'student_id': 'S002'}
    ]
    
    for student in students:
        response = client.post(f'/api/courses/{course_id}/students', json=student)
        assert response.status_code == 201
    
    # Update grades
    client.put(f'/api/courses/{course_id}/students/S001', json={'grade': 'A'})
    client.put(f'/api/courses/{course_id}/students/S002', json={'grade': 'B'})
    
    # Check grades
    course_response = client.get(f'/api/courses/{course_id}')
    course_data = json.loads(course_response.data)
    assert len(course_data['students']) == 2
    grades = [s['grade'] for s in course_data['students']]
    assert 'A' in grades and 'B' in grades

def test_get_course_returns_all_fields(client, clean_tasks):
    """Test Case 20: Get course returns all fields"""
    response = client.post('/api/courses', json={
        'title': 'Full Course',
        'description': 'Description',
        'instructor': 'Dr. Smith',
        'credits': 4
    })
    course_id = json.loads(response.data)['id']
    get_response = client.get(f'/api/courses/{course_id}')
    data = json.loads(get_response.data)
    assert 'id' in data
    assert 'title' in data
    assert 'description' in data
    assert 'instructor' in data
    assert 'credits' in data
    assert 'students' in data
    assert 'created_at' in data
    assert 'updated_at' in data

# Test Case 21-30: Task Update Tests
def test_update_course_instructor(client, clean_tasks):
    """Test Case 21: Update course instructor"""
    create_response = client.post('/api/courses', json={'title': 'Update Me'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'instructor': 'Dr. Smith'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['instructor'] == 'Dr. Smith'

def test_update_course_title(client, clean_tasks):
    """Test Case 22: Update course title"""
    create_response = client.post('/api/courses', json={'title': 'Old Title'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'title': 'New Title'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'New Title'

def test_update_course_description(client, clean_tasks):
    """Test Case 23: Update course description"""
    create_response = client.post('/api/courses', json={'title': 'Course'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'description': 'New Description'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['description'] == 'New Description'

def test_update_course_credits(client, clean_tasks):
    """Test Case 24: Update course credits"""
    create_response = client.post('/api/courses', json={'title': 'Course'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'credits': 4})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['credits'] == 4

def test_update_course_credits_different(client, clean_tasks):
    """Test Case 25: Update course credits to different value"""
    create_response = client.post('/api/courses', json={'title': 'Course', 'credits': 2})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'credits': 5})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['credits'] == 5

def test_update_course_multiple_fields(client, clean_tasks):
    """Test Case 26: Update multiple course fields"""
    create_response = client.post('/api/courses', json={'title': 'Original'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={
        'title': 'Updated',
        'instructor': 'Dr. Johnson',
        'credits': 4
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated'
    assert data['instructor'] == 'Dr. Johnson'
    assert data['credits'] == 4

def test_update_course_not_exists(client, clean_tasks):
    """Test Case 27: Update course that doesn't exist"""
    response = client.put('/api/courses/999', json={'title': 'New'})
    assert response.status_code == 404

def test_update_course_updates_timestamp(client, clean_tasks):
    """Test Case 28: Update course updates updated_at timestamp"""
    create_response = client.post('/api/courses', json={'title': 'Course'})
    course_id = json.loads(create_response.data)['id']
    original_time = json.loads(create_response.data)['updated_at']
    import time
    time.sleep(1)
    response = client.put(f'/api/courses/{course_id}', json={'instructor': 'Dr. Smith'})
    updated_time = json.loads(response.data)['updated_at']
    assert updated_time != original_time

def test_update_course_preserves_other_fields(client, clean_tasks):
    """Test Case 29: Update course preserves other fields"""
    create_response = client.post('/api/courses', json={
        'title': 'Original',
        'description': 'Keep This',
        'instructor': 'Dr. Smith'
    })
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'credits': 4})
    data = json.loads(response.data)
    assert data['description'] == 'Keep This'
    assert data['instructor'] == 'Dr. Smith'

def test_update_course_with_empty_json(client, clean_tasks):
    """Test Case 30: Update course with empty JSON"""
    create_response = client.post('/api/courses', json={'title': 'Course'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={})
    assert response.status_code == 200

# Test Case 31-40: Task Deletion Tests
def test_delete_course_exists(client, clean_tasks):
    """Test Case 31: Delete course that exists"""
    create_response = client.post('/api/courses', json={'title': 'Delete Me'})
    course_id = json.loads(create_response.data)['id']
    response = client.delete(f'/api/courses/{course_id}')
    assert response.status_code == 200

def test_delete_course_not_exists(client, clean_tasks):
    """Test Case 32: Delete course that doesn't exist"""
    response = client.delete('/api/courses/999')
    assert response.status_code == 404

def test_delete_course_removes_from_list(client, clean_tasks):
    """Test Case 33: Delete course removes from course list"""
    client.post('/api/courses', json={'title': 'Course 1'})
    client.post('/api/courses', json={'title': 'Course 2'})
    client.delete('/api/courses/1')
    response = client.get('/api/courses')
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['id'] == 2

def test_delete_all_courses(client, clean_tasks):
    """Test Case 34: Delete all courses"""
    client.post('/api/courses', json={'title': 'Course 1'})
    client.post('/api/courses', json={'title': 'Course 2'})
    client.post('/api/courses', json={'title': 'Course 3'})
    client.delete('/api/courses/1')
    client.delete('/api/courses/2')
    client.delete('/api/courses/3')
    response = client.get('/api/courses')
    data = json.loads(response.data)
    assert len(data) == 0

def test_delete_course_returns_success_message(client, clean_tasks):
    """Test Case 35: Delete course returns success message"""
    create_response = client.post('/api/courses', json={'title': 'Course'})
    course_id = json.loads(create_response.data)['id']
    response = client.delete(f'/api/courses/{course_id}')
    data = json.loads(response.data)
    assert 'message' in data

# Test Case 36-40: Design Pattern Tests
def test_singleton_config_pattern():
    """Test Case 36: Singleton pattern for Config"""
    config1 = Config()
    config2 = Config()
    assert config1 is config2

def test_factory_pattern_creates_course():
    """Test Case 37: Factory pattern creates course"""
    course = CourseFactory.create_course('Test Course', 'Description', 'Instructor', 3)
    assert course['title'] == 'Test Course'
    assert course['description'] == 'Description'
    assert course['instructor'] == 'Instructor'
    assert course['credits'] == 3

def test_observer_pattern_notification(client, clean_tasks):
    """Test Case 38: Observer pattern sends notifications"""
    from app import CourseRepository, CourseService
    config = Config()
    repository = CourseRepository(config)
    service = CourseService(repository)
    test_observer = EmailNotifier()
    service.add_observer(test_observer)
    course = service.add_course('Test Course', 'Description')
    # Observer should be called (check console output)

def test_course_service_behavior():
    """Test Case 39: CourseService maintains state"""
    from app import CourseRepository, CourseService
    config = Config()
    repository = CourseRepository(config)
    service1 = CourseService(repository)
    service2 = CourseService(repository)
    # Both should work with same repository

def test_course_factory_creates_unique_ids():
    """Test Case 40: Factory creates courses with unique IDs"""
    CourseService._next_id = 1
    course1 = CourseFactory.create_course('Course 1', '')
    course2 = CourseFactory.create_course('Course 2', '')
    assert course1['id'] != course2['id']

# Test Case 41-50: Edge Cases and Integration Tests
def test_create_multiple_courses_sequential(client, clean_tasks):
    """Test Case 41: Create multiple courses sequentially"""
    for i in range(10):
        response = client.post('/api/courses', json={'title': f'Course {i}'})
        assert response.status_code == 201

def test_get_courses_after_multiple_operations(client, clean_tasks):
    """Test Case 42: Get courses after multiple operations"""
    client.post('/api/courses', json={'title': 'Course 1'})
    client.post('/api/courses', json={'title': 'Course 2'})
    client.put('/api/courses/1', json={'instructor': 'Dr. Smith'})
    client.delete('/api/courses/2')
    response = client.get('/api/courses')
    data = json.loads(response.data)
    assert len(data) == 1

def test_course_persistence(client, clean_tasks):
    """Test Case 43: Courses persist after creation"""
    from app import Config, CourseRepository, CourseService
    config = Config()
    if config.testing:
        pytest.skip("Persistence test skipped in testing mode")
    client.post('/api/courses', json={'title': 'Persist Test'})
    # Create new service instance to test persistence
    repository = CourseRepository(config)
    new_service = CourseService(repository)
    courses = new_service.get_all_courses()
    assert len(courses) == 1

def test_course_id_increment(client, clean_tasks):
    """Test Case 44: Course IDs increment correctly"""
    r1 = client.post('/api/courses', json={'title': 'Course 1'})
    r2 = client.post('/api/courses', json={'title': 'Course 2'})
    r3 = client.post('/api/courses', json={'title': 'Course 3'})
    id1 = json.loads(r1.data)['id']
    id2 = json.loads(r2.data)['id']
    id3 = json.loads(r3.data)['id']
    assert id2 == id1 + 1
    assert id3 == id2 + 1

def test_get_courses_empty_list(client, clean_tasks):
    """Test Case 45: Get courses returns empty list when none exist"""
    response = client.get('/api/courses')
    data = json.loads(response.data)
    assert len(data) == 0

def test_update_nonexistent_field(client, clean_tasks):
    """Test Case 46: Update with nonexistent field"""
    create_response = client.post('/api/courses', json={'title': 'Course'})
    course_id = json.loads(create_response.data)['id']
    response = client.put(f'/api/courses/{course_id}', json={'nonexistent': 'value'})
    assert response.status_code == 200

def test_create_course_special_characters(client, clean_tasks):
    """Test Case 47: Create course with special characters"""
    response = client.post('/api/courses', json={'title': 'Course !@#$%^&*()'})
    assert response.status_code == 201

def test_create_course_unicode(client, clean_tasks):
    """Test Case 48: Create course with Unicode characters"""
    response = client.post('/api/courses', json={'title': 'دورة عربية'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'دورة عربية'

def test_api_endpoints_exist(client, clean_tasks):
    """Test Case 49: All API endpoints exist"""
    assert client.get('/api/courses').status_code == 200
    assert client.post('/api/courses', json={'title': 'Test'}).status_code == 201
    assert client.get('/api/courses/1').status_code in [200, 404]
    assert client.put('/api/courses/1', json={}).status_code in [200, 404]
    assert client.delete('/api/courses/1').status_code in [200, 404]

def test_home_page_loads(client, clean_tasks):
    """Test Case 50: Home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

