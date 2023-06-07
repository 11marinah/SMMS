import os
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import passwordandemail
import smtplib
import time
class log:
    #рамка страницы входа
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500+200+100")
        self.root.title("Cтраница входа в систему ioitms")
        self.root.config(bg="white")
        self.root.focus_force()

        self.thecode=''

        self.smlogo=PhotoImage(file="IMAGES/logo1.png")
        self.smlogolbl=Label(self.root,image=self.smlogo).place(x=20,y=50,width=625,height=350)

        self.idemployee=StringVar()
        self.passwordemployee=StringVar()


        logiframe = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        logiframe.place(x=530, y=100, width=300, height=250)
        logititlelbl = Label(logiframe, text="Войдите в ioitms ", font=("times new roman", 20,"bold"), bg="white",fg="black").place(x=0,y=10,relwidth=1)

        usernamelbl = Label(logiframe, text="логин ", font=("times new roman", 15), bg="white",fg="gray").place(x=60,y=50)
        usernametxt=Entry(logiframe,textvariable=self.idemployee,font=("times new roman",12), bg="#E5E4E2").place(x=60,y=75,width=150,height=20)

        passwdlbl = Label(logiframe, text="Пароль ", font=("times new roman", 15), bg="white",fg="gray").place(x=60,y=100)
        passwdtxt=Entry(logiframe,textvariable=self.passwordemployee,font=("times new roman",12),show="*", bg="#E5E4E2").place(x=60,y=125,width=150,height=20)

        loginbtn = Button(logiframe, text="Вход", font=("times new roman", 15),command=self.login, bg="#FF9C34",fg="white", cursor="hand2").place(x=50, y=170, width=180, height=25)
        forgotbtn = Button(logiframe, text="Забыли пароль?", font=("times new roman", 10,"bold"),command=self.forgetpassword, bg="white",fg="#FF9C34",bd=0,activebackground="white", cursor="hand2").place(x=50, y=210, width=180, height=25)


        #функция для входа
    def login(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.idemployee.get()=="" or self.passwordemployee.get()=="":
                messagebox.showerror("Error", "All fields are required",parent=self.root)
            else:
                conn = cur.execute("Select usertype from Employee where eid=? and password=?",(self.idemployee.get(),self.passwordemployee.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid username",parent=self.root)
                else:
                    if user[0]=="Администратор":
                        self.root.destroy()
                        os.system("python Homepage.py")
                    else:
                        self.root.destroy()
                        os.system("python Billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            #функция забыл пароль
    def forgetpassword(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.idemployee.get()=="" :
                messagebox.showerror("Error", "Username is required",parent=self.root)
            else:
                conn = cur.execute("Select email from Employee where eid=? ",(self.idemployee.get(),))
                theemail=cur.fetchone()
                if theemail==None:
                    messagebox.showerror("Error","Invalid username \ntry again",parent=self.root)
                else:
                    #Reset password
                    self.resetcode=StringVar()
                    self.resetnewpassword=StringVar()
                    self.resetconfirmpassword=StringVar()
                    #call the semailfunction
                    chk = self.semailcode(theemail[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                        self.passwordresetwindow=Toplevel(self.root)
                        self.passwordresetwindow.title('Reset password')
                        self.passwordresetwindow.geometry('400x350+500+100')
                        self.passwordresetwindow.focus_force()

                        resetpasswordlbl = Label(self.passwordresetwindow, text="Reset password ", font=("times new roman", 15, "bold"),bg="#FF9C34", fg="white").pack(side=TOP,fill=X)

                        emailcodelbl = Label(self.passwordresetwindow, text="Enter the code sent to your password ", font=("times new roman", 13)).place(x=10,y=40)
                        emailcodetxt = Entry(self.passwordresetwindow, textvariable=self.resetcode, font=("times new roman", 13),bg='lightyellow').place(x=10,y=70,width=260,height=30)

                        newpasswordlbl = Label(self.passwordresetwindow, text="New password ",font=("times new roman", 13)).place(x=10, y=110)
                        newpasswordtxt = Entry(self.passwordresetwindow, textvariable=self.resetnewpassword,font=("times new roman", 13), bg='lightyellow').place(x=10, y=140, width=260,height=30)

                        confirmpasswordlbl = Label(self.passwordresetwindow, text="Confirm password ",font=("times new roman", 13)).place(x=10, y=180)
                        confirmpasswordtxt = Entry(self.passwordresetwindow, textvariable=self.resetconfirmpassword,font=("times new roman", 13), bg='lightyellow').place(x=10, y=210, width=260,height=30)

                        self.emailcodebtn = Button(self.passwordresetwindow, text="Submit",font=("times new roman", 13),command=self.codevalidation, bg="lightgray", fg="#FF9C34", cursor="hand2")
                        self.emailcodebtn.place(x=280, y=70, width=100, height=30)

                        self.resetnewpasswordbtn = Button(self.passwordresetwindow, text="Reset password",state=DISABLED,font=("times new roman", 13),command=self.resetpssword, bg="#FF9C34", fg="white",cursor="hand2")
                        self.resetnewpasswordbtn.place(x=50, y=270, width=260, height=30)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        #функция для сброса пароля
    def resetpssword(self):
        if self.resetnewpassword.get()=="" or self.resetconfirmpassword.get()=="":
            messagebox.showerror("Error","The password is required",parent=self.passwordresetwindow)
        elif self.resetnewpassword.get()!=self.resetconfirmpassword.get():
            messagebox.showerror("Error","The passwords doesn't match",parent=self.passwordresetwindow)
        else:
            conn = sqlite3.connect(database=r'ioitms.db')
            cur = conn.cursor()
            try:
                cur.execute("Update Employee SET password=? where eid=?",(self.resetnewpassword.get(),self.idemployee.get()))
                conn.commit()
                messagebox.showinfo("Success","Password successfully updated")
                self.passwordresetwindow.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            #функция для проверки правильности кода, отправленного по электронной почте
    def codevalidation(self):
        if int(self.thecode)==int(self.resetcode.get()):
            self.resetnewpasswordbtn.config(state=NORMAL)
            self.emailcodebtn.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid code try again",parent=self.forgetpassword)

            #функция отправки кода на почту
    def semailcode(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        myemail=passwordandemail.myemail
        mypassword=passwordandemail.mypassword
        s.login(myemail,mypassword)
        self.thecode=int(time.strftime("%H%M%S"))+int(time.strftime("%S"))
        print(self.thecode)

        subject='Reset password code'
        messag=f'Dear Sir/Madam,\n\n YOUR RESET CODE IS {str(self.thecode)}.\n\nWith Regards,\nioitms Team'
        messag="Subject:{}\n\n{}".format(subject,messag)
        s.sendmail(myemail,to_,messag)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'

if __name__ == "__main__":
    root = Tk()
    obj = log(root)
    root.mainloop()