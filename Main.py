from re import match
from Student import Student
from Subject import Subject
from Teacher import Teacher
from Headmaster import Headmaster

import Sqlite
import sqlite3

def main():
    

    database_file = r"C:\Users\raula\Desktop\facultate\anul 2 sem 1\Intermediate programming\Assignment\UniversitySystem\University.sqlite"
    
    conn = Sqlite.create_connection(database_file)
    
    #uncomment this only if you want to initialize a different database
    #Sqlite.intialize_DB(conn, database_file)

    user_log_in(conn)

    conn.close()

def user_log_in(conn: sqlite3.Connection):

    print("Hello! What are you logging in as ? \n1. Headmaster\n2. Teacher\n3. Student")
    nr = input("Please select a number: ")
    
    match int(nr):

        case 1:
                id = input("Please enter your id: ")
                password = input("Please enter your password: ")
                headmaster = Sqlite.logIn_as_headmaster(conn,id, password)

        case 2:
                id = input("Please enter your id: ")
                password = input("Please enter your password")
        case 3:
                id = input("Please enter your id: ")
                password = input("Please enter your password")
        case _:
            print("This is not permitted! Access Denied!")






if __name__ == "__main__":
    main()


