import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

from pw9.domains.SystemManagementMark import SystemManagementMark
from pw9.domains.Student import Student
from pw9.domains.Course import Course
from pw9.domains.Mark import Mark


class OutputUI:
    def __init__(self):
        self.system = SystemManagementMark()
        self.root = None
        
    def draw_exit(self):
        """Show goodbye message"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.system.ioSystem.saveDataUsingPickleBackGround()
            self.root.destroy()
            return True
        return False
    
    def hander_add_student(self):
        """Add student handler"""
        student_id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        dob = self.student_dob_entry.get().strip()
        
        errors = []
        if not student_id:
            errors.append("ID must not be empty.")
        elif any(stu.get_id() == student_id for stu in self.system.students):
            errors.append("Student ID already exists.")
        if not name:
            errors.append("Name must not be empty.")
        try:
            datetime.strptime(dob, "%d/%m/%y")
        except ValueError:
            errors.append("DoB is invalid. Use format DD/MM/YY.")
        
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return
        
        self.system.students.append(Student(student_id, name, dob))
        self.system.ioSystem.saveDataUsingPickleBackGround()
        
        messagebox.showinfo("Success", "Student added successfully!")
        
        # Clear entries
        self.student_id_entry.delete(0, tk.END)
        self.student_name_entry.delete(0, tk.END)
        self.student_dob_entry.delete(0, tk.END)
        
        self.show_student_list()
    
    def hander_add_course(self):
        """Add course handler"""
        course_id = self.course_id_entry.get().strip()
        name = self.course_name_entry.get().strip()
        
        errors = []
        if not course_id:
            errors.append("Course ID must not be empty.")
        elif any(course.get_id() == course_id for course in self.system.courses):
            errors.append("Course ID already exists.")
        if not name:
            errors.append("Course name must not be empty.")
        
        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return
        
        self.system.courses.append(Course(course_id, name))
        self.system.ioSystem.saveDataUsingPickleBackGround()
        
        messagebox.showinfo("Success", "Course added successfully!")
        
        # Clear entries
        self.course_id_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)
        
        self.show_course_list()
    
    def hander_add_mark_for_student_in_course(self):
        """Add mark handler"""
        cid = self.mark_course_id_entry.get().strip()
        sid = self.mark_student_id_entry.get().strip()
        mark_str = self.mark_value_entry.get().strip()
        credit_str = self.mark_credit_entry.get().strip()
        
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
            messagebox.showerror("Error", "\n".join(errors))
            return
        
        found = False
        for mark in self.system.marks:
            if mark.get_cid() == cid and mark.get_sid() == sid:
                mark.set_mark(mark_val)
                mark.set_credit(credit_val)
                found = True
        
        if not found:
            self.system.marks.append(Mark(cid, sid, mark_val, credit_val))
        
        self.system.ioSystem.saveDataUsingPickleBackGround()
        
        messagebox.showinfo("Success", "Mark added/updated successfully!")
        
        # Clear entries
        self.mark_course_id_entry.delete(0, tk.END)
        self.mark_student_id_entry.delete(0, tk.END)
        self.mark_value_entry.delete(0, tk.END)
        self.mark_credit_entry.delete(0, tk.END)
        
        self.show_mark_list()
    
    def show_student_list(self):
        """Display student list in treeview"""
        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        # Add students
        for stu in self.system.students:
            self.student_tree.insert(
                "",
                tk.END,
                values=(stu.get_id(), stu.get_name(), stu.get_dob())
            )
    
    def show_course_list(self):
        """Display course list in treeview"""
        # Clear existing items
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # Add courses
        for course in self.system.courses:
            self.course_tree.insert(
                "",
                tk.END,
                values=(course.get_id(), course.get_name())
            )
    
    def show_mark_list(self):
        """Display mark list in text widget"""
        self.marks_text.delete(1.0, tk.END)
        
        for course in self.system.courses:
            cid = course.get_id()
            self.marks_text.insert(tk.END, f"{cid} :\n", "bold")
            
            for stu in self.system.students:
                sid = stu.get_id()
                mark_val = self.system.findMark4Student(cid, sid)
                self.marks_text.insert(
                    tk.END,
                    f"  {sid:<12} {stu.get_name():<20} {mark_val:5.2f}\n"
                )
            
            self.marks_text.insert(tk.END, "\n")
        
        self.marks_text.tag_config("bold", font=("Courier", 10, "bold"))
    
    def show_gpa(self):
        """Display GPA in treeview"""
        # Clear existing items
        for item in self.gpa_tree.get_children():
            self.gpa_tree.delete(item)
        
        self.system.countGPA()
        
        # Add students with GPA
        for stu in self.system.students:
            self.gpa_tree.insert(
                "",
                tk.END,
                values=(stu.get_id(), stu.get_name(), f"{stu.get_gpa():.2f}")
            )
    
    def create_add_student_tab(self):
        """Create Add Student tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="1. Add Student")
        
        content = tk.Frame(frame)
        content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(content, text="ADD STUDENT IN CLASS", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=20
        )
        
        tk.Label(content, text="ID:", font=("Arial", 11)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.student_id_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.student_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(content, text="Name:", font=("Arial", 11)).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.student_name_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.student_name_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(content, text="Dob (DD/MM/YY):", font=("Arial", 11)).grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.student_dob_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.student_dob_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Button(
            content,
            text="Add Student",
            command=self.hander_add_student,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        ).grid(row=4, column=0, columnspan=2, pady=20)
    
    def create_add_course_tab(self):
        """Create Add Course tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Add Course")
        
        content = tk.Frame(frame)
        content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(content, text="ADD COURSE IN CLASS", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=20
        )
        
        tk.Label(content, text="ID:", font=("Arial", 11)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.course_id_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.course_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(content, text="Name:", font=("Arial", 11)).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.course_name_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.course_name_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Button(
            content,
            text="Add Course",
            command=self.hander_add_course,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        ).grid(row=3, column=0, columnspan=2, pady=20)
    
    def create_add_mark_tab(self):
        """Create Add Mark tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="3. Add Mark")
        
        content = tk.Frame(frame)
        content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(content, text="ADD MARK IN CLASS", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=20
        )
        
        tk.Label(content, text="Course ID:", font=("Arial", 11)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.mark_course_id_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.mark_course_id_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(content, text="Student ID:", font=("Arial", 11)).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.mark_student_id_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.mark_student_id_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(content, text="Mark:", font=("Arial", 11)).grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.mark_value_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.mark_value_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(content, text="Credit:", font=("Arial", 11)).grid(
            row=4, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.mark_credit_entry = tk.Entry(content, width=30, font=("Arial", 11))
        self.mark_credit_entry.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Button(
            content,
            text="Add Mark",
            command=self.hander_add_mark_for_student_in_course,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        ).grid(row=5, column=0, columnspan=2, pady=20)
    
    def create_view_students_tab(self):
        """Create View Students tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="4. Student List")
        
        tk.Label(frame, text="===== STUDENT LIST =====", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Button(
            frame,
            text="Refresh",
            command=self.show_student_list,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        ).pack(pady=5)
        
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.student_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "NAME", "DOB"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.student_tree.yview)
        
        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("NAME", text="NAME")
        self.student_tree.heading("DOB", text="DOB")
        
        self.student_tree.column("ID", width=150)
        self.student_tree.column("NAME", width=250)
        self.student_tree.column("DOB", width=150)
        
        self.student_tree.pack(fill=tk.BOTH, expand=True)
        
        self.show_student_list()
    
    def create_view_courses_tab(self):
        """Create View Courses tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="5. Course List")
        
        tk.Label(frame, text="===== COURSE LIST =====", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Button(
            frame,
            text="Refresh",
            command=self.show_course_list,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        ).pack(pady=5)
        
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.course_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "NAME"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.course_tree.yview)
        
        self.course_tree.heading("ID", text="ID")
        self.course_tree.heading("NAME", text="NAME")
        
        self.course_tree.column("ID", width=200)
        self.course_tree.column("NAME", width=400)
        
        self.course_tree.pack(fill=tk.BOTH, expand=True)
        
        self.show_course_list()
    
    def create_view_marks_tab(self):
        """Create View Marks tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="6. Mark List")
        
        tk.Label(frame, text="===== MARK LIST =====", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Button(
            frame,
            text="Refresh",
            command=self.show_mark_list,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        ).pack(pady=5)
        
        text_frame = tk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.marks_text = scrolledtext.ScrolledText(
            text_frame,
            font=("Courier", 10),
            wrap=tk.NONE
        )
        self.marks_text.pack(fill=tk.BOTH, expand=True)
        
        self.show_mark_list()
    
    def create_view_gpa_tab(self):
        """Create View GPA tab"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="7. GPA")
        
        tk.Label(frame, text="===== GPA =====", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Button(
            frame,
            text="Refresh",
            command=self.show_gpa,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        ).pack(pady=5)
        
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.gpa_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "NAME", "GPA"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.gpa_tree.yview)
        
        self.gpa_tree.heading("ID", text="ID")
        self.gpa_tree.heading("NAME", text="NAME")
        self.gpa_tree.heading("GPA", text="GPA")
        
        self.gpa_tree.column("ID", width=150)
        self.gpa_tree.column("NAME", width=250)
        self.gpa_tree.column("GPA", width=100)
        
        self.gpa_tree.pack(fill=tk.BOTH, expand=True)
        
        self.show_gpa()
    
    def main(self):
        """Main GUI setup - replaces curses version"""
        self.root = tk.Tk()
        self.root.title("STUDENT MANAGEMENT SYSTEM")
        self.root.geometry("900x600")
        
        # Title bar
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=15)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create all tabs
        self.create_add_student_tab()
        self.create_add_course_tab()
        self.create_add_mark_tab()
        self.create_view_students_tab()
        self.create_view_courses_tab()
        self.create_view_marks_tab()
        self.create_view_gpa_tab()
        
        # Exit button at bottom
        exit_btn = tk.Button(
            self.root,
            text="8. Exit",
            command=self.draw_exit,
            bg="#c0392b",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        )
        exit_btn.pack(pady=10)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.draw_exit)
        
        # Start GUI
        self.root.mainloop()