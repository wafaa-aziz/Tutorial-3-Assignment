import sqlite3

db = sqlite3.connect("students.db")
db.execute("PRAGMA foreign_keys = ON")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS grades")
cursor.execute("DROP TABLE IF EXISTS registered_courses")
cursor.execute("DROP TABLE IF EXISTS student")
cursor.execute("""
CREATE TABLE student (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")
cursor.execute("""
CREATE TABLE registered_courses (
    student_id INTEGER,
    course_id TEXT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")
cursor.execute("""
CREATE TABLE grades (
    student_id INTEGER,
    course_id TEXT,
    grade REAL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")
students = [
    (1, "Wafaa Aziz", 20),
    (2, "Sara Ali", 21),
    (3, "Omar Hassan", 19)
]

cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)
registered_courses = [
    (1, "CS101"),
    (1, "MATH201"),
    (2, "CS101"),
    (2, "ENG105"),
    (3, "MATH201"),
    (3, "ENG105")
]

cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered_courses)
grades = [
    (1, "CS101", 88),
    (1, "MATH201", 92),
    (2, "CS101", 75),
    (2, "ENG105", 81),
    (3, "MATH201", 64),
    (3, "ENG105", 90)
]

cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)
db.commit()
print("Maximum grade for each student:")

cursor.execute("""
SELECT g.student_id, g.course_id, g.grade
FROM grades g
JOIN (
    SELECT student_id, MAX(grade) AS max_grade
    FROM grades
    GROUP BY student_id
) m
ON g.student_id = m.student_id AND g.grade = m.max_grade
ORDER BY g.student_id;
""")

for row in cursor.fetchall():
    print(row)
print("\nAverage grade for each student:")

cursor.execute("""
SELECT student_id, AVG(grade)
FROM grades
GROUP BY student_id
ORDER BY student_id;
""")

for row in cursor.fetchall():
    print(row)
db.close()