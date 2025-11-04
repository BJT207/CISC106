"""
Technical Debt code
Bakery Curriculum for Tech Debt assignment
Version: 0.0.4

Follow the instructions on the Google doc to clean up this file.

Date: 11/10/2023
"""
from dataclasses import dataclass
from data import DATA
from bakery import assert_equal

# (4.2)
target_grade = 3.5

# (2.1)
@dataclass
class Course:
    course_code: str
    title: str
    grade: str

# (2.2)
@dataclass
class Student:
    name: str
    transcript: list[Course]

# (3.1)
def clean_transcripts(transcripts: str) -> list[Student]:
    students = []
    for student_data_block in transcripts.split('-------'):
        lines = student_data_block.strip().split('\n')
        students.append(create_transcript(lines))
    return students

# (3.2)
def create_transcript(lines: list[str]) -> Student:
    name = lines[-1][6:]
    courses = truncate_demographics(lines)
    return Student(name, courses)

# (3.3)
def truncate_demographics(lines: list[str]) -> list[Course]:
    courses = []
    take_until_toggle = True
    for line in lines:
        if line.startswith('Demographics:'):
            take_until_toggle = False
        elif take_until_toggle:
            courses.append(parse_class_str(line))
    return courses

# (3.4)
def parse_class_str(line: str) -> Course:
    # Example: "CISC-108,Intro to Computer Science,C"
    course, title, grade = line.split(',')
    return Course(course, title, grade)

# (4.1)
def get_target_students(students: list[Student]) -> list[str]:
    transcripts = []
    for student in students:
        if average_grade(filter_compsci_courses(student.transcript)) >= target_grade:
            transcripts.append(student.name)
    return transcripts

# (4.3)
def filter_compsci_courses(courses: list[Course]) -> list[Course]:
    compsci_courses = []
    for course in courses:
        if course.course_code.startswith('CISC'):
            compsci_courses.append(course)
    return compsci_courses

# (4.4)
def average_grade(courses: list[Course]) -> float:
    total = 0.0
    for course in courses:
        total += letter_to_gpa(course.grade)
    return total / len(courses)

# (4.5)
def letter_to_gpa(grade: str) -> float:
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.0
    elif grade == 'C':
        return 2.0
    elif grade == 'D':
        return 1.0
    else:
        return 0.0

# (1)
class_transcipts = clean_transcripts(DATA)
assert_equal(get_target_students(class_transcipts), ['Thomas Silva', 'Kyle Blair', 'William Cantu', 'Lisa Fernandez', 'Katherine Mcdowell', 'Alan Turing', 'Edsger W. Dijkstra', 'Craig Mcneil', 'Mary King', 'Brandon Campbell'])