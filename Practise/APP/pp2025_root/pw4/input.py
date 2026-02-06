from pw4.domains.Course import Course
from pw4.domains.Student import Student
from pw4.domains.Mark import Mark
from datetime import datetime

class InputSystem:
    def __init__(self):
        self.__courses = []   # list[Course]
        self.__students = []  # list[Student]
        self.__marks = []     # list[Mark]
        
        self.inputAll()

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
  