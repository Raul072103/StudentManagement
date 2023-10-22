from re import sub
import sqlite3
from sqlite3 import Connection, Error

from Headmaster import Headmaster
from Student import Student
from Subject import Subject

from Teacher import Teacher

def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)

def insert_teacher(conn: Connection, teacher: Teacher, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        sql = """INSERT INTO teachers(teacher_id, name, age, address, email, password)
                 VALUES(?, ?, ?, ?, ?, ?); """
        data = (teacher.id, teacher.name, teacher.age, teacher.address, teacher.email, teacher.password)
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        #we also need to insert the subjects the teacher is teaching
        insert_teacher_subjects(conn, teacher.subjects_taught, headmaster)
    else:
        print("You don't have the authorization to do this action!")

def insert_student(conn: Connection, student: Student, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        sql = """INSERT INTO students(student_id, name, age, address, email, password, current_year)
                 VALUES(?, ?, ?, ?, ?, ?, ?)"""
        data = (student.id, student.name, student.age, student.address, student.email, student.password, student.current_year)
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        #we also need to show the subjects the student is taking
        insert_student_subjects(conn, student, headmaster)
    else:
        print("You don't have the authorization to do this action!")

def insert_subject(conn: Connection, subject: Subject, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        sql = """INSERT INTO subjects(subject_code, subject_name, subject_year, credits_worth)
                 VALUES(?, ?, ?, ?)"""
        data = (subject.code, subject.name, subject.year, subject.credits_worth)
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        cur.close()

def delete_student(conn: Connection, student_id: str, headmaster: Headmaster):

    if type(headmaster) == Headmaster:

        #first we need to delete all the subjects the student is taking
        cur = conn.cursor()
        sql1 = """DELETE 
                  FROM student_subjects
                  WHERE student_id = ?"""
        cur.execute(sql1, student_id) 

        sql2 = """DELETE
                 FROM students
                 WHERE student_id = ?"""
        cur.execute(sql2, (student_id, ))
        conn.commit()
        cur.close()

def delete_subject(conn: Connection, subject_code: str, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        sql = """DELETE
                 FROM subjects
                 WHERE subject_code = ?"""
        cur = conn.cursor()
        cur.execute(sql, (subject_code, ))
        conn.commit()
        cur.close()

def delete_teacher(conn: Connection, teacher_id: str, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        sql = """DELETE
                 FROM teachers
                 WHERE teacher_id = ?"""
        cur = conn.cursor()
        cur.execute(sql, (teacher_id, ))
        conn.commit()
        cur.close()

def view_student_info(conn: Connection, student_id: str, person):

    if (type(person) == Student or Teacher or Headmaster):
        sql = """SELECT student_id, name, age, email, address, current_year
                 FROM students
                 WHERE student_id = ?
                 """
        cur = conn.cursor()
        cur.execute(sql, (student_id,))
        conn.commit()

        row = cur.fetchall()

        print(row)

        cur.close()

def view_teacher_info(conn: Connection, teacher_id: str, teacher):

    if (type(teacher) == Teacher or Headmaster):
        sql = """SELECT teacher_id, name, age, email, address
                 FROM teachers
                 WHERE teacher_id = ?
                 """
        cur = conn.cursor()
        cur.execute(sql, (teacher_id,))
        conn.commit()

        row = cur.fetchall()

        print(row)

        cur.close()

def view_all_teachers(conn: Connection, teacher):

    if (type(teacher) == Teacher or Headmaster):
        sql = """SELECT teacher_id, name, age, email, address
                 FROM teachers
                 """
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()

def insert_teacher_subjects(conn: Connection, subjects: Subject ,teacher):

    if (type(teacher) == Teacher or Headmaster):
        
        sql = """INSERT INTO teacher_subjects(teacher_id, subject_code)
                 VALUES(?, ?)"""
        cur = conn.cursor()
        
        for i in range(0, len(subjects)):
            
            cur.execute(sql, (teacher.id, subjects[i].code))
            conn.commit()

        cur.close()

def insert_student_subjects(conn: Connection, student: Student ,teacher):

    if (type(teacher) == Teacher or Headmaster):
        
        sql = """INSERT INTO student_subjects(student_id, subject_code)
                 VALUES(?, ?)"""
        cur = conn.cursor()
        
        subjects = student.subjects

        for i in range(0, len(subjects)):
            
            cur.execute(sql, (student.id, subjects[i].code))
            conn.commit()

        cur.close()        


def create_tables(database):

    sql_create_teachers_table = """ CREATE TABLE IF NOT EXISTS teachers(
                                            teacher_id text PRIMARY KEY,
                                            name text NOT NULL,
                                            age integer,
                                            address text NOT NULL,
                                            email text NOT NULL,
                                            password text NOT NULL
                                        );"""

    sql_create_subjects_table = """CREATE TABLE IF NOT EXISTS subjects(
                                            subject_code text PRIMARY KEY,
                                            subject_name text NOT NULL,
                                            subject_year text NOT NULL,
                                            credits_worth REAL
                                );"""
    
    sql_create_students_table = """CREATE TABLE IF NOT EXISTS students(
                                            student_id text PRIMARY KEY,
                                            name text NOT NULL,
                                            age integer,
                                            address text NOT NULL,
                                            email text NOT NULL,
                                            password text NOT NULL,
                                            current_year integer
                                );"""
    
    sql_create_teacher_subjects_table = """CREATE TABLE IF NOT EXISTS teacher_subjects(
                                            teacher_id text,
                                            subject_code text,

                                            PRIMARY KEY(teacher_id, subject_code),
                                            FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id)
                                 );"""
    
    sql_create_student_subjects_table = """CREATE TABlE IF NOT EXISTS student_subjects(
                                            student_id text,
                                            subject_code text,

                                            PRIMARY KEY(student_id, subject_code),
                                            FOREIGN KEY(student_id) REFERENCES students(student_id)
                                );"""
    
    
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_teachers_table)
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_subjects_table)
        create_table(conn, sql_create_teacher_subjects_table)
        create_table(conn, sql_create_student_subjects_table)
    else:
        print("Error! Cannot create the database connection")
    
    return conn

if __name__ == '__main__':
    
    database = r"C:\Users\raula\Desktop\facultate\anul 2 sem 1\Intermediate programming\Assignment\UniversitySystem\University.sqlite"

    conn = create_tables(database)
    
    subject1 = Subject("AI", "CS4016", 4, 5)
    subject2 = Subject("CA", "CS2014", 2, 5)
    subject3 = Subject("AA", "CS4018", 4, 5)
    subject4 = Subject("DB", "CS1016", 1, 5)

    derek = Teacher("Derek Bridge", 50, "Cork", "derekbridge@ucc.ie", "100101001", "TheFinalBoss", [subject1, subject2, subject3])
    derek2 = Teacher("Derek Bridge", 50, "Cork", "derekbridge@ucc.ie", "100101002", "TheFinalBoss", [subject1, subject2, subject3])
    derek3 = Teacher("Derek Bridge", 50, "Cork", "derekbridge@ucc.ie", "100101003", "TheFinalBoss", [subject1, subject2, subject3])
    derek4 = Teacher("Derek Bridge", 50, "Cork", "derekbridge@ucc.ie", "100101004", "TheFinalBoss", [subject1, subject2, subject3])

    raul = Student("Spatariu Raul", 20, "Fagaras", "raulandrei2019@gmail.com", "100000323",
                "superSecretPassword", 2, [subject1, subject2, subject3], [5.6, 7.8, 9.0])
    
    alin = Student("Spatariu Alin", 23, "Fagaras", "alin.spatariu@gmail.com", "123124300",
                "superSecretPassword2", 4, [subject1, subject2, subject3], [5.6, 7.8, 9.0])

    racu = Headmaster("Maria Racu", 45, "Fagaras", "maria.racu@ucc.ie", "100000001", "MariaRacu", [subject1, subject2])
    
    with(conn):
        #insert_teacher(conn, derek2, racu)
        #insert_teacher(conn, derek3, racu)
        #insert_teacher(conn, derek4, racu)

        #insert_student(conn, alin, racu)
        #insert_student(conn, raul, racu)
        #insert_subject(conn, subject1, racu)
        delete_student(conn, "100000323", racu)
        #delete_teacher(conn, "100101001", racu)
        #delete_subject(conn, "CS4016", racu)
        #view_student_info(conn, "100000323", raul)
        #view_all_teachers(conn, derek)
        #insert_teacher_subjects(conn, derek.subjects_taught, derek)
        #insert_student_subjects(conn, raul, racu)

    conn.close()



