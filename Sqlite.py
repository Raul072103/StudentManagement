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
    
    
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_teachers_table)
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_subjects_table)
    else:
        print("Error! Cannot create the database connection")
    
    return conn

if __name__ == '__main__':
    
    database = r"C:\Users\raula\Desktop\facultate\anul 2 sem 1\Intermediate programming\Assignment\UniversitySystem\University.sqlite"

    conn = create_tables(database)
    
    conn = create_connection(database)
    subject1 = Subject("AI", "CS4016", 4, 5)
    subject2 = Subject("CA", "CS2014", 2, 5)
    subject3 = Subject("AA", "CS4018", 4, 5)
    subject4 = Subject("DB", "CS1016", 1, 5)

    derek = Teacher("Derek Bridge", 50, "Cork", "derekbridge@ucc.ie", "100101001", "TheFinalBoss", [subject1, subject2, subject3])

    raul = Student("Spatariu Raul", 20, "Fagaras", "raulandrei2019@gmail.com", "100000323",
                "superSecretPassword", 2, [subject1, subject2, subject3], [5.6, 7.8, 9.0])
    
    alin = Student("Spatariu Alin", 23, "Fagaras", "alin.spatariu@gmail.com", "123124300",
                "superSecretPassword2", 4, [subject1, subject2, subject3], [5.6, 7.8, 9.0])

    racu = Headmaster("Maria Racu", 45, "Fagaras", "maria.racu@ucc.ie", "100000001", "MariaRacu", [subject1, subject2])
    
    with(conn):
        #insert_teacher(conn, derek, racu)
        #insert_student(conn, alin, racu)
        insert_subject(conn, subject1, racu)


    conn.close()



