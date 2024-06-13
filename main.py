import tkinter as tk
from tkinter import messagebox
from student import StudentInformationSystemGUI
from course import CourseInformationSystemGUI 

class SimpleStudentInformationSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Student Information System")
        self.configure(bg="#DDDDDD")
        self.geometry("1400x700")
        self.resizable(False, False)

        self.create_buttons()
        self.create_student_registration_interface()

    def create_buttons(self):
        left_menu = tk.Frame(self, bg="#2E2D2D", bd=5, width=200, relief=tk.GROOVE)
        left_menu.place(x=10, y=15, width=300, height=675)

        menu_label = tk.Label(
            left_menu,
            text="MENU",
            font=("Arial", 35, "bold"),
            bg="gray",
            fg="white"
        )
        menu_label.place(x=0, y=0, width=290)

        text_label = tk.Label(
            left_menu,
            text="Choose Registration",
            font=("Arial", 15),
            bg="#2E2D2D",
            fg="white",
        )
        text_label.place(x=50, y=100)

        student_button = tk.Button(
            left_menu,
            text="STUDENT",
            font=("Arial", 15, "bold"),
            bg="gray",
            foreground="white",
            command=self.create_student_registration_interface
        )
        student_button.place(x=40, y=180, width=200)

        course_button = tk.Button(
            left_menu,
            text="COURSE",
            font=("Arial", 15, "bold"),
            bg="gray",
            foreground="white",
            command=self.create_course_registration_interface
        )
        course_button.place(x=40, y=240, width=200)

        exit_button = tk.Button(
            left_menu,
            text="EXIT",
            font=("Arial", 15, "bold"),
            bg="gray",
            foreground="white",
            command=self.confirm_exit
        )
        exit_button.place(x=40, y=580, width=200)

    def confirm_exit(self):
        confirm = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
        if confirm == "yes":
            self.destroy()

    def create_student_registration_interface(self):
        if hasattr(self, "student_interface_frame"):
            self.student_interface_frame.destroy()

        self.student_interface_frame = tk.Frame(self, bg="#A6A6A6")
        self.student_interface_frame.place(x=320, y=15, width=1070, height=675)

        self.student_app = StudentInformationSystemGUI(self.student_interface_frame)

    def create_course_registration_interface(self):
        if hasattr(self, "course_interface_frame"):
            self.course_interface_frame.destroy()

        self.course_interface_frame = tk.Frame(self, bg="#A6A6A6")
        self.course_interface_frame.place(x=320, y=15, width=1070, height=675)

        self.course_app = CourseInformationSystemGUI(self.course_interface_frame)

def main():
    app = SimpleStudentInformationSystem()
    app.mainloop()

if __name__ == "__main__":
    main()
