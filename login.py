from tkinter import*
from tkinter import messagebox
import pymysql
import pymysql.cursors
import subprocess
import cv2,os
import glob
import numpy as np
win=Tk()
win.config(bg="gray")
win.geometry("500x400")
win.title("Welcome to Login")
win.resizable(False,False)
#function for login
def login():
    try:
        cam = cv2.VideoCapture(0) 
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if not cam.isOpened():
            messagebox.showerror("Error", "Camera not detected!")
            return

        # Get latest image file
        training_path = 'C:\\Users\\Deepanshu\\Documents\\python\\project\\TrainingImage\\'
        list_of_files = glob.glob(training_path + '*') 

        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            name = os.path.splitext(os.path.basename(latest_file))[0]
            name = int(name) + 1
        else:
            name = 1  # First image name

        face_detected = False
        while not face_detected:
            ret, img = cam.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image!")
                return

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_detected = True
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_img_path = os.path.join(training_path, f"{name}.jpg")
                cv2.imwrite(face_img_path, img[y:y+h, x:x+w])

            cv2.imshow('Face Capture', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # User Input (Make sure text & text2 are defined in your UI)
        user = text.get()
        password = text2.get()

        # Database Connection
        try:
            conn = pymysql.connect(host='localhost', user='root', password='*******', db='deepanshu')
            a = conn.cursor()
            a.execute("SELECT * FROM login WHERE Username=%s AND Password=%s", (user, password))
            result = a.fetchall()
            count = a.rowcount

            if count > 0:
                messagebox.showinfo("Success", "Login Successful!")
                win.destroy()
                subprocess.run(["python", "login2.py"])
            else:
                messagebox.showerror("Error", "Invalid Credentials! Try again.")

            conn.close()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
    
def forgot():
        winn=Tk()
        winn.config(bg="orange")
        winn.geometry("350x270")
        winn.title("Welcome to Forgot Password")
        def reset():
                #intialise the variable
                name=var.get()
                new=var2.get()
                old=var3.get()
                #check both password are same
                if(new==old):
                        #connect to the datadase
                        conn = pymysql.connect(host='localhost',user='root',password='*********',db='deepanshu')
                        mydb=conn.cursor()
                        mydb.execute("select * from login where Username = '"+name+"'")
                        mydb.execute("update fun set Password='"+new+"' where Username = '"+name+"'")
                        conn.commit()
                        result=mydb.fetchall()
                        count=mydb.rowcount
                        if count>0:
                                messagebox.showinfo("Message","Successful")
                                
                        else:
                                messagebox.showerror("Message","INVALID")
                else:
                        messagebox.showerror("Message","Not match")
                        
        lb=Label(winn,text="Username",width=10,bg="orange",font=15).grid(row=1,column=0,padx=10,pady=10)
        lb2=Label(winn,text="New Password",width=15,bg="orange",font=15).grid(row=2,column=0,padx=10,pady=10)
        lb3=Label(winn,text="Re-enter Password",width=15,bg="orange",font=15).grid(row=3,column=0,padx=10,pady=10)
        var=Entry(winn)
        var.grid(row=1,column=1,padx=10,pady=10)
        var2=Entry(winn)
        var2.grid(row=2,column=1,padx=10,pady=10)
        var3=Entry(winn)
        var3.grid(row=3,column=1,padx=10,pady=10)
        btn=Button(winn,text="Change",command=reset,font=10,bd=5,relief="raised").place(x=120,y=150)
        winn.mainloop()

def sign():
        sin=Tk()
        sin.config(bg="light blue")
        sin.geometry("370x250")
        sin.title("Welcome to Sign up")
        def insert():
                #intialise the variable
                name=tx.get()
                username=tx2.get()
                password=tx3.get()
                #connect to the datadase
                try:
                        conn = pymysql.connect(host='localhost',user='root',password='*********',db='deepanshu')
                        mydb=conn.cursor()
                        mydb.execute("insert into login(Username,Password) values('"+username+"','"+password+"')")
                        conn.commit()
                        messagebox.showinfo("Message","Successful")
                      
                except:
                        conn.rollback()
                        messagebox.showerror("Message","Failed")
                conn.close()
        lb=Label(sin,text="Name",width=10,bg="light blue",font=15).grid(row=1,column=0,padx=10,pady=10)    
        lb=Label(sin,text="Username",width=10,bg="light blue",font=15).grid(row=2,column=0,padx=10,pady=10)
        lb2=Label(sin,text="Password",width=15,bg="light blue",font=15).grid(row=3,column=0,padx=10,pady=10)
        tx=Entry(sin)
        tx.grid(row=1,column=1,padx=10,pady=10)
        tx2=Entry(sin)
        tx2.grid(row=2,column=1,padx=10,pady=10)
        tx3=Entry(sin)
        tx3.grid(row=3,column=1,padx=10,pady=10)
        btn=Button(sin,text="Submit",command=insert,font=5,bd=5,relief="raised").place(x=120,y=150)
        

        

#label 
lb=Label(win,text="ARTIFICIAL CAMERA",font=40,bd=10,relief="raised",width=50 ).grid(row=0)
#Frame 
frame2=Frame(win,bd=10,relief="raised",width=400,height=280,bg="orange").place(x=50,y=100)
frame3=Frame(win,bd=9,relief="raised",width=400,height=40).place(x=50,y=100)
lb1=Label(frame3,text="Login ",font=20).place(x=220,y=102)
lb2=Label(frame2,text="Username",font=20,width=10,bg="orange").place(x=100,y=150)
lb3=Label(frame2,text="Password",font=20,width=10,bg="orange").place(x=100,y=190)
#Entry Box
text=Entry(frame2)
text.place(x=270,y=150)
text2=Entry(frame2,show="*")
text2.place(x=270,y=190)
#Button
login=Button(frame2,text="Login",font=10,bd=5,relief="groove",command=login).place(x=100,y=250)
forget=Button(frame2,text="Forgot",font=10,bd=5,relief="groove",command=forgot).place(x=320,y=250)
sign=Button(frame2,text="Sign up",font=10,bd=5,relief="groove",command=sign).place(x=205,y=310)

win.mainloop()


