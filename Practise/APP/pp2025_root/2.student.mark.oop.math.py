from datetime import datetime


class Student:
    def __init__(self, id, name, dob):
        self.__id = id
        self.__name = name
        self.__dob = dob

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_dob(self, dob):
        self.__dob = dob


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
    def __init__(self, cid, sid, mark):
        self.__cid = cid
        self.__sid = sid
        self.__mark = mark

    def get_cid(self):
        return self.__cid

    def get_sid(self):
        return self.__sid

    def get_mark(self):
        return self.__mark

    def set_cid(self, cid):
        self.__cid = cid

    def set_sid(self, sid):
        self.__sid = sid

    def set_mark(self, mark):
        self.__mark = mark


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
        n = int(input("Input number of students in a class : "))
        while n <= 0:
            print("Invalid number! Must be > 0.")
            n = int(input("Input number of students in a class : "))

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
        n = int(input("Input number of courses in a class : "))
        while n <= 0:
            print("Invalid number! Must be > 0.")
            n = int(input("Input number of courses in a class : "))

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

    def getMark4Student(self, sid: str) -> float:
        mark = float(input(f"   Mark for student {sid} : "))
        return mark

    def inputMarks4Course(self) -> None:
        cid = self.chooseCourse()
        print(f"\nMark for Course {cid}")

        for stu in self.__students:
            sid = stu.get_id()
            mark_val = self.getMark4Student(sid)
            self.__marks.append(Mark(cid, sid, mark_val))

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

    def showAll(self) -> None:
        self.showCourseList()
        self.showStudentList()
        self.showMark4AllCourse()


if __name__ == "__main__":
    # Test for SystemManagementMark
    smm = SystemManagementMark()
    smm.showAll()
