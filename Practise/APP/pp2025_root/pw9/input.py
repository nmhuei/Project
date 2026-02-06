from pw9.domains.Course import Course
from pw9.domains.Student import Student
from pw9.domains.Mark import Mark
from datetime import datetime
import tarfile, os, gzip, pickle, threading

BASE_DIR = os.path.dirname(__file__)

class IOSystem:
    def __init__(self):
        self.__courses = []   # list[Course]
        self.__students = []  # list[Student]
        self.__marks = []     # list[Mark]


        self.loadDataUsingPickle()
    
    # Tar + Gzip    
    def compress_all(self):
        self.writeData2Files()
        files = [
            os.path.join(BASE_DIR, "students.txt"), 
            os.path.join(BASE_DIR, "courses.txt"), 
            os.path.join(BASE_DIR, "marks.txt"),
        ]

        archive_path = os.path.join(BASE_DIR, "students.dat")
        with tarfile.open(archive_path, "w:gz") as tar:
            for f in files:
                if os.path.exists(f):
                    tar.add(f, arcname=os.path.basename(f))

        for f in files:
            if os.path.exists(f):
                os.remove(f)

    def inputData(self):
        archive_path = os.path.join(BASE_DIR, "students.dat")
        if os.path.exists(archive_path):
            # Decompress 
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=BASE_DIR)

            # Load
            self.readDataFromFiles()
        else:
            self.inputAll()
    
    # Pickle + Gzip       
    def saveDataUsingPickle(self):
        data = {
            "students" : self.__students,
            "courses" : self.__courses,
            "marks" : self.__marks,
        }
        
        with gzip.open(os.path.join(BASE_DIR, "students.dat"), "wb") as f:
            pickle.dump(data, f)
            
        os.replace(os.path.join(BASE_DIR, "students.dat"), "./pw9/students.dat")
            
    def loadDataUsingPickle(self):
        if not os.path.exists(os.path.join(BASE_DIR, "students.dat")):
            self.inputAll()
            return 
    
        try:
            with gzip.open(os.path.join(BASE_DIR, "students.dat"), "rb") as f:
                data = pickle.load(f)
                
            self.__students = data["students"]
            self.__courses = data["courses"]
            self.__marks = data["marks"]

        except (pickle.UnpicklingError, EOFError, OSError) as e:
            print("Failed to load students.dat (file may be empty or corrupted). Re-entering data...\n")
            self.inputAll()
    
    # Run pickle in background
    def saveDataUsingPickleBackGround(self):
        t = threading.Thread(
            target=self.saveDataUsingPickle,
            daemon=True
        )
    
        t.start()
    
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

    # ===== WRITE TO FILE =====
    def writeStudents2File(self, path: str) -> None:
        """Write students to a text file, one per line: id,name,dob"""
        with open(path, "w", encoding="utf-8") as f:
            for stu in self.__students:
                f.write(f"{stu.get_id()},{stu.get_name()},{stu.get_dob()}\n")

    def writeCourses2File(self, path: str) -> None:
        """Write courses to a text file, one per line: id,name"""
        with open(path, "w", encoding="utf-8") as f:
            for course in self.__courses:
                f.write(f"{course.get_id()},{course.get_name()}\n")

    def writeMarks2File(self, path: str) -> None:
        """Write marks to a text file, one per line: cid,sid,mark,credit"""
        with open(path, "w", encoding="utf-8") as f:
            for mark in self.__marks:
                f.write(
                    f"{mark.get_cid()},{mark.get_sid()},{mark.get_mark()},{mark.get_credit()}\n"
                )

    def writeData2Files(
        self,
        students_path: str = os.path.join(BASE_DIR, "students.txt"),
        courses_path: str = os.path.join(BASE_DIR, "courses.txt"),
        marks_path: str = os.path.join(BASE_DIR, "marks.txt"),
    ) -> None:
        """Convenience helper to write all data to three files."""
        self.writeStudents2File(students_path)
        self.writeCourses2File(courses_path)
        self.writeMarks2File(marks_path)

    # ===== READ FROM FILE =====
    def readStudentsFromFile(self, path: str) -> None:
        """Read students from a text file created by writeStudents2File."""
        self.__students = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    sid, name, dob = line.split(",", 2)
                    self.__students.append(Student(sid, name, dob))
        except FileNotFoundError:
            # If file does not exist, keep list empty
            return

    def readCoursesFromFile(self, path: str) -> None:
        """Read courses from a text file created by writeCourses2File."""
        self.__courses = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    cid, name = line.split(",", 1)
                    self.__courses.append(Course(cid, name))
        except FileNotFoundError:
            return

    def readMarksFromFile(self, path: str) -> None:
        """Read marks from a text file created by writeMarks2File."""
        self.__marks = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    cid, sid, mark_str, credit_str = line.split(",", 3)
                    mark_val = float(mark_str)
                    credit_val = int(credit_str)
                    self.__marks.append(Mark(cid, sid, mark_val, credit_val))
        except FileNotFoundError:
            return

    def readDataFromFiles(
        self,
        students_path: str = os.path.join(BASE_DIR, "students.txt"),
        courses_path: str = os.path.join(BASE_DIR, "courses.txt"),
        marks_path: str = os.path.join(BASE_DIR, "marks.txt"),
    ) -> None:
        """Convenience helper to read all data from three files."""
        self.readStudentsFromFile(students_path)
        self.readCoursesFromFile(courses_path)
        self.readMarksFromFile(marks_path)

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
  