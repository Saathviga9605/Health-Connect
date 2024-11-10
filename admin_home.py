from tkinter import *
from tkinter import messagebox
from tkinter import ttk, simpledialog
from connect_Test import (delete_doctor, delete_patient, add_doctor, edit_doctor_details, edit_patient_details, add_patient, get_patient_data, get_doctor_data, get_doctors_by_dept, get_patients_by_dept, DB_Connect)
import time

# Singleton Pattern for Database Connection
class DB_Connect_Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = DB_Connect()  # Assuming DB_Connect is defined elsewhere
        return cls._instance

# Observer Pattern for Logging
class Observer:
    def update(self, message):
        raise NotImplementedError

class Logger(Observer):
    def update(self, message):
        print(f"LOG: {message}")  # Log the message

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

# Facade Pattern for Patient Data Management
class PatientDataFacade:
    def __init__(self, db_connect):
        self.db_connect = db_connect

    def get_patient_with_department(self, patient_id):
        patient_query = """SELECT ID, Name, Contact_Number, Disease_Name, 
                           Treatment_Details, Department, Doctor_id 
                           FROM Patients WHERE ID = :id"""
        department_query = """SELECT * FROM Departments 
                              WHERE Dept_id = (SELECT Department
                              FROM Patients WHERE ID = :id)"""

        try:
            # Fetching patient details
            self.db_connect.cursor.execute(patient_query, {"id": patient_id})
            patient_data = self.db_connect.cursor.fetchone()

            # Fetching related department details
            self.db_connect.cursor.execute(department_query, {"id": patient_id})
            department_data = self.db_connect.cursor.fetchone()

            return {"patient": patient_data, "department": department_data}
        except Exception as e:
            print(f"Error fetching patient or department data: {e}")
            return None
#STARTEGY
class SearchStrategy:
    def search(self, query):
        raise NotImplementedError

class SearchByName(SearchStrategy):
    def search(self, query):
        # Replace with actual database search logic
        cursor = DB_Connect().cursor  # Assuming DB_Connect establishes a connection
        query_string = "SELECT * FROM Patients WHERE Name LIKE :name"
        cursor.execute(query_string, {"name": f"%{query}%"})
        return cursor.fetchall()  # Return all matching records

class SearchByDisease(SearchStrategy):
    def search(self, query):
        # Replace with actual database search logic
        cursor = DB_Connect().cursor  # Assuming DB_Connect establishes a connection
        query_string = "SELECT * FROM Patients WHERE Disease_Name LIKE :disease"
        cursor.execute(query_string, {"disease": f"%{query}%"})
        return cursor.fetchall()  # Return all matching records

class SearchByDepartment(SearchStrategy):
    def search(self, query):
        # Replace with actual database search logic
        cursor = DB_Connect().cursor  # Assuming DB_Connect establishes a connection
        query_string = "SELECT * FROM Patients WHERE Department = :department"
        cursor.execute(query_string, {"department": query})
        return cursor.fetchall()  # Return all matching records

class PatientSearchContext:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute_search(self, query):
        return self.strategy.search(query)

def search_patient():
    def perform_search():
        query = query_entry.get()
        if not query:
            messagebox.showerror("Input Error", "Please enter a search term.")
            return

        # Get selected search strategy
        if search_var.get() == "name":
            context = PatientSearchContext(SearchByName())
        elif search_var.get() == "disease":
            context = PatientSearchContext(SearchByDisease())
        elif search_var.get() == "department":
            context = PatientSearchContext(SearchByDepartment())
        else:
            messagebox.showerror("Input Error", "Invalid search option.")
            return

        results = context.execute_search(query)
        if results:
            # Display results in a new window (you can implement this)
            display_search_results(results)
        else:
            messagebox.showinfo("No Results", "No patients found.")

    root = Toplevel()
    root.title("Search Patient")
    root.geometry("1000x600+400+200")
    root.resizable(False,False)

    login_bg_image = PhotoImage(file="hospital.png")
    Label(root, image=login_bg_image).place(relheight=1, relwidth=1)
    
    search_var = StringVar(value="name")  # Default search option

    Label(root, text="Search Patient", font=('georgia', 24)).place(x=440,y=70)

    frame = Frame(root, width=350, height=350, bg="LightYellow")
    frame.place(x=370, y=120)

    
    #Button(patterns_window, text="Singleton Demo",width=30,bg='lemon chiffon',border=4,font=('georgia',12),command=singleton_demo).place(x=400,y=200)
    Radiobutton(frame, text="By Name", variable=search_var, value="name",font=('georgia',12)).place(x=100,y=50)
    Radiobutton(frame, text="By Disease", variable=search_var, value="disease",font=('georgia',12)).place(x=100,y=100)
    Radiobutton(frame, text="By Department", variable=search_var, value="department",font=('georgia',12)).place(x=100,y=150)

    Label(frame, text="Enter Search Query:",font=('georgia',12)).place(x=50,y=200)
    query_entry = Entry(frame,width=35)
    query_entry.place(x=50,y=250)

    Button(frame,text="Search",font=('georgia',12),command=perform_search).place(x=140,y=300)

    root.mainloop()

def display_search_results(results):
    results_window = Toplevel()
    results_window.title("Search Results")
    results_window.geometry("1000x600+400+200")
    results_window.resizable(False,False)

    tree = ttk.Treeview(results_window, columns=("ID", "Name", "Contact", "Disease", "Department"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact", text="Contact")
    tree.heading("Disease", text="Disease")
    tree.heading("Department", text="Treatment Details")

    for result in results:
        tree.insert("", "end", values=result)

    tree.pack(fill="both", expand=True)


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

    global admin_image 
    admin_image = PhotoImage(file="hospital.png")
    Label(admin_root, image=admin_image).place(relheight=1, relwidth=1)

    frame = Frame(admin_root, width=400, height=500, bg="light cyan")
    frame.place(x=350, y=120)

    Label(frame, text='Admin Dashboard', fg='#57a1f8', bg='white', font=('Georgie', 24, 'bold')).place(x=65, y=10)

    Button(frame, width=20, text="Manage patient", bg='lemon chiffon', border=4, font=('Georgia', 12), command=adminpatientmgmt).place(x=110, y=100)
    Button(frame, width=20, text="Manage doctor", bg='lemon chiffon', border=4, font=('Georgia', 12), command=admindoctormgmt).place(x=110, y=200)
    Button(frame, width=20, text="View details", bg='lemon chiffon', border=4, font=('Georgia', 12), command=viewdetails).place(x=110, y=300)

    # Add buttons for design patterns
    Button(frame, width=20, text="Show Design Patterns", bg='lemon chiffon', border=4, font=('Georgia', 12), command=show_design_patterns).place(x=110, y=400)

def show_design_patterns():
    # Create a new window to show design patterns
    patterns_window = Toplevel()
    patterns_window.title("Design Patterns Demonstration")
    patterns_window.geometry("1000x600+400+200")

    global admin_bg_image 
    admin_bg_image = PhotoImage(file="hospital.png")
    Label(patterns_window, image=admin_bg_image).place(relheight=1, relwidth=1)


    
    # Singleton Pattern Demonstration
    def singleton_demo():
        db_connect1 = DB_Connect_Singleton()
        db_connect2 = DB_Connect_Singleton()
        if db_connect1 is db_connect2:
            messagebox.showinfo("Singleton Pattern", "Only one instance of DB_Connect exists.")
        else:
            messagebox.showerror("Singleton Pattern", "Multiple instances exist!")

    # Observer Pattern Demonstration
    def observer_demo():
        logger = Logger()
        subject = Subject()
        subject.attach(logger)
        subject.notify("Observer Pattern: A new operation has been performed.")
        messagebox.showinfo("Observer Pattern", "Observer has been notified.")

    # Facade Pattern Demonstration
    def facade_demo():
        patient_id = simpledialog.askinteger("Input", "Enter patient ID:")
        db_connect = DB_Connect_Singleton()
        facade = PatientDataFacade(db_connect)
        patient_info = facade.get_patient_with_department(patient_id)  # Example patient ID
        if patient_info:
            messagebox.showinfo("Facade Pattern", f"Patient Info: {patient_info['patient']}\nDepartment Info: {patient_info['department']}")
        else:
            messagebox.showerror("Facade Pattern", "Failed to fetch patient data.")

    # Add buttons for each design pattern demonstration
    Button(patterns_window, text="Singleton Demo",width=30,bg='lemon chiffon',border=4,font=('georgia',12),command=singleton_demo).place(x=400,y=200)
    Button(patterns_window, text="Observer Demo", width=30,bg='lemon chiffon',border=4,font=('georgia',12),command=observer_demo).place(x=400,y=250)
    Button(patterns_window, text="Strategy Demo",width=30,bg='lemon chiffon',border=4,font=('georgia',12), command=search_patient).place(x=400,y=300)
    Button(patterns_window, text="Facade Demo",width=30,bg='lemon chiffon',border=4,font=('georgia',12), command=facade_demo).place(x=400,y=350)


def adminpatientmgmt():
    root = Toplevel()
    root.title("Patient Management")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    image_path = PhotoImage(file="hospital.png")
    bg_image = Label(root, image=image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=400, height=500, bg="light cyan")
    frame.place(x=350, y=80)

    heading = Label(frame, text='Patient Management', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=45, y=10)

    Button(frame, width=20, text="Add patient", bg='lemon chiffon', border=4, font=('Georgia', 12), command=addpatient).place(x=110, y=100)
    Button(frame, width=20, text="Remove patient", bg='lemon chiffon', border=4, font=('Georgia', 12), command=removepatient).place(x=110, y=200)
    Button(frame, width=20, text="Edit details ", bg='lemon chiffon', border=4, font=('Georgia', 12), command=editpatdetails).place(x=110, y=300)
    #Button(frame,width=20,text='Search patient',bg='lemon chiffon', border=4, font=('Georgia', 12), command=search_patient).place(x=110, y=400)

    root.mainloop()

def admindoctormgmt():
    root = Toplevel()
    root.title("Doctor Management")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=400, height=350, bg="light cyan")
    frame.place(x=350, y=120)

    heading = Label(frame, text='Doctor Management', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
    heading.place(x=55, y=10)

    Button(frame, width=20, text="Add doctor", bg='lemon chiffon', border=4, font=('Georgia', 12), command =adddoctor).place(x=110, y=100)
    Button(frame, width=20, text="Remove doctor", bg='lemon chiffon', border=4, font=('Georgia', 12), command=removedoctor).place(x=110, y=200)
    Button(frame, width=20, text="Edit details ", bg='lemon chiffon', border=4, font=('Georgia', 12), command=editdocdetails).place(x=110, y=300)
    
    root.mainloop()

def viewdetails():
    root = Toplevel()
    root.title("View Doctor and Patient Details")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=500, height=500, bg="light cyan")
    frame.place(x=275, y=80)

    heading = Label(frame, text='View Details', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
    heading.place(x=160, y=10)

    Button(frame, width=30, text="View Patients", bg='lemon chiffon', border=4, font=('Georgia', 12), command=viewpatient).place(x=110, y=100)
    Button(frame, width=30, text="View Doctors", bg='lemon chiffon', border=4, font=('Georgia', 12), command=viewdoctor).place(x=110, y=200)
    Button(frame, width=30, text="Find Doctors by Department", bg='lemon chiffon', border=4, font=('Georgia', 12), command=viewdoctorsbydept).place(x=110, y=300)
    Button(frame, width=30, text="Find Patients by Department", bg='lemon chiffon', border=4, font=('Georgia', 12), command=viewpatientsbydept).place(x=110, y=400)

def viewpatient():
    root = Toplevel()
    root.title("View Patient Data")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    frame = Frame(root)
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

    frame = Frame(root)
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
            print("Data missing for doctor :", doctor) 

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

def viewdoctorsbydept():
    root = Toplevel()
    root.title("View Doctors by Department")
    root.geometry("800x500+400+200")
    root.resizable(False, False)

    root.configure(bg="#f0f0f0")  # Light gray background

    dept_input = simpledialog.askstring("Input", "Enter Department ID")

    frame = Frame(root, bg="#ffffff", bd=2, relief="solid")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=("D_Id", "Name", "Department"), show="headings")
    tree.heading("D_Id", text="Doctor ID")
    tree.heading("Name", text="Name")
    tree.heading("Department", text="Department")

    for col in ("D_Id", "Name", "Department"):
        tree.column(col, width=150, anchor="center")

    doctor_data = get_doctors_by_dept(dept_input)
    for doctor in doctor_data:
        if dept_input.lower() in str(doctor[2]).lower():
            tree.insert("", "end", values=doctor)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

def viewpatientsbydept():
    root = Toplevel()
    root.title("View Patients by Department")
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.configure(bg="#f0f0f0")  # Example light gray color

    dept_input = simpledialog.askstring("Input", "Enter Department ID")

    frame = Frame(root, bg="#ffffff", bd=2, relief="solid")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact_Number", "Disease_Name", "Treatment_Details", "Department", "Doctor_id"), show="headings")
    tree.heading("ID", text="Patient ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact_Number", text="Contact Number")
    tree.heading("Disease_Name", text="Disease Name")
    tree.heading("Treatment_Details", text="Treatment Details")
    tree.heading("Department", text="Department")
    tree.heading("Doctor_id", text="Doctor ID")

    for col in ("ID", "Name", "Contact_Number", "Disease_Name", "Treatment_Details", "Department", "Doctor_id"):
        tree.column(col, width=120, anchor="center")

    patient_data = get_patients_by_dept(dept_input)
    for patient in patient_data:
        if dept_input.lower() in str(patient[5]).lower():
            tree.insert("", "end", values=patient)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

def adddoctor():
    def submit_doctor():
        if not d_id_entry.get() or not name_entry.get() or not dname_entry.get():
            messagebox.showerror("Input Error", "Value required in all fields")
            return
        add_doctor(d_id_entry.get(), name_entry.get(), dname_entry.get())
        messagebox.showinfo("Success", "Doctor added successfully")

    global d_id_entry, name_entry, dname_entry
    root = Toplevel()
    root.title("Add Doctor")
    root.configure(bg='#fff')
    root.geometry("1000x600+400+200")
    root.resizable(False, False)

    root.image_path = PhotoImage(file="hospital.png")  
    bg_image = Label(root, image=root.image_path)
    bg_image.place(relheight=1, relwidth=1)

    frame = Frame(root, width=350, height=450, bg="light cyan")
    frame.place(x=370, y=130)

    heading = Label(frame, text='Add doctor', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light ', 24, 'bold'))
    heading.place(x=85, y=10)

    Label(frame, text=' Doctor ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=100)
    d_id_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    d_id_entry.place(x=30, y=130)

    Label(frame, text='Name:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=170)
    name_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    name_entry.place(x=30, y=200)

    Label(frame, text='Department:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=240)
    dname_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    dname_entry.place(x=30, y=270)

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

    heading = Label(frame, text='Remove doctor', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
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

    heading = Label(frame, text='Add Patient', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
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

def check_patient_exists(patient_id):
    try:
        cursor = DB_Connect().cursor  # Assuming DB_Connect establishes a connection
        query = "SELECT COUNT(*) FROM Patients WHERE ID = :id"
        cursor.execute(query, {"id": patient_id})
        count = cursor.fetchone()[0]
        return count > 0  # Returns True if patient exists, False otherwise
    except Exception as e:
        print(f"Error checking if patient exists: {e}")
        return False

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

    heading = Label(frame, text='Remove Patient', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
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

    heading = Label(frame, text='Edit Patient Details', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI light', 24, 'bold'))
    heading.place(x=30, y=10)

    Label(frame, text='Patient ID:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=100)
    patdocid_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light ', 11))
    patdocid_entry.place(x=30, y=130)

    Label(frame, text='Detail to edit:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=170)
    editdet_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    editdet_entry.place(x=30, y=200)

    Label(frame, text='New value for detail:', fg='black', font=('Microsoft YaHei UI light', 11)).place(x=30, y=240)
    newval_entry = Entry(frame, width=35, fg='black', border=2, bg='white', font=('Microsoft YaHei UI light', 11))
    newval_entry.place(x=30, y=270)

    Button(frame, text="Edit Details", width=20, bg='lemon chiffon', font=('Georgia', 12), command=submit_edit_patient).place(x=75, y=320)

    root.mainloop()

def design_patterns():
    # Initialize the logger and subject for the observer pattern
    logger = Logger()
    subject = Subject()
    subject.attach(logger)

    # Example of logging an operation
    subject.notify("Design patterns implemented in the hospital management system.")

    # Example of using the facade pattern
    db_connect = DB_Connect_Singleton()
    facade = PatientDataFacade(db_connect)
    patient_info = facade.get_patient_with_department(1)  # Example patient ID
    if patient_info:
        print("Patient Info:", patient_info)


homepage()