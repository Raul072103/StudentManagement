import sqlite3
from sqlite3 import Connection, Error

from zmq import Flag

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
        insert_teacher_subjects(conn, teacher, headmaster)
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

        #raise exceptions
        if rows1 == None:
            raise ValueError

        subject_list = []
        subject_list_codes = []
        for i in rows1:
            subject = Subject(*i)
            subject_list.append(subject)
            subject_list_codes.append(subject.code)


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


        #print(mark_list)


        sql3 = """SELECT  name, age, address, email, student_id, password, current_year
                 FROM students
                 WHERE student_id = ?
                 """
        
        cur.execute(sql3, (student_id,))
        conn.commit()

        row = cur.fetchall()
        
        #print(row)

        (name, age, address, email, student_id2, password, current_year) = row[0]

        current_student = Student(name, age, address, email, student_id2, password, current_year, mark_list)

        print(current_student)

        cur.close()

def view_teacher_info(conn: Connection, teacher_id: str, teacher):

    if (type(teacher) == Teacher or Headmaster):
        cur = conn.cursor()

        sql1 = """SELECT subject_name, subject_code, subject_year, credits_worth
                  FROM subjects 
                  WHERE subject_code IN 
                  (
                    SELECT subject_code
                    FROM teacher_subjects
                    WHERE teacher_id = ?
                  ) """
        
        sql2 = """SELECT  name, age, address, email, teacher_id, password
                 FROM teachers
                 WHERE teacher_id = ?
                 """
        
        cur.execute(sql1, (teacher_id, ))
        conn.commit()

        rows1 = cur.fetchall()
        subject_list = []

        for row in rows1:
            (name, code, year, credits) = row
            temp_subject = Subject(name, code, year, credits)
            subject_list.append(temp_subject)

        cur.execute(sql2, (teacher_id,))
        conn.commit()

        row2 = cur.fetchall()

        (name, age, address, email, id, password) = row2[0]
        temp_teacher = Teacher(name, age, address, email, id, password, subject_list)
        print(temp_teacher)

        cur.close()

def view_all_students(conn: Connection, teacher):

    if (type(teacher) == Teacher or Headmaster):
        sql = """SELECT student_id, name, age, email, address,current_year
                 FROM students;
                 """
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        rows = cur.fetchall()

        for row in rows:
            (id, name, age, email, address, current_year) = row
            print("name = %s, id = %s, age = %d, email = %s, address = %s, current_year = %d" %(id, name, age, email, address, current_year))

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

def view_all_subjects(conn: Connection):

    sql = """SELECT subject_name, subject_code, subject_year, credits_worth
            FROM subjects;"""
    
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    rows = cur.fetchall()

    for row in rows:
        (name, code, year, credits) = row
        curr_subject = Subject(name, code, year, credits)
        print(curr_subject)

    cur.close()

def insert_teacher_subjects(conn: Connection, teacher , responsiblePerson):

    if (type(teacher) == Teacher or Headmaster):
        
        sql = """INSERT INTO teacher_subjects(teacher_id, subject_code)
                 VALUES(?, ?)"""
        cur = conn.cursor()
        
        subjects = teacher.subjects_taught
        for i in range(0, len(subjects)):
            
            cur.execute(sql, (teacher.id, subjects[i].code))
            conn.commit()

        cur.close()

def insert_student_subjects(conn: Connection, student: Student ,teacher):

    if (type(teacher) == Teacher or Headmaster):
        
        sql = """INSERT INTO student_subjects(student_id, subject_code)
                 VALUES(?, ?)"""
        cur = conn.cursor()
        
        subjects = student.subjects()

        for i in subjects:
            
            cur.execute(sql, (student.id, i))
            conn.commit()

        cur.close()        

def insert_student_marks(conn: Connection, student: Student, teacher): 

    if (type(teacher) == Teacher or Headmaster):
        mark_list = student.marks_list()
        subject = student.subjects()
        cur = conn.cursor()
        for i in range(0, len(mark_list)):
            sql = """INSERT INTO marks(student_id, subject_code, mark)
                     VALUES(?, ?, ?)"""
            
            cur.execute(sql, (student.id, subject[i] , mark_list[i]))
            conn.commit()

        cur.close()

def get_headMaster_from_DB(conn: Connection, teacher_id):

    cur = conn.cursor()

    sql1 = """SELECT ts.subject_code
                  FROM teacher_subjects AS ts
                    JOIN teachers as t
                    ON t.teacher_id = ts.teacher_id
                  WHERE t.teacher_id = ?;"""
    sql2 = """SELECT subject_code, subject_name, subject_year, credits_worth
                  FROM subjects
                  WHERE subject_code = ? ;"""

    sql3 = """SELECT  name, age, address, email, teacher_id, password
                 FROM teachers
                 WHERE teacher_id = ? ;"""
    cur.execute(sql1, (teacher_id, ))
    conn.commit()

    rows1 = cur.fetchall()
    subject_list = []

    for code in rows1:
        cur.execute(sql2, (*code, ))
        conn.commit()

        temp_row = cur.fetchall()
        subject_list.append(temp_row)

    cur.execute(sql3, (teacher_id, ))
    conn.commit()
    rows1 = cur.fetchall()

    (name, age, address, email, id, password) = rows1[0]
    temp_headmaster = Headmaster(name, age, address, email, id, password, subject_list)
    cur.close()       
    return temp_headmaster


def logIn_as_headmaster(conn: Connection, id, password):

    cur = conn.cursor()
    sql = """SELECT teacher_id, password
             FROM teachers
             WHERE teacher_id = ?;"""
    cur.execute(sql, (id, ))
    conn.commit()

    row = cur.fetchall()

    if len(row) == 0:
        print("Wrong id or password! Access Denied!")
        cur.close()
        exit()
    else:
        (correct_id, correct_password) = row[0]
        if id == correct_id and correct_password == password:
            curr_headmaster = get_headMaster_from_DB(conn, id)
            print("Login successfull")
        else:
            print("Wrong id or password! Access Denied!")
            cur.close()
            exit()

    cur.close()
    #print(type(curr_headmaster), '\n', curr_headmaster)
    return curr_headmaster


def get_teacher_from_DB(conn: Connection, teacher_id):

    cur = conn.cursor()

    sql1 = """SELECT ts.subject_code
                  FROM teacher_subjects AS ts
                    JOIN teachers as t
                    ON t.teacher_id = ts.teacher_id
                  WHERE t.teacher_id = ?;"""
    sql2 = """SELECT subject_code, subject_name, subject_year, credits_worth
                  FROM subjects
                  WHERE subject_code = ? ;"""

    sql3 = """SELECT  name, age, address, email, teacher_id, password
                 FROM teachers
                 WHERE teacher_id = ? ;"""
    cur.execute(sql1, (teacher_id, ))
    conn.commit()

    rows1 = cur.fetchall()
    subject_list = []

    for code in rows1:
        cur.execute(sql2, (*code, ))
        conn.commit()

        temp_row = cur.fetchall()
        subject_list.append(temp_row)

    cur.execute(sql3, (teacher_id, ))
    conn.commit()
    rows1 = cur.fetchall()

    (name, age, address, email, id, password) = rows1[0]
    temp_teacher = Teacher(name, age, address, email, id, password, subject_list)
    cur.close()       
    return temp_teacher


def logIn_as_teacher(conn: Connection, id, password):

    cur = conn.cursor()
    sql = """SELECT teacher_id, password
             FROM teachers
             WHERE teacher_id = ?;"""
    cur.execute(sql, (id, ))
    conn.commit()

    row = cur.fetchall()

    if len(row) == 0:
        print("Wrong id or password! Access Denied!")
        cur.close()
        exit()
    else:
        (correct_id, correct_password) = row[0]
        if id == correct_id and correct_password == password:
            curr_teacher = get_teacher_from_DB(conn, id)
            print("Login successfull")
        else:
            print("Wrong id or password! Access Denied!")
            cur.close()
            exit()

    cur.close()
    return curr_teacher


def get_student_from_DB(conn: Connection, student_id):

    cur = conn.cursor()

    sql1 = """SELECT m.subject_code, m.mark
                  FROM marks AS m
                    JOIN students as s
                    ON s.student_id = m.student_id
                  WHERE s.student_id = ?;"""

    sql2 = """SELECT  name, age, address, email, student_id, password, current_year
                 FROM students
                 WHERE student_id = ? ;"""
    
    cur.execute(sql1, (student_id, ))
    conn.commit()

    rows1 = cur.fetchall()

    subject_mark = {}

    for row in rows1:
        (temp_code, temp_mark) = row
        subject_mark[temp_code] = temp_mark

    cur.execute(sql2, (student_id, ))
    conn.commit()
    rows2 = cur.fetchall()

    (name, age, address, email, id, password, current_year) = rows2[0]
    temp_student = Student(name, age, address, email, id, password, current_year, subject_mark)
    cur.close()       
    return temp_student


def logIn_as_student(conn: Connection, id, password):

    cur = conn.cursor()
    sql = """SELECT student_id, password
             FROM students
             WHERE student_id = ?;"""
    cur.execute(sql, (id, ))
    conn.commit()

    row = cur.fetchall()

    if len(row) == 0:
        print("Wrong id or password! Access Denied!")
        cur.close()
        exit()
    else:
        (correct_id, correct_password) = row[0]
        if id == correct_id and correct_password == password:
            curr_student = get_student_from_DB(conn, id)
            print("Login successfull")
        else:
            print("Wrong id or password! Access Denied!")
            cur.close()
            exit()

    cur.close()
    return curr_student


#give marks to the students you are teaching at
def give_marks(conn: Connection, teacher):

    if (type(teacher) == Teacher or Headmaster):
        
        print(teacher.subjects_taught)
        subject_code_mark = input("Enter the subject you would like to mark: ")

        print("All the students taking that subject are: ")
        sql = """SELECT student_id
                 FROM marks
                 WHERE subject_code = ?; """
        cur = conn.cursor()
        cur.execute(sql, (subject_code_mark, ))
        conn.commit()
        
        rows = cur.fetchall()

        if rows == None:
            raise ValueError

        for row in rows:
            print(row)
        
        student_id = input("The student you want to grade is: ")
        mark = input("The mark you want to give is: ")

        sql2 = """UPDATE marks
                  SET mark = ?
                  WHERE student_id = ? AND subject_code = ?; """
        
        cur.execute(sql2, (mark, student_id, subject_code_mark))
        conn.commit()

        cur.close()

def get_subject_from_DB(conn: Connection, subject_code):

    sql = """SELECT subject_name, subject_year, credits_worth
             FROM subjects
             WHERE subject_code = ?; """

    cur = conn.cursor()
    cur.execute(sql, (subject_code, ))
    conn.commit()
    
    row = cur.fetchall()

    (name, year, credits) = row[0]
    curr_subject = Subject(name, subject_code, year, credits)
    cur.close()

    return curr_subject




def create_tables(conn: Connection, database):

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
    
    
    #conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_teachers_table)
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_subjects_table)
        create_table(conn, sql_create_teacher_subjects_table)
        create_table(conn, sql_create_student_subjects_table)
        create_table(conn, sql_create_student_mark_table)
    else:
        print("Error! Cannot create the database connection")
    
    #return conn

class Singleton:
    _instance = None


    def __new__(cls, database_file):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(database_file)
            intialize_DB(cls._instance.conn, database_file)

        return cls._instance
    
    def get_connection(self):
        return self.conn
    
    
    

def intialize_DB(conn, database):
    #database = r"C:\Users\raula\Desktop\facultate\anul 2 sem 1\Intermediate programming\Assignment\UniversitySystem\University.sqlite"

    #db_instance = Singleton(database)

    #conn = db_instance.get_connection

    create_tables(conn, database)

    #first year subjects
    subject11 = Subject("Introduction to Relational Databases", "CS1106", 1, 5)
    subject12 = Subject("Computer Hardware Organisation", "CS1110", 1, 5)
    subject13 = Subject("Systems Organisation", "CS1111", 1, 5)
    subject14 = Subject("Foundations of Computer Science I", "CS1112", 1, 5)
    subject15 = Subject("Foundations of Computer Science II", "CS1113", 1, 5)
    subject16 = Subject("Web Development I", "CS1116", 1, 5)
    subject17 = Subject("Web Development II", "CS1117", 1, 5)
    subject18 = Subject("Introduction to Programming", "CS1118", 1, 5)
    first_year_subjects = [subject11, subject12, subject13, subject14, subject15, subject16, subject17, subject18]

    #second year subjects
    subject21 = Subject("Information Storage and Management I", "CS2208", 2, 5)
    subject22 = Subject("Information Storage and Management II", "CS2209", 2, 5)
    subject23 = Subject("Operating Systems 1", "CS2503", 2, 5)
    subject24 = Subject("Network Computing", "CS2505", 2, 5)
    subject25 = Subject("Operating Systems II", "CS2506", 2, 5)
    subject26 = Subject("Computer Architecture", "CS2507", 2, 5)
    subject27 = Subject("Intermediate Programming", "CS2513", 2, 5)
    subject28 = Subject("Introduction to Java", "CS2514", 2, 5)
    second_year_subjects = [subject21, subject22, subject23, subject24, subject25, subject26, subject27, subject28]

    #third year subjects
    subject31 = Subject("Advanced Programming with Java", "CS3318", 3, 5)
    subject32 = Subject("Software Engineering", "CS3500", 3, 5)
    subject33 = Subject("Cloud Infrastructure and Services", "CS3204", 3, 5)
    subject34 = Subject("Networks and Data Communications", "CS3509", 3, 5)
    subject35 = Subject("Ethical Hacking and Web Security", "CS3511", 3, 5)
    subject36 = Subject("C-Programming for Microcontrollers", "CS3514", 3, 5)
    third_year_subjects = [subject31, subject32, subject33, subject34, subject35, subject36]

    #fourth year subjects
    subject41 = Subject("Special Topics in Computing I", "CS4092", 4, 5)
    subject42 = Subject("Special Topics in Computing II", "CS4093", 4, 5)
    subject43 = Subject("Principles of Compilation", "CS4150", 4, 5)
    subject44 = Subject("Parallel and Grid Computing", "CS4402", 4, 5)
    subject45 = Subject("Multimedia Compression and Delivery", "CS4405", 4, 5)
    subject46 = Subject("Artificial Intelligence I", "CS4618", 4, 5)
    subject47 = Subject("Artificial Intelligence II", "CS4619", 4, 5)
    subject48 = Subject("Algorithm Analysis", "CS4407", 4, 5)
    fourth_year_subjects = [subject41, subject42, subject43, subject44, subject45, subject46, subject47, subject48]

    #teachers
    teacher1 = Teacher("Cathal Francis Hoare", 1, "Cork", "cathal.francis.hoare@ucc.ie", "100000001", "MasterOfOOP", [subject21, subject22, subject23, subject24, subject25, subject26, subject27, subject28])
    teacher2 = Teacher("Derek Bridge", 1, "Cork", "derekbridge@ucc.ie", "100000002", "TheFinalBoss", [subject41, subject42, subject43, subject44, subject45, subject46, subject47, subject48])
    teacher3 = Teacher("Gregory Provan", 50, "Cork", "derekbridge@ucc.ie", "100101003", "AlgorithmAnalyzer", [subject31, subject32, subject33, subject34, subject35, subject36])

    #headmaster
    headmaster = Headmaster("The BOSS", 1, "Cork", "the.Boss@ucc.ie", "100000000", "IamTheBOSS", [subject11, subject12, subject13])

    #students
    student1 = Student("Spatariu Raul", 20, "Fagaras", "raulandrei2019@gmail.com", "200000001",
                "superSecretPassword", 2, {subject21.code: 0.0, subject22.code: 0.0, subject23.code: 0.0, subject24.code: 0.0, subject25.code: 0.0, subject26.code: 0.0, subject27.code: 0.0, subject28.code: 0.0})
    student2 = Student("Spatariu Alin", 21, "Fagaras", "raul.is.the.best@gmail.com", "200000002",
                       "anotherSecretPassword", 3, {subject31.code: 0.0, subject32.code: 0.0, subject33.code: 0.0, subject34.code: 0.0, subject35.code: 0.0, subject36.code: 0.0})
    student3 = Student("Mircea Mihai", 22, "Fagaras", "mircea.mihai@gmail.com", "200000003",
                       "anotherOtherSecretPassword", 4, {subject41.code: 0.0, subject42.code: 0.0, subject43.code: 0.0, subject44.code: 0.0, subject45.code: 0.0, subject46.code: 0.0, subject47.code: 0.0, subject48.code: 0.0})
    student4 = Student("Ganea David", 19, "Fagaras", "ganea.david@gmail.com", "200000004",
                       "anotherOtherAnotherSecretPassword", 1, {subject11.code: 0.0, subject12.code: 0.0, subject13.code: 0.0, subject14.code: 0.0, subject15.code: 0.0, subject16.code: 0.0, subject17.code: 0.0, subject18.code: 0.0})

    whole_subject_lists = [first_year_subjects, second_year_subjects, third_year_subjects, fourth_year_subjects]

    teacher_list = [headmaster, teacher1, teacher2, teacher3]

    student_list = [student1, student2, student3, student4]

    #insert all the subjects
    #for subject_list in whole_subject_lists:
    #    for subject in subject_list:
    #        insert_subject(conn, subject, headmaster)

    #insert all the teachers
    for teacher in teacher_list:
        insert_teacher(conn, teacher, headmaster)

    #insert all students
    for student in student_list:
        insert_student(conn, student, headmaster)
    


if __name__ == '__main__':

    database_file = r"C:\Users\raula\Desktop\facultate\anul 2 sem 1\Intermediate programming\Assignment\UniversitySystem\University.sqlite"
    
    conn = create_connection(database_file)

    #first year subjects
    subject11 = Subject("Introduction to Relational Databases", "CS1106", 1, 5)
    subject12 = Subject("Computer Hardware Organisation", "CS1110", 1, 5)
    subject13 = Subject("Systems Organisation", "CS1111", 1, 5)
    subject14 = Subject("Foundations of Computer Science I", "CS1112", 1, 5)
    subject15 = Subject("Foundations of Computer Science II", "CS1113", 1, 5)
    subject16 = Subject("Web Development I", "CS1116", 1, 5)
    subject17 = Subject("Web Development II", "CS1117", 1, 5)
    subject18 = Subject("Introduction to Programming", "CS1118", 1, 5)
    first_year_subjects = [subject11, subject12, subject13, subject14, subject15, subject16, subject17, subject18]

    #second year subjects
    subject21 = Subject("Information Storage and Management I", "CS2208", 2, 5)
    subject22 = Subject("Information Storage and Management II", "CS2209", 2, 5)
    subject23 = Subject("Operating Systems 1", "CS2503", 2, 5)
    subject24 = Subject("Network Computing", "CS2505", 2, 5)
    subject25 = Subject("Operating Systems II", "CS2506", 2, 5)
    subject26 = Subject("Computer Architecture", "CS2507", 2, 5)
    subject27 = Subject("Intermediate Programming", "CS2513", 2, 5)
    subject28 = Subject("Introduction to Java", "CS2514", 2, 5)
    second_year_subjects = [subject21, subject22, subject23, subject24, subject25, subject26, subject27, subject28]

    #third year subjects
    subject31 = Subject("Advanced Programming with Java", "CS3318", 3, 5)
    subject32 = Subject("Software Engineering", "CS3500", 3, 5)
    subject33 = Subject("Cloud Infrastructure and Services", "CS3204", 3, 5)
    subject34 = Subject("Networks and Data Communications", "CS3509", 3, 5)
    subject35 = Subject("Ethical Hacking and Web Security", "CS3511", 3, 5)
    subject36 = Subject("C-Programming for Microcontrollers", "CS3514", 3, 5)
    third_year_subjects = [subject31, subject32, subject33, subject34, subject35, subject36]

    #fourth year subjects
    subject41 = Subject("Special Topics in Computing I", "CS4092", 4, 5)
    subject42 = Subject("Special Topics in Computing II", "CS4093", 4, 5)
    subject43 = Subject("Principles of Compilation", "CS4150", 4, 5)
    subject44 = Subject("Parallel and Grid Computing", "CS4402", 4, 5)
    subject45 = Subject("Multimedia Compression and Delivery", "CS4405", 4, 5)
    subject46 = Subject("Artificial Intelligence I", "CS4618", 4, 5)
    subject47 = Subject("Artificial Intelligence II", "CS4619", 4, 5)
    subject48 = Subject("Algorithm Analysis", "CS4407", 4, 5)
    fourth_year_subjects = [subject41, subject42, subject43, subject44, subject45, subject46, subject47, subject48]

      #teachers
    teacher1 = Teacher("Cathal Francis Hoare", 1, "Cork", "cathal.francis.hoare@ucc.ie", "100000001", "MasterOfOOP", [subject21, subject22, subject23, subject24, subject25, subject26, subject27, subject28])
    teacher2 = Teacher("Derek Bridge", 1, "Cork", "derekbridge@ucc.ie", "100000002", "TheFinalBoss", [subject41, subject42, subject43, subject44, subject45, subject46, subject47, subject48])
    teacher3 = Teacher("Gregory Provan", 50, "Cork", "derekbridge@ucc.ie", "100101003", "AlgorithmAnalyzer", [subject31, subject32, subject33, subject34, subject35, subject36])

    #headmaster
    headmaster = Headmaster("The BOSS", 1, "Cork", "the.Boss@ucc.ie", "100000000", "IamTheBOSS", [subject11, subject12, subject13])

    teacher_list = [headmaster, teacher1, teacher2, teacher3, headmaster]

    
    for teacher in teacher_list:
        insert_teacher(conn, teacher, headmaster)

    conn.close()
    
    