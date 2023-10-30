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

                exit_option = False

                while(exit_option != True):
                    headmaster.print_options()
                    option = input("Select an option: ")

                    match int(option):
                        # 1. view_students = view_all students
                        case 1:
                                Sqlite.view_all_students(conn, headmaster)
                        # 2. view info about a student = view_student_info
                        case 2:
                                student_id = input("Enter student's id: ")

                                try:
                                    Sqlite.view_student_info(conn, student_id, headmaster)
                                except ValueError:
                                    print("You have entered a wrong student id")
                        # 3. give marks to students that are taking your subjects
                        case 3:
                                try:
                                    Sqlite.give_marks(conn, headmaster)
                                except ValueError:
                                    print("You have entered a wrong subject code")
                        # 4. delete a student
                        case 4:
                                student_id = input("The student ID of the student you want to delete is: ")
                                Sqlite.delete_student(conn, student_id, headmaster)
                        # 5. insert a student
                        case 5:
                                name = input("Enter the name of the student: ")
                                age = int(input("Enter the age of the student: "))
                                address = input("Enter the address: ")
                                email = input("Enter the email: ")
                                id = input("Enter the student_id: ")
                                password = input("Enter the password: ")
                                current_year = input("Enter the current_year: ")
                                subject_codes_list = input("Enter the code of the subjects the student is taking separated by space\n ")
                                subject_codes_list = subject_codes_list.split(' ')

                                subject_dictionary = {}
                                for subject in subject_codes_list:
                                    subject_dictionary[subject] = 0.0

                                student_inserted = Student(name, age, address, email, id, 
                                                        password, current_year, subject_dictionary)
                                
                                Sqlite.insert_student(conn, student_inserted, headmaster)
                            # 6. view all teachers
                        case 6:
                            Sqlite.view_all_teachers(conn, headmaster)
                            # 7. view teacher info
                        case 7:
                            teacher_id = input("Enter teacher's id: ")
                            Sqlite.view_teacher_info(conn, teacher_id, headmaster)
                        # 8. delete teacher
                        case 8:
                            teacher_id = input("Enter the id of the teacher you want to delete: ")
                            Sqlite.delete_teacher(conn, teacher_id, headmaster)
                        # 9. insert teacher
                        case 9:
                            name = input("Enter the name of the teacher: ")
                            age = int(input("Enter the age of the teacher: "))
                            address = input("Enter the address: ")
                            email = input("Enter the email: ")
                            id = input("Enter the teacher_id: ")
                            password = input("Enter the password: ")
                            subject_codes_list = input("Enter the code of the subjects, separated by a sapce,  that will be taught by the teacher:\n ")
                            subject_codes_list = subject_codes_list.split(' ')

                            subject_list = []

                            for subject_code in subject_codes_list:
                                curr_subject = Sqlite.get_subject_from_DB(conn, subject_code)
                                subject_list.append(curr_subject)

                            teacher_inserted = Teacher(name, age, address, email, id, 
                                                        password, subject_list)
                                
                            Sqlite.insert_student(conn, student_inserted, headmaster) 
                        # 10. view all subjects
                        case 10:
                            print("Here is the list with all the subjects: ")
                            Sqlite.view_all_subjects(conn)
                        # 11. delete a subject
                        case 11:
                            code = input("Enter the code of the subject you want to delete: ")
                            Sqlite.delete_subject(conn, code, headmaster)
                        # 12. insert a subject          
                        case 12:
                            name = input("Enter the name of the subject you want to insert: ")
                            code = input("Enter the name of the code of the subject you want to insert: ")
                            year = int(input("Enter the year in which the subject is taught: "))
                            credits_worth = int(input("Enter how many credits is the subject worth: "))
                            temp_subject = Subject(name, code, year, credits_worth)
                            Sqlite.insert_subject(conn, temp_subject, headmaster)
                        # 13. exit
                        case 13:
                              exit("You have exited the program")
                        case _:
                              print("This is not accepted please exit or try again")

                    print("If you want to exit the program please enter Yes, othewise enter No")
                    current_exit_option = input()
                    if current_exit_option.lower() == "yes":
                         exit_option = True
                    else:
                         exit_option = False


        case 2:
                id = input("Please enter your id: ")
                password = input("Please enter your password: ")
                teacher = Sqlite.logIn_as_teacher(conn,id, password)

                exit_option = False

                while(exit_option != True):
                    teacher.print_options()
                    option = input("Select an option: ")

                    match int(option):
                        # 1. view_students = view_all students
                        case 1:
                                Sqlite.view_all_students(conn, teacher)
                        # 2. view info about a student = view_student_info
                        case 2:
                                student_id = input("Enter student's id: ")

                                try:
                                    Sqlite.view_student_info(conn, student_id, teacher)
                                except ValueError:
                                    print("You have entered a wrong student id")
                        # 3. view all teachers
                        case 3:
                            Sqlite.view_all_teachers(conn, teacher)    
                        # 4. view this teacher infromation 
                        case 4:
                            Sqlite.view_teacher_info(conn, teacher.id, teacher)    
                        # 5. view all subjects
                        case 5:
                            print("Here is the list with all the subjects: ")
                            Sqlite.view_all_subjects(conn)            
                        # 6. give marks to students that are taking your subjects
                        case 6:
                                try:
                                    Sqlite.give_marks(conn, teacher)
                                except ValueError:
                                    print("You have entered a wrong subject code")
                        # 7. exit
                        case 7:
                              exit("You have exited the program")
                        case _:
                              print("This is not accepted please exit or try again")

                    print("If you want to exit the program please enter Yes, othewise enter No")
                    current_exit_option = input()
                    if current_exit_option.lower() == "yes":
                         exit_option = True
                    else:
                         exit_option = False


        case 3:
                id = input("Please enter your id: ")
                password = input("Please enter your password: ")
                student = Sqlite.logIn_as_student(conn,id, password)

                exit_option = False

                while(exit_option != True):
                    student.print_options()
                    option = input("Select an option: ")

                    match int(option):
                        # 1. display my infromation
                        case 1:
                             Sqlite.view_student_info(conn, student.id, student)
                        # 2. print my total number of credits
                        case 2:
                             print("The total number of credits is: %d" %(student.get_total_credits() ))
                        # 3. view all subjects
                        case 3:
                            print("Here is the list with all the subjects: ")
                            Sqlite.view_all_subjects(conn)            
                        # 4. exit
                        case 4:
                              exit("You have exited the program")
                        case _:
                              print("This is not accepted please exit or try again")

                    print("If you want to exit the program please enter Yes, othewise enter No")
                    current_exit_option = input()
                    if current_exit_option.lower() == "yes":
                         exit_option = True
                    else:
                         exit_option = False

        case _:
            print("This is not permitted! Access Denied!")






if __name__ == "__main__":
    main()


