import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

class CourseInformationSystemGUI:
    def __init__(self, root):
        self.root = root
        self.connect_to_mysql()
        self.create_title_label()

    def connect_to_mysql(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1122",
            database="student_information_system"
        )
        self.cursor = self.connection.cursor()

    def load_courses(self):
        # Load courses from the database
        self.tree.delete(*self.tree.get_children())  # Clear existing data in Treeview
        self.cursor.execute("SELECT course_code, course_title FROM courses")
        courses = self.cursor.fetchall()
        for course in courses:
            self.tree.insert("", "end", values=course)

    def create_title_label(self):
        title_label = tk.Label(
            self.root,
            text="COURSE REGISTRATION",
            font=("Arial", 35, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            fg="white",
            padx=89
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        self.fields = ["courseCode", "courseTitle"]

        self.coursecode_label = tk.Label(self.root, text="Course Code:", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.coursecode_label.place(x=80, y=100)
        self.coursecode_entries = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.coursecode_entries.place(x=230, y=100, width=180)

        self.coursetitle_label = tk.Label(self.root, text="Course Title:", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.coursetitle_label.place(x=440, y=100)
        self.coursetitle_entries = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.coursetitle_entries.place(x=590, y=100, width=400)

        self.tosearch_label = tk.Label(self.root, text="To Search for Course Information:", font=("Arial", 17, "bold"), bg="#A6A6A6", fg="black")
        self.tosearch_label.place(x=80, y=300)

        self.search_label = tk.Label(self.root, text="Enter Keyword to Search:", font=("Arial", 17), bg="#A6A6A6", fg="black")
        self.search_label.place(x=130, y=340)

        self.search_entry = tk.Entry(self.root, font=("Arial", 17), bg="white", fg="black")
        self.search_entry.place(x=410, y=340, width=420)

#----------------------------------------------------- BUTTONS --------------------------------------------------------
            
        # Add Student button
        self.add_button = tk.Button(self.root, text="ADD", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.add_course)
        self.add_button.place(x=250, y=200, width=250)

        # Delete button
        self.delete_button = tk.Button(self.root, text="DELETE", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.delete_course)
        self.delete_button.place(x=250, y=250, width=250)

        # Edit and Save buttons
        self.edit_button = tk.Button(self.root, text="EDIT", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.edit_course)
        self.edit_button.place(x=600, y=200, width=250)

        self.save_button = tk.Button(self.root, text="SAVE", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.save_changes)
        self.save_button.place(x=600, y=250, width=250)

        # Search Button
        self.search_button = tk.Button(self.root, text="SEARCH", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.search_course)
        self.search_button.place(x=850, y=340, width=130)

        # Cancel button
        self.cancel_button = tk.Button(self.root, text="CANCEL", font=("Arial", 13, "bold"), bg="#2E2D2D", fg="white", command=self.cancel_edit)
        self.cancel_button.place(x=350, y=150, width=350)

#--------------------------------------------------------------- TREEVIEW --------------------------------------------------------

        # Create Treeview
        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("Course Code","Course Title"), show="headings")

        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Title", text="Course Title")

        self.tree.column("Course Code", width=100)  # Adjust width as needed
        self.tree.column("Course Title", width=200)  # Adjust width as needed
        self.tree.place(x=200, y=400, width=700, height=250)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview.Heading", background="#2E2D2D",  foreground="white", font=("Arial", 12, "bold"))

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=900, y=400, height=250)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Load existing courses
        self.load_courses()

        self.selected_item = None

    def edit_course(self):
        selected_item = self.tree.selection()
        if len(selected_item) != 1:
            messagebox.showwarning("Warning", "Please select only one course to edit.")
            return

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Store the selected item for later use
        self.selected_item = selected_item

        # Extract course information from the selected item
        course_code = self.tree.item(selected_item, "values")[0]

        # Fetch course details from the database
        self.cursor.execute("SELECT course_title FROM Courses WHERE course_code = %s", (course_code,))
        course_info = self.cursor.fetchone()

        # Check if course information is found
        if course_info:
            course_title = course_info[0]

            # Display course information in entry fields for editing
            self.coursecode_entries.delete(0, "end")
            self.coursecode_entries.insert(0, course_code)

            self.coursetitle_entries.delete(0, "end")
            self.coursetitle_entries.insert(0, course_title)
        else:
            messagebox.showwarning("Warning", "Course not found in the database.")

    def clear_entry_fields(self):
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def cancel_edit(self):
        self.selected_item = None
        self.clear_entry_fields()
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Retrieve edited values from entry fields
        edited_course_code = self.coursecode_entries.get()
        edited_course_title = self.coursetitle_entries.get()

        # Check if any field is empty
        if edited_course_code == '' or edited_course_title == '':
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        selected_course_code = self.tree.item(self.selected_item, "values")[0]

        if edited_course_code != selected_course_code and self.check_course(edited_course_code):
            messagebox.showerror("Error", "Course code already exists.")
            return

        # Update Treeview with the edited values
        self.tree.item(self.selected_item, values=(edited_course_code, edited_course_title))

        # Update MySQL database with the edited values
        try:
            self.cursor.execute("UPDATE Courses SET course_code = %s, course_title = %s WHERE course_code = %s",
                                (edited_course_code, edited_course_title, selected_course_code))  # Adjusted column names
            self.connection.commit()
            self.selected_item = None
            messagebox.showinfo("Success", "Changes saved successfully!")
        except mysql.connector.IntegrityError as e:
            # Handle duplicate entry error
            messagebox.showerror("Error", f"Failed to update course: {e}")

        self.selected_item = None
        self.clear_entry_fields()

    def update_course(self, selected_course_code, edited_course_code, edited_course_title):
        # Execute an SQL UPDATE query to update the course information
        self.cursor.execute("UPDATE Courses SET course_code = %s, course_title = %s WHERE course_code = %s",
                            (edited_course_code, edited_course_title, selected_course_code))
        self.connection.commit()

        messagebox.showinfo("Success", "Course information updated successfully!")

    def add_course(self):
        course_code = self.coursecode_entries.get()
        course_title = self.coursetitle_entries.get()
        if not course_code or not course_title:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        self.cursor.execute("INSERT INTO Courses (course_code, course_title) VALUES (%s, %s)", (course_code, course_title))
        self.connection.commit()
        self.tree.insert("", "end", values=(course_code, course_title))
        self.coursecode_entries.delete(0, tk.END)
        self.coursetitle_entries.delete(0, tk.END)
        messagebox.showinfo("Success", "Course added successfully!")

    def delete_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to delete.")
            return
        confirm = messagebox.askquestion("Confirmation", "Are you sure you want to delete the selected course(s)?")
        if confirm != "yes":
            return
        course_code = self.tree.item(selected_item, "values")[0]
        self.cursor.execute("DELETE FROM Courses WHERE course_code = %s", (course_code,))
        self.connection.commit()
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", f"Course {course_code} deleted successfully!")

    def check_course(self, course_code):
        # Execute an SQL query to check if the course code exists in the database
        self.cursor.execute("SELECT COUNT(*) FROM Courses WHERE LOWER(course_code) = %s", (course_code.lower(),))
        count = self.cursor.fetchone()[0]
        return count > 0

    def delete_course_from_database(self, course_code):
        # Delete the course from the Courses table
        self.cursor.execute("DELETE FROM Courses WHERE course_code = %s", (course_code,))
        self.connection.commit()

        # Update corresponding course code to "N/A" in the student table
        self.cursor.execute("UPDATE Students SET course_code = 'N/A' WHERE course_code = %s", (course_code,))
        self.connection.commit()

        messagebox.showinfo("Success", f"Course {course_code} deleted successfully!")

    def search_course(self, event=None):
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

def main():
    root = tk.Tk()
    root.title("Course Registration")
    root.configure(bg="#A6A6A6")
    root.geometry("1070x675") 
    root.resizable(False, False) 

    course_app = CourseInformationSystemGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
