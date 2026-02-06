students = []
courses = []
marks = []

# INPUT STUDENT LIST
def isValidStudentName(name : str) -> str:
    return 1

def isValidStudentId(id : str) -> str:
    return 1

def isValidStudentDob(dob : str) -> str:
    parts = dob.split("/")
    
    if len(parts) != 3:
        return 0
    
    return 1

def inputValidStudent():
    print("Student : ")
    
    id = input("     - ID : ")
    while not isValidStudentId(id):
        print("     - Invalid Student ID.")
        id = input("     - ID : ")
        
    
    name = input("     - Name : ")
    while not isValidStudentName(name):
        print("     - Invalid Student Name.")
        name = input("     - Name : ")
    
    dob = input("     - DoB (DD/MM/YY): ")
    while not isValidStudentDob(dob):
        print("     - Invalid Student DoB.")
        dob = input("     - DoB (DD/MM/YY): ")
        
    return {
        "id"    : id,
        "name"  : name,
        "dob"   : dob,    
    }
    
def inputStudent():
    student = inputValidStudent()
    students.append(student)
    
    return 

def inputStudentList():
    n = int(input("Input number of students in a class : "))
    while n <= 0:
        print("Valid number!")
        n = int(input("Input number of students in a class : "))
        
    for _ in range(n):
        inputStudent()
        
    return 
        
# INPUT COURSE LIST
def isValidCourseName(name : str) -> str:
    return 1

def isValidCourseId(id : str) -> str:
    return 1
    
def inputValidCourse():
    print("Course : ")
    
    id = input("     - ID : ")
    while not isValidStudentId(id):
        print("     - Invalid Course ID.")
        id = input("     - ID : ")    
    
    name = input("     - Name : ")
    while not isValidStudentName(name):
        print("     - Invalid Course Name.")
        name = input("     - Name : ")
        
    return {
        "id"    : id,
        "name"  : name,
    }
    
def inputCourse():
    course = inputValidCourse()
    courses.append(course)
    
    return

def inputCourseList():
    n = int(input("Input number of courses in a class : "))
    while n <= 0:
        print("Valid number!")
        n = int(input("Input number of courses in a class : "))
        
    for _ in range(n):
        inputCourse()
        
    return 
    
# 
def haveCourseId(cid : str) -> bool:
    if not any(cid == course["id"] for course in courses):
        return 0

    return 1

# Select a course, input marks for student in this course
def chooseCourse():
    showCourseList()
    n = int(input("Choose index of course : "))
    
    while n not in [1, len(courses) + 1]:
        n = int(input("Choose other index of course : "))
    
    return courses[n-1]["id"]

def getMark4Student(sid):
    mark = float(input(f"   Mark for student {sid} : "))
    
    return mark
    
def inputMarks4Course():
    cid = chooseCourse()
    print(f"\nMark for Course {cid}")
    
    for stu in students:
        mark = getMark4Student(stu["id"])
        marks.append({
            "cid"   : cid,
            "sid"   : stu["id"],
            "mark"  : mark,
        })
    
    return
        
# Input functions        
def inputAll():
    inputStudentList()
    inputCourseList()
    inputMarks4Course()

# Listing functions
def showCourseList():
    print("\n ===== COURSE LIST ======")
    for i, course in enumerate(courses):
        print(f"{i+1}. {course["id"]}")

def showStudentList():
    print("\n ===== STUDENT LIST ======")
    for i, stu in enumerate(students):
        print(f"{stu["id"]:<12} {stu["name"]:<20} {stu["dob"]:<8}")
  
def findMark4Student(cid, sid):
    for mark in marks:
        if (mark["cid"] == cid and mark["sid"] == sid):
            return mark["mark"]
        
    return 0  
        
def showMark4Course(cid):
    print(f"{cid} :")
    for stu in students:
        mark = findMark4Student(cid, stu["id"])
        print(f"    {stu["id"]:<12} {stu["name"]:<20} {mark:5.2f}") 
        
    return
        
def showMark4AllCourse():
    print("\n ===== MARK LIST =====")
    for course in courses:
        cid = course["id"]
        
        showMark4Course(cid)
        
    return

def showAll():
    showCourseList()
    showStudentList()
    showMark4AllCourse()
    
if __name__ == "__main__":
    inputAll()
    showAll()