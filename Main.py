from Student import Student
from Subject import Subject
from Teacher import Teacher
from Headmaster import Headmaster

import Sqlite

def main():
    print("alo")

    database_file = r"C:\Users\raula\Desktop\facultate\anul 2 sem 1\Intermediate programming\Assignment\UniversitySystem\University.sqlite"
    
    conn = Sqlite.create_connection(database_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM teachers")
    conn.commit()
    cur.execute("DELETE FROM students")
    conn.commit()
    cur.execute("DELETE FROM teacher_subjects")
    conn.commit()
    cur.execute("DELETE FROM student_subjects")
    conn.commit()
    cur.execute("DELETE FROM marks")
    conn.commit()
    cur.close()
    Sqlite.intialize_DB(conn, database_file)

    conn.close()

    print("alo")

if __name__ == "__main__":
    main()


