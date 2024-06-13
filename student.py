import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

class StudentInformationSystemGUI:
    def __init__(self, root):
        self.root = root
        self.connection = create_connection()
        if self.connection:
            self.create_title_label()
            self.load_courses_from_database() 
        else:
            messagebox.showerror("Error", "Failed to connect to the database. Application will now exit.")
            root.destroy()

    def load_courses_from_database(self):
        self.course_options = []
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT course_code FROM courses")
                    courses = cursor.fetchall()
                    self.course_options = [course[0] for course in courses]
            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Failed to fetch courses from the database.")

        self.selected_course = tk.StringVar(self.root)

        if self.course_options:
            self.selected_course.set(self.course_options[0])
            self.course_dropdown = tk.OptionMenu(self.root, self.selected_course, *self.course_options)
        else:
            self.selected_course.set("None")
            self.course_dropdown = tk.OptionMenu(self.root, self.selected_course, "None")

        self.course_dropdown.config(font=("Arial", 12), bg="white", fg="black")
        self.course_dropdown.place(x=160, y=340, width=250)

    def check_course_code(self, course_code):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
                    if cursor.fetchone():
                        return True
            except Error as e:
                print(f"Error: {e}")
        return False

    def create_title_label(self):
        title_label = tk.Label(
            self.root,
            text="STUDENT REGISTRATION",
            font=("Arial", 35, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            fg="white",
            padx=89
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Labels and Entry fields
        self.labels = ["Student ID", "First Name", "Last Name", "Gender", "Year Level"]
        self.entries = {label: tk.Entry(self.root, font=("Arial", 17,), bg="white", fg="black") for label in self.labels}

        self.tosearch_label = tk.Label(self.root, text="To Search for Student Information:", font=("Arial", 17, "bold"), bg="#A6A6A6", fg="black")
        self.tosearch_label.place(x=450, y=90)

        self.search_label = tk.Label(self.root, text="Enter Keyword to Search:", font=("Arial", 17), bg="#A6A6A6", fg="black")
        self.search_label.place(x=450, y=140)

        self.search_entry = tk.Entry(self.root, font=("Arial", 17), bg="white", fg="black")
        self.search_entry.place(x=720, y=140, width=230)

        # Place labels and entry fields on the GUI
        x_label_position = 10
        x_entry_position = 160
        y_start_position = 100
        y_increment = 50
        entry_width = 250

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(
                self.root, text=label, font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black"
            )
            label_widget.place(x=x_label_position, y=y_start_position + i * y_increment)

            entry_widget = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
            entry_widget.place(x=x_entry_position, y=y_start_position + i * y_increment, width=entry_width)
            self.entries[label] = entry_widget

        # Gender dropdown
        self.gender_label = tk.Label(self.root, text="Gender", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.gender_label.place(x=x_label_position, y=y_start_position + 3 * y_increment)

        self.gender_variable = tk.StringVar(self.root)
        self.gender_variable.set("Male")  # Default value
        self.gender_dropdown = tk.OptionMenu(self.root, self.gender_variable, "Male", "Female")
        self.gender_dropdown.config(font=("Arial", 12), bg="white", fg="black")
        self.gender_dropdown.place(x=x_entry_position, y=y_start_position + 3 * y_increment, width=entry_width)

#----------------------------------------------------- BUTTONS --------------------------------------------------------

        # Add Student button
        self.add_button = tk.Button(self.root, text="ADD", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.add_student)
        self.add_button.place(x=50, y=470, width=150)

        # Delete button
        self.delete_button = tk.Button(self.root, text="DELETE", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.delete_student)
        self.delete_button.place(x=50, y=520, width=150)

        # Edit and Save buttons
        self.edit_button = tk.Button(self.root, text="EDIT", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.edit_student)
        self.edit_button.place(x=250, y=470, width=150)

        self.save_button = tk.Button(self.root, text="SAVE", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.save_changes)
        self.save_button.place(x=250, y=520, width=150)

        # Search Button
        self.search_button = tk.Button(self.root, text="SEARCH", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.search_student)
        self.search_button.place(x=960, y=140, width=100)

        # Cancel button
        self.cancel_button = tk.Button(self.root, text="CANCEL", font=("Arial", 13, "bold"), bg="#2E2D2D", fg="white", command=self.cancel_edit)
        self.cancel_button.place(x=100, y=400, width=250)

#--------------------------------------------------------------- TREEVIEW -------------------------------------------------------

        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID Number", "First Name", "Last Name", "Gender", "Course", "Year Level"), show="headings", selectmode="extended")

        self.tree.heading("ID Number", text="ID Number", anchor=tk.CENTER)
        self.tree.heading("First Name", text="First Name", anchor=tk.CENTER)
        self.tree.heading("Last Name", text="Last Name", anchor=tk.CENTER)
        self.tree.heading("Gender", text="Gender", anchor=tk.CENTER)
        self.tree.heading("Course", text="Course", anchor=tk.CENTER)
        self.tree.heading("Year Level", text="Year Level", anchor=tk.CENTER)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview.Heading", background="#2E2D2D",  foreground="white", font=("Arial", 12, "bold"))

        self.tree.column("ID Number", width=70)
        self.tree.column("First Name", width=100) 
        self.tree.column("Last Name", width=100)
        self.tree.column("Gender", width=50)
        self.tree.column("Course", width=50)
        self.tree.column("Year Level", width=50)
        self.tree.place(x=440, y=200, width=600, height=460)

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=1040, y=200, height=460)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.load_students()

        self.selected_item = None

    def load_students(self):
        self.tree.delete(*self.tree.get_children())

        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM students")
                    students = cursor.fetchall()
                    for student in students:
                        self.tree.insert("", "end", values=student)
            except Error as e:
                print(f"Error: {e}")

    def edit_student(self):
        selected_items = self.tree.selection()
        if len(selected_items) != 1:
            messagebox.showwarning("Warning", "Please select only one student to edit.")
            return

        # Store the ID of the selected item
        self.selected_item = selected_items[0]
        student_id = self.tree.item(self.selected_item, "values")[0]

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE idNum = %s", (student_id,))
            student = cursor.fetchone()

            if student:
                self.entries["Student ID"].delete(0, "end")
                self.entries["Student ID"].insert(0, student["idNum"])

                self.entries["First Name"].delete(0, "end")
                self.entries["First Name"].insert(0, student["first_name"])

                self.entries["Last Name"].delete(0, "end")
                self.entries["Last Name"].insert(0, student["last_name"])

                self.gender_variable.set(student["gender"])
                self.selected_course.set(student["course_code"])
                self.entries["Year Level"].delete(0, "end")
                self.entries["Year Level"].insert(0, student["yearLevel"])
            else:
                messagebox.showwarning("Warning", "Student not found in the database.")
        except Error as e:
            messagebox.showerror("Error", f"Failed to fetch student details: {e}")
        finally:
            cursor.close()


    def clear_entry_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return

        # Retrieve edited values from entry fields and dropdowns
        edited_values = [
            self.entries["Student ID"].get(),
            self.entries["First Name"].get(),
            self.entries["Last Name"].get(),
            self.gender_variable.get(),
            self.selected_course.get(),
            self.entries["Year Level"].get()
        ]

        original_idNum = self.tree.item(self.selected_item, "values")[0]

        new_idNum = edited_values[0]

        # Check if the new idNum already exists in the database and it's different from the original idNum
        if new_idNum != original_idNum and self.check_IDNo(new_idNum):
            messagebox.showerror("Error", f"Student ID '{new_idNum}' already exists.")
            return

        # Update the corresponding row in the Treeview widget
        self.tree.item(self.selected_item, values=edited_values)

        # Check if the idNum has been modified
        if new_idNum != original_idNum:
            # Update the corresponding row in the database
            self.update_student_in_database(edited_values, original_idNum)
        else:
            # Update other student information without changing idNum
            self.update_student_in_database(edited_values, new_idNum)

        # Clear the selected item and entry fields
        self.selected_item = None
        self.clear_entry_fields()

    def update_student_in_database(self, edited_values, original_idNum):
        try:
            cursor = self.connection.cursor()
            
            # SQL UPDATE statement
            update_query = """
            UPDATE students 
            SET idNum = %s, first_name = %s, last_name = %s, gender = %s, course_code = %s, yearLevel = %s 
            WHERE idNum = %s
            """
            
            # Execute the update query with the edited values
            cursor.execute(update_query, (
                edited_values[0], edited_values[1], edited_values[2], 
                edited_values[3], edited_values[4], edited_values[5], original_idNum)
            )
            
            # Commit the transaction
            self.connection.commit()
            
            messagebox.showinfo("Success", "Student information updated successfully.")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update student information: {e}")
        finally:
            cursor.close()

    def check_IDNo(self, idNo):
        try:
            with self.connection.cursor() as cursor:
                # Execute a SELECT query to check if the student ID exists in the database
                cursor.execute("SELECT idNum FROM students WHERE idNum = %s", (idNo,))
                # Fetch the result
                result = cursor.fetchone()
                # If a row is fetched, it means the student ID exists
                if result:
                    return True
                else:
                    return False
        except Error as e:
            print(f"Error: {e}")
            return False


    def add_student(self):
        student_id = self.entries["Student ID"].get().strip()
        first_name = self.entries["First Name"].get().strip()
        last_name = self.entries["Last Name"].get().strip()
        gender = self.gender_variable.get()
        course = self.selected_course.get()
        year_level = self.entries["Year Level"].get().strip()

        if not (student_id and first_name and last_name and gender and course and year_level):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not self.check_course_code(course):
            messagebox.showerror("Error", f"Course code {course} does not exist in the database.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO students (idNum, first_name, last_name, gender, course_code, yearLevel)  VALUES (%s, %s, %s, %s, %s, %s)",
                (student_id, first_name, last_name, gender, course, year_level)
            )
            self.connection.commit()

            self.tree.insert("", "end", values=(student_id, first_name, last_name, gender, course, year_level))
            self.clear_entries()
            messagebox.showinfo("Success", "Student added successfully!")

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Student {student_id} already exists.")

    def delete_student(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select student(s) to delete.")
            return

        confirm = messagebox.askquestion("Confirmation", "Are you sure you want to delete the selected student(s)?")
        if confirm != "yes":
            return

        try:
            cursor = self.connection.cursor()
            for item in selected_items:
                student_id = self.tree.item(item, "values")[0]
                cursor.execute("DELETE FROM students WHERE idNum = %s", (student_id,))
                self.tree.delete(item)

            self.connection.commit()

            messagebox.showinfo("Success", "Selected student(s) deleted successfully!")

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to delete student(s).")

    def search_student(self, event=None):
        keyword = self.search_entry.get().lower()

        if not keyword.strip():
            messagebox.showwarning("Warning", "Please enter a keyword to search.")
            return

        # Clear previous selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        # Highlight rows matching the search keyword
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(keyword in value.lower() for value in values):
                self.tree.selection_add(item)

    def cancel_edit(self):
        self.clear_entries()
        self.selected_item = None

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1122",
            database="student_information_system"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1080x720")
    root.title("Student Information System")
    root.configure(bg="#A6A6A6")
    app = StudentInformationSystemGUI(root)
    root.mainloop()
