import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# Replace these with your MySQL server details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"
DB_DATABASE = "student"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Activity Points System")
        self.root.geometry("600x400")  # Set initial window size

        # Establish MySQL connection
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        self.cursor = self.conn.cursor()

        # Configure a standard color scheme
        self.bg_color = "#f0f0f0"  # Light gray background
        self.button_color = "#4CAF50"  # Green buttons
        self.label_color = "#333"  # Dark gray labels

        self.root.configure(bg=self.bg_color)

        self.login_button = tk.Button(
            root, text="Student Login", command=self.student_login,
            width=20, height=2, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.login_button.pack(pady=20)

        self.teacher_button = tk.Button(
            root, text="Teacher Login", command=self.teacher_login,
            width=20, height=2, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.teacher_button.pack(pady=20)

    def create_window(self, title, width, height):
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry(f"{width}x{height}")
        new_window.configure(bg=self.bg_color)
        return new_window

    def student_login(self):
        self.login_window = self.create_window("Student Login", 600, 400)

        # Labels and entry widgets
        self.username_label = tk.Label(
            self.login_window, text="Username:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.login_window, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(
            self.login_window, text="Password:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.login_window, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(
            self.login_window, text="Login", command=self.validate_student_login,
            width=15, height=1, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.login_button.pack(pady=20)

    def teacher_login(self):
        self.login_window = self.create_window("Teacher Login", 600, 400)

        # Labels and entry widgets
        self.username_label = tk.Label(
            self.login_window, text="Username:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.login_window, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(
            self.login_window, text="Password:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.login_window, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(
            self.login_window, text="Login", command=self.validate_teacher_login,
            width=15, height=1, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.login_button.pack(pady=20)

    def validate_student_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the database for the provided username and password
        query = "SELECT * FROM students WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            # Successful login
            self.show_student_menu(username)
        else:
            # Failed login
            messagebox.showerror("Student Login", "Invalid username or password")

    def validate_teacher_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the database for the provided username and password
        query = "SELECT * FROM teachers WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            # Successful login
            self.show_teacher_menu(username)
        else:
            # Failed login
            messagebox.showerror("Teacher Login", "Invalid username or password")

    def show_teacher_menu(self, username):
        self.teacher_menu = self.create_window("Teacher Menu", 600, 400)

        # Buttons
        self.modify_points_button = tk.Button(
            self.teacher_menu, text="Modify Activity Points", command=self.modify_activity_points,
            width=30, height=2, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.modify_points_button.pack(pady=20)

        self.add_student_button = tk.Button(
            self.teacher_menu, text="Add Student", command=self.add_student,
            width=30, height=2, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.add_student_button.pack(pady=20)
        
        self.show_activity_button = tk.Button(
            self.teacher_menu, text="Check Student Activity Points",
            command=self.check_student_activity_points, width=30, height=2,
            font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.show_activity_button.pack(pady=20)

    def show_student_menu(self, username):
        self.student_menu = self.create_window("Student Menu", 600, 400)

        # Buttons
        self.new_activity_button = tk.Button(
            self.student_menu, text="Submit New Activity", command=self.submit_new_activity,
            width=20, height=2, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.new_activity_button.pack(pady=20)

        self.show_activity_button = tk.Button(
            self.student_menu, text="Show Activity Points",
            command=lambda: self.show_activity_points(username), width=20, height=2,
            font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.show_activity_button.pack(pady=20)

    def modify_activity_points(self):
        student_identifier = simpledialog.askstring("Modify Activity Points", "Enter the student's ID:")

        if student_identifier:
            # Check if the input is numeric to determine whether it's an ID or a username
            is_numeric = student_identifier.isdigit()

            if is_numeric:
                # It's an ID, so query using ID
                query = "SELECT * FROM students WHERE id = %s"
            else:
                # It's a username, so query using username
                query = "SELECT * FROM students WHERE username = %s"

            self.cursor.execute(query, (student_identifier,))
            student = self.cursor.fetchone()

            if student:
                new_points = simpledialog.askinteger("Modify Activity Points", "Enter the points to add:")

                if new_points is not None:
                    # Calculate the new total points
                    total_points = student[3] + new_points  # Assuming points are stored in the fourth column (index 3)

                    # Update the student's activity points
                    update_query = "UPDATE students SET points = %s WHERE id = %s"
                    self.cursor.execute(update_query, (total_points, student[0]))  # Assuming student ID is in the first column (index 0)
                    self.conn.commit()

                    messagebox.showinfo("Modify Activity Points", f"Activity points for {student_identifier} modified successfully!\nNew Total Points: {total_points}")
                else:
                    messagebox.showinfo("Modify Activity Points", "Operation canceled. No points were added.")
            else:
                messagebox.showerror("Modify Activity Points", f"Student with identifier '{student_identifier}' not found.")

    def add_student(self):
        self.add_student_window = self.create_window("Add Student", 600, 400)

        # Labels and entry widgets
        self.student_id_label = tk.Label(
            self.add_student_window, text="Id:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.student_id_label.pack(pady=10)
        self.student_id_entry = tk.Entry(self.add_student_window, font=("Helvetica", 14))
        self.student_id_entry.pack(pady=10)

        self.student_username_label = tk.Label(
            self.add_student_window, text="Username:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.student_username_label.pack(pady=10)
        self.student_username_entry = tk.Entry(self.add_student_window, font=("Helvetica", 14))
        self.student_username_entry.pack(pady=10)

        self.student_password_label = tk.Label(
            self.add_student_window, text="Password:", font=("Helvetica", 14),
            bg=self.bg_color, fg=self.label_color
        )
        self.student_password_label.pack(pady=10)
        self.student_password_entry = tk.Entry(self.add_student_window, show="*", font=("Helvetica", 14))
        self.student_password_entry.pack(pady=10)

        self.add_student_button = tk.Button(
            self.add_student_window, text="Add Student", command=self.validate_and_add_student,
            width=15, height=1, font=("Helvetica", 14), bg=self.button_color, fg="white"
        )
        self.add_student_button.pack(pady=20)

    def validate_and_add_student(self):
        student_id = self.student_id_entry.get()
        username = self.student_username_entry.get()
        password = self.student_password_entry.get()

        # Check if the username already exists
        query_check_username = "SELECT * FROM students WHERE username = %s"
        self.cursor.execute(query_check_username, (username,))
        existing_student = self.cursor.fetchone()

        if existing_student:
            messagebox.showerror("Add Student", "Username already exists. Please choose a different username.")
        else:
            # Add the new student to the database
            query_add_student = "INSERT INTO students (id, username, password, points) VALUES (%s, %s, %s, 0)"
            self.cursor.execute(query_add_student, (student_id, username, password))
            self.conn.commit()

            messagebox.showinfo("Add Student", f"Student {username} added successfully!")

    def submit_new_activity(self):
        activity_name = simpledialog.askstring("Activity Submission", "Enter the activity name:")
        if activity_name:
            # Retrieve student ID from the database using the student's username
            username = self.username_entry.get()
            query_student_id = "SELECT id FROM students WHERE username = %s"
            self.cursor.execute(query_student_id, (username,))
            student_id = self.cursor.fetchone()[0]

            # Check if the activity exists in the activities table
            query_activity = "SELECT points FROM activities WHERE activity_name = %s"
            self.cursor.execute(query_activity, (activity_name,))
            activity = self.cursor.fetchone()

            if activity:
                # Increment the student's points with the points associated with the activity
                new_points = activity[0]  # Assuming points are stored in the first column (index 0) of the activities table
                query_update_points = "UPDATE students SET points = points + %s WHERE id = %s"
                self.cursor.execute(query_update_points, (new_points, student_id))
                self.conn.commit()

                messagebox.showinfo("Activity Submission", f"Activity '{activity_name}' submitted successfully! Points added: {new_points}")
            else:
                messagebox.showerror("Activity Submission", f"Error: Activity '{activity_name}' not found in the activities table.")

    def check_student_activity_points(self):
        student_identifier = simpledialog.askstring("Check Student Activity Points", "Enter the student's ID:")
        if student_identifier:
            # Check if the input is numeric to determine whether it's an ID or a username
            is_numeric = student_identifier.isdigit()

            if is_numeric:
                # It's an ID, so query using ID
                query = "SELECT * FROM students WHERE id = %s"
            else:
                messagebox.showerror("Check Student Activity Points", "Invalid student ID.")
                return

            self.cursor.execute(query, (student_identifier,))
            student = self.cursor.fetchone()

            if student:
                student_id, username, _, points = student  # Assuming points are stored in the fourth column (index 3)
                messagebox.showinfo("Check Student Activity Points", f"Student ID: {student_id}\nUsername: {username}\nActivity Points: {points}")
            else:
                messagebox.showerror("Check Student Activity Points", f"Student with ID {student_identifier} not found.")

    def show_activity_points(self, username):
        query = "SELECT points FROM students WHERE username = %s"
        self.cursor.execute(query, (username,))
        student_points = self.cursor.fetchone()[0]
        messagebox.showinfo("Activity Points", f"Your activity points: {student_points}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    # Close the database connection
    app.cursor.close()
    app.conn.close()
