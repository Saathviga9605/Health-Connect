import oracledb
from tkinter import messagebox

# Establish a connection to the Oracle database
connection = oracledb.connect(
    user="system",
    password="dborcl",
    dsn="localhost:1522/xe"
)
cursor = connection.cursor()

# Function to add a new doctor
def add_doctor(d_id, name, department):
    try:
        doctor_id = int(d_id)  # Ensure ID is an integer
        cursor.callproc('add_doctor', [doctor_id, name, department])  # Use existing cursor
        connection.commit()  # Use existing connection for commit
        return "Doctor added successfully."
    except oracledb.IntegrityError as e:
        if e.args[0].code == 1:
            return "Error: Doctor with this ID already exists."
        else:
            return f"Database integrity error: {str(e)}"
    except oracledb.DatabaseError as e:
        return f"Error occurred: {str(e)}"
    except ValueError:
        return "Invalid ID format. Please enter a numeric ID."


'''def add_doctor(d_id, name, department, cursor, connection):
    try:
        # Ensure ID is an integer
        doctor_id = int(d_id)  
        
        # Call the stored procedure
        cursor.callproc('add_doctor', [doctor_id, name, department])
        
        connection.commit()  # Commit transaction if successful
        return "Doctor added successfully."
    except oracledb.IntegrityError as e:
        # Handle unique constraint violation (duplicate ID)
        if e.code == 1:
            return "Error: Doctor with this ID already exists."
        else:
            return f"Database integrity error: {e}"
    except oracledb.DatabaseError as e:
        return f"Error occurred: {str(e)}"
    except ValueError:
        return "Invalid ID format. Please enter a numeric ID."
'''


def add_patient(ID, Name, Contact_Number, Disease_Name, Department, Doctor_id, Treatment_Details):
    try:
        # Convert inputs to required types and validate them
        try:
            patient_id = int(ID)  # Convert ID to int
            dept = int(Department)  # Convert Department to int
            doc_id = int(Doctor_id)  # Convert Doctor_id to int
        except ValueError:
            return "Patient ID, Department, and Doctor ID must be numeric values."

        # Ensure the contact number is valid (you can add more validation if needed)
        if len(Contact_Number) < 10:
            return "Please enter a valid contact number."

        # Execute the insert query
        cursor.execute("""
            INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Department, Doctor_id, Treatment_Details)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, [patient_id, Name, Contact_Number, Disease_Name, dept, doc_id, Treatment_Details])

        # Commit the transaction if everything is successful
        connection.commit()
        return "Patient added successfully."

    except oracledb.Error as error:
        # Check for the specific custom error raised by the trigger
        error_code = error.args[0].code if hasattr(error.args[0], 'code') else None
        if error_code == -20001:
            return "Department ID does not exist in the Departments table."
        else:
            return f"Database error occurred: {error}"

# Function to check if patient ID already exists in the database
def check_patient_exists(patient_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT 1 FROM patients WHERE patient_id = :id"
            cursor.execute(query, id=patient_id)
            result = cursor.fetchone()
            return result is not None  # Returns True if patient exists, otherwise False
    except oracledb.DatabaseError as e:
        print(f"Error checking patient existence: {e}")  # Replace with logging if needed
        return False
    
# Function to edit doctor details
def edit_doctor_details(D_Id, Name=None, Department=None):
    try:
        updates = []
        params = {}

        if Name:
            updates.append("Name = :name")
            params["name"] = Name
        if Department:
            updates.append("Department = :department")
            params["department"] = Department

        if not updates:
            return "No updates specified."

        query = f"UPDATE Doctors SET {', '.join(updates)} WHERE D_Id = :d_id"
        params["d_id"] = D_Id
        cursor.execute(query, params)
        
        connection.commit()
        return "Doctor details updated successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to delete a doctor
def delete_doctor(D_Id):
    try:
        d_id = int(D_Id)
        cursor.execute("DELETE FROM Doctors WHERE D_Id = :1", [d_id])
        
        connection.commit()
        return "Doctor deleted successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to delete a patient
def delete_patient(ID):
    try:
        patient_id = int(ID)
        cursor.execute("DELETE FROM Patients WHERE ID = :1", [patient_id])
        
        connection.commit()
        return "Patient deleted successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

def edit_patient_details(ID, field_name, new_value):
    try:
        valid_fields = {
            "Name": "Name",
            "Contact Number": "Contact_Number",
            "Disease Name": "Disease_Name",
            "Treatment Details": "Treatment_Details",
            "Department": "Department",
            "Doctor ID": "Doctor_id"
        }
        
        # Map user-friendly field name to database column name
        column_name = valid_fields.get(field_name)
        if not column_name:
            return "Invalid detail to edit specified."

        # Update query
        query = f"UPDATE Patients SET {column_name} = :new_value WHERE ID = :id"
        params = {"new_value": new_value, "id": int(ID)}
        
        # Execute the update
        cursor.execute(query, params)
        connection.commit()
        return "Patient details updated successfully."
    
    except oracledb.Error as error:
        return f"Error occurred: {error}"

def get_patient_data():
    """Fetch patient data from the database."""
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        cursor.execute("""
            SELECT ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id 
            FROM Patients
        """)
        patient_data = cursor.fetchall()  # Fetching all patient data
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return patient_data

def get_doctor_data():
    """Fetch doctor data from the database."""
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        cursor.execute("""
            SELECT D_ID, Name, Department
            FROM Doctors
        """)
        doctor_data = cursor.fetchall()  # Fetching all doctor data
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return doctor_data

def get_doctors_by_dept(dept_input):
    """Fetch doctor data by department from the database."""
    if not dept_input:
        print("No department input provided.")
        return []
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        # Query to select doctors by matching department ID or name
        cursor.execute("""
            SELECT D_Id, Name, Department
            FROM Doctors
            WHERE Department IN (
                SELECT Dept_id FROM Departments WHERE Dept_id = :dept OR LOWER(D_Name) LIKE LOWER(:dept_name)
            )
        """, dept=dept_input, dept_name=f"%{dept_input}%")
        
        doctor_data = cursor.fetchall()  # Fetch all matching doctor data
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return doctor_data

def get_patients_by_dept(dept_input):
    """Fetch patient data by department from the database."""
    if not dept_input:
        print("No department input provided.")
        return []
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        # Use LIKE to support both department ID and name in the query
        cursor.execute("""
            SELECT ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id
            FROM Patients
            WHERE Department IN (
                SELECT Dept_id FROM Departments WHERE Dept_id = :dept OR LOWER(D_Name) LIKE LOWER(:dept_name)
            )
        """, dept=dept_input, dept_name=f"%{dept_input}%")
        patient_data = cursor.fetchall()  # Fetch all matching patient data
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return patient_data

def get_audit_logs():
    """Fetch audit logs from the Patient_Audit table."""
    try:
        cursor = connection.cursor()  # Create a new cursor for this operation
        cursor.execute("""
            SELECT Audit_ID, Patient_ID, Action, Action_Time 
            FROM Patient_Audit
            ORDER BY Action_Time DESC
        """)
        audit_logs = cursor.fetchall()  # Fetch all audit logs
    except oracledb.Error as error:
        print(f"Database error occurred: {error}")
        return []
    finally:
        cursor.close()  # Close the cursor after fetching data
    return audit_logs

def view_audit_logs():
    root = Toplevel()
    root.title("View Audit Logs")
    root.geometry("800x400")
    root.resizable(False, False)

    frame = Frame(root)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Audit_ID", "Patient_ID", "Action", "Action_Time"), show="headings")

    tree.heading("Audit_ID", text="Audit ID")
    tree.heading("Patient_ID", text="Patient ID")
    tree.heading("Action", text="Action")
    tree.heading("Action_Time", text="Action Time")

    # Set column widths
    tree.column("Audit_ID", width=80)
    tree.column("Patient_ID", width=80)
    tree.column("Action", width=120)
    tree.column("Action_Time", width=150)

    audit_logs = get_audit_logs()

    for log in audit_logs:
        tree.insert("", "end", values=log)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

from tkinter import *
from tkinter import messagebox
from tkinter import ttk,simpledialog
from connect_Test import (delete_doctor, delete_patient, add_doctor_procedure, edit_doctor_details, edit_patient_details, add_patient, get_patient_data, get_doctor_data, get_doctors_by_dept, get_patients_by_dept)

def homepage():
    root = Tk()
    root.title("HealthConnect Home Page")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    global bg_image  
    bg_image = PhotoImage(file="hospital bg.png")
    Label(root, image=bg_image).place(relheight=1, relwidth=1)

    Label(root, text='Health Connect', bg='light cyan', font=('Georgia', 30)).place(x=350, y=48)

    Button(root, width=20, text="Login Here to Continue", bg='blanched almond', border=4, font=('Georgia', 12), command=adminlogin).place(x=400, y=450)

    root.mainloop()

def adminlogin():
    global user, code, login_bg_image 

    login_root = Toplevel()
    login_root.title("Login")
    login_root.configure(bg='#fff')
    login_root.geometry("1000x600+400+200")
    login_root.resizable(False, False)
    
    login_bg_image = PhotoImage(file="hospital.png")
    Label(login_root, image=login_bg_image).place(relheight=1, relwidth=1)

    frame = Frame(login_root, width=350, height=350, bg="LightYellow")
    frame.place(x=370, y=120)

    Label(frame, text='Admin Login', fg='#57a1f8', bg='white', font=('Georgie', 24, 'bold')).place(x=65, y=10)

    Label(frame, text='Username:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=80)
    user = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    user.place(x=30, y=110)

    Label(frame, text='Password:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=150)
    code = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11), show="*")
    code.place(x=30, y=180)

    Button(frame, width=39, pady=7, text='Sign In', bg='sea green', fg='white', border=0, command=check_login).place(x=35, y=250)

def check_login():
    if user.get() == "hdba" and code.get() == "dba123":
        adminpage()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def adminpage():
    admin_root = Toplevel()  
    admin_root.title("Admin Home Page")
    admin_root.geometry("1000x600+400+200")
    admin_root.resizable(False, False)

    global admin_bg_image 
    admin_bg_image = PhotoImage(file="hospital.png")
    Label(admin_root, image=admin_bg_image).place(relheight=1, relwidth=1)

    frame = Frame(admin_root, width=400, height=350, bg="light cyan")
    frame.place(x=350, y=120)

    Label(frame, text='Admin Dashboard', fg='#57a1f8', bg='white', font=('Georgie', 24, 'bold')).place(x=65, y=10)

    Button(frame, width=20, text="Manage patient", bg='lemon chiffon', border=4, font=('Georgia', 12), command=adminpatientmgmt).place(x=110, y=100)
    Button(frame, width=20, text="Manage doctor", bg='lemon chiffon', border=4, font=('Georgia', 12), command=admindoctormgmt).place(x=110, y=200)
    Button(frame, width=20, text="View details", bg='lemon chiffon', border=4, font=('Georgia', 12), command=viewdetails).place(x=110, y=300)
    #Button(frame, width=20, text="View Audit Logs", bg='lemon chiffon', border=4, font=('Georgia', 12), command=view_audit_logs).place(x=110, y=400)

def adminpatientmgmt():
    root=Toplevel()
    root.title("Patient Management")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    image_path = PhotoImage(file="hospital.png")
    bg_image = Label(root, image=image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=400, height=350, bg="light cyan")
    frame.place(x=350, y=120)

    heading = Label(frame, text='Patient Management', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=45, y=10)

    Button(frame,width=20,text="Add patient", bg='lemon chiffon', border=4, font=('Georgia', 12),command=addpatient).place(x=110,y=100)
    Button(frame,width=20,text="Remove patient", bg='lemon chiffon', border=4, font=('Georgia', 12),command=removepatient).place(x=110,y=200)
    Button(frame,width=20,text="Edit details ", bg='lemon chiffon', border=4, font=('Georgia', 12),command=editpatdetails).place(x=110,y=300)

    root.mainloop()

def admindoctormgmt():
    root=Toplevel()
    root.title("Doctor Management")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=400, height=350, bg="light cyan")
    frame.place(x=350, y=120)

    heading = Label(frame, text='Doctor Management', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=55, y=10)

    Button(frame,width=20,text="Add doctor", bg='lemon chiffon', border=4, font=('Georgia', 12),command=adddoctor).place(x=110,y=100)
    Button(frame,width=20,text="Remove doctor", bg='lemon chiffon', border=4, font=('Georgia', 12),command=removedoctor).place(x=110,y=200)
    Button(frame,width=20,text="Edit details ", bg='lemon chiffon', border=4, font=('Georgia', 12),command=editdocdetails).place(x=110,y=300)
    
    root.mainloop()

def viewdetails():
    root=Toplevel()
    root.title("View Doctor and Patient Details")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=500, height=500, bg="light cyan")
    frame.place(x=275, y=80)

    heading = Label(frame, text='View Details', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=160, y=10)

    Button(frame,width=30,text="View Patients", bg='lemon chiffon', border=4, font=('Georgia', 12),command=viewpatient).place(x=110,y=100)
    Button(frame,width=30,text="View Doctors", bg='lemon chiffon', border=4, font=('Georgia', 12),command=viewdoctor).place(x=110,y=200)
    Button(frame,width=30,text="Find Doctors by Department", bg='lemon chiffon', border=4, font=('Georgia', 12),command=viewdoctorsbydept).place(x=110,y=300)
    Button(frame,width=30,text="Find Patients by Department", bg='lemon chiffon', border=4, font=('Georgia', 12),command=viewpatientsbydept).place(x=110,y=400)

import tkinter as tk
from tkinter import ttk

def viewpatient():
    root = Toplevel()
    root.title("View Patient Data")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact_Number", "Disease_Name", "Treatment_Details", "Department", "Doctor_id"), show="headings")

    tree.heading("ID", text="Patient ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact_Number", text="Contact Number")
    tree.heading("Disease_Name", text="Disease Name")
    tree.heading("Treatment_Details", text="Treatment Details")
    tree.heading("Department", text="Department")
    tree.heading("Doctor_id", text="Doctor ID")

    # Set column widths
    tree.column("ID", width=80)
    tree.column("Name", width=120)
    tree.column("Contact_Number", width=120)
    tree.column("Disease_Name", width=150)
    tree.column("Treatment_Details", width=200)
    tree.column("Department", width=100)
    tree.column("Doctor_id", width=80)

    patient_data = get_patient_data()

    for patient in patient_data:
        if len(patient) == 7:
            tree.insert("", "end", values=patient)
        else:
            print("Data missing for patient:", patient) 

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

def viewdoctor():
    root = Toplevel()
    root.title("View Doctor Data")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Doctor_ID", "Name", "Department"), show="headings")

    tree.heading("Doctor_ID", text="Doctor ID")
    tree.heading("Name", text="Name")
    tree.heading("Department", text="Department")

    tree.column("Doctor_ID", width=80)
    tree.column("Name", width=120)
    tree.column("Department", width=100)

    doctor_data = get_doctor_data() 

    for doctor in doctor_data:
        if len(doctor) == 3:
            tree.insert("", "end", values=doctor)
        else:
            print("Data missing for doctor:", doctor) 

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

from tkinter import simpledialog

def viewdoctorsbydept():
    root = Toplevel()
    root.title("View Doctors by Department")
    root.geometry("800x500+400+200")
    root.resizable(False, False)

    # Set background color for the root window
    root.configure(bg="#f0f0f0")  # Light gray background

    # Ask for department input
    dept_input = simpledialog.askstring("Input", "Enter Department ID")

    # Create a white frame with border for the Treeview
    frame = Frame(root, bg="#ffffff", bd=2, relief="solid")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Define Treeview columns and headings
    tree = ttk.Treeview(
        frame, 
        columns=("D_Id", "Name", "Department"), 
        show="headings"
    )
    tree.heading("D_Id", text="Doctor ID")
    tree.heading("Name", text="Name")
    tree.heading("Department", text="Department")

    # Set column widths and center alignment
    for col in ("D_Id", "Name", "Department"):
        tree.column(col, width=150, anchor="center")

    # Fetch and filter data based on department input
    doctor_data = get_doctors_by_dept(dept_input)
    for doctor in doctor_data:
        if dept_input.lower() in str(doctor[2]).lower():  # Assuming doctor[2] is the Department column
            tree.insert("", "end", values=doctor)

    # Adding a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # Pack Treeview and scrollbar
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()


def viewpatientsbydept():
    root = Toplevel()
    root.title("View Patients by Department")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    # Set background color instead of an image
    root.configure(bg="#f0f0f0")  # Example light gray color

    # Ask for department input
    dept_input = simpledialog.askstring("Input", "Enter Department ID")

    frame = Frame(root, bg="#ffffff", bd=2, relief="solid")  # White frame with border
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(
        frame, 
        columns=("ID", "Name", "Contact_Number", "Disease_Name", "Treatment_Details", "Department", "Doctor_id"), 
        show="headings"
    )
    tree.heading("ID", text="Patient ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact_Number", text="Contact Number")
    tree.heading("Disease_Name", text="Disease Name")
    tree.heading("Treatment_Details", text="Treatment Details")
    tree.heading("Department", text="Department")
    tree.heading("Doctor_id", text="Doctor ID")

    # Set column widths and center alignment
    for col in ("ID", "Name", "Contact_Number", "Disease_Name", "Treatment_Details", "Department", "Doctor_id"):
        tree.column(col, width=120, anchor="center")

    # Fetch and filter data based on department input
    patient_data = get_patients_by_dept(dept_input)
    for patient in patient_data:
        if dept_input.lower() in str(patient[5]).lower():  # Assuming patient[5] is the Department column
            tree.insert("", "end", values=patient)

    # Adding a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

import oracledb
from tkinter import *
from tkinter import messagebox


# Define procedure to add doctor
def add_doctor_procedure(doctor_id, doctor_name, doctor_department):
    try:
        # Call the stored procedure to add a doctor
        cursor.callproc("add_doctor", [doctor_id, doctor_name, doctor_department])
        connection.commit()
        messagebox.showinfo("Success", "Doctor added successfully!")
    except oracledb.DatabaseError as e:
        # Check if the error is due to the trigger
        error_code = e.args[0].code if e.args else None
        if error_code == -20001:  # This is the error code from the trigger for invalid department
            messagebox.showerror("Error", "Invalid Department Number. Please choose a valid department number.")
        else:
            messagebox.showerror("Error", f"Failed to add doctor: {e}")

# Define the adddoctor function with enhanced handling
def adddoctor():
    def submit_doctor():
        try:
            doctor_id = int(d_id_entry.get())
            doctor_name = name_entry.get()
            doctor_department = int(dname_entry.get())
            add_doctor_procedure(doctor_id, doctor_name, doctor_department)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid details.")

    global d_id_entry, name_entry, dname_entry
    root = Toplevel()
    root.title("Add Doctor")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    # Load background image
    root.image_path = PhotoImage(file="hospital.png")
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    # Create frame for form
    frame = Frame(root, width=400, height=450, bg="light cyan")
    frame.place(x=370, y=130)

    heading = Label(frame, text='Add Doctor', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
    heading.place(x=85, y=10)

    # Doctor ID field
    Label(frame, text='Doctor ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=100)
    d_id_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('georgia', 11))
    d_id_entry.place(x=30, y=130)

    # Doctor Name field
    Label(frame, text='Name:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=170)
    name_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('georgia', 11))
    name_entry.place(x=30, y=200)

    # Department ID field
    Label(frame, text='Department:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=240)
    dname_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('georgia', 11))
    dname_entry.place(x=30, y=270)

    # Submit Button
    Button(frame, text="Add Doctor", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_doctor).place(x=75, y=320)

    root.mainloop()

def removedoctor():
    def submit_remove_doctor():
        if not did_entry.get():
            messagebox.showerror("Input Error", "Doctor ID required")
            return
        delete_doctor(did_entry.get())
        messagebox.showinfo("Success", "Doctor removed successfully")

    global did_entry
    root = Toplevel()
    root.title("Remove Doctor")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=350, height=350, bg="light cyan")
    frame.place(x=370, y=150)

    heading = Label(frame, text='Remove doctor', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=60, y=10)

    Label(frame, text='Doctor ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=120)
    did_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    did_entry.place(x=30, y=150)

    Button(frame, text="Remove Doctor", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_remove_doctor).place(x=75, y=200)

    root.mainloop()

def editdocdetails():
    def submit_edit_doctor():
        if not docpatid_entry.get() or not detail_entry.get() or not change_entry.get():
            messagebox.showerror("Input Error", "All fields are required")
            return

        detail = detail_entry.get().lower()
        value = change_entry.get()

        if detail == "name":
            result = edit_doctor_details(D_Id=docpatid_entry.get(), Name=value)
        elif detail == "department":
            result = edit_doctor_details(D_Id=docpatid_entry.get(), Department=value)
        else:
            messagebox.showerror("Input Error", "Invalid detail to edit")
            return

        if result == "Doctor details updated successfully.":
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

    global docpatid_entry, detail_entry, change_entry
    root = Toplevel()
    root.title("Edit Doctor Details")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=350, height=400, bg="light cyan")
    frame.place(x=370, y=130)

    heading = Label(frame, text='Edit Doctor Details', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=30, y=10)

    Label(frame, text='Doctor ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=100)
    docpatid_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    docpatid_entry.place(x=30, y=130)

    Label(frame, text='Detail to edit (Name/Department):', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=170)
    detail_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    detail_entry.place(x=30, y=200)

    Label(frame, text='New value for detail:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=240)
    change_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    change_entry.place(x=30, y=270)

    Button(frame, text="Edit Details", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_edit_doctor).place(x=75, y=320)
    root.mainloop()

def addpatient():
    def submit_patient():
        patient_id = patid_entry.get()
        patient_name = patname_entry.get()
        contact = contact_entry.get()
        disease = disname_entry.get()
        department = deptname_entry.get()
        doctor_id = docid_entry.get()
        treatment = treatment_entry.get()

        if not patient_id or not patient_name or not contact or not disease or not treatment or not department or not doctor_id:
            messagebox.showerror("Input Error", "All fields are required")
            return

        if len(contact) < 10:
            messagebox.showerror("Input Error", "Please enter a valid contact number")
            return

        if check_patient_exists(patient_id):
            messagebox.showerror("Error", "Patient ID already exists")
        else:
            result = add_patient(patient_id, patient_name, contact, disease, department, doctor_id, treatment)
            if "successfully" in result:
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Database Error", result)

    global patid_entry, patname_entry, contact_entry, disname_entry, treatment_entry, deptname_entry, docid_entry
    root = Toplevel()
    root.title("Add Patient")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=750, height=450, bg="light cyan")
    frame.place(x=140, y=100)

    heading = Label(frame, text='Add Patient', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=280, y=10)

    Label(frame, text='Patient ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=90)
    patid_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    patid_entry.place(x=30, y=120)

    Label(frame, text='Patient Name:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=160)
    patname_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    patname_entry.place(x=30, y=190)

    Label(frame, text='Contact number:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=430, y=90)
    contact_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    contact_entry.place(x=430, y=120)

    Label(frame, text='Disease Name:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=430, y=160)
    disname_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    disname_entry.place(x=430, y=190)

    Label(frame, text='Treatment Details:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=230)
    treatment_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    treatment_entry.place(x=30, y=260)

    Label(frame, text='Department:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=430, y=230)
    deptname_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    deptname_entry.place(x=430, y=260)

    Label(frame, text='Doctor ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=230, y=300)
    docid_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    docid_entry.place(x=230, y=330)

    Button(frame, text="Add Patient", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_patient).place(x=280, y=380)

    root.mainloop()


def removepatient():
    def submit_remove_patient():
        if not patid_entry.get():
            messagebox.showerror("Input Error", "Patient ID required")
            return
        delete_patient(patid_entry.get())
        messagebox.showinfo("Success", "Patient removed successfully")

    global patid_entry
    root = Toplevel()
    root.title("Remove Patient")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=350, height=350, bg="light cyan")
    frame.place(x=370, y=150)

    heading = Label(frame, text='Remove Patient', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=60, y=10)

    Label(frame, text='Patient ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=120)
    patid_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    patid_entry.place(x=30, y=150)

    Button(frame, text="Remove Patient", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_remove_patient).place(x=75, y=200)

    root.mainloop()

def editpatdetails():
    def submit_edit_patient():
        if not patdocid_entry.get() or not editdet_entry.get() or not newval_entry.get():
            messagebox.showerror("Input Error", "All fields are required")
            return
        
        field_name = editdet_entry.get().strip()
        new_value = newval_entry.get().strip()
        pat_id = patdocid_entry.get().strip()
    
        result = edit_patient_details(pat_id, field_name, new_value)
        
        if "successfully" in result:
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

    global patdocid_entry, editdet_entry, newval_entry
    root = Toplevel()
    root.title("Edit Patient Details")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=350, height=400, bg="light cyan")
    frame.place(x=370, y=150)

    heading = Label(frame, text='Edit Patient Details', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=30, y=10)

    Label(frame, text='Patient ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=100)
    patdocid_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    patdocid_entry.place(x=30, y=130)

    Label(frame, text='Detail to edit:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=170)
    editdet_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    editdet_entry.place(x=30, y=200)

    Label(frame, text='New value for detail:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=240)
    newval_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    newval_entry.place(x=30, y=270)

    Button(frame, text="Edit Details", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_edit_patient).place(x=75, y=320)

    root.mainloop()

homepage()
