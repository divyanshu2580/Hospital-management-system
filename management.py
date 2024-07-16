import tkinter as tk
from tkinter import *
from tkinter import ttk , messagebox 
from PIL import Image , ImageTk
import pymysql
import hashlib
from tkcalendar import Calendar
import subprocess
import platform
from dotenv import load_dotenv , dotenv_values
load_dotenv()
import os
from datetime import date as dt_date ,timedelta

root_password = os.getenv("ROOT_PASSWORD")
admin_password = os.getenv("ADMIN_PASSWORD")
admin_username = os.getenv("ADMIN_USERNAME")

connection_params = {
    'host': 'localhost',  
    'user': 'root',       
    'password': root_password, 
    'database': 'hospital_management_system',  }
try:
    conn = pymysql.connect(**connection_params)
    print(f"Connection successful to database : {connection_params['database']}")
    
    def fade_in(frame, alpha=0):
        alpha = min(alpha, 1)
        frame.update()
        frame.tkraise()
        color = int(alpha * 128)  
        if alpha < 1:
            frame.config(bg=f"#{0:02x}{0:02x}{color:02x}")
            alpha += 0.1
            root.after(50, fade_in, frame, alpha)
        else:
            frame.config(bg="white")

    def fade_out(frame, next_frame, alpha=1):
        alpha = max(alpha, 0)
        frame.update()
        color = int(alpha * 128)  
        if alpha > 0:
            frame.config(bg=f"#{0:02x}{0:02x}{color:02x}")
            alpha -= 0.1
            root.after(50, fade_out, frame, next_frame, alpha)
        else:
            next_frame.tkraise()
            fade_in(next_frame)

    def show_frame(next_frame):
        global current_frame
        fade_out(current_frame, next_frame)
        current_frame = next_frame

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width-14}x{screen_height-85}+0+0")
    root.title("Care Connect")
    root.iconbitmap("images/logo.ico")

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Start page 

    start_frame = tk.Frame(container, bg="white")
    label1 = tk.Label(start_frame, text=" CARE CONNECT " , bg="navy" , fg="white", font=("Futura" , 50))
    label1.pack(pady=40)

    image_path = "images/logo.png"
    logo_image = Image.open(image_path)
    logo_image = logo_image.resize((1000,250) , Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    image_label = tk.Label(start_frame, image=logo_photo, border=0)
    image_label.pack(pady=50)

    start_nav_frame = tk.Frame(start_frame , bg="white" , border=0)
    start_nav_frame.pack(side="top", pady=50)

    button1 = tk.Button(start_nav_frame, text="Doctor", font=("Futura" , 20), bg="navy" , fg="white",command=lambda: show_frame(doc_login_frame))
    button1.pack(side="left",padx=20)

    button2 = tk.Button(start_nav_frame, text="Patient", font=("Futura" , 20), bg="navy" , fg="white", command=lambda: show_frame(pat_login_frame))
    button2.pack(side="left",padx=20)

    button3 = tk.Button(start_nav_frame, text="Admin", font=("Futura" , 20), bg="navy" , fg="white", command=lambda: show_frame(admin_login_frame))
    button3.pack(side="left",padx=20)

    start_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # patient signup page

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def patient_signup():
        username_pat = entry_username_pat.get()
        email_pat = entry_patemail.get()
        gender_pat = gender_var_pat.get()
        age_pat = entry_age_pat.get()
        address_pat = entry_address_pat.get()
        password_pat = entry_password_pat.get()
        if username_pat and password_pat:
            hashed_password = hash_password(password_pat)
            try:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO patient(p_email,p_name,p_age,gender,address,password) VALUES (%s, %s,%s,%s, %s ,%s)"
                    cursor.execute(sql, (email_pat,username_pat,age_pat,gender_pat,address_pat, hashed_password))
                    conn.commit()

                messagebox.showinfo("Success", "User registered successfully!")
                entry_username_pat.delete(0, tk.END)
                entry_password_pat.delete(0, tk.END)
                entry_age_pat.delete(0,tk.END)
                entry_address_pat.delete(0,tk.END)
                entry_patemail.delete(0,tk.END)
                gender_var_pat.set("Select Gender")
                show_frame(pat_login_frame)

            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def clear_pat_signup():
        entry_username_pat.delete(0, tk.END)
        entry_password_pat.delete(0, tk.END)
        entry_patemail.delete(0, tk.END)
        gender_var_pat.set("Select Gender")
        entry_address_pat.delete(0, tk.END)
        entry_age_pat.delete(0,tk.END)


    pat_signup_frame = tk.Frame(container, bg="white")

    image_path5 = "images/logo.png"
    logo_image5 = Image.open(image_path5)
    logo_image5 = logo_image5.resize((200,60) , Image.LANCZOS)
    logo_photo5 = ImageTk.PhotoImage(logo_image5)

    image_label5 = tk.Label(pat_signup_frame, image=logo_photo5, border=0)
    image_label5.pack(pady=20)

    pat_signup_nav_frame = tk.Frame(pat_signup_frame , bg="navy")
    pat_signup_nav_frame.pack(side="top",fill="x", ipady=5)

    button1 = tk.Button(pat_signup_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(start_frame))
    button1.pack(side="left",padx=5)

    button5 = tk.Button(pat_signup_nav_frame, text="Login", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(pat_login_frame))
    button5.pack(side="left",padx=5)

    button2 = tk.Button(pat_signup_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button2.pack(side="right",padx=10)

    button3 = tk.Button(pat_signup_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=clear_pat_signup)
    button3.pack(side="right",padx=5)

    label2 = tk.Label(pat_signup_frame, text="Sign Up", bg="white" , fg="navy", font=("Futura" , 30))
    label2.pack(pady=10, padx=20,ipadx=20)

    pat_email_sign_frame = tk.Frame(pat_signup_frame , bg="navy")
    pat_email_sign_frame.pack(side="top")

    label_patemail = tk.Label(pat_email_sign_frame, text="  Enter  User  Email:   ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_patemail.pack(side="left", padx=10 , pady=10)
    entry_patemail = tk.Entry(pat_email_sign_frame, bg='white',border=1,font=('Times New Roman', 20) )
    entry_patemail.pack(side="left", padx=10 , pady=10)

    pat_username_sign_frame = tk.Frame(pat_signup_frame , bg="navy")
    pat_username_sign_frame.pack(side="top")

    label_username_pat = tk.Label(pat_username_sign_frame, text="    Enter  Username:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_username_pat.pack(pady=5, side="left", padx=10)
    entry_username_pat = tk.Entry(pat_username_sign_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_username_pat.pack(side="left", padx=10 , pady=5)

    pat_age_sign_frame = tk.Frame(pat_signup_frame , bg="navy")
    pat_age_sign_frame.pack(side="top")

    label_age_pat = tk.Label(pat_age_sign_frame, text="    Enter  Your Age:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_age_pat.pack(pady=5, side="left", padx=10)
    entry_age_pat = tk.Entry(pat_age_sign_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_age_pat.pack(side="left", padx=10 , pady=5)

    gender_sign_frame_pat = tk.Frame(pat_signup_frame , bg="navy")
    gender_sign_frame_pat.pack(side="top")

    label_patgender = tk.Label(gender_sign_frame_pat, text=" Select  your Gender:     ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_patgender.pack(side="left", padx=10 , pady=10)

    gender_var_pat = tk.StringVar()
    gender_var_pat.set("Select Gender")  

    genders_pat = ["Male", "Female", "Other"]
    gender_menu_pat = tk.OptionMenu(gender_sign_frame_pat, gender_var_pat, *genders_pat)
    gender_menu_pat.pack(side="left", padx=40, pady=10)
    gender_menu_pat.configure(bg='dark slate blue', fg='white',font=('Times New Roman', 20))

    address_sign_frame_pat = tk.Frame(pat_signup_frame , bg="navy")
    address_sign_frame_pat.pack(side="top")

    label_address_pat = tk.Label(address_sign_frame_pat, text="     Enter   Address:     ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_address_pat.pack(pady=5, side="left", padx=10)
    entry_address_pat = tk.Entry(address_sign_frame_pat, bg='white',font=('Times New Roman', 20), border=1)
    entry_address_pat.pack(side="left", padx=10 , pady=5)

    pass_sign_frame_pat = tk.Frame(pat_signup_frame , bg="navy")
    pass_sign_frame_pat.pack(side="top")

    label_password_pat = tk.Label(pass_sign_frame_pat, text="Create your Password:",bg='navy', fg='white',font=('Times New Roman', 20))
    label_password_pat.pack(side="left", padx=10 , pady=10)
    entry_password_pat = tk.Entry(pass_sign_frame_pat, bg='white',border=1,font=('Times New Roman', 20) ,show="*")  # Show * for password
    entry_password_pat.pack(side="left", padx=10 , pady=10)

    login_page_label_pat = tk.Label(pat_signup_frame, text="already signed up ??", font=('Times New Roman', 15 ,"underline"), bg="white" ,fg="steel blue")
    login_page_label_pat.pack(side="top",pady=10)
    login_page_label_pat.bind("<Button-1>",lambda e: show_frame(pat_login_frame))

    tk.Button(pat_signup_frame, text='Sign Up', font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=patient_signup).pack(side="top", padx=0, pady=45)

    pat_signup_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # patient login page

    def patient_login():
        log_username_pat = entry_usernamepat_log.get()
        log_password_pat = entry_password_pat_log.get()

        if log_username_pat and log_password_pat:
            hashed_password = hash_password(log_password_pat)
            try:
                with conn.cursor() as cursor:
                    sql = "SELECT password FROM patient WHERE p_name = %s"
                    cursor.execute(sql, (log_username_pat,))
                    result = cursor.fetchone()

                    if result:
                        db_hashed_password = result[0]  
                        if hashed_password == db_hashed_password:
                            messagebox.showinfo("Success", "Login successful!")
                            entry_usernamepat_log.delete(0, tk.END)
                            entry_password_pat_log.delete(0, tk.END)
                            show_frame(patient_frame)

                        else:
                            messagebox.showerror("Login Failed", "Incorrect password!")
                    else:
                        messagebox.showerror("Login Failed", "Username not found!")

            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def clear_pat_login():
        entry_usernamepat_log.delete(0, tk.END)
        entry_password_pat_log.delete(0, tk.END)
    
    pat_login_frame = tk.Frame(container, bg="white")

    image_path2 = "images/logo.png"
    logo_image2 = Image.open(image_path2)
    logo_image2 = logo_image2.resize((200,60) , Image.LANCZOS)
    logo_photo2 = ImageTk.PhotoImage(logo_image2)

    image_label2 = tk.Label(pat_login_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    pat_login_nav_frame = tk.Frame(pat_login_frame , bg="navy")
    pat_login_nav_frame.pack(side="top",fill="x", ipady=5)

    button1 = tk.Button(pat_login_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(start_frame))
    button1.pack(side="left",padx=5)

    button2 = tk.Button(pat_login_nav_frame, text="Sign Up", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(pat_signup_frame))
    button2.pack(side="left",padx=5)

    button3 = tk.Button(pat_login_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(pat_login_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=clear_pat_login)
    button4.pack(side="right",padx=5)

    label2 = tk.Label(pat_login_frame, text="Login", bg="white" , fg="navy", font=("Futura" , 30))
    label2.pack(pady=10, padx=20,ipadx=20)

    image_path6 = "images/login.png"
    logo_image6 = Image.open(image_path6)
    logo_image6 = logo_image6.resize((224,140) , Image.LANCZOS)
    logo_photo6 = ImageTk.PhotoImage(logo_image6)

    image_label6 = tk.Label(pat_login_frame, image=logo_photo6, border=0 , bg="white")
    image_label6.pack(pady=20)

    username_pat_frame = tk.Frame(pat_login_frame, bg="navy")
    username_pat_frame.pack(side="top",ipadx=10,ipady=10)

    label_usernamepat_log= tk.Label(username_pat_frame, text="    Enter  Username:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_usernamepat_log.pack(pady=5, side="left", padx=10)
    entry_usernamepat_log = tk.Entry(username_pat_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_usernamepat_log.pack(side="left", padx=10 , pady=5)

    pass_pat_frame = tk.Frame(pat_login_frame , bg="navy")
    pass_pat_frame.pack(side="top",ipadx=10,ipady=10)

    label_password_pat_log = tk.Label(pass_pat_frame, text="    Enter  Password:     " ,bg='navy', fg='white',font=('Times New Roman', 20))
    label_password_pat_log.pack(side="left", padx=10 , pady=10)
    entry_password_pat_log = tk.Entry(pass_pat_frame, bg='white',border=1,font=('Times New Roman', 20) ,show="*")  
    entry_password_pat_log.pack(side="left", padx=10 , pady=10)

    login_page_label = tk.Label(pat_login_frame, text="Don't have account ??", font=('Times New Roman', 15 ,"underline"), bg="white" ,fg="steel blue")
    login_page_label.pack(side="top",pady=10)
    login_page_label.bind("<Button-1>",lambda e: show_frame(pat_signup_frame))

    tk.Button(pat_login_frame, text='Login', font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=patient_login).pack(side="top", padx=0, pady=45)

    pat_login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # patient frame 

    def display_appointment():
        query1 = "select distinct  a.a_id, p.p_name,a.app_date, a.app_time, a.status from appointments AS a inner join patient AS p on p.p_name = a.p_name order by a.app_date, a.app_time"

        with conn.cursor() as cursor:

            cursor.execute(query1)
            conn.commit()
            data3 = cursor.fetchall()
            return data3
        
    patient_frame = tk.Frame(container, bg="white")

    image_label2 = tk.Label(patient_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    pat_name_label = tk.Label(patient_frame, text=f"Welcome Patient", bg="white" , fg="navy", font=("Futura" , 30))
    pat_name_label.pack(pady=10, padx=20,ipadx=20)
    
    patient_nav_frame = tk.Frame(patient_frame , bg="navy")
    patient_nav_frame.pack(side="top",fill="x", ipady=5)

    button2 = tk.Button(patient_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(patient_frame))
    button2.pack(side="left",padx=5)
    
    def refresh_data_sch():
        update_display(tree1)

    def logout_patient():
        show_frame(start_frame)
        clear_pat_login()

    button1 = tk.Button(patient_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=logout_patient )
    button1.pack(side="left",padx=5)

    button3 = tk.Button(patient_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(patient_nav_frame, text="Refresh", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=refresh_data_sch)
    button4.pack(side="right",padx=5)
    
    patient_button_frame = tk.Frame(patient_frame , bg="white" , border=0)
    patient_button_frame.pack(side="top", pady=20)

    button1 = tk.Button(patient_button_frame, text="Schedule Appointments ", font=("Futura" , 20), bg="dark slate blue" , fg="white",command=lambda: show_frame(schedule_app_frame))
    button1.pack(side="left",padx=20)

    button2 = tk.Button(patient_button_frame, text="View Your History", font=("Futura" , 20), bg="dark slate blue" , fg="white", command=lambda: show_frame(patient_history_frame))
    button2.pack(side="left",padx=20)
    
    schedules_label = tk.Label(patient_frame, text=f"Schedules", bg="white" ,border=0, fg="navy", font=("Futura" , 20))
    schedules_label.pack(pady=10)
    
    style1 = ttk.Style(patient_frame)
    style1.theme_use('alt')

    style1.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25, font=('Futura', 12))
    style1.configure("Treeview.Heading", background="navy", foreground="white", font=('Futura', 12, 'bold'))

    def populate_treeview(tree1, data3):
        tree1.delete(*tree1.get_children())
        for row in data3:
            tree1.insert("", "end", values=row)

    def update_display(tree1):
        data3 = display_appointment()
        populate_treeview(tree1, data3)

    tree1 = ttk.Treeview(patient_frame, columns=('a_id','p_name','a_date','start_time','status'), show="headings", style="Treeview")

    data3 = display_appointment()
    tree1.heading("a_id", text="Scheduling ID")
    tree1.heading("p_name", text="Patient Name")
    tree1.heading("a_date", text="Scheduled Date")
    tree1.heading("start_time", text="Scheduled Time")
    tree1.heading("status", text="Medication Status")

    update_display(tree1)

    tree1.pack(fill="both",expand=True)

    patient_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # appointment frame 

    def add_appointment(p_name,app_date, app_time, symptoms, concerns):
        try:
            with conn.cursor() as cursor:

                app_time_formatted = f"{app_time}:00"

                query = "INSERT INTO appointments (p_name,app_date, app_time, symptoms, concerns) VALUES (%s,%s, %s, %s, %s)"
                cursor.execute(query, (p_name,app_date, app_time_formatted, symptoms, concerns))

                conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Appointment Booked!!")
                clear_schedule_appointment()
        except Exception as e:
            messagebox.showwarning(f"Error adding appointment:",e)

    def clear_schedule_appointment():
        hour_var.set("Select The Time")
        entry_symptoms.delete(0, tk.END)
        entry_pat_app_name.delete(0, tk.END)
        entry_concerns.delete(0, tk.END)
        date_label.config(text="Selected Date: None")

    def select_datetime():
        def on_select():
            selected_date = cal.get_date()
            date_label.config(text=f"Selected Date: {selected_date}")
            datetime_window.destroy()

        datetime_window = tk.Toplevel(root)
        datetime_window.title("Care Connect")
        datetime_window.geometry('300x270+150+300')
        datetime_window.iconbitmap("images/logo.ico")

        today = dt_date.today()
        max_date = today + timedelta(days=7)
        cal = Calendar(datetime_window, selectmode='day', date_pattern='yyyy-mm-dd', mindate=today, maxdate=max_date,
                    background='dark slate blue', foreground='white', headersbackground='navy', headersforeground='white',
                    selectbackground='navy', selectforeground='white')
        cal.pack(padx=10, pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Futura", 16), background="dark slate blue", foreground="white")

        select_button = ttk.Button(datetime_window, text="Select", command=on_select, style="TButton")
        select_button.pack(padx=10, pady=10)

    def submit_appointment():
        selected_date = date_label.cget("text").replace("Selected Date: ", "")
        selected_hour = hour_var.get()

        if selected_date == "None" or selected_hour == "Select The Time":
            print("Please select a valid date and time.")
            return

        symptoms = entry_symptoms.get()
        concerns = entry_concerns.get()
        pat_name=entry_pat_app_name.get()

        add_appointment(pat_name,selected_date, selected_hour, symptoms, concerns)
        
    def refresh_data():
        update_display(tree3)
            
    appointment_frame = tk.Frame(container, bg="navy")
    
    
    schedule_app_frame = tk.Frame(container, bg="white")

    image_label2 = tk.Label(schedule_app_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    sch_name_label = tk.Label(schedule_app_frame, text=f"Schedule Appointment ", bg="white" , fg="navy", font=("Futura" , 30))
    sch_name_label.pack(pady=10, padx=20,ipadx=20)
    
    schedule_nav_frame = tk.Frame(schedule_app_frame , bg="navy")
    schedule_nav_frame.pack(side="top",fill="x", ipady=5)

    button2 = tk.Button(schedule_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(patient_frame))
    button2.pack(side="left",padx=5)

    button1 = tk.Button(schedule_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=logout_patient)
    button1.pack(side="left",padx=5)


    button3 = tk.Button(schedule_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(schedule_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=clear_schedule_appointment)

    button4.pack(side="right",padx=5)

    pat_appointment_name_frame = tk.Frame(schedule_app_frame , bg="navy")
    pat_appointment_name_frame.pack(side="top",pady=5)

    label_pat_app_name = tk.Label(pat_appointment_name_frame, text="  Enter  Your Names :   ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_pat_app_name.pack(side="left", padx=10 , pady=10)
    entry_pat_app_name = tk.Entry(pat_appointment_name_frame, bg='white',border=1,font=('Times New Roman', 20) )
    entry_pat_app_name.pack(side="left", padx=10 , pady=10)


    button4 = tk.Button(schedule_app_frame, text="Select Date", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=select_datetime)
    button4.pack(side="top",padx=5,pady=10)

    date_label = tk.Label(schedule_app_frame, text="Selected Date: None", bg="white", fg="navy", font=("Futura", 16))
    date_label.pack(pady=5)
    
    time_frame = tk.LabelFrame(schedule_app_frame, text="          Select    Time    for    Appointment       ", bg="navy" , fg="white", font=("Futura" , 20))
    time_frame.pack(pady=5)

    hour_var = tk.StringVar(value="Select The Time")

    hours = [str(i).zfill(2) for i in range(9, 19)]

    hour_option = tk.OptionMenu(time_frame, hour_var, *hours)
    hour_option.grid( padx=145, pady=10)
    hour_option.config(width=20, bg="dark slate blue", fg="white", font=("Futura", 15))

    menu = hour_option.nametowidget(hour_option.menuname)
    menu.config(bg='dark slate blue', fg='white', font=("Futura", 10))

    symptoms_frame = tk.Frame(schedule_app_frame , bg="navy")
    symptoms_frame.pack(side="top",pady=5)

    label_symptoms = tk.Label(symptoms_frame, text="  Enter  Symptoms :   ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_symptoms.pack(side="left", padx=10 , pady=10)
    entry_symptoms = tk.Entry(symptoms_frame, bg='white',border=1,font=('Times New Roman', 20) )
    entry_symptoms.pack(side="left", padx=10 , pady=10)

    concerns_frame = tk.Frame(schedule_app_frame , bg="navy")
    concerns_frame.pack(side="top",pady=5)

    label_concerns = tk.Label(concerns_frame, text="    Enter  Concern :    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_concerns.pack(pady=5, side="left", padx=10)
    entry_concerns = tk.Entry(concerns_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_concerns.pack(side="left", padx=10 , pady=5)

    button5 = tk.Button(schedule_app_frame, text="Submit Application ", font=("Futura" , 20), bg="dark slate blue" , fg="white", command=submit_appointment)
    button5.pack(side="top",padx=5,pady=30)

    schedule_app_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # doctor signup page 

    def doctor_signup():
        username_doc = entry_usernamedoc.get()
        email_doc = entry_doc_email.get()
        gender_doc = gender_var.get()
        address_doc = entry_docaddress.get()
        specialist_doc = entry_specialist.get()
        age_doc = entry_age_doc.get()
        password_doc = entry_passworddoc.get()
        if username_doc and password_doc:
            hashed_password_doc = hash_password(password_doc)
            try:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO doctor(d_email,d_name,d_age,d_gender,d_address,specialist,d_password) VALUES (%s, %s ,%s ,%s,%s, %s ,%s)"
                    cursor.execute(sql, (email_doc,username_doc,age_doc,gender_doc,address_doc,specialist_doc, hashed_password_doc))
                    conn.commit()

                messagebox.showinfo("Success", "Doctor registered successfully!")
                entry_usernamedoc.delete(0, tk.END)
                entry_passworddoc.delete(0, tk.END)
                entry_doc_email.delete(0, tk.END)
                entry_age_doc.delete(0,tk.END)
                entry_specialist.delete(0, tk.END)
                gender_var.set("Select Gender")
                entry_docaddress.delete(0, tk.END)
                show_frame(doc_login_frame)

            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_doc_signup():
        entry_usernamedoc.delete(0, tk.END)
        entry_passworddoc.delete(0, tk.END)
        entry_doc_email.delete(0, tk.END)
        entry_specialist.delete(0, tk.END)
        entry_age_doc.delete(0,tk.END)
        gender_var.set("Select Gender")
        entry_docaddress.delete(0, tk.END)

    doc_signup_frame = tk.Frame(container, bg="white")

    image_path1 = "images/logo.png"
    logo_image1 = Image.open(image_path1)
    logo_image1 = logo_image1.resize((200,60) , Image.LANCZOS)
    logo_photo1 = ImageTk.PhotoImage(logo_image1)

    image_label1 = tk.Label(doc_signup_frame, image=logo_photo1, border=0)
    image_label1.pack(pady=20)

    doc_signup_nav_frame = tk.Frame(doc_signup_frame , bg="navy")
    doc_signup_nav_frame.pack(side="top",fill="x", ipady=5)

    button1 = tk.Button(doc_signup_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(start_frame))
    button1.pack(side="left",padx=5)

    button5 = tk.Button(doc_signup_nav_frame, text="Login", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(doc_login_frame))
    button5.pack(side="left",padx=5)

    button2 = tk.Button(doc_signup_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button2.pack(side="right",padx=10)

    button3 = tk.Button(doc_signup_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=clear_doc_signup)
    button3.pack(side="right",padx=5)

    label2 = tk.Label(doc_signup_frame, text="Sign Up", bg="white" , fg="navy", font=("Futura" , 30))
    label2.pack(pady=10, padx=20,ipadx=20)

    email_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    email_sign_frame.pack(side="top")

    label_docemail = tk.Label(email_sign_frame, text="  Enter  User  Email:   ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_docemail.pack(side="left", padx=10 , pady=10)
    entry_doc_email = tk.Entry(email_sign_frame, bg='white',border=1,font=('Times New Roman', 20) )
    entry_doc_email.pack(side="left", padx=10 , pady=10)

    username_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    username_sign_frame.pack(side="top")

    label_usernamedoc = tk.Label(username_sign_frame, text="    Enter  Username:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_usernamedoc.pack(pady=5, side="left", padx=10)
    entry_usernamedoc = tk.Entry(username_sign_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_usernamedoc.pack(side="left", padx=10 , pady=5)

    age_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    age_sign_frame.pack(side="top")

    label_doc_age = tk.Label(age_sign_frame, text="     Enter Your  Age:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_doc_age.pack(pady=5, side="left", padx=10)
    entry_age_doc = tk.Entry(age_sign_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_age_doc.pack(side="left", padx=10 , pady=5)

    gender_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    gender_sign_frame.pack(side="top")

    label_docgender = tk.Label(gender_sign_frame, text=" Select  your  Gender:     ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_docgender.pack(side="left", padx=10 , pady=10 )

    gender_var = tk.StringVar()
    gender_var.set("Select Gender")  

    genders = ["Male", "Female", "Other"]
    gender_menu = tk.OptionMenu(gender_sign_frame, gender_var, *genders)
    gender_menu.pack(side="left", padx=40, pady=10 )
    gender_menu.configure(bg='dark slate blue', fg='white',font=('Times New Roman', 20))

    address_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    address_sign_frame.pack(side="top")

    label_docaddress = tk.Label(address_sign_frame, text="     Enter   Address:     ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_docaddress.pack(pady=5, side="left", padx=10)
    entry_docaddress = tk.Entry(address_sign_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_docaddress.pack(side="left", padx=10 , pady=5)

    specialist_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    specialist_sign_frame.pack(side="top")

    label_specialist = tk.Label(specialist_sign_frame, text="    Enter  Speciality:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_specialist.pack(pady=5, side="left", padx=10)
    entry_specialist = tk.Entry(specialist_sign_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_specialist.pack(side="left", padx=10 , pady=5)

    pass_sign_frame = tk.Frame(doc_signup_frame , bg="navy")
    pass_sign_frame.pack(side="top")

    label_passworddoc = tk.Label(pass_sign_frame, text="Create your Password:",bg='navy', fg='white',font=('Times New Roman', 20))
    label_passworddoc.pack(side="left", padx=10 , pady=10)
    entry_passworddoc = tk.Entry(pass_sign_frame, bg='white',border=1,font=('Times New Roman', 20) ,show="*")  # Show * for password
    entry_passworddoc.pack(side="left", padx=10 , pady=10)

    login_page_label = tk.Label(doc_signup_frame, text="already signed up ??", font=('Times New Roman', 15 ,"underline"), bg="white" ,fg="steel blue")
    login_page_label.pack(side="top",pady=10)
    login_page_label.bind("<Button-1>",lambda e: show_frame(doc_login_frame))

    tk.Button(doc_signup_frame, text='Sign Up', font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=doctor_signup).pack(side="top", padx=0, pady=45)

    doc_signup_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # doctor login page 

    def doctor_login(): 
        log_username_doc = entry_usernamedoc_log.get()
        log_password_doc = entry_password_doc_log.get()

        if log_username_doc and log_password_doc:
            hashed_password_doc = hash_password(log_password_doc)
            try:
                with conn.cursor() as cursor:
                    sql = "SELECT d_password FROM doctor WHERE d_name = %s"
                    cursor.execute(sql, (log_username_doc,))
                    result = cursor.fetchone()

                    if result:
                        db_hashed_password_doc = result[0]  
                        if hashed_password_doc == db_hashed_password_doc:
                            messagebox.showinfo("Success", "Login successful!")
                            entry_usernamedoc.delete(0, tk.END)
                            entry_passworddoc.delete(0, tk.END)
                            show_frame(doctor_frame)

                        else:
                            messagebox.showerror("Login Failed", "Incorrect password!")
                    else:
                        messagebox.showerror("Login Failed", "Username not found!")

            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_doc_login():
        entry_usernamedoc_log.delete(0, tk.END)
        entry_password_doc_log.delete(0, tk.END)

    doc_login_frame = tk.Frame(container, bg="white")

    image_label2 = tk.Label(doc_login_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    doc_login_nav_frame = tk.Frame(doc_login_frame , bg="navy")
    doc_login_nav_frame.pack(side="top",fill="x", ipady=5)

    button1 = tk.Button(doc_login_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(start_frame))
    button1.pack(side="left",padx=5)

    button2 = tk.Button(doc_login_nav_frame, text="Sign Up", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(doc_signup_frame))
    button2.pack(side="left",padx=5)

    button3 = tk.Button(doc_login_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(doc_login_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=clear_doc_login)
    button4.pack(side="right",padx=5)

    label2 = tk.Label(doc_login_frame, text="Login", bg="white" , fg="navy", font=("Futura" , 30))
    label2.pack(pady=10, padx=20,ipadx=20)

    image_path3 = "images/login.png"
    logo_image3 = Image.open(image_path3)
    logo_image3 = logo_image3.resize((224,140) , Image.LANCZOS)
    logo_photo3 = ImageTk.PhotoImage(logo_image3)

    image_label4 = tk.Label(doc_login_frame, image=logo_photo3, border=0 , bg="white")
    image_label4.pack(pady=20)

    username_doc_frame = tk.Frame(doc_login_frame, bg="navy")
    username_doc_frame.pack(side="top",ipadx=10,ipady=10)

    label_usernamedoc_log= tk.Label(username_doc_frame, text="    Enter  Username:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_usernamedoc_log.pack(pady=5, side="left", padx=10)
    entry_usernamedoc_log = tk.Entry(username_doc_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_usernamedoc_log.pack(side="left", padx=10 , pady=5)

    pass_doc_frame = tk.Frame(doc_login_frame , bg="navy")
    pass_doc_frame.pack(side="top",ipadx=10,ipady=10)

    label_passworddoc_log = tk.Label(pass_doc_frame, text="    Enter  Password:     " ,bg='navy', fg='white',font=('Times New Roman', 20))
    label_passworddoc_log.pack(side="left", padx=10 , pady=10)
    entry_password_doc_log = tk.Entry(pass_doc_frame, bg='white',border=1,font=('Times New Roman', 20) ,show="*")  # Show * for password
    entry_password_doc_log.pack(side="left", padx=10 , pady=10)

    login_page_label = tk.Label(doc_login_frame, text="Don't have account ??", font=('Times New Roman', 15 ,"underline"), bg="white" ,fg="steel blue")
    login_page_label.pack(side="top",pady=10)
    login_page_label.bind("<Button-1>",lambda e: show_frame(doc_signup_frame))

    tk.Button(doc_login_frame, text='Login', font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=doctor_login).pack(side="top", padx=0, pady=45)

    doc_login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # doctor page 
    
    doctor_frame = tk.Frame(container, bg="white")
    
    image_label2 = tk.Label(doctor_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    doc_name_label = tk.Label(doctor_frame, text=f"Welcome Doctor", bg="white" , fg="navy", font=("Futura" , 30))
    doc_name_label.pack(pady=10, padx=20,ipadx=20)
    
    doctor_nav_frame = tk.Frame(doctor_frame , bg="navy")
    doctor_nav_frame.pack(side="top",fill="x", ipady=5)

    button2 = tk.Button(doctor_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(doctor_frame))
    button2.pack(side="left",padx=5)

    def log_out_doctor():
        show_frame(start_frame)
        clear_doc_login()

    button1 = tk.Button(doctor_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=log_out_doctor)
    button1.pack(side="left",padx=5)

    button3 = tk.Button(doctor_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(doctor_nav_frame, text="Refresh", font=("Futura" , 20), width= 10,bg="dark slate blue" , fg="white",command= refresh_data_sch)
    button4.pack(side="right",padx=5)
    
    doctor_button_frame = tk.Frame(doctor_frame , bg="white" , border=0)
    doctor_button_frame.pack(side="top", pady=20)

    button1 = tk.Button(doctor_button_frame, text="View Appointments ", font=("Futura" , 20), bg="dark slate blue" , fg="white",command=lambda: show_frame(appointment_frame))
    button1.pack(side="left",padx=20)

    button2 = tk.Button(doctor_button_frame, text="View Patient History", font=("Futura" , 20), bg="dark slate blue" , fg="white", command=lambda: show_frame(patient_history_frame))
    button2.pack(side="left",padx=20)

    style1 = ttk.Style(doctor_frame)
    style1.theme_use('alt')

    style1.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25, font=('Futura', 12))
    style1.configure("Treeview.Heading", background="navy", foreground="white", font=('Futura', 12, 'bold'))

    tree1 = ttk.Treeview(doctor_frame, columns=('a_id','p_name','a_date','start_time','status'), show="headings", style="Treeview")

    data3 = display_appointment()
    tree1.heading("a_id", text="Scheduling ID")
    tree1.heading("p_name", text="Patient Name")
    tree1.heading("a_date", text="Scheduled Date")
    tree1.heading("start_time", text="Scheduled Time")
    tree1.heading("status", text="Medication Status")

    update_display(tree1)

    tree1.pack(fill="both",expand=True)

    doctor_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # appointment_frame
    
    selected_row_id = None

    def handle_click(event):
        global selected_row_id
        region = tree3.identify("region", event.x, event.y)

        if region == "cell":
            column = tree3.identify_column(event.x)

            if column == "#7":
                item = tree3.item(tree3.focus())
                values = item['values']
                selected_row_id = values[0]
                
                option_dialog(root, ["Diagnosed", "Cancel"])

    def option_dialog(parent, options):
        dialog = tk.Toplevel(parent)
        dialog.title("Select Status")
        dialog.iconbitmap("images/logo.ico")
        dialog.configure(background="navy")
        dialog.geometry('200x200')
        
        var = tk.StringVar(dialog)
        var.set(options[0]) 
        
        option_menu = ttk.OptionMenu(dialog, var, options[0], *options)
        option_menu.pack(padx=20, pady=20)
        
        style = ttk.Style()
        style.configure('TMenubutton', background='dark slate blue', foreground='white', font=('Times New Roman', 15))
        option_menu.configure(style='TMenubutton')
        
        button_ok = tk.Button(dialog, text="OK", font=("Futura", 15), width=10, bg="dark slate blue", fg="white", command=lambda: dialog_ok(dialog, var))
        button_ok.pack(pady=10)

    def dialog_ok(dialog, var):
        global selected_row_id
        
        action = var.get()
        
        with  conn.cursor() as cursor:
            
            if action == "Diagnosed":
                new_status = "Diagnosed"
            elif action == "Cancel":
                new_status = "Cancel"
            else:
                new_status = None
            
            if new_status and selected_row_id:
                if new_status == "Diagnosed":
                    cursor.execute("UPDATE appointments SET status = %s WHERE a_id = %s", (new_status, selected_row_id))
                                        
                    cursor.execute("SELECT * FROM appointments WHERE a_id = %s AND status = 'Diagnosed'", (selected_row_id,))
                    row_data = cursor.fetchone()
                    
                    if row_data:

                        cursor.execute("INSERT INTO app_history (a_id, p_name, app_date, app_time, symptoms, concerns, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", row_data)

                        cursor.execute("DELETE FROM appointments WHERE a_id = %s AND status = 'Diagnosed'", (selected_row_id,))
                        
                        show_frame(medication_frame)
                        display_pat_name_app() 
                        display_pat_symptoms_app()
                        display_pat_concerns_app()

                    dialog.destroy()
                    refresh_data()
                
                if new_status == "Cancel":
                    cursor.execute("UPDATE appointments SET status = %s WHERE a_id = %s", (new_status, selected_row_id))
                    
                    cursor.execute("SELECT * FROM appointments WHERE a_id = %s AND status = 'Cancel'", (selected_row_id,))
                    row_data = cursor.fetchone()
                    
                    if row_data:
                        cursor.execute("INSERT INTO app_history (a_id, p_name, app_date, app_time, symptoms, concerns, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", row_data)
                        
                        cursor.execute("DELETE FROM appointments WHERE a_id = %s AND status = 'Cancel'", (selected_row_id,))
                
                    conn.commit()
                    
                    dialog.destroy()
                    refresh_data()
                    messagebox.showerror("Appointment Cancelled","You Cancelled The Appointment!!")

            else:
                messagebox.showerror("Invalid action selected")

    def refresh_data():
        update_display(tree3)

    def display_appointment():
        query1 = "select distinct  a.a_id, p.p_name,a.app_date, a.app_time, a.symptoms, a.concerns , a.status from appointments AS a inner join patient AS p on p.p_name = a.p_name order by a.app_date, a.app_time"

        with conn.cursor() as cursor:

            cursor.execute(query1)
            conn.commit()
            data3 = cursor.fetchall()
            return data3
            
    appointment_frame = tk.Frame(container, bg="navy")
    
    image_label2 = tk.Label(appointment_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    doc_name_label = tk.Label(appointment_frame, text=f"Appointments for You ", bg="white" , fg="navy", font=("Futura" , 30))
    doc_name_label.pack(pady=10, padx=20,ipadx=20)
    
    appointment_nav_frame = tk.Frame(appointment_frame , bg="navy")
    appointment_nav_frame.pack(side="top",fill="x", ipady=5)

    button2 = tk.Button(appointment_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(doctor_frame))
    button2.pack(side="left",padx=5)

    button1 = tk.Button(appointment_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=log_out_doctor)
    button1.pack(side="left",padx=5)

    button3 = tk.Button(appointment_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button_refresh = tk.Button(appointment_nav_frame, text="Refresh", font=("Futura", 20), width=10, bg="dark slate blue", fg="white", command=refresh_data)
    button_refresh.pack(side="right", padx=10)

    app_name_label = tk.Label(appointment_frame, text=f"Active Appointments", bg="white" , fg="navy", font=("Futura" , 20))
    app_name_label.pack(pady=10)

    style3 = ttk.Style(appointment_frame)
    style3.theme_use('alt')

    style3.configure("Treeview", background="#d3d3d3", foreground="black", rowheight=25, font=('Futura', 12))
    style3.configure("Treeview.Heading", background="navy", foreground="white", font=('Futura', 12, 'bold'))

    def populate_treeview(tree3, data3):
        tree3.delete(*tree3.get_children())
        for row in data3:
            tree3.insert("", "end", values=row)

    def update_display(tree3):
        data3 = display_appointment()
        populate_treeview(tree3, data3)

    tree3 = ttk.Treeview(appointment_frame, columns=('a_id','p_name','a_date','start_time', 'Symptoms','Concerns','status'), show="headings", style="Treeview")

    data3 = display_appointment()
    tree3.heading("a_id", text="Appointment ID")
    tree3.heading("p_name", text="Patient Name")
    tree3.heading("a_date", text="Appointment Date")
    tree3.heading("start_time", text="Appointment Time")
    tree3.heading("Symptoms", text="Symptoms")
    tree3.heading("Concerns", text="Concerns")
    tree3.heading("status", text="Status")

    tree3.bind("<ButtonRelease-1>", handle_click)
    update_display(tree3)

    tree3.pack(fill="both",expand=True)

    appointment_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # medication page 

    def display_pat_name_app():
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT p_name FROM app_history WHERE a_id = %s", (selected_row_id,))
            appointment_details = cursor.fetchone()
        
        if appointment_details:
            p_name = appointment_details[0]  
            pat_name_label.config(text=f"Patient Name: {p_name}")
        
    def display_pat_symptoms_app():
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT symptoms FROM app_history WHERE a_id = %s", (selected_row_id,))
            appointment_details = cursor.fetchone()
        
        if appointment_details:
            p_symptoms = appointment_details[0]  
            pat_symptoms_label.config(text=f"Patient Symptoms: {p_symptoms}")
    
    def display_pat_concerns_app():
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT concerns FROM app_history WHERE a_id = %s", (selected_row_id,))
            appointment_details = cursor.fetchone()
        
        if appointment_details:
            p_concerns = appointment_details[0]  
            pat_concerns_label.config(text=f"Patient Concerns: {p_concerns}")
    
    def medicate():
        precautions = precautions_entry.get()
        medication = medication_entry.get()

        if not precautions or not medication:
            messagebox.showerror("Input Error", "Please enter precautions and medication.")
            return 

        try:
            with conn.cursor() as cursor:
                query = "INSERT INTO medication (a_id, precautions, medications) VALUES (%s, %s, %s)"
                cursor.execute(query, (selected_row_id, precautions, medication))

                cursor.execute("INSERT INTO pat_med_history (m_id , a_id, p_name, app_date, app_time, symptoms, medications) SELECT m.m_id,a.a_id, a.p_name, a.app_date, a.app_time, a.symptoms, m.medications FROM app_history AS a JOIN medication AS m ON a.a_id = m.a_id WHERE a.a_id = %s", (selected_row_id,))
                        
                conn.commit()
                
                messagebox.showinfo("Success", "Medication and precautions added successfully.")
                
                clear_prec_med()
                
                show_frame(appointment_frame)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Database Error", f"You already diagnosed {display_pat_name_app.p_name}!!")
    
    def clear_prec_med():
        precautions_entry.delete(0,tk.END)
        medication_entry.delete(0,tk.END)
        pat_name_label.config(text="Patient Name: ")
        pat_symptoms_label.config(text="Patient Symptoms: ")
        pat_concerns_label.config(text="Patient Concerns: ")

    medication_frame = tk.Frame(container, bg="navy")
    
    image_label2 = tk.Label(medication_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    med_name_label = tk.Label(medication_frame, text=f"Diagnose Patient", bg="white" , fg="navy", font=("Futura" , 30))
    med_name_label.pack(pady=10, padx=20,ipadx=10)

    medication_nav_frame = tk.Frame(medication_frame , bg="navy")
    medication_nav_frame.pack(side="top",fill="x", ipady=5,pady=10)

    button2 = tk.Button(medication_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(doctor_frame))
    button2.pack(side="left",padx=5)

    button1 = tk.Button(medication_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=log_out_doctor)
    button1.pack(side="left",padx=5)

    button3 = tk.Button(medication_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(medication_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=clear_prec_med)
    button4.pack(side="right",padx=10)

    pat_data_frame =  tk.Frame(medication_frame , bg="navy")
    pat_data_frame.pack(side="top",fill="x", ipady=5)

    pat_name_label = tk.Label(pat_data_frame, text="",bg='navy', fg='white', font=("Futura" , 20))
    pat_name_label.pack(side="left",ipadx=10)

    pat_data_frame1 =  tk.Frame(medication_frame , bg="navy")
    pat_data_frame1.pack(side="top",fill="x", ipady=5)

    pat_symptoms_label = tk.Label(pat_data_frame1, text=f"Patient Symptoms: ",bg='navy', fg='white', font=("Futura" , 20))
    pat_symptoms_label.pack(side="left",ipadx=10)

    pat_data_frame2 =  tk.Frame(medication_frame ,bg="navy")
    pat_data_frame2.pack(side="top",fill="x", ipady=5)

    pat_concerns_label = tk.Label(pat_data_frame2, text=f"Patient Concerns: ",bg='navy', fg='white', font=("Futura" , 20))
    pat_concerns_label.pack(side="left",ipadx=10)

    pat_data_frame3 =  tk.Frame(medication_frame , bg="white")
    pat_data_frame3.pack(side="top", ipady=5, pady=10)

    precautions_label = tk.Label(pat_data_frame3, text=f"Enter the Precautions: ", bg="white" , fg="navy", font=("Futura" , 20))
    precautions_label.pack(pady=10,side="left")
    precautions_entry = tk.Entry(pat_data_frame3, bg='white',font=('Times New Roman', 20), border=1)
    precautions_entry.pack(side="left", padx=10 , pady=5)

    pat_data_frame4 =  tk.Frame(medication_frame , bg="white")
    pat_data_frame4.pack(side="top", ipady=5, pady=10)

    medications_label = tk.Label(pat_data_frame4, text=f" Enter the Medication:  ", bg="white" , fg="navy", font=("Futura" , 20))
    medications_label.pack(pady=10,side="left")
    medication_entry = tk.Entry(pat_data_frame4, bg='white',font=('Times New Roman', 20), border=1)
    medication_entry.pack(side="left", padx=10 , pady=5)

    button4 = tk.Button(medication_frame, text="Submit Diagnosis", font=("Futura" , 20), bg="dark slate blue" , fg="white",command=medicate)
    button4.pack(side="top",padx=10,pady=50)

    medication_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # patient history page 

    def display_patient_details():
        patient_name = hit_pat_name_entry.get()

        if not patient_name:
            messagebox.showinfo("Error", "Please enter a patient name")
            return

        with conn.cursor() as cursor:
            cursor.execute("SELECT pmh_id ,p_name , app_date , app_time ,symptoms,medications FROM pat_med_history  WHERE p_name = %s", (patient_name))
            hist_data = cursor.fetchone() 

        clear_displayed_details()

        if hist_data:
            label_id.config(text=f"ID: {hist_data[0]}")
            label_name.config(text=f"Patient Name: {hist_data[1]}")
            label_sched_date.config(text=f"Scheduling Date: {hist_data[2]}")
            label_appointment_time.config(text=f"Appointment Time: {hist_data[3]}")
            label_symptoms.config(text=f"Symptoms: {hist_data[4]}")
            label_medications.config(text=f"Medications: {hist_data[5]}")
        else:
            messagebox.showinfo("Not Found", f"No records found for patient: {patient_name}")

    def clear_displayed_details():
        hit_pat_name_entry.delete(0, tk.END)
        label_id.config(text="ID: ")
        label_name.config(text="Patient Name: ")
        label_sched_date.config(text="Scheduling Date: ")
        label_appointment_time.config(text="Appointment Time: ")
        label_symptoms.config(text="Symptoms: ")
        label_medications.config(text="Medications: ")

    patient_history_frame = tk.Frame(container, bg="navy")
    
    image_label2 = tk.Label(patient_history_frame, image=logo_photo2, border=0)
    image_label2.pack(pady=20)

    hist_name_label = tk.Label(patient_history_frame, text=f"Patient History", bg="white" , fg="navy", font=("Futura" , 30))
    hist_name_label.pack(pady=10, padx=20,ipadx=20)
    
    pat_history_nav_frame = tk.Frame(patient_history_frame , bg="navy")
    pat_history_nav_frame.pack(side="top",fill="x", ipady=5)

    button2 = tk.Button(pat_history_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(doctor_frame))
    button2.pack(side="left",padx=5)

    def logout_history():
        clear_doc_login()
        clear_pat_login()
        clear_displayed_details()
        show_frame(start_frame)

    button1 = tk.Button(pat_history_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=logout_history)
    button1.pack(side="left",padx=5)

    button3 = tk.Button(pat_history_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(pat_history_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=clear_displayed_details)
    button4.pack(side="right",padx=10)

    hit_pat_name_frame = tk.Frame(patient_history_frame, bg="navy")
    hit_pat_name_frame.pack(pady=10,side="top",ipadx=10,ipady=10)

    hit_pat_name_label= tk.Label(hit_pat_name_frame, text="    Enter  Patient Name:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    hit_pat_name_label.pack(pady=5, side="left", padx=10)

    hit_pat_name_entry = tk.Entry(hit_pat_name_frame, bg='white',font=('Times New Roman', 20), border=1)
    hit_pat_name_entry.pack(side="left", padx=10 , pady=5)

    button5 = tk.Button(hit_pat_name_frame, text="Fetch", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white" ,command= display_patient_details)
    button5.pack(side="right",padx=10)

    hist_name_label = tk.Label(patient_history_frame, text=f"Patient History", bg="white" , fg="navy", font=("Futura" , 20))
    hist_name_label.pack(pady=10)

    label_id = tk.Label(patient_history_frame, text="ID: ", font=("Times New Roman", 20), bg="white", fg="navy")
    label_id.pack(pady=5, padx=130, anchor="w")

    label_name = tk.Label(patient_history_frame, text="Patient Name: ", font=("Times New Roman", 20), bg="white", fg="navy")
    label_name.pack(pady=5, padx=130, anchor="w")

    label_sched_date = tk.Label(patient_history_frame, text="Scheduling Date: ", font=("Times New Roman", 20), bg="white", fg="navy")
    label_sched_date.pack(pady=5, padx=130, anchor="w")

    label_appointment_time = tk.Label(patient_history_frame, text="Appointment Time: ", font=("Times New Roman", 20), bg="white", fg="navy")
    label_appointment_time.pack(pady=5, padx=130, anchor="w")

    label_symptoms = tk.Label(patient_history_frame, text="Symptoms: ", font=("Times New Roman", 20), bg="white", fg="navy")
    label_symptoms.pack(pady=5, padx=130, anchor="w")

    label_medications = tk.Label(patient_history_frame, text="Medications: ", font=("Times New Roman", 20), bg="white", fg="navy")
    label_medications.pack(pady=5, padx=130, anchor="w")

    patient_history_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # admin login page 

    def  admin_login():
        admin_username= entry_usernameadm.get()
        admin_password= entry_passwordadm.get()
        if admin_username == admin_username and admin_password == admin_password:
            messagebox.showinfo("Admin Login Success",f"Welcome {admin_username}")
            entry_usernameadm.delete(0, tk.END)
            entry_passwordadm.delete(0, tk.END)
            show_frame(admin_frame)
        else :
            messagebox.showinfo("Admin Login Unsuccessful","Fill The Fields Correctly")    
    
    def clear_admin():
        entry_usernameadm.delete(0,tk.END)
        entry_passwordadm.delete(0,tk.END)

    admin_login_frame = tk.Frame(container, bg="white")

    image_label3 = tk.Label(admin_login_frame, image=logo_photo2, border=0)
    image_label3.pack(pady=20)

    admin_login_nav_frame = tk.Frame(admin_login_frame , bg="navy")
    admin_login_nav_frame.pack(side="top",fill="x", ipady=5)

    button1 = tk.Button(admin_login_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(start_frame))
    button1.pack(side="left",padx=5)

    button3 = tk.Button(admin_login_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    button4 = tk.Button(admin_login_nav_frame, text="Clear", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=clear_admin)
    button4.pack(side="right",padx=5)

    label2 = tk.Label(admin_login_frame, text="Admin Login", bg="white" , fg="navy", font=("Futura" , 30))
    label2.pack(pady=10, padx=20,ipadx=20)

    image_label4 = tk.Label(admin_login_frame, image=logo_photo3, border=0 , bg="white")
    image_label4.pack(pady=20)

    username_adm_frame = tk.Frame(admin_login_frame, bg="navy")
    username_adm_frame.pack(side="top",ipadx=10,ipady=10)

    label_usernameadm = tk.Label(username_adm_frame, text="    Enter  Username:    ",bg='navy', fg='white',font=('Times New Roman', 20))
    label_usernameadm.pack(pady=5, side="left", padx=10)
    entry_usernameadm = tk.Entry(username_adm_frame, bg='white',font=('Times New Roman', 20), border=1)
    entry_usernameadm.pack(side="left", padx=10 , pady=5)

    pass_admin_frame = tk.Frame(admin_login_frame , bg="navy")
    pass_admin_frame.pack(side="top",ipadx=10,ipady=10)

    label_passwordadm = tk.Label(pass_admin_frame, text="    Enter  Password:     " ,bg='navy', fg='white',font=('Times New Roman', 20))
    label_passwordadm.pack(side="left", padx=10 , pady=10)
    entry_passwordadm = tk.Entry(pass_admin_frame, bg='white',border=1,font=('Times New Roman', 20) ,show="*") 
    entry_passwordadm.pack(side="left", padx=10 , pady=10)

    tk.Button(admin_login_frame, text='Login', font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=admin_login).pack(side="top", padx=0, pady=45)

    admin_login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # admin page 

    admin_frame = tk.Frame(container, bg="navy")

    image_label3 = tk.Label(admin_frame, image=logo_photo2, border=0)
    image_label3.pack(pady=20)
    
    label2 = tk.Label(admin_frame, text="Welcome Admin", bg="white" , fg="navy", font=("Futura" , 30))
    label2.pack(pady=10, padx=20,ipadx=20)

    admin_nav_frame = tk.Frame(admin_frame , bg="navy")
    admin_nav_frame.pack(side="top",fill="x", ipady=5)

    button1 = tk.Button(admin_nav_frame, text="Home", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white",command=lambda: show_frame(admin_frame))
    button1.pack(side="left",padx=5)

    def log_out_admin():
        show_frame(start_frame)
        clear_admin

    button4 = tk.Button(admin_nav_frame, text="Log Out", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=log_out_admin)
    button4.pack(side="left",padx=5)

    button3 = tk.Button(admin_nav_frame, text="Exit", font=("Futura" , 20),width= 10, bg="dark slate blue" , fg="white", command=exit)
    button3.pack(side="right",padx=10)

    def open_mysql_workbench():
        if platform.system() == "Windows":
            workbench_path = r"C:\Program Files\MySQL\MySQL Workbench 8.0\MySQLWorkbench.exe"
            if os.path.exists(workbench_path):
                subprocess.Popen([workbench_path])
            else:
                print("MySQL Workbench executable not found.")
        elif platform.system() == "Darwin": 
            subprocess.Popen(["open", "-a", "MySQLWorkbench"])
        elif platform.system() == "Linux":
            subprocess.Popen(["mysql-workbench"])
        else:
            print("Unsupported OS")
        root.withdraw()

    button5 = tk.Button(admin_nav_frame, text="Manage Database by server", font=("Futura" , 20), bg="dark slate blue" , fg="white", command=open_mysql_workbench)
    button5.pack(side="left",padx=10)

    admin_nav_frame1 = tk.Frame(admin_frame , bg="navy")
    admin_nav_frame1.pack(side="top",fill="x", ipady=5)

    def fetch_data(table_name):
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            return rows

    def populate_treeview(tree, columns, rows):
        tree["columns"] = columns
        tree["show"] = "headings"  
        for col in columns:
            tree.heading(col, text=col, anchor='center')
            tree.column(col, anchor='center')
        for row in rows:
            tree.insert('', 'end', values=row)

    def on_double_click(event, tree, table_name):
        item = tree.identify('item', event.x, event.y)
        column = tree.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1

        if col_index == 0:
            return

        x, y, width, height = tree.bbox(item, column)
        current_value = tree.item(item, 'values')[col_index]

        entry = tk.Entry(tree)
        entry.insert(0, current_value)
        entry.place(x=x, y=y + height // 2, anchor='w', width=width)

        def save_edit_inner(event):
            new_value = entry.get()
            tree.set(item, column, new_value)

            row_id = tree.item(item, 'values')[0]

            if table_name == 'app_history':
                pk_column = 'app_his_id'  
            elif table_name == 'patient':
                pk_column = 'p_id'
            elif table_name == 'medication':
                pk_column = 'm_id' 
            elif table_name == 'appointments':
                pk_column = 'a_id' 
            elif table_name == 'doctor':
                pk_column = 'd_id' 
            elif table_name == 'pat_med_history':
                pk_column = 'pmh_id' 
            else:
                return

            col_name = tree.heading(column, 'text')

            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name} SET {col_name} = %s WHERE {pk_column} = %s", (new_value, row_id))
                    conn.commit()
            except Exception as e:
                print(f"Error updating database: {e}")

            entry.destroy()

        entry.bind('<Return>', save_edit_inner)
        entry.focus()

    def refresh_treeview(tree, table_name):
        tree.delete(*tree.get_children())
        columns = []
        rows = []
        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
        populate_treeview(tree, columns, rows)

    style = ttk.Style()
    style.configure("Custom.TButton",
                    font=("futura", 20),
                    padding=[8,8],
                    background="dark slate blue",
                    foreground="white",
                    borderwidth=1)
    style.map("Custom.TButton",
            background=[("active", "#45a049")])

    style.configure("TNotebook.Tab", 
                    font=("futura", 20),
                    padding=[10,5],
                    background="dark slate blue",
                    foreground="white")
    style.map("TNotebook.Tab", 
            background=[("selected", "#45a049")],
            foreground=[("selected", "white")])

    notebook = ttk.Notebook(admin_frame)
    notebook.pack(fill='both', expand=True)

    tables = {
        'app_history': ttk.Treeview(notebook),
        'patient': ttk.Treeview(notebook),
        'medication': ttk.Treeview(notebook),
        'appointments': ttk.Treeview(notebook),
        'doctor': ttk.Treeview(notebook),
        'pat_med_history': ttk.Treeview(notebook),
    }

    for table_name, tree in tables.items():
        columns = []
        rows = []
        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
        populate_treeview(tree, columns, rows)
        tree.bind('<Double-1>', lambda event, tree=tree, table_name=table_name: on_double_click(event, tree, table_name))
        notebook.add(tree, text=table_name.capitalize()) 


    refresh_button = ttk.Button(admin_nav_frame, text="Refresh", style="Custom.TButton",
                            command=lambda: refresh_treeview(tables[notebook.tab(notebook.select(), "text").lower()], notebook.tab(notebook.select(), "text").lower()))
    refresh_button.pack(pady=10 , padx=10 , side="right")


    admin_frame.place(relx=0, rely=0, relwidth=1, relheight=1)    

    def exit():
        root.destroy()

    current_frame = start_frame
    current_frame.tkraise()
    root.update()
    root.mainloop()

except pymysql.MySQLError as e:
    print(f"MySQL error: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed")
    else:
        print("No connection to close")