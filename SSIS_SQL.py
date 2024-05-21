import tkinter as tk
import pandas as pd
from tkinter import ttk
import customtkinter 
from tkinter import messagebox
import mysql.connector

count = 0
class EditCourseWindow:
    def __init__(self, main_window, main_window_class, specific_course):
        process = Processing
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.specific_course = specific_course
        self.window = tk.Toplevel(self.main_window)
        self.window.title("Edit Course")
        self.window.geometry("730x75") 
        

        self.code_str = tk.StringVar(value = specific_course[0])
        self.desc_str = tk.StringVar(value = specific_course[1])

        self.code_label = tk.Label(self.window, text="Course Code:",padx=1, pady=1).grid(row=0,column=0)
        self.code_entry = tk.Entry(self.window, textvariable=self.code_str,width=20)
        self.code_entry.bind("<KeyRelease>", self.allow_edit_button)

        self.desc_label = tk.Label(self.window, text="Course Description:", padx=5, pady=1).grid(row=1, column=0)
        self.desc_entry = tk.Entry(self.window,textvariable=self.desc_str, width=100)
        self.desc_entry.bind("<KeyRelease>", self.allow_edit_button)

        self.edit_course_button = tk.Button(self.window, text="Edit Course", command=self.edit_course)
 
        self.code_entry.grid(row=0, column=1, padx=1, pady=1,sticky='w')
        self.desc_entry.grid(row=1, column=1, padx=1, pady=1)
        self.edit_course_button.grid(row=3, column=1, padx=1, pady=1, sticky='w')

        
    def edit_course(self):
        process = Processing
        self.course_data = process.read_table("courses")
        self.edited_course = [self.code_entry.get().upper(), self.desc_entry.get().upper(), self.specific_course[0].upper()]
        if self.desc_entry.get().upper() in [self.course_data[row][1] for row in range(0,len(self.course_data))] or self.code_entry.get() in [self.course_data[row][0] for row in range(0,len(self.course_data))]: 
                messagebox.showerror(title="Course Duplicate", message="Course already exists")
                self.window.lift()
        else:   
            if self.desc_entry.get() == self.specific_course[1] and self.code_entry.get() ==  self.specific_course[0]:
                messagebox.showerror(title="Course Duplicate", message="No Changes has been made")
                self.window.lift()
            else:
                result = messagebox.askquestion(title="Exit Edit Course", message="Is the edit final")
                if result == 'yes':
                    process = Processing
                    messagebox.showinfo(title="Action Successful", message="Course Edit is successful")
                    process.update(self.edited_course, "course")
                    self.course_data = process.read_table("courses")
                    self.main_window_class.set_desc_combo([val[1] + " (" +val[0]+")" for val in self.course_data])
                    self.students_list = process.read_table("students")
                    self.main_window_class.set_students("students")
                    self.main_window_class.set_courses("courses")
                    process.show_students(self.students_list)
                    self.window.destroy()
                else:
                    self.window.lift()

    def allow_edit_button(self, event):
        self.edited_course = [self.code_entry.get(), self.desc_entry.get()]
        if self.edited_course[0] == "" or self.edited_course[1] == "":
            self.edit_course_button['state'] = "disabled"
        else:
            self.edit_course_button['state'] = "normal"
        
        
    
class AddCourseWindow:
    def __init__(self, main_window, main_window_class):
        process = Processing
        self.courses_list = process.read_table("courses")
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.window = tk.Toplevel(self.main_window)
        self.window.title("Add Course")
        self.window.geometry("730x75")

        self.code_label = tk.Label(self.window, text="Course Code:", padx=1, pady=1).grid(row=0,column=0)
        self.code_entry = tk.Entry(self.window, width=20)
        self.code_entry.bind("<KeyRelease>", self.allow_add_button)

        self.desc_label = tk.Label(self.window, text="Course Description:", padx=1, pady=1).grid(row=1, column=0)
        self.desc_entry = tk.Entry(self.window, width=100)
        self.desc_entry.bind("<KeyRelease>",self.allow_add_button)

        self.add_course_button = tk.Button(self.window, text="Add Course", state=["disabled"], command=self.add_course)
        

        self.code_entry.grid(row=0, column=1, padx=1, pady=1,sticky='w')
        self.desc_entry.grid(row=1, column=1, padx=1, pady=1)
        self.add_course_button.grid(row=3, column=1, padx=1, pady=1, sticky='w')
    def add_course(self):
        process = Processing
        self.course_data = process.read_table("courses")
        self.added_course = [self.code_entry.get().upper(), self.desc_entry.get().upper()]
        
        if self.added_course[0] != "" and self.added_course[1] != "" and self.added_course[0] not in [self.course_data[row][0] for row in range(0,len(self.course_data))] and self.added_course[1] not in [self.course_data[row][1] for row in range(0,len(self.course_data))]:
            result = messagebox.askquestion(title="Exit Add Course", message="Is the Added Course final")
            if result == "yes":
                messagebox.showinfo(title="Action Succesful", message="Course Added succesfully")
                process.insert_new(self.added_course, "courses")
                self.course_data = process.read_table("courses")
                self.students_list = process.read_table("students")
                self.main_window_class.set_students("students")
                self.main_window_class.set_courses("courses")
                self.main_window_class.set_desc_combo([val[1] + " (" +val[0]+")" for val in self.course_data])
            else:
                self.window.lift()
        else:
            messagebox.showerror(title="Course Duplicate", message="Course already exists")

    def allow_add_button(self, event):
        self.added_course = [self.code_entry.get(), self.desc_entry.get()]
        if self.added_course[0] != "" and self.added_course[1] != "" :
            self.add_course_button['state'] = "normal"
        else:
            self.add_course_button['state'] = "disabled"
   
        
class AddStudentWindow:
    def __init__(self, main_window, main_window_class):
        process = Processing
        self.course_data = process.read_table("courses")
        self.student_data = process.read_table("students")
        year_range = ['1', '2', '3', '4']
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.window = tk.Toplevel(self.main_window)
        self.label_frame = tk.Frame(self.window)
        self.entry_frame = tk.Frame(self.window)
        self.window.title("Edit Student")
        self.window.geometry("300x160")
        self.window.resizable(False, False)

        self.entry_dict ={}
        self.entry_list = ["ID Number:", "Name:", "Year Level:", "Gender:"]
        for value in self.entry_list:
            if value == "ID Number:":
                valid_entry = self.window.register(process.valid_id_entry)
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, validate="key", validatecommand=(valid_entry, '%P'), width=30)
                self.entry.grid(row=self.entry_list.index(value), column=1)
                self.entry_dict[value] = self.entry
                self.entry.bind("<KeyRelease>", self.allow_add_button)
            elif value == "Year Level:":
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.year_combo = ttk.Combobox(self.entry_frame, width=27, values=year_range, state="readonly")
                self.year_combo.grid(row=self.entry_list.index(value),column=1)
                self.year_combo.bind("<<ComboboxSelected>>", self.allow_add_button)
                self.entry_dict[value] = self.year_combo
            else:
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, width=30)
                self.entry.grid(row=self.entry_list.index(value),column=1)
                self.entry.bind("<KeyRelease>", self.allow_add_button)
                self.entry_dict[value] = self.entry

        self.enrollment_status_var = tk.StringVar(value="Not Enrolled")
        self.enroll_label = tk.Label(self.label_frame, text="Enrollment Status:")
        self.enroll_label.grid(row=5, column=0)
        self.enroll_combo = ttk.Combobox(self.entry_frame, textvariable=self.enrollment_status_var,
                                        values=["Enrolled", "Not Enrolled"], state="readonly", width=27)
        self.enroll_combo.grid(row=5, column=1)
        self.enroll_combo.bind("<<ComboboxSelected>>", self.allow_course_combo)

        self.course_var = tk.StringVar(value="")
        self.courses_label = tk.Label(self.label_frame, text="Course:", width=10)
        self.courses_label.grid(row=6,column=0)
        self.courses_combo = ttk.Combobox(self.entry_frame, width=27, textvariable=self.course_var, values=[])
        self.set_code_combo([self.course_data[row][0] for row in range(0,len(self.course_data))])
        self.courses_combo.grid(row=6,column=1)
        self.courses_combo.bind("<<ComboboxSelected>>", self.allow_add_button)
        
        if self.enroll_combo.get() != "Enrolled":
            self.courses_combo.set("None")
            self.courses_combo["state"] = "disabled"
        else:
            self.courses_combo["state"] = "readonly"

        self.add_button = tk.Button(self.window, text="Edit", command=self.add_student)
        
        self.label_frame.grid(row=0, column=0)
        self.entry_frame.grid(row=0, column=1)
        self.add_button.grid(row=5, column=1)

    def add_student(self):
        process = Processing
        self.courses_var = self.courses_combo.get()
        self.enrollment_status_var = self.enroll_combo.get()
        main = MainWindow(self.main_window)
        self.new_info = [self.entry_dict["ID Number:"].get(), self.entry_dict["Name:"].get(), 
                        self.entry_dict["Year Level:"].get(), 
                        self.entry_dict["Gender:"].get(), 
                        self.enrollment_status_var, self.courses_var]
        
        result = messagebox.askquestion(title="Exit Edit Student", message="Is the Edit final")
        try:
            if result == "yes":
                process.insert_new(self.new_info, "student")
                self.students_list = process.read_table("students")
                self.main_window_class.set_students("students")
                self.main_window_class.set_courses("courses")
                process.show_students(self.students_list)
                main.set_id_combo([val[1] + " (" +val[0]+")" for val in self.students_list])
                self.window.destroy()
            else:
                self.window.lift()
                self.enroll_combo.set(self.enrollment_status_var) 
            pass
        except(mysql.connector.errors.IntegrityError):
            messagebox.showwarning(title="Invalid Input", message="ID Number already exists")
            self.window.lift()
        else:
            if result == "yes":
                messagebox.showinfo(title="Action Succesful", message="Edit Successful")
                self.window.destroy()
            else:
                self.window.lift()
                self.enroll_combo.set(self.enrollment_status_var) 

    def allow_add_button(self, event):
        self.id_str = self.entry_dict["ID Number:"].get()
        id_to_int = self.id_str[0:3] + self.id_str[5:8]
        if all(entry.get() for entry in self.entry_dict.values()) and len(self.entry_dict["ID Number:"].get())==9 and self.id_str[4] == "-" :
            self.add_button["state"] = "normal"
            try:
                id_int = int(id_to_int)
                pass
            except(ValueError):
                messagebox.showwarning(title="Invalid Input", message="ID Number isn't the expected format (Ex. 1111-2222)")
                self.window.lift()
        else:
            self.add_button["state"] = "disabled"  

    def allow_course_combo(self, event):
        picked = self.enroll_combo.get()
        if picked == "Enrolled" and self.courses_combo.get() == "None":
            self.courses_combo.set("")
            self.courses_combo["state"] = "readonly"
            self.add_button["state"] = "disabled"
        else:
            self.courses_combo.set("None")
            self.courses_combo["state"] = "disabled"
            self.add_button["state"] = "normal"

    def set_code_combo(self, val):
        self.courses_combo['values'] = val

        
   

class EditStudentWindow:
    def __init__(self, main_window, main_window_class,specific_student):
        process = Processing
        self.course_data = process.read_table("courses")
        year_range = ['1', '2', '3', '4']
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.window = tk.Toplevel(self.main_window)
        self.label_frame = tk.Frame(self.window)
        self.entry_frame = tk.Frame(self.window)
        self.window.title("Edit Student")
        self.window.geometry("300x160")
        self.window.resizable(False, False)

        self.id_str = tk.StringVar(self.window, value=specific_student[0])
        self.name_str = tk.StringVar(self.window, value=specific_student[1])
        self.year_str = tk.StringVar(self.window, value=specific_student[2])
        self.gender_str = tk.StringVar(self.window, value=specific_student[3])
        self.enroll_str = tk.StringVar(self.window, value=specific_student[4])
        self.course_str = tk.StringVar(self.window, value=specific_student[5])
        self.entry_dict ={}
        self.entry_list = ["ID Number:", "Name:", "Year Level:", "Gender:"]
        self.entry_val = [self.id_str, self.name_str, self.year_str, self.gender_str]
       
        for value in self.entry_list:
            if value == "ID Number:":
                valid_entry = self.window.register(process.valid_id_entry)
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, textvariable=self.entry_val[self.entry_list.index(value)], validate="key", validatecommand=(valid_entry, '%P'), state="disabled", width=30)
                self.entry.grid(row=self.entry_list.index(value), column=1)
                self.entry_dict[value] = self.entry
                self.entry.bind("<KeyRelease>", self.allow_edit_button)
            elif value == "Year Level:":
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.year_combo = ttk.Combobox(self.entry_frame, textvariable=self.entry_val[self.entry_list.index(value)], width=27, values=year_range, state="readonly")
                self.year_combo.grid(row=self.entry_list.index(value),column=1)
                self.year_combo.bind("<<ComboboxSelected>>", self.allow_edit_button)
                self.entry_dict[value] = self.year_combo
            else:
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, textvariable=self.entry_val[self.entry_list.index(value)],width=30)
                self.entry.grid(row=self.entry_list.index(value),column=1)
                self.entry.bind("<KeyRelease>", self.allow_edit_button)
                self.entry_dict[value] = self.entry

        self.enroll_label = tk.Label(self.label_frame, text="Enrollment Status:")
        self.enroll_label.grid(row=5, column=0)
        self.enroll_combo = ttk.Combobox(self.entry_frame, textvariable=self.enroll_str,
                                        values=["Enrolled", "Not Enrolled"], state="readonly", width=27)
        self.enroll_combo.grid(row=5, column=1)
        self.enroll_combo.bind("<<ComboboxSelected>>", self.allow_course_combo)
        self.courses_label = tk.Label(self.label_frame, text="Course:", width=10)
        self.courses_label.grid(row=6,column=0)
        self.courses_combo = ttk.Combobox(self.entry_frame, width=27, textvariable=self.course_str, values=[])
        self.set_code_combo([self.course_data[row][0] for row in range(0,len(self.course_data))])
        self.courses_combo.grid(row=6,column=1)
        self.courses_combo.bind("<<ComboboxSelected>>", self.allow_edit_button)
        
        if self.enroll_combo.get() != "Enrolled":
            self.courses_combo.set("None")
            self.courses_combo["state"] = "disabled"
        else:
            self.courses_combo["state"] = "readonly"

        self.edit_button = tk.Button(self.window, text="Edit", command=self.edit_student)
        
        self.label_frame.grid(row=0, column=0)
        self.entry_frame.grid(row=0, column=1)
        self.edit_button.grid(row=5, column=1)
    def edit_student(self):
        process = Processing
        self.courses_var = self.courses_combo.get()
        self.enrollment_status_var = self.enroll_combo.get()
        main = MainWindow(self.main_window)
        self.new_info = [self.entry_dict["Name:"].get(), 
                        self.entry_dict["Year Level:"].get(), 
                        self.entry_dict["Gender:"].get(), 
                        self.enrollment_status_var, self.courses_var, self.entry_dict["ID Number:"].get()]
        
        result = messagebox.askquestion(title="Exit Edit Student", message="Is the Edit final")
        if result == "yes":
            process.update(self.new_info, "student")
            self.students_list = process.read_table("students")
            self.main_window_class.set_students("students")
            self.main_window_class.set_courses("courses")
            process.show_students(self.students_list)
            main.set_id_combo([val[1] + " (" +val[0]+")" for val in self.students_list])
            messagebox.showinfo(title="Action Succesful", message="Edit Successful")
            self.window.destroy()
        else:
            self.window.lift()

    def allow_edit_button(self, event):
        if all(entry.get() for entry in self.entry_dict.values()):
            self.edit_button["state"] = "normal"
        else:
            self.edit_button["state"] = "disabled"  

    def allow_course_combo(self, event):
        picked = self.enroll_combo.get()
        if picked == "Enrolled" and self.courses_combo.get() == "None":
            self.courses_combo.set("")
            self.courses_combo["state"] = "readonly"
            self.edit_button["state"] = "disabled"
        else:
            self.courses_combo.set("None")
            self.courses_combo["state"] = "disabled"
            self.edit_button["state"] = "normal"

    def set_code_combo(self, val):
        self.courses_combo['values'] = val

class MainWindow:
    def __init__(self, window):
        process = Processing
        self.students_list = process.read_table("students")
        self.courses_list = process.read_table("courses")
        self.window = window
        self.desc_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.top_frame = tk.Frame(window, padx=5)
        self.course_frame = tk.Frame(self.top_frame, pady=5)
        self.student_frame = tk.Frame(self.top_frame, pady=5)
        self.desc_label = tk.Label(self.course_frame, text="Course Description (Course Code):")
        self.desc_list = ttk.Combobox(self.course_frame, textvariable=self.desc_var,values=[], width=110, justify="center")
        self.set_desc_combo([val[1] + " (" +val[0]+")" for val in self.courses_list])
        self.desc_list.bind("<KeyRelease>", self.desc_search)
        self.add_course = tk.Button(self.course_frame, text="Add Course",command=self.open_add_course_window, height=1, padx=5, pady=5)
        self.edit_course = tk.Button(self.course_frame, text="Edit Course",command=self.open_edit_course_window,height=1, padx=5, pady=5)
        self.del_course = tk.Button(self.course_frame, text="Delete Course",command=self.delete_course,height=1, padx=5, pady=5)
        self.separation = tk.Label(self.top_frame, text="|", height=2, padx=5, pady=5)
        self.stud_label = tk.Label(self.student_frame, text="Name (ID Number):")
        self.stud_list = ttk.Combobox(self.student_frame, textvariable=self.id_var,values=[], width=40, justify="center")
        self.set_id_combo([val[1] + " (" +val[0]+")" for val in self.students_list])
        self.stud_list.bind("<KeyRelease>", self.student_search)
        self.add_stud = tk.Button(self.student_frame, text="Add Student",command=self.open_add_student_window,height=1, padx=5, pady=5)
        self.edit_stud = tk.Button(self.student_frame, text="Edit Student", command=self.open_edit_student_window, height=1, padx=5, pady=5)
        self.del_stud = tk.Button(self.student_frame, text= "Delete Student",command=self.delete_student,height=1, padx=5, pady=5)
        

        process.show_students(self.students_list)

        self.top_frame.grid(row=0,column=1, padx=10, pady=10)
        self.course_frame.grid(row=0, column=0)
        self.student_frame.grid(row=0, column=2)
        self.desc_label.grid(row=0, column=1)
        self.desc_list.grid(row=1, column=0, columnspan=3)
        self.add_course.grid(row=2,column=0, pady=5)
        self.edit_course.grid(row=2, column=1, pady=5)
        self.del_course.grid(row=2,column=2, pady=5)
        self.separation.grid(row=0, column=1, rowspan=2)

        self.stud_label.grid(row=0, column=1)
        self.stud_list.grid(row=1, column=0, columnspan=3)
        self.add_stud.grid(row=2, column=0, padx=5, pady=5)
        self.edit_stud.grid(row=2, column=1, padx=5, pady=5)
        self.del_stud.grid(row=2, column=2, padx=5, pady=5)

        
    
    def set_id_combo(self, val):
        self.stud_list['values'] = val

    def set_desc_combo(self, val):
        self.desc_list['values'] = val
        self.desc_list.set("")

    def set_students(self, val):
        process = Processing
        self.students_list = process.read_table(val)
        return self.students_list

    def set_courses(self,val):
        process = Processing
        self.courses_list = process.read_table(val)
        return self.courses_list

    def desc_search(self,event):
        process = Processing
        self.courses_list = process.read_table("courses")
        value = event.widget.get()
        if value == '':
            self.desc_list['values'] = [val[1] + " (" +val[0]+")" for val in self.courses_list]
        else:
            items = []
            for data in [val[1] + " (" +val[0]+")" for val in self.courses_list]:
                if value.upper() in data:
                    items.append(data)
            self.desc_list['values'] = items
       
    def student_search(self, event):
        process = Processing
        self.students_list = process.read_table("students")
        value = event.widget.get()
        if value == '':
            self.stud_list['values'] = [val[1] + " (" +val[0]+")" for val in self.students_list]
        else:
            items = []
            for data in [val[1] + " (" +val[0]+")" for val in self.students_list]:
                if value.lower() in data.lower():
                    items.append(data)
            self.stud_list['values'] = items
       

    def open_edit_student_window(self):
        process = Processing
        self.students_list = process.read_table("students")
        self.courses_list = process.read_table("courses")
        if self.stud_list.get()== "":
            messagebox.showerror(title='Button Error', message="No Student picked!")
        elif self.stud_list.get() not in [val[1] + " (" +val[0]+")" for val in self.students_list]:
            messagebox.showerror(title='Button Error', message="No existing Student picked!")
        else:
            self.get_id = self.stud_list.get().split(' (')
            self.specific_id = self.get_id[1].split(')')
            specific_student = process.get_specific_stud(self.specific_id[0])
            EditStudentWindow(self.window, self, specific_student)

    def open_add_student_window(self):
        add_student_window = AddStudentWindow(self.window, self)
    
    def delete_student(self):
        process = Processing
        self.students_list = process.read_table("students")
        self.courses_list = process.read_table("courses")
        if self.stud_list.get() == "":
            messagebox.showerror(title='Button Error', message="No Student picked!")
        elif self.stud_list.get() not in [val[1] + " (" +val[0]+")" for val in self.students_list]:
            messagebox.showerror(title='Button Error', message="No existing Student picked!")
        else:
            self.get_id = self.stud_list.get().split(' (')
            self.specific_id = self.get_id[1].split(')')
            specific_student = self.specific_id[0]
            messagebox.showinfo(title="Action Successful", message="Student successfully deleted")
            process.delete_row(specific_student, "id")
            self.students_list = process.read_table("students")
            self.stud_list['textvariable'] = tk.StringVar(value="")
            process.show_students(self.students_list)
            self.set_id_combo([val[1] + " (" +val[0]+")" for val in self.students_list])
            
        
    def open_add_course_window(self):
        add_course_window = AddCourseWindow(self.window, self)

    def open_edit_course_window(self):
        process = Processing
        self.students_list = process.read_table("students")
        self.courses_list = process.read_table("courses")
        if self.desc_list.get()== "":
            messagebox.showerror(title='Button Error', message="No Course picked!")
        elif self.desc_list.get() not in [val[1] + " (" +val[0]+")" for val in self.courses_list]:
            messagebox.showerror(title='Button Error', message="No existing Course picked!")
        else:
            self.get_code = self.desc_list.get().split(' (')
            self.specific_course = self.get_code[1].split(')')
            specific_course = process.get_specific_course(self.specific_course[0])
            EditCourseWindow(self.window, self, specific_course)

    def delete_course(self):
        process = Processing
        self.students_list = process.read_table("students")
        self.courses_list = process.read_table("courses")
        if self.desc_list.get() == "":
            messagebox.showerror(title='Button Error', message="No Course picked!")
        elif self.desc_list.get() not in [val[1] + " (" +val[0]+")" for val in self.courses_list]:
            messagebox.showerror(title='Button Error', message="No existing Course picked!")
        else:
            self.get_code = self.desc_list.get().split(' (')
            self.specific_course = self.get_code[1].split(')')
            specific_course = process.get_specific_course(self.specific_course[0])
            messagebox.showinfo(title="Action Successful", message="Course successfully deleted")
            process.delete_row(specific_course[0], "code")
            self.desc_list['textvariable'] = tk.StringVar(value="")
            self.students_list = process.read_table("students")
            self.courses_list = process.read_table("courses")
            process.show_students(self.students_list)
            self.set_desc_combo([val[1] + " (" +val[0]+")" for val in self.courses_list])

class Processing:
    def read_table(table):
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        specific_table = connect.cursor()
        if table == "students":
            specific_table.execute("SELECT * FROM students")
            return specific_table.fetchall()
        elif table == "courses":
            specific_table.execute("SELECT * FROM courses")
            return specific_table.fetchall()
        else:
            messagebox.showwarning(message="table doesn't exist")
        connect.commit()
        connect.close()
    def get_specific_stud(id_num):
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        students = connect.cursor()
        students.execute("SELECT * FROM students WHERE ID_Number = %(id_num)s", {'id_num':id_num})
        stud_tuple = students.fetchone()
        specific_student = []
        for val in stud_tuple:
            specific_student.append(val)
        connect.commit()
        connect.close()
        return specific_student
    def get_specific_course(course_code):
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        courses = connect.cursor()
        courses.execute("SELECT * FROM courses WHERE Course_Code = %(code)s", {'code':course_code})
        courses_tuple = courses.fetchone()
        specific_course = []
        for val in courses_tuple:
            specific_course.append(val)
        connect.commit()
        connect.close()
        return specific_course
    
    def get_ids():
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        id = connect.cursor()
        id.execute("SELECT ID_Number FROM students")
        id_tuple = id.fetchall()
        ids_list = []
        for val in id_tuple:
            ids_list.append(val[0])
        connect.commit()
        connect.close()
        return ids_list

    def show_students(students):
        process = Processing
        students_frame = customtkinter.CTkScrollableFrame(window, height=450, width=700,fg_color='#d9d9d9')
        showlist = []
        id_sort = tk.Button(students_frame,text="ID Number", command=process.id_sort)
        name_sort = tk.Button(students_frame,text="Student Name", command=process.name_sort)
        year_sort = tk.Button(students_frame,text="Year Level", command=process.year_sort)
        gender_sort = tk.Button(students_frame,text="Gender", command=process.gender_sort)
        enroll_sort = tk.Button(students_frame,text="Enrollement Status", command=process.enroll_sort)
        course_sort = tk.Button(students_frame,text="Course_Code", command=process.course_sort)
        for i, row in enumerate(students, start=1):
            showlist.append(row[0])
            for col in range(0, 6):
                tk.Label(students_frame, text=row[col], bg="#d9d9d9").grid(row=i, column=col, padx=17, pady=3)

        students_frame.grid(row=2, column=1, padx=45, pady=10)
        students_frame.grid_propagate()
        id_sort.grid(row=0,column=0,padx=17)
        name_sort.grid(row=0,column=1,padx=17)
        year_sort.grid(row=0,column=2,padx=17)
        gender_sort.grid(row=0,column=3,padx=17)
        enroll_sort.grid(row=0,column=4,padx=17)
        course_sort.grid(row=0,column=5,padx=17)
        
    def id_sort():
        global count 
        count +=1
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                    port='3306', database='myssis')
        sort_cur = connect.cursor()
        if (count%2) == 0:
            sort_cur.execute("SELECT * FROM students ORDER BY ID_Number")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        else:
            sort_cur.execute("SELECT * FROM students ORDER BY ID_Number DESC")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        connect.commit()
    def name_sort():
        global count 
        count +=1
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                    port='3306', database='myssis')
        sort_cur = connect.cursor()
        if (count%2) == 0:
            sort_cur.execute("SELECT * FROM students ORDER BY Student_Name")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        else:
            sort_cur.execute("SELECT * FROM students ORDER BY Student_Name DESC")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        connect.commit()
    def year_sort():
        global count 
        count +=1
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                    port='3306', database='myssis')
        sort_cur = connect.cursor()
        if (count%2) == 0:
            sort_cur.execute("SELECT * FROM students ORDER BY Year_Level")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        else:
            sort_cur.execute("SELECT * FROM students ORDER BY Year_Level DESC")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        connect.commit()
    def gender_sort():
        global count 
        count +=1
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                    port='3306', database='myssis')
        sort_cur = connect.cursor()
        if (count%2) == 0:
            sort_cur.execute("SELECT * FROM students ORDER BY Gender")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        else:
            sort_cur.execute("SELECT * FROM students ORDER BY Gender DESC")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        connect.commit()
    def enroll_sort():
        global count 
        count +=1
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                    port='3306', database='myssis')
        sort_cur = connect.cursor()
        if (count%2) == 0:
            sort_cur.execute("SELECT * FROM students ORDER BY Enrollment_Status")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        else:
            sort_cur.execute("SELECT * FROM students ORDER BY Enrollment_Status DESC")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        connect.commit()
    def course_sort():
        global count 
        count +=1
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                    port='3306', database='myssis')
        sort_cur = connect.cursor()
        if (count%2) == 0:
            sort_cur.execute("SELECT * FROM students ORDER BY Course_Code")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        else:
            sort_cur.execute("SELECT * FROM students ORDER BY Course_Code DESC")
            sort = sort_cur.fetchall()
            process.show_students(sort)
        connect.commit()
    def update(update_list, table):
        process = Processing
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        update_row = connect.cursor()
        if table == "student":
            #modify code to allow null value in students table
            if update_list[4] == "None":
                update_row.execute("UPDATE students SET Student_Name = %(name)s, Year_Level = %(year)s, Gender = %(gender)s, Enrollment_Status = %(enroll)s, Course_Code = NULL WHERE ID_Number = %(id)s", 
                                   {'name':update_list[0],
                                    'year':update_list[1],
                                    'gender':update_list[2],
                                    'enroll':update_list[3],
                                    'id':update_list[5]
                                    })
            else:
                update_row.execute("UPDATE students SET Student_Name = %s, Year_Level = %s, Gender = %s, Enrollment_Status = %s, Course_Code = %s WHERE ID_Number = %s", update_list)
        elif table == "course":
            update_state = "CALL Update_Course(%s, %s, %s)"
            update_val = (update_list[0],update_list[1],update_list[2]) 
            update_row.execute(update_state,update_val)
        connect.commit()
        connect.close()
    def insert_new(new_list, table):
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        new_row = connect.cursor()
        if table == "student":
            if new_list[5] == "None":
                new_row.execute("INSERT INTO students (ID_Number, Student_Name, Year_Level, Gender, Enrollment_Status, Course_Code)"
                                "VALUES (%(id)s, %(name)s, %(year)s, %(gender)s, %(enroll)s, NULL)", {
                    'id': new_list[0],
                    'name': new_list[1],
                    'year': new_list[2],
                    'gender': new_list[3],
                    'enroll': new_list[4]
                })
            else:
                new_row.execute("INSERT INTO students (ID_Number, Student_Name, Year_Level, Gender, Enrollment_Status, Course_Code)"
                                "VALUES (%(id)s, %(name)s, %(year)s, %(gender)s, %(enroll)s, %(course)s)", {
                    'id': new_list[0],
                    'name': new_list[1],
                    'year': new_list[2],
                    'gender': new_list[3],
                    'enroll': new_list[4],
                    'course': new_list[5]
                })

        elif table == "courses":
            new_row.execute("INSERT INTO courses (Course_Code, Course_Description) VALUES (%(code)s, %(description)s)", {
                'code': new_list[0],
                'description': new_list[1]
            })
        connect.commit()
        connect.close()

    def delete_row(key, type):
        connect = mysql.connector.connect(host='localhost', user='root', password='15ITH6Corei5',
                                     port='3306', database='myssis')
        delete_row = connect.cursor()
        if type == "id":
            delete_row.execute("DELETE FROM students WHERE ID_Number = %(key)s", {'key':key})
        elif type == "code":
            delete_comm = "CALL Delete_Course(%s)"
            delete_row.execute(delete_comm, (key,))
        connect.commit()
        connect.close()
    def valid_id_entry(entry):
        return len(entry) <= 9

    
if __name__ == "__main__":
        window = tk.Tk()
        main_window = MainWindow(window)
        window.title("Simple Student Information System")
        window.geometry("1040x600")
        window.configure(bg="Maroon")
        window.resizable(False,False)
        window.mainloop()
