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
        #we also need to insert the marks the student has
        insert_student_marks(conn, student, headmaster)
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
        cur.execute(sql1, (student_id, )) 

        #second delete the marks
        sql2 = """DELETE 
                  FROM MARKS
                  WHERE student_id = ?"""
        cur.execute(sql2, (student_id, ))

        sql3 = """DELETE
                 FROM students
                 WHERE student_id = ?"""
        cur.execute(sql3, (student_id, ))

        
        conn.commit()
        cur.close()

def delete_subject(conn: Connection, subject_code: str, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        cur = conn.cursor()
        #delete also the subjects from the other tables
        sql1 = """DELETE
                  FROM student_subjects
                  WHERE subject_code = ?"""
        sql2 = """DELETE
                FROM teacher_subjects
                WHERE subject_code = ?"""
        sql3 = """DELETE
                 FROM subjects
                 WHERE subject_code = ?"""
        sql4 = """DELETE
                  FROM marks
                  WHERE subject_code = ?"""
        
        cur.execute(sql1, (subject_code, ))
        conn.commit()
        cur.execute(sql2, (subject_code, ))
        conn.commit()
        cur.execute(sql3, (subject_code, ))
        conn.commit()
        cur.execute(sql4, (subject_code, ))
        conn.commit()
        cur.close()

def delete_teacher(conn: Connection, teacher_id: str, headmaster: Headmaster):

    if type(headmaster) == Headmaster:
        cur = conn.cursor()
        #first we delete all subjects that are taught by the teacher
        sql1 = """DELETE
                  FROM teacher_subjects
                  WHERE teacher_id = ?
                  """
        cur.execute(sql1, (teacher_id, ))
        conn.commit()

        sql2 = """DELETE
                 FROM teachers
                 WHERE teacher_id = ?"""
        cur.execute(sql2, (teacher_id, ))
        conn.commit()
        cur.close()

def view_student_info(conn: Connection, student_id: str, person):

    if (type(person) == Student or Teacher or Headmaster):
        cur = conn.cursor()
        #first I want to get the subjects the student is taking
        sql1 = """SELECT s.subject_name, s.subject_code, s.subject_year, s.credits_worth
                  FROM 
                    student_subjects AS ss
                    JOIN subjects AS s
                    ON ss.subject_code = s.subject_code
                  WHERE ss.student_id = ? 
                  """
        
        cur.execute(sql1, (student_id, ))
        rows1 = cur.fetchall()

        subject_list = []
        subject_list_codes = []
        for i in rows1:
            subject = Subject(*i)
            subject_list.append(subject)
            subject_list_codes.append(subject.code)

        for i in subject_list:
            print(i)
        #now extract the marks the student got
        sql2 = """SELECT subject_code, mark
                  FROM marks
                  WHERE student_id = ?"""
        
        cur.execute(sql2, (student_id, ))
        rows2 = cur.fetchall()

        #i make a dictionary because I am not sure if the marks will be inserted in the order I want
        mark_list = {}
        for i in rows2:
            s_code, mark = i
            mark_list[s_code] = mark

        #now I need to make a list with the corresponding order
        mark_arr = [0] * len(mark_list)

        for i in mark_list:
            mark_arr[subject_list_codes.index(i)] = mark_list[i]

        print(mark_arr)


        sql3 = """SELECT  name, age, address, email, student_id, password, current_year
                 FROM students
                 WHERE student_id = ?
                 """
        
        cur.execute(sql3, (student_id,))
        conn.commit()

        row = cur.fetchall()

        #current_student = Student(*row)

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

def insert_student_marks(conn: Connection, student: Student, teacher): 

    if (type(teacher) == Teacher or Headmaster):
        mark_list = student.marks_list
        subject = student.subjects
        cur = conn.cursor()
        for i in range(0, len(mark_list)):
            sql = """INSERT INTO marks(student_id, subject_code, mark)
                     VALUES(?, ?, ?)"""
            
            cur.execute(sql, (student.id, subject[i].code , mark_list[i]))
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
                                            subject_year integer NOT NULL,
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
    
    sql_create_student_subjects_table = """CREATE TABLE IF NOT EXISTS student_subjects(
                                            student_id text,
                                            subject_code text,

                                            PRIMARY KEY(student_id, subject_code),
                                            FOREIGN KEY(student_id) REFERENCES students(student_id)
                                );"""
    
    sql_create_student_mark_table = """CREATE TABLE IF NOT EXISTS marks(
                                            student_id text,
                                            subject_code text,
                                            mark REAL,

                                            PRIMARY KEY(student_id, subject_code, mark)
                                            FOREIGN KEY(student_id) REFERENCES students(student_id)
                                );"""
    
    
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_teachers_table)
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_subjects_table)
        create_table(conn, sql_create_teacher_subjects_table)
        create_table(conn, sql_create_student_subjects_table)
        create_table(conn, sql_create_student_mark_table)
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
        #delete_student(conn, "100000323", racu)
        #delete_teacher(conn, "100101001", racu)
        #delete_subject(conn, "CS4016", racu)
        #for i in raul.subjects:
            #insert_subject(conn, i, racu)
        view_student_info(conn, "100000323", raul)
        #view_all_teachers(conn, derek)
        #insert_teacher_subjects(conn, derek.subjects_taught, derek)
        #insert_student_subjects(conn, raul, racu)


        
    conn.close()



