import curses
from datetime import datetime

from pw5.domains.SystemManagementMark import SystemManagementMark
from pw5.domains.Student import Student
from pw5.domains.Course import Course
from pw5.domains.Mark import Mark


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
                self.system.ioSystem.compress_all()
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
                self.system.ioSystem.compress_all()
                break
            
            stdscr.getch()
