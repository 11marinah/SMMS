from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class emp:
    #рамка страницы сотрудника
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="white")
        self.root.focus_force()

        # переменные
        self.empsearchby=StringVar()
        self.empsearchtext=StringVar()

        self.empid=StringVar()
        self.empgender=StringVar()
        self.empcontact=StringVar()
        self.empname=StringVar()
        self.empdob=StringVar()
        self.empdoj=StringVar()
        self.empemail=StringVar()
        self.emppassword=StringVar()
        self.empusertype=StringVar()
        self.empsalary = StringVar()

        #рамка поиска
        frsearch=LabelFrame(self.root,text="Поиск сотрудника",font=("Times new roman",15,"bold"),bd=2,relief=RIDGE,bg="white")
        frsearch.place(x=250,y=30,width=600,height=70)
        searchcb=ttk.Combobox(frsearch,textvariable=self.empsearchby,values=("Выбрать", "Email", "Name", "Contact"),state='readonly',justify=CENTER,font=("times new roman",15))
        searchcb.place(x=10,y=10,width=180)
        searchcb.current(0)
        searchtext=Entry(frsearch,textvariable=self.empsearchtext,font=("times new roman",15),bg="lightyellow").place(x=200,y=10)
        searchbtn=Button(frsearch,text="Поиск",command=self.search,font=("times new roman",15),bg="#7D6608",fg="white",cursor="hand2").place(x=410,y=10,width=150,height=30)

        #данные сотрудника
        empdetailslbl=Label(self.root,text="Сведения о сотруднике",font=("times new roman",15),bg="#BA4A00",fg="white").place(x=50,y=100,width=1000)
        empidlbl=Label(self.root,text="СID",font=("times new roman",15),bg="white").place(x=50,y=150)
        empgenderlbl=Label(self.root,text="Пол",font=("times new roman",15),bg="white").place(x=380,y=150)
        empcontactlbl=Label(self.root,text="Номер телефона",font=("times new roman",15),bg="white").place(x=700,y=150)
        empidtxt=Entry(self.root,textvariable=self.empid,font=("times new roman",15),bg="lightyellow").place(x=220,y=150,width=150)
        empgendercb = ttk.Combobox(self.root, textvariable=self.empgender, values=("Выбрать", "Женский", "Мужской"),state='readonly', justify=CENTER, font=("times new roman", 15))
        empgendercb.place(x=515,y=150,width=180)
        empgendercb.current(0)
        empcontacttxt=Entry(self.root,textvariable=self.empcontact,font=("times new roman",15),bg="lightyellow").place(x=870,y=150,width=180)
        empnamelbl=Label(self.root,text="Имя",font=("times new roman",15),bg="white").place(x=50,y=190)
        empdoblbl=Label(self.root,text="День рождения",font=("times new roman",15),bg="white").place(x=380,y=190)
        empdojlbl=Label(self.root,text="дата вступления",font=("times new roman",15),bg="white").place(x=700,y=190)
        empnametxt=Entry(self.root,textvariable=self.empname,font=("times new roman",15),bg="lightyellow").place(x=220,y=190,width=150)
        empdobtxt=Entry(self.root,textvariable=self.empdob,font=("times new roman",15),bg="lightyellow").place(x=515,y=190,width=180)
        empdojtxt=Entry(self.root,textvariable=self.empdoj,font=("times new roman",15),bg="lightyellow").place(x=870,y=190,width=180)
        empemaillbl=Label(self.root,text="Электронная почта",font=("times new roman",15),bg="white").place(x=50,y=230)
        emppasswordlbl=Label(self.root,text="Пароль",font=("times new roman",15),bg="white").place(x=380,y=230)
        empusertypelbl=Label(self.root,text="Тип пользователя",font=("times new roman",15),bg="white").place(x=700,y=230)
        empemailtxt=Entry(self.root,textvariable=self.empemail,font=("times new roman",15),bg="lightyellow").place(x=220,y=230,width=150)
        emppasswordtxt=Entry(self.root,textvariable=self.emppassword,font=("times new roman",15),bg="lightyellow").place(x=515,y=230,width=180)
        empusertypegendercb = ttk.Combobox(self.root, textvariable=self.empusertype, values=("Администратор", "Сотрудник"),state='readonly', justify=CENTER, font=("times new roman", 15))
        empusertypegendercb.place(x=870,y=230,width=180)
        empusertypegendercb.current(0)
        empaddresslbl = Label(self.root, text="Адрес", font=("times new roman", 15), bg="white").place(x=50, y=270)
        empsalarylbl = Label(self.root, text="Зарплата", font=("times new roman", 15), bg="white").place(x=380, y=270)
        self.empaddresstxt = Text(self.root,font=("times new roman", 15), bg="lightyellow")
        self.empaddresstxt.place(x=220,y=270,width=150,height=30)
        empsalarytxt = Entry(self.root, textvariable=self.empsalary, font=("times new roman", 15), bg="lightyellow").place(x=515,y=270,width=180)

        #кнопки
        savebtn=Button(self.root,text="Сохранить",command=self.save,font=("times new roman",15),bg="#2C3E50",fg="white",cursor="hand2").place(x=250,y=305,width=110,height=30)
        updatebtn=Button(self.root,text="Обновление",command=self.update,font=("times new roman",15),bg="#7D6608",fg="white",cursor="hand2").place(x=400,y=305,width=110,height=30)
        deletebtn=Button(self.root,text="Удалить",command=self.delete,font=("times new roman",15),bg="#BA4A00",fg="white",cursor="hand2").place(x=550,y=305,width=110,height=30)
        clearbtn=Button(self.root,text="Очистить",command=self.clear,font=("times new roman",15),bg="#607d8b",fg="white",cursor="hand2").place(x=700,y=305,width=110,height=30)

        #таблица данных сотрудника
        empframe = Frame(self.root, bd=3, relief=RIDGE)
        empframe.place(x=0, y=350, relwidth=1, height=150)
        yscroll = Scrollbar(empframe, orient=VERTICAL)
        xscroll = Scrollbar(empframe, orient=HORIZONTAL)
        self.employeetable = ttk.Treeview(empframe, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "password", "usertype", "address", "salary"),yscrollcommand=yscroll.set,xscrollcommand=xscroll.set)
        xscroll.pack(side=BOTTOM,fill=X)
        yscroll.pack(side=RIGHT,fill=Y)
        xscroll.config(command=self.employeetable.xview)
        yscroll.config(command=self.employeetable.yview)
        self.employeetable.heading("eid", text="СID")
        self.employeetable.heading("name", text="Имя")
        self.employeetable.heading("email", text="Электронная почта")
        self.employeetable.heading("gender", text="Пол")
        self.employeetable.heading("contact", text="Номер телефона")
        self.employeetable.heading("dob", text="День рождения")
        self.employeetable.heading("doj", text="Дата вступления")
        self.employeetable.heading("password", text="Пароль")
        self.employeetable.heading("usertype", text="Тип пользователь")
        self.employeetable.heading("address", text="Адрес")
        self.employeetable.heading("salary", text="Зарплата")
        self.employeetable["show"] = "headings"
        self.employeetable.column("eid",width=90)
        self.employeetable.column("name",width=80)
        self.employeetable.column("email", width=120)
        self.employeetable.column("gender", width=90)
        self.employeetable.column("contact", width=110)
        self.employeetable.column("dob", width=100)
        self.employeetable.column("doj", width=100)
        self.employeetable.column("password", width=90)
        self.employeetable.column("usertype", width=110)
        self.employeetable.column("address", width=100)
        self.employeetable.column("salary", width=100)
        self.employeetable.pack(fill=BOTH, expand=1)
        self.employeetable.bind("<ButtonRelease-1>",self.getdata)
        self.displai()

        #кнопка сохранения
    def save(self):
        conn=sqlite3.connect(database=r'ioitms.db')
        cur=conn.cursor()
        try:
            if self.empid.get()=="":
                messagebox.showerror("Error", "ID is required",parent=self.root)
            else:
                cur.execute("Select * from Employee where eid=?",(self.empid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This ID is already assigned,try another one",parent=self.root)
                else:
                    cur.execute("Insert into Employee (eid, name, email, gender, contact, dob, doj, password, usertype, address, salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.empid.get(),
                                        self.empname.get(),
                                        self.empemail.get(),
                                        self.empgender.get(),
                                        self.empcontact.get(),
                                        self.empdob.get(),
                                        self.empdoj.get(),
                                        self.emppassword.get(),
                                        self.empusertype.get(),
                                        self.empaddresstxt.get('1.0',END),
                                        self.empsalary.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Employee successfuly added",parent=self.root)
                    self.displai()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

            #кнопка отображения
    def displai(self):
        conn=sqlite3.connect(database=r'ioitms.db')
        cur=conn.cursor()
        try:
            cur.execute("Select * from Employee ")
            rows=cur.fetchall()
            self.employeetable.delete(*self.employeetable.get_children())
            for row in rows:
                self.employeetable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            #получить данные
    def getdata(self,ev):
        f=self.employeetable.focus()
        content=(self.employeetable.item(f))
        row=content['values']
        # print(row)
        self.empid.set(row[0])
        self.empname.set(row[1])
        self.empemail.set(row[2])
        self.empgender.set(row[3])
        self.empcontact.set(row[4])
        self.empdob.set(row[5])
        self.empdoj.set(row[6])
        self.emppassword.set(row[7])
        self.empusertype.set(row[8])
        self.empaddresstxt.delete('1.0', END)
        self.empaddresstxt.insert(END,row[9])
        self.empsalary.set(row[10])

        #кнопка обновления
    def update(self):
        conn=sqlite3.connect(database=r'ioitms.db')
        cur=conn.cursor()
        try:
            if self.empid.get()=="":
                messagebox.showerror("Error", "ID is required",parent=self.root)
            else:
                cur.execute("Select * from Employee where eid=?",(self.empid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","This ID is invalid",parent=self.root)
                else:
                    cur.execute("update Employee set name=? , email=? , gender=? , contact=? , dob=? , doj=? , password=? , usertype=?, address=? , salary=?  where eid=?",(
                                        self.empname.get(),
                                        self.empemail.get(),
                                        self.empgender.get(),
                                        self.empcontact.get(),
                                        self.empdob.get(),
                                        self.empdoj.get(),
                                        self.emppassword.get(),
                                        self.empusertype.get(),
                                        self.empaddresstxt.get('1.0',END),
                                        self.empsalary.get(),
                                        self.empid.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Employee successfuly updated",parent=self.root)
                    self.displai()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

        #кнопка удаления
    def delete(self):
        conn=sqlite3.connect(database=r'ioitms.db')
        cur=conn.cursor()
        try:
            if self.empid.get() == "":
                messagebox.showerror("Error", "ID is required", parent=self.root)
            else:
                cur.execute("Select * from Employee where eid=?", (self.empid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This ID is invalid", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Are you sure you want to delete this data?", parent=self.root)
                    if op==True:
                        cur.execute("delete from Employee where eid=?",(self.empid.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Employee successfully deleted", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            #кнопка очистки
    def clear(self):
        self.empid.set("")
        self.empname.set("")
        self.empemail.set("")
        self.empgender.set("Select")
        self.empcontact.set("")
        self.empdob.set("")
        self.empdoj.set("")
        self.emppassword.set("")
        self.empusertype.set("Admin")
        self.empaddresstxt.delete('1.0', END)
        self.empsalary.set("")
        self.empsearchtext.set("")
        self.empsearchby.set("Select")
        self.displai()

        #кнопка поиска
    def search(self):
        conn=sqlite3.connect(database=r'ioitms.db')
        cur=conn.cursor()
        try:
            if self.empsearchby.get() =="Select":
                messagebox.showerror("Error","Search by name,email or contact",parent=self.root)
            elif self.empsearchtext.get()=="":
                messagebox.showerror("Error","Search input is required",parent=self.root)
            else:
                cur.execute("Select * from Employee where "+self.empsearchby.get()+" LIKE '%"+self.empsearchtext.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.employeetable.delete(*self.employeetable.get_children())
                    for row in rows:
                        self.employeetable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Data not found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = emp(root)
    root.mainloop()