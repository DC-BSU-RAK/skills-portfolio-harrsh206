import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class Student:
    def __init__(self, student_code, name, mark1, mark2, mark3, exam_mark):
        self.student_code = int(student_code)
        self.name = name
        self.mark1 = int(mark1)
        self.mark2 = int(mark2)
        self.mark3 = int(mark3)
        self.exam_mark = int(exam_mark)
    
    @property
    def coursework_total(self):
        return self.mark1 + self.mark2 + self.mark3
    
    @property
    def total_score(self):
        return self.coursework_total + self.exam_mark
    
    @property
    def percentage(self):
        return (self.total_score / 160) * 100
    
    @property
    def grade(self):
        percentage = self.percentage
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

class StudentManager:
    def __init__(self, filename):
        self.filename = filename
        self.students = []
        self.load_data()
    
    def load_data(self):
        """Load student data from file"""
        if not os.path.exists(self.filename):
            # Create sample data if file doesn't exist
            sample_data = """5
1001,John Smith,15,12,14,68
1002,Emma Johnson,18,16,17,82
1003,Michael Brown,8,10,9,45
1004,Sarah Davis,16,15,14,72
1005,David Wilson,12,11,13,58"""
            with open(self.filename, 'w') as f:
                f.write(sample_data)
        
        self.students = []
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                num_students = int(lines[0].strip())
                
                for line in lines[1:]:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        student = Student(data[0], data[1], data[2], data[3], data[4], data[5])
                        self.students.append(student)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def save_data(self):
        """Save student data to file"""
        try:
            with open(self.filename, 'w') as f:
                f.write(f"{len(self.students)}\n")
                for student in self.students:
                    f.write(f"{student.student_code},{student.name},{student.mark1},{student.mark2},{student.mark3},{student.exam_mark}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def get_all_students(self):
        return self.students
    
    def get_student_by_code(self, code):
        for student in self.students:
            if student.student_code == code:
                return student
        return None
    
    def get_student_by_name(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None
    
    def get_highest_scoring_student(self):
        if not self.students:
            return None
        return max(self.students, key=lambda x: x.total_score)
    
    def get_lowest_scoring_student(self):
        if not self.students:
            return None
        return min(self.students, key=lambda x: x.total_score)
    
    def add_student(self, student_code, name, mark1, mark2, mark3, exam_mark):
        # Check if student code already exists
        if self.get_student_by_code(student_code):
            return False, "Student code already exists"
        
        try:
            student = Student(student_code, name, mark1, mark2, mark3, exam_mark)
            self.students.append(student)
            return True, "Student added successfully"
        except Exception as e:
            return False, f"Error adding student: {str(e)}"
    
    def delete_student(self, student_code):
        student = self.get_student_by_code(student_code)
        if student:
            self.students.remove(student)
            return True, "Student deleted successfully"
        return False, "Student not found"
    
    def update_student(self, student_code, **kwargs):
        student = self.get_student_by_code(student_code)
        if not student:
            return False, "Student not found"
        
        try:
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            return True, "Student updated successfully"
        except Exception as e:
            return False, f"Error updating student: {str(e)}"

class ModernStudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8fafc')
        
        # Initialize student manager
        self.manager = StudentManager("studentMarks.txt")
        
        # Colors
        self.colors = {
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'light': '#f8fafc',
            'dark': '#1e293b',
            'sidebar': '#1e293b',
            'header': '#334155'
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        # Create main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Main content area
        self.create_main_content(main_container)
    
    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.colors['sidebar'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        title_frame.pack(fill=tk.X, pady=20, padx=15)
        
        tk.Label(title_frame, text="STUDENT MANAGER", font=("Arial", 16, "bold"), 
                bg=self.colors['sidebar'], fg="white").pack(anchor=tk.W)
        
        # Navigation menu
        nav_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        nav_frame.pack(fill=tk.X, padx=15, pady=20)
        
        # Main navigation sections
        main_nav_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 All Students", self.view_all_students),
            ("🔍 Find Student", self.view_individual_student)
        ]
        
        tk.Label(nav_frame, text="MAIN NAVIGATION", font=("Arial", 10, "bold"),
                bg=self.colors['sidebar'], fg="#94a3b8").pack(anchor=tk.W, pady=(0, 10))
        
        for text, command in main_nav_items:
            btn = tk.Button(nav_frame, text=text, font=("Arial", 11), 
                          bg=self.colors['sidebar'], fg="#cbd5e1", bd=0,
                          anchor=tk.W, justify=tk.LEFT,
                          command=command)
            btn.pack(fill=tk.X, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['primary'], fg="white"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['sidebar'], fg="#cbd5e1"))
        
        # Analytics section
        tk.Label(nav_frame, text="ANALYTICS", font=("Arial", 10, "bold"),
                bg=self.colors['sidebar'], fg="#94a3b8").pack(anchor=tk.W, pady=(20, 10))
        
        analytics_items = [
            ("🏆 Top Performers", self.show_highest_student),
            ("📉 Lowest Scores", self.show_lowest_student),
            ("📊 Sort & Filter", self.sort_students)
        ]
        
        for text, command in analytics_items:
            btn = tk.Button(nav_frame, text=text, font=("Arial", 11), 
                          bg=self.colors['sidebar'], fg="#cbd5e1", bd=0,
                          anchor=tk.W, justify=tk.LEFT,
                          command=command)
            btn.pack(fill=tk.X, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['primary'], fg="white"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['sidebar'], fg="#cbd5e1"))
        
        # Management section
        tk.Label(nav_frame, text="MANAGEMENT", font=("Arial", 10, "bold"),
                bg=self.colors['sidebar'], fg="#94a3b8").pack(anchor=tk.W, pady=(20, 10))
        
        management_items = [
            ("➕ Add Student", self.add_student),
            ("✏️ Edit Records", self.update_student),
            ("🗑️ Delete Student", self.delete_student)
        ]
        
        for text, command in management_items:
            btn = tk.Button(nav_frame, text=text, font=("Arial", 11), 
                          bg=self.colors['sidebar'], fg="#cbd5e1", bd=0,
                          anchor=tk.W, justify=tk.LEFT,
                          command=command)
            btn.pack(fill=tk.X, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['primary'], fg="white"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['sidebar'], fg="#cbd5e1"))
        
        # Progress section
        progress_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        progress_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)
        
        tk.Label(progress_frame, text="YOUR PROGRESS", font=("Arial", 10, "bold"),
                bg=self.colors['sidebar'], fg="#94a3b8").pack(anchor=tk.W)
        
        tk.Label(progress_frame, text=f"{len(self.manager.students)} Students Managed", 
                font=("Arial", 10), bg=self.colors['sidebar'], fg="#cbd5e1").pack(anchor=tk.W, pady=(5, 0))
        
        # Calculate average grade distribution
        grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in self.manager.students:
            grade_count[student.grade] += 1
        
        grade_text = " | ".join([f"{grade}:{count}" for grade, count in grade_count.items() if count > 0])
        tk.Label(progress_frame, text=f"Grades: {grade_text}", 
                font=("Arial", 9), bg=self.colors['sidebar'], fg="#94a3b8").pack(anchor=tk.W, pady=(2, 10))
        
        # Sign out button
        signout_btn = tk.Button(sidebar, text="🚪 Sign Out", font=("Arial", 11),
                               bg=self.colors['sidebar'], fg="#cbd5e1", bd=0,
                               command=self.root.quit)
        signout_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=10)
        signout_btn.bind("<Enter>", lambda e: signout_btn.config(bg=self.colors['danger'], fg="white"))
        signout_btn.bind("<Leave>", lambda e: signout_btn.config(bg=self.colors['sidebar'], fg="#cbd5e1"))
    
    def create_main_content(self, parent):
        main_content = tk.Frame(parent, bg=self.colors['light'])
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_content, bg="white", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Student Analytics Dashboard", font=("Arial", 20, "bold"),
                bg="white", fg=self.colors['dark']).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Content area
        self.content_frame = tk.Frame(main_content, bg=self.colors['light'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def create_card(self, parent, title, value, color, width=200):
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1)
        card.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(card, text=title, font=("Arial", 12), 
                bg="white", fg=self.colors['secondary']).pack(pady=(15, 5))
        
        tk.Label(card, text=value, font=("Arial", 24, "bold"), 
                bg="white", fg=color).pack(pady=5)
        
        return card
    
    def show_dashboard(self):
        self.clear_content()
        
        # Welcome section
        welcome_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        welcome_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(welcome_frame, text="Welcome to Student Manager", 
                font=("Arial", 16, "bold"), bg=self.colors['light'], 
                fg=self.colors['dark']).pack(anchor=tk.W)
        
        tk.Label(welcome_frame, text="Manage and analyze student performance data", 
                font=("Arial", 12), bg=self.colors['light'], 
                fg=self.colors['secondary']).pack(anchor=tk.W, pady=(5, 20))
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        stats_frame.pack(fill=tk.X, pady=10)
        
        total_students = len(self.manager.students)
        avg_percentage = sum(s.percentage for s in self.manager.students) / total_students if total_students > 0 else 0
        highest_student = self.manager.get_highest_scoring_student()
        lowest_student = self.manager.get_lowest_scoring_student()
        
        self.create_card(stats_frame, "Total Students", total_students, self.colors['primary'])
        self.create_card(stats_frame, "Average %", f"{avg_percentage:.1f}%", self.colors['success'])
        self.create_card(stats_frame, "Highest Score", f"{highest_student.percentage:.1f}%" if highest_student else "N/A", self.colors['warning'])
        self.create_card(stats_frame, "Lowest Score", f"{lowest_student.percentage:.1f}%" if lowest_student else "N/A", self.colors['danger'])
        
        # Grade distribution card
        grade_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        grade_frame.pack(fill=tk.X, pady=10)
        
        grade_card = tk.Frame(grade_frame, bg="white", relief=tk.RAISED, bd=1)
        grade_card.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(grade_card, text="Grade Distribution", font=("Arial", 12), 
                bg="white", fg=self.colors['secondary']).pack(pady=(15, 10))
        
        grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in self.manager.students:
            grade_count[student.grade] += 1
        
        for grade in ['A', 'B', 'C', 'D', 'F']:
            grade_row = tk.Frame(grade_card, bg="white")
            grade_row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(grade_row, text=grade, font=("Arial", 10, "bold"), 
                    bg="white", fg=self.get_grade_color(grade), width=3).pack(side=tk.LEFT)
            tk.Label(grade_row, text=f"{grade_count[grade]} students", font=("Arial", 10),
                    bg="white", fg=self.colors['dark']).pack(side=tk.LEFT, padx=10)
        
        # Recent students table
        table_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(table_frame, text="Recent Student Records", font=("Arial", 14, "bold"),
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        # Create table
        self.create_students_table(table_frame, self.manager.students[:10])  # Show first 10 students
    
    def create_students_table(self, parent, students):
        table_container = tk.Frame(parent, bg="white", relief=tk.SUNKEN, bd=1)
        table_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Table header
        header_frame = tk.Frame(table_container, bg=self.colors['header'])
        header_frame.pack(fill=tk.X)
        
        headers = ["Student Name", "Student Code", "Coursework", "Exam", "Total %", "Grade"]
        widths = [25, 12, 12, 8, 10, 8]  # Character widths for proper alignment
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(header_frame, text=header, font=("Arial", 10, "bold"),
                    bg=self.colors['header'], fg="white", width=width, anchor=tk.CENTER).grid(
                    row=0, column=i, padx=1, pady=1, sticky="ew")
        
        # Configure header grid weights for proper resizing
        for i in range(len(headers)):
            header_frame.columnconfigure(i, weight=1)
        
        # Table content
        canvas = tk.Canvas(table_container, bg="white")
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display students
        for i, student in enumerate(students):
            row_color = "#f8fafc" if i % 2 == 0 else "white"
            row_frame = tk.Frame(scrollable_frame, bg=row_color)
            row_frame.pack(fill=tk.X)
            
            # Configure grid for proper column alignment
            for col in range(len(headers)):
                row_frame.columnconfigure(col, weight=1)
            
            # Student Name - Left aligned
            tk.Label(row_frame, text=student.name, font=("Arial", 9),
                    bg=row_color, width=25, anchor=tk.W).grid(row=0, column=0, padx=1, pady=2, sticky="w")
            
            # Student Code - Center aligned
            tk.Label(row_frame, text=student.student_code, font=("Arial", 9),
                    bg=row_color, width=12, anchor=tk.CENTER).grid(row=0, column=1, padx=1, pady=2)
            
            # Coursework Total - Center aligned
            tk.Label(row_frame, text=student.coursework_total, font=("Arial", 9),
                    bg=row_color, width=12, anchor=tk.CENTER).grid(row=0, column=2, padx=1, pady=2)
            
            # Exam Mark - Center aligned
            tk.Label(row_frame, text=student.exam_mark, font=("Arial", 9),
                    bg=row_color, width=8, anchor=tk.CENTER).grid(row=0, column=3, padx=1, pady=2)
            
            # Percentage - Center aligned
            tk.Label(row_frame, text=f"{student.percentage:.1f}%", font=("Arial", 9),
                    bg=row_color, width=10, anchor=tk.CENTER).grid(row=0, column=4, padx=1, pady=2)
            
            # Grade - Center aligned with color
            grade_color = self.get_grade_color(student.grade)
            tk.Label(row_frame, text=student.grade, font=("Arial", 9, "bold"),
                    bg=row_color, fg=grade_color, width=8, anchor=tk.CENTER).grid(row=0, column=5, padx=1, pady=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def get_grade_color(self, grade):
        colors = {
            'A': '#10b981',
            'B': '#3b82f6',
            'C': '#f59e0b',
            'D': '#f97316',
            'F': '#ef4444'
        }
        return colors.get(grade, '#64748b')
    
    def view_all_students(self):
        self.clear_content()
        
        header_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        header_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(header_frame, text="All Student Records", font=("Arial", 16, "bold"),
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        students = self.manager.get_all_students()
        
        # Create detailed table
        table_container = tk.Frame(self.content_frame, bg="white", relief=tk.SUNKEN, bd=1)
        table_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Table header
        header_frame = tk.Frame(table_container, bg=self.colors['header'])
        header_frame.pack(fill=tk.X)
        
        headers = ["Student Name", "Student Code", "CW1", "CW2", "CW3", "Coursework", "Exam", "Total %", "Grade"]
        widths = [20, 12, 6, 6, 6, 10, 8, 10, 8]  # Character widths
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(header_frame, text=header, font=("Arial", 10, "bold"),
                    bg=self.colors['header'], fg="white", width=width, anchor=tk.CENTER).grid(
                    row=0, column=i, padx=1, pady=1, sticky="ew")
        
        # Configure header grid
        for i in range(len(headers)):
            header_frame.columnconfigure(i, weight=1)
        
        # Table content
        canvas = tk.Canvas(table_container, bg="white")
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        total_percentage = 0
        
        for i, student in enumerate(students):
            row_color = "#f8fafc" if i % 2 == 0 else "white"
            row_frame = tk.Frame(scrollable_frame, bg=row_color)
            row_frame.pack(fill=tk.X)
            
            # Configure grid
            for col in range(len(headers)):
                row_frame.columnconfigure(col, weight=1)
            
            # Student Name - Left aligned
            tk.Label(row_frame, text=student.name, font=("Arial", 9),
                    bg=row_color, width=20, anchor=tk.W).grid(row=0, column=0, padx=1, pady=1, sticky="w")
            
            # Student Code - Center aligned
            tk.Label(row_frame, text=student.student_code, font=("Arial", 9),
                    bg=row_color, width=12, anchor=tk.CENTER).grid(row=0, column=1, padx=1, pady=1)
            
            # Individual coursework marks - Center aligned
            tk.Label(row_frame, text=student.mark1, font=("Arial", 9),
                    bg=row_color, width=6, anchor=tk.CENTER).grid(row=0, column=2, padx=1, pady=1)
            tk.Label(row_frame, text=student.mark2, font=("Arial", 9),
                    bg=row_color, width=6, anchor=tk.CENTER).grid(row=0, column=3, padx=1, pady=1)
            tk.Label(row_frame, text=student.mark3, font=("Arial", 9),
                    bg=row_color, width=6, anchor=tk.CENTER).grid(row=0, column=4, padx=1, pady=1)
            
            # Coursework Total - Center aligned
            tk.Label(row_frame, text=student.coursework_total, font=("Arial", 9),
                    bg=row_color, width=10, anchor=tk.CENTER).grid(row=0, column=5, padx=1, pady=1)
            
            # Exam Mark - Center aligned
            tk.Label(row_frame, text=student.exam_mark, font=("Arial", 9),
                    bg=row_color, width=8, anchor=tk.CENTER).grid(row=0, column=6, padx=1, pady=1)
            
            # Percentage - Center aligned
            tk.Label(row_frame, text=f"{student.percentage:.1f}%", font=("Arial", 9),
                    bg=row_color, width=10, anchor=tk.CENTER).grid(row=0, column=7, padx=1, pady=1)
            
            # Grade - Center aligned with color
            grade_color = self.get_grade_color(student.grade)
            tk.Label(row_frame, text=student.grade, font=("Arial", 9, "bold"),
                    bg=row_color, fg=grade_color, width=8, anchor=tk.CENTER).grid(row=0, column=8, padx=1, pady=1)
            
            total_percentage += student.percentage
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary
        summary_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        summary_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(summary_frame, text=f"Total Students: {len(students)} | Average Percentage: {total_percentage/len(students):.1f}%", 
                font=("Arial", 11, "bold"), bg=self.colors['light'], fg=self.colors['dark']).pack()

    # ... (rest of the methods remain the same as in the previous code)
    def view_individual_student(self):
        student_code = simpledialog.askinteger("Find Student", "Enter student code:")
        if student_code is None:
            return
        
        student = self.manager.get_student_by_code(student_code)
        if not student:
            messagebox.showerror("Error", f"Student with code {student_code} not found.")
            return
        
        self.clear_content()
        
        header_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        header_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(header_frame, text=f"Student Record - {student.name}", font=("Arial", 16, "bold"),
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        # Student details card
        details_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=1)
        details_frame.pack(fill=tk.X, pady=10, padx=50)
        
        details = [
            ("Student Code", student.student_code),
            ("Student Name", student.name),
            ("Coursework 1", f"{student.mark1}/20"),
            ("Coursework 2", f"{student.mark2}/20"),
            ("Coursework 3", f"{student.mark3}/20"),
            ("Coursework Total", f"{student.coursework_total}/60"),
            ("Exam Mark", f"{student.exam_mark}/100"),
            ("Overall Total", f"{student.total_score}/160"),
            ("Percentage", f"{student.percentage:.1f}%"),
            ("Grade", student.grade)
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(details_frame, bg="white")
            row_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(row_frame, text=label, font=("Arial", 11, "bold"),
                    bg="white", fg=self.colors['secondary'], width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=("Arial", 11),
                    bg="white", fg=self.colors['dark']).pack(side=tk.LEFT, padx=10)
    
    def show_highest_student(self):
        student = self.manager.get_highest_scoring_student()
        if not student:
            messagebox.showinfo("Info", "No students found.")
            return
        
        self.show_student_detail(student, "Highest Scoring Student", "🏆")
    
    def show_lowest_student(self):
        student = self.manager.get_lowest_scoring_student()
        if not student:
            messagebox.showinfo("Info", "No students found.")
            return
        
        self.show_student_detail(student, "Lowest Scoring Student", "📉")
    
    def show_student_detail(self, student, title, emoji):
        self.clear_content()
        
        header_frame = tk.Frame(self.content_frame, bg=self.colors['light'])
        header_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(header_frame, text=f"{emoji} {title}", font=("Arial", 16, "bold"),
                bg=self.colors['light'], fg=self.colors['dark']).pack(anchor=tk.W)
        
        # Student card
        card_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        card_frame.pack(fill=tk.X, pady=20, padx=100)
        
        # Header with grade
        card_header = tk.Frame(card_frame, bg=self.get_grade_color(student.grade))
        card_header.pack(fill=tk.X)
        
        tk.Label(card_header, text=f"{student.name} - Grade {student.grade}", 
                font=("Arial", 14, "bold"), bg=self.get_grade_color(student.grade), 
                fg="white").pack(pady=10)
        
        # Details
        details_frame = tk.Frame(card_frame, bg="white")
        details_frame.pack(fill=tk.X, padx=20, pady=15)
        
        details = [
            ("Student Code", student.student_code),
            ("Coursework Total", f"{student.coursework_total}/60"),
            ("Exam Mark", f"{student.exam_mark}/100"),
            ("Overall Score", f"{student.total_score}/160"),
            ("Percentage", f"{student.percentage:.1f}%")
        ]
        
        for label, value in details:
            row_frame = tk.Frame(details_frame, bg="white")
            row_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(row_frame, text=label, font=("Arial", 11),
                    bg="white", fg=self.colors['secondary'], width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=("Arial", 11, "bold"),
                    bg="white", fg=self.colors['dark']).pack(side=tk.LEFT)
    
    def sort_students(self):
        # Create sort dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Sort Students")
        dialog.geometry("300x200")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Sort Students By", font=("Arial", 14, "bold"),
                bg="white", fg=self.colors['dark']).pack(pady=20)
        
        sort_var = tk.StringVar(value="name")
        
        options = [
            ("Student Name", "name"),
            ("Student Code", "code"),
            ("Percentage", "percentage"),
            ("Grade", "grade")
        ]
        
        for text, value in options:
            tk.Radiobutton(dialog, text=text, variable=sort_var, value=value,
                          bg="white", font=("Arial", 11)).pack(anchor=tk.W, padx=50, pady=5)
        
        def apply_sort():
            sort_by = sort_var.get()
            students = self.manager.get_all_students()
            
            if sort_by == "name":
                students.sort(key=lambda x: x.name)
            elif sort_by == "code":
                students.sort(key=lambda x: x.student_code)
            elif sort_by == "percentage":
                students.sort(key=lambda x: x.percentage, reverse=True)
            elif sort_by == "grade":
                grade_order = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
                students.sort(key=lambda x: grade_order.get(x.grade, 0), reverse=True)
            
            dialog.destroy()
            self.view_all_students()
        
        tk.Button(dialog, text="Apply Sort", font=("Arial", 12),
                 bg=self.colors['primary'], fg="white", command=apply_sort).pack(pady=20)
    
    def add_student(self):
        self.show_add_student_dialog()
    
    def update_student(self):
        student_code = simpledialog.askinteger("Update Student", "Enter student code to update:")
        if student_code is None:
            return
        
        student = self.manager.get_student_by_code(student_code)
        if not student:
            messagebox.showerror("Error", f"Student with code {student_code} not found.")
            return
        
        self.show_update_student_dialog(student)
    
    def delete_student(self):
        student_code = simpledialog.askinteger("Delete Student", "Enter student code to delete:")
        if student_code is None:
            return
        
        student = self.manager.get_student_by_code(student_code)
        if not student:
            messagebox.showerror("Error", f"Student with code {student_code} not found.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete {student.name}?")
        if confirm:
            success, message = self.manager.delete_student(student_code)
            if success:
                self.manager.save_data()
                messagebox.showinfo("Success", message)
                self.show_dashboard()
            else:
                messagebox.showerror("Error", message)
    
    def show_add_student_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x500")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="Add New Student", font=("Arial", 16, "bold"),
                bg="white", fg=self.colors['dark']).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        entries = {}
        fields = [
            ("Student Code", "entry"),
            ("Student Name", "entry"), 
            ("Coursework 1 (0-20)", "entry"),
            ("Coursework 2 (0-20)", "entry"),
            ("Coursework 3 (0-20)", "entry"),
            ("Exam Mark (0-100)", "entry")
        ]
        
        for i, (label, field_type) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Arial", 10), bg="white").grid(row=i, column=0, sticky=tk.W, pady=8)
            entry = tk.Entry(form_frame, font=("Arial", 10), width=20)
            entry.grid(row=i, column=1, pady=8, padx=10)
            entries[label] = entry
        
        def submit():
            try:
                code = int(entries["Student Code"].get())
                name = entries["Student Name"].get()
                m1 = int(entries["Coursework 1 (0-20)"].get())
                m2 = int(entries["Coursework 2 (0-20)"].get())
                m3 = int(entries["Coursework 3 (0-20)"].get())
                exam = int(entries["Exam Mark (0-100)"].get())
                
                if not (1000 <= code <= 9999):
                    messagebox.showerror("Error", "Student code must be between 1000-9999")
                    return
                if not all(0 <= mark <= 20 for mark in [m1, m2, m3]):
                    messagebox.showerror("Error", "Coursework marks must be 0-20")
                    return
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be 0-100")
                    return
                
                success, message = self.manager.add_student(code, name, m1, m2, m3, exam)
                if success:
                    self.manager.save_data()
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.show_dashboard()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        tk.Button(dialog, text="Add Student", font=("Arial", 12), 
                 bg=self.colors['primary'], fg="white", command=submit).pack(pady=20)
    
    def show_update_student_dialog(self, student):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update {student.name}")
        dialog.geometry("400x500")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text=f"Update {student.name}", font=("Arial", 16, "bold"),
                bg="white", fg=self.colors['dark']).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        entries = {}
        fields = [
            ("Student Name", student.name),
            ("Coursework 1", student.mark1),
            ("Coursework 2", student.mark2), 
            ("Coursework 3", student.mark3),
            ("Exam Mark", student.exam_mark)
        ]
        
        for i, (label, value) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Arial", 10), bg="white").grid(row=i, column=0, sticky=tk.W, pady=8)
            entry = tk.Entry(form_frame, font=("Arial", 10), width=20)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, pady=8, padx=10)
            entries[label] = entry
        
        def submit():
            try:
                name = entries["Student Name"].get()
                m1 = int(entries["Coursework 1"].get())
                m2 = int(entries["Coursework 2"].get())
                m3 = int(entries["Coursework 3"].get())
                exam = int(entries["Exam Mark"].get())
                
                if not all(0 <= mark <= 20 for mark in [m1, m2, m3]):
                    messagebox.showerror("Error", "Coursework marks must be 0-20")
                    return
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be 0-100")
                    return
                
                success, message = self.manager.update_student(
                    student.student_code, name=name, mark1=m1, mark2=m2, mark3=m3, exam_mark=exam
                )
                if success:
                    self.manager.save_data()
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.show_dashboard()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        tk.Button(dialog, text="Update Student", font=("Arial", 12),
                 bg=self.colors['primary'], fg="white", command=submit).pack(pady=20)

def main():
    root = tk.Tk()
    app = ModernStudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()