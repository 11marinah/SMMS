import os
from tkinter import *
from PIL import Image,ImageTk
from Employee import emp
from Supplier import supp
from Category import cat
from Products import prod
from Sales import sal
from About import ab
from tkinter import messagebox
import time
import sqlite3
from Billing import bil
class ioitms:
    #рамка домашней страницы
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="#F7DC6F")

        self.icon_title=PhotoImage(file="IMAGES/shopping-cart.png")
        title=Label(self.root,text="Супермаркет ioitms",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#6E2C00",fg="white",anchor="w",padx="20").place(x=0,y=0,relwidth=1,height=70)

            #Время
        logoutbtn=Button(self.root,text="Выйти",command=self.logout,font=("times new roman",15,"bold"),bg="#D4AC0D",cursor="hand2").place(x=1150,y=10,width=150,height=50)
        self.clocklbl=Label(self.root,text="Универсальный магазин в вашем районе\t\t Дата: DD-MM-YYYY\t\t Время: HH:MM:SS",font=("times new roman",15),bg="#2C3E50",fg="white")
        self.clocklbl.place(x=0,y=70,relwidth=1,height=30)

            #Меню
        self.menulogo=Image.open("IMAGES/logo1.png")
        self.menulogo=self.menulogo.resize((270,130),Image.Resampling.LANCZOS)
        self.menulogo=ImageTk.PhotoImage(self.menulogo)

        lftmenu=Frame(self.root,bd=2,relief=RIDGE,bg="#F7DC6F")
        lftmenu.place(x=0,y=102,width=270,height=565)

        menulogolbl=Label(lftmenu,image=self.menulogo)
        menulogolbl.pack(side=TOP,fill=X)

        menulbl=Label(lftmenu,text="Меню",font=("times new roman",20,"bold"),bg="#D4AC0D").pack(side=TOP,fill=X)
        employeebtn=Button(lftmenu,text="Сотрудник",command=self.employee,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        supplierbtn=Button(lftmenu,text="Поставщик",command=self.supplier,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        categorybtn=Button(lftmenu,text="Категория",command=self.category,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        productbtn=Button(lftmenu,text="Товары",command=self.products,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        salesbtn=Button(lftmenu,text="Продажи",command=self.sales,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        sellingbtn=Button(lftmenu,text="Выставление счетов",command=self.billing,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        aboutbtn=Button(lftmenu,text="О программе",command=self.about,font=("times new roman",20,"bold"),bg="#D4AC0D",bd=3,cursor="hand2").pack(side=TOP,fill=X)

            #общее количество в системе
        self.employeelbl=Label(self.root,text="Общее количество\nсотрудников\n[ 0 ]",bd=5,relief=RIDGE,bg="#D35400",fg="black",font=("times new roman",20,"bold"))
        self.employeelbl.place(x=300,y=170,height=200,width=300)
        self.supplierlbl = Label(self.root, text="Общее количество\nпоставщиков\n[ 0 ]", bd=5, relief=RIDGE, bg="#D35400", fg="black",font=("times new roman", 20, "bold"))
        self.supplierlbl.place(x=1000, y=170, height=200, width=300)
        self.categorylbl = Label(self.root, text="Общее количество\nкатегорий\n[ 0 ]", bd=5, relief=RIDGE, bg="#D35400", fg="black",font=("times new roman", 20, "bold"))
        self.categorylbl.place(x=650, y=270, height=200, width=300)
        self.productslbl = Label(self.root, text="Общее количество\nтоваров\n[ 0 ]", bd=5, relief=RIDGE, bg="#D35400", fg="black",font=("times new roman", 20, "bold"))
        self.productslbl.place(x=300, y=400, height=200, width=300)
        self.saleslbl = Label(self.root, text="Общий объем\nпродаж\n[ 0 ]", bd=5, relief=RIDGE, bg="#D35400", fg="black",font=("times new roman", 20, "bold"))
        self.saleslbl.place(x=1000, y=400, height=200, width=300)

            #Нижний колонтитул
        footerlbl=Label(self.root,text="Система управления супермаркетом ioitms | Copyright © 2023",font=("times new roman",10),bg="#2C3E50",fg="white").pack(side=BOTTOM,fill=X)

        self.totals()
            #функции для доступа к классам
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=emp(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supp(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = cat(self.new_win)

    def products(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = prod(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = sal(self.new_win)

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = bil(self.new_win)

    def about(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ab(self.new_win)

        #функция для подсчета итогов в системе
    def totals(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            conn = cur.execute("Select * from Employee")
            theemployee = cur.fetchall()
            self.employeelbl.config(text=f'Общее количество\nсотрудников\n[ {str(len(theemployee))} ]')

            conn = cur.execute("Select * from Supplier")
            thesupplier = cur.fetchall()
            self.supplierlbl.config(text=f'Общее количество\nпоставщиков\n[ {str(len(thesupplier))} ]')

            conn = cur.execute("Select * from Category")
            thecategory = cur.fetchall()
            self.categorylbl.config(text=f'Общее количество\nкатегорий\n[ {str(len(thecategory))} ]')

            conn=cur.execute("Select * from Products")
            theproduct=cur.fetchall()
            self.productslbl.config( text=f'Общее количество\nтоваров\n[ {str(len(theproduct))} ]')

            checkss=len(os.listdir('Checks'))
            self.saleslbl.config( text=f'Общий объем\nпродаж\n[ {str(checkss)} ]')

            btime = time.strftime("%I:%M:%S")
            bdate = time.strftime("%d-%m-%Y")
            self.clocklbl.config(text=f"Универсальный магазин в вашем районе\t\t Дата: {str(bdate)}\t\t Время: {str(btime)}")
            self.clocklbl.after(200, self.totals)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        # функция выхода
    def logout(self):
        self.root.destroy()
        os.system("python Login.py")

if __name__=="__main__":
    root=Tk()
    obj=ioitms(root)
    root.mainloop()