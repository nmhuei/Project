from datetime import datetime
import numpy as np
import math, curses

class Student:
    def __init__(self, id, name, dob):
        self.__id = id
        self.__name = name
        self.__dob = dob
        self.__gpa = 0.0

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob
    
    def get_gpa(self):
        return self.__gpa

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_dob(self, dob):
        self.__dob = dob
        
    def set_gpa(self, gpa):
        self.__gpa = gpa


class Course:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name


class Mark:
    def __init__(self, cid, sid, mark, credit):
        self.__cid = cid
        self.__sid = sid
        self.__mark = math.floor(mark * 10) / 10
        self.__credit = credit

    def get_cid(self):
        return self.__cid

    def get_sid(self):
        return self.__sid

    def get_mark(self):
        return self.__mark
    
    def get_credit(self):
        return self.__credit

    def set_cid(self, cid):
        self.__cid = cid

    def set_sid(self, sid):
        self.__sid = sid

    def set_mark(self, mark):
        self.__mark = math.floor(mark * 10) / 10
        
    def set_credit(self, credit):
        self.__credit = credit


class InputSystem:
    def __init__(self):
        self.__courses = []   # list[Course]
        self.__students = []  # list[Student]
        self.__marks = []     # list[Mark]

    def get_courses(self):
        return self.__courses

    def get_students(self):
        return self.__students

    def get_marks(self):
        return self.__marks

    # ===== INPUT STUDENT LIST =====

    def isValidStudentName(self, name: str) -> bool:
        return len(name.strip()) > 0

    def isValidStudentId(self, id: str) -> bool:
        return len(id.strip()) > 0

    def isValidStudentDob(self, dob: str) -> bool:
        try:
            datetime.strptime(dob, "%d/%m/%y")
            return True
        except ValueError:
            return False

    def inputValidStudent(self) -> Student:
        print("Student : ")

        id = input("     - ID : ")
        while not self.isValidStudentId(id):
            print("     - Invalid Student ID.")
            id = input("     - ID : ")

        name = input("     - Name : ")
        while not self.isValidStudentName(name):
            print("     - Invalid Student Name.")
            name = input("     - Name : ")

        dob = input("     - DoB (DD/MM/YY): ")
        while not self.isValidStudentDob(dob):
            print("     - Invalid Student DoB.")
            dob = input("     - DoB (DD/MM/YY): ")

        return Student(id, name, dob)

    def inputStudent(self) -> None:
        student = self.inputValidStudent()
        self.__students.append(student)

    def inputStudentList(self) -> None:
        while True:
            raw = input("Input number of students in a class : ")
            raw = raw.strip()
            if not raw:
                print("Please enter a number.")
                continue
            try:
                n = int(raw)
            except ValueError:
                print("Invalid input. Please enter a valid integer number.")
                continue

            if n <= 0:
                print("Invalid number! Must be > 0.")
                continue
            break

        for _ in range(n):
            self.inputStudent()

    # ===== INPUT COURSE LIST =====

    def isValidCourseName(self, name: str) -> bool:
        return len(name.strip()) > 0

    def isValidCourseId(self, id: str) -> bool:
        return len(id.strip()) > 0

    def inputValidCourse(self) -> Course:
        print("Course : ")

        id = input("     - ID : ")
        while not self.isValidCourseId(id):
            print("     - Invalid Course ID.")
            id = input("     - ID : ")

        name = input("     - Name : ")
        while not self.isValidCourseName(name):
            print("     - Invalid Course Name.")
            name = input("     - Name : ")

        return Course(id, name)

    def inputCourse(self) -> None:
        course = self.inputValidCourse()
        self.__courses.append(course)

    def inputCourseList(self) -> None:
        while True:
            raw = input("Input number of courses in a class : ")
            raw = raw.strip()
            if not raw:
                print("Please enter a number.")
                continue
            try:
                n = int(raw)
            except ValueError:
                print("Invalid input. Please enter a valid integer number.")
                continue

            if n <= 0:
                print("Invalid number! Must be > 0.")
                continue
            break

        for _ in range(n):
            self.inputCourse()

    def haveCourseId(self, cid: str) -> bool:
        return any(cid == course.get_id() for course in self.__courses)

    # Select a course, input marks for students in this course

    def chooseCourse(self) -> str:
        print("\n ===== COURSE LIST ======")
        for i, course in enumerate(self.__courses):
            print(f"{i + 1}. {course.get_id()} - {course.get_name()}")

        while True:
            raw = input("Choose index of course : ")
            raw = raw.strip()
            if not raw:
                print("Please enter a number.")
                continue
            try:
                n = int(raw)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if 1 <= n <= len(self.__courses):
                return self.__courses[n - 1].get_id()

            print(f"Index out of range. Please enter a number between 1 and {len(self.__courses)}.")

    def getMark4Student(self, sid: str):
        # Get a valid mark (float)
        while True:
            raw_mark = input(f"   Mark for student {sid} : ")
            raw_mark = raw_mark.strip()
            if not raw_mark:
                print("     - Please enter a mark.")
                continue
            try:
                mark = float(raw_mark)
            except ValueError:
                print("     - Invalid input. Please enter a valid number for mark.")
                continue
            break

        # Get a valid credit (int)
        while True:
            raw_credit = input(f"   Credit for student {sid} : ")
            raw_credit = raw_credit.strip()
            if not raw_credit:
                print("     - Please enter a credit.")
                continue
            try:
                credit = int(raw_credit)
            except ValueError:
                print("     - Invalid input. Please enter a valid integer for credit.")
                continue
            if credit <= 0:
                print("     - Credit must be > 0.")
                continue
            break

        return mark, credit

    def inputMarks4Course(self) -> None:
        cid = self.chooseCourse()
        print(f"\nMark for Course {cid}")

        for stu in self.__students:
            sid = stu.get_id()
            mark_val, credit_val = self.getMark4Student(sid)
            self.__marks.append(Mark(cid, sid, mark_val, credit_val))

    # Input all data
    def inputAll(self) -> None:
        self.inputStudentList()
        self.inputCourseList()
        self.inputMarks4Course()
        

class SystemManagementMark:
    def __init__(self):
        inputSystem = InputSystem()
        inputSystem.inputAll()

        self.courses = inputSystem.get_courses()
        self.students = inputSystem.get_students()
        self.marks = inputSystem.get_marks()
        self.gpas = []

    # ===== Listing functions =====

    def showCourseList(self) -> None:
        print("\n ===== COURSE LIST ======")
        for i, course in enumerate(self.courses):
            print(f"{i + 1}. {course.get_id()} - {course.get_name()}")

    def showStudentList(self) -> None:
        print("\n ===== STUDENT LIST ======")
        for stu in self.students:
            print(f"{stu.get_id():<12} {stu.get_name():<20} {stu.get_dob():<8}")

    def findMark4Student(self, cid: str, sid: str) -> float:
        for mark in self.marks:
            if mark.get_cid() == cid and mark.get_sid() == sid:
                return mark.get_mark()
        return 0.0

    def showMark4Course(self, cid: str) -> None:
        print(f"{cid} :")
        for stu in self.students:
            sid = stu.get_id()
            mark_val = self.findMark4Student(cid, sid)
            print(f"    {sid:<12} {stu.get_name():<20} {mark_val:5.2f}")

    def showMark4AllCourse(self) -> None:
        print("\n ===== MARK LIST =====")
        for course in self.courses:
            cid = course.get_id()
            self.showMark4Course(cid)

    def showGPA(self):
        self.countGPA()
        print("\n ===== GPA =====")
        for stu in self.students:
            print(f"{stu.get_id():<12} {stu.get_name():<20} {stu.get_gpa():5.2f}")

    def showAll(self) -> None:
        self.showCourseList()
        self.showStudentList()
        self.showMark4AllCourse()
        self.showGPA()

    # Count GPA
    def countGPA4Student(self, sid):
        marks_val = []
        credits_val = []
        
        for mark in self.marks:
            if mark.get_sid() == sid:
                marks_val.append(mark.get_mark())
                credits_val.append(mark.get_credit())
                
        if not credits_val:
            return 0        
        
        marks_val = np.array(marks_val)
        credits_val = np.array(credits_val)
                
        return np.sum(marks_val * credits_val) / np.sum(credits_val)
    
    def countGPA(self):
        for stu in self.students:
            gpa_val = self.countGPA4Student(stu.get_id())
            stu.set_gpa(gpa_val)
        self.students.sort(key=lambda s: s.get_gpa(), reverse=True)
            
class OutputUI:
    def __init__(self):
        self.MENU_ITEMS = [
            "1. Add student",
            "2. Add course",
            "3. Add mark",
            "4. Show student list",
            "5. Show course list",
            "6. Show mark list",
            "7. Show GPA",
            "8. Exit",
        ]

        self.system = SystemManagementMark()
        self.choice = 0

    def draw_menu(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 2, "STUDENT MANAGEMENT SYSTEM")

        for i, item in enumerate(self.MENU_ITEMS):
            stdscr.addstr(i + 2, 4, item)

        stdscr.refresh()

    def get_input(self, stdscr, y, x, message, max_len):
        curses.echo()
        stdscr.addstr(y, x, message)
        stdscr.refresh()

        s = stdscr.getstr(y, x + len(message) + 2, max_len).decode()
        curses.noecho()

        return s

    def hander_add_student(self, stdscr):
        curses.echo()
        stdscr.clear()
        stdscr.addstr(0, 2, "ADD STUDENT IN CLASS")

        id = self.get_input(stdscr, 2, 4, "ID : ", 12)
        name = self.get_input(stdscr, 3, 4, "Name : ", 20)
        dob = self.get_input(stdscr, 4, 4, "Dob (DD/MM/YY): ", 8)

        errors = []
        if not id.strip():
            errors.append("ID must not be empty.")
        elif any(stu.get_id() == id for stu in self.system.students):
            errors.append("Student ID already exists.")
        if not name.strip():
            errors.append("Name must not be empty.")
        try:
            datetime.strptime(dob, "%d/%m/%y")
        except ValueError:
            errors.append("DoB is invalid. Use format DD/MM/YY.")

        if errors:
            row = 6
            for msg in errors:
                stdscr.addstr(row, 4, msg)
                row += 1
            stdscr.addstr(row + 1, 4, "Press any key to continue...")
            stdscr.getch()
            return

        self.system.students.append(Student(id, name, dob))
        stdscr.refresh()

    def hander_add_course(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 2, "ADD COURSE IN CLASS")

        id = self.get_input(stdscr, 2, 4, "ID : ", 12)
        name = self.get_input(stdscr, 3, 4, "Name : ", 20)

        errors = []
        if not id.strip():
            errors.append("Course ID must not be empty.")
        elif any(course.get_id() == id for course in self.system.courses):
            errors.append("Course ID already exists.")
        if not name.strip():
            errors.append("Course name must not be empty.")

        if errors:
            row = 5
            for msg in errors:
                stdscr.addstr(row, 4, msg)
                row += 1
            stdscr.addstr(row + 1, 4, "Press any key to continue...")
            stdscr.getch()
            return

        self.system.courses.append(Course(id, name))
        stdscr.refresh()

    def hander_add_mark_for_student_in_course(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 2, "ADD MARK IN CLASS")

        cid = self.get_input(stdscr, 2, 4, "Course ID: ", 8)
        sid = self.get_input(stdscr, 3, 4, "Student ID: ", 12)
        mark_str = self.get_input(
            stdscr, 4, 4, f"Mark for student {sid} in course {cid} : ", 5
        )
        credit_str = self.get_input(
            stdscr, 5, 4, f"Credit for student {sid} in course {cid} : ", 1
        )

        errors = []
        if not any(course.get_id() == cid for course in self.system.courses):
            errors.append("Course ID does not exist.")
        if not any(stu.get_id() == sid for stu in self.system.students):
            errors.append("Student ID does not exist.")

        mark_val = None
        credit_val = None
        try:
            mark_val = float(mark_str)
        except ValueError:
            errors.append("Mark must be a number.")

        try:
            credit_val = int(credit_str)
            if credit_val <= 0:
                errors.append("Credit must be > 0.")
        except ValueError:
            errors.append("Credit must be an integer.")

        if errors:
            row = 7
            for msg in errors:
                stdscr.addstr(row, 4, msg)
                row += 1
            stdscr.addstr(row + 1, 4, "Press any key to continue...")
            stdscr.getch()
            return

        found = False
        for mark in self.system.marks:
            if mark.get_cid() == cid and mark.get_sid() == sid:
                mark.set_mark(mark_val)
                mark.set_credit(credit_val)
                found = True

        if not found:
            self.system.marks.append(Mark(cid, sid, mark_val, credit_val))

        stdscr.refresh()

    def show_student_list(self, stdscr):
        stdscr.clear()

        stdscr.addstr(0, 2, "===== STUDENT LIST =====")
        stdscr.addstr(2, 2, "ID          NAME                 DOB")
        for i, stu in enumerate(self.system.students):
            stdscr.addstr(
                i + 3,
                2,
                f"{stu.get_id():12} {stu.get_name():<20} {stu.get_dob():8}",
            )

        stdscr.addstr(self.height-2, 0, "Press any key to return MENU...")
        stdscr.refresh()

    def show_course_list(self, stdscr):
        stdscr.clear()

        stdscr.addstr(0, 2, "===== COURSE LIST =====")
        stdscr.addstr(2, 2, "ID          NAME")
        for i, course in enumerate(self.system.courses):
            stdscr.addstr(
                i + 3,
                2,
                f"{course.get_id():12} {course.get_name():<20}",
            )

        stdscr.addstr(self.height-2, 0, "Press any key to return MENU...")
        stdscr.refresh()

    def show_mark_list(self, stdscr):
        stdscr.clear()

        stdscr.addstr(0, 2, "===== MARK LIST =====")
        row = 2
        for course in self.system.courses:
            cid = course.get_id()
            stdscr.addstr(row, 2, f"{cid} :")
            row += 1
            for stu in self.system.students:
                sid = stu.get_id()
                mark_val = self.system.findMark4Student(cid, sid)
                stdscr.addstr(
                    row,
                    4,
                    f"{sid:<12} {stu.get_name():<20} {mark_val:5.2f}",
                )
                row += 1
            row += 1

        stdscr.addstr(self.height-2, 0, "Press any key to return MENU...")
        stdscr.refresh()

    def show_gpa(self, stdscr):
        stdscr.clear()
        self.system.countGPA()

        stdscr.addstr(0, 2, "===== GPA =====")
        stdscr.addstr(2, 2, "ID          NAME                 GPA")
        for i, stu in enumerate(self.system.students):
            stdscr.addstr(
                i + 3,
                2,
                f"{stu.get_id():12} {stu.get_name():<20} {stu.get_gpa():5.2f}",
            )

        stdscr.addstr(self.height-2, 0, "Press any key to return MENU...")
        stdscr.refresh()

    def main(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        self.height, self.width = stdscr.getmaxyx()

        while True:
            self.draw_menu(stdscr)

            choice_str = self.get_input(
                stdscr,
                len(self.MENU_ITEMS) + 3,
                2,
                "Choose option (1-8) or q to exit: ",
                1,
            )

            if choice_str.lower() == "q":
                break

            try:
                self.choice = int(choice_str)
            except ValueError:
                continue

            if self.choice == 1:
                self.hander_add_student(stdscr)
            elif self.choice == 2:
                self.hander_add_course(stdscr)
            elif self.choice == 3:
                self.hander_add_mark_for_student_in_course(stdscr)
            elif self.choice == 4:
                self.show_student_list(stdscr)
            elif self.choice == 5:
                self.show_course_list(stdscr)
            elif self.choice == 6:
                self.show_mark_list(stdscr)
            elif self.choice == 7:
                self.show_gpa(stdscr)
            elif self.choice == 8:
                break
            
            stdscr.getch()

if __name__ == "__main__":
    # Test for SystemManagementMark
    cli = OutputUI()
    curses.wrapper(cli.main)