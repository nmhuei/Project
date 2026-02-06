import numpy as np

from pw6.input import IOSystem


class SystemManagementMark:
    def __init__(self):
        # InputSystem will handle loading from students.dat or asking for input.
        self.ioSystem = IOSystem()

        self.courses = self.ioSystem.get_courses()
        self.students = self.ioSystem.get_students()
        self.marks = self.ioSystem.get_marks()
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
