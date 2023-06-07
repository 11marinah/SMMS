from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import os
import sqlite3
class sal:
    # рамка страницы продажи
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="white")
        self.root.focus_force()

        #переменные
        self.salinv=StringVar()
        self.salinfo=[]
        saldeatilslbl = Label(self.root, text="Подробная информация о распродажах", font=("times new roman", 20), bg="#BA4A00",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        salinvlbl = Label(self.root, text="Номер счета-фактуры", font=("times new roman", 15), bg="white").place(x=50, y=100)
        salinvtxt = Entry(self.root, textvariable=self.salinv, font=("times new roman", 15), bg="lightyellow").place(x=250, y=100, width=200, height=30)

        searchbtn = Button(self.root, text="Поиск",command=self.search, font=("times new roman", 15), bg="#7D6608",fg="white", cursor="hand2").place(x=500, y=100, width=150, height=30)
        clearbtn = Button(self.root, text="Очистить",command=self.clear, font=("times new roman", 15), bg="gray",fg="white", cursor="hand2").place(x=700, y=100, width=150, height=30)

        # Таблицы данных о продажах
        sinvframe = Frame(self.root, bd=3, relief=RIDGE)
        sinvframe.place(x=50, y=150, width=410, height=320)

        yscroll=Scrollbar(sinvframe,orient=VERTICAL)
        self.sallist=Listbox(sinvframe,font=("times new roman",15),bg="white",yscrollcommand=yscroll.set)
        yscroll.pack(side=RIGHT,fill=Y)
        yscroll.config(command=self.sallist.yview)
        self.sallist.pack(fill=BOTH,expand=1)
        self.sallist.bind("<ButtonRelease-1>",self.getdata)

        salframe = Frame(self.root, bd=3, relief=RIDGE)
        salframe.place(x=580, y=150, width=410, height=320)

        saldonelbl = Label(salframe, text="Осуществленные продажи", font=("times new roman", 20), bg="#BA4A00",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X)


        y1scroll = Scrollbar(salframe, orient=VERTICAL)
        self.saleschecks = Text(salframe, bg="lightyellow", yscrollcommand=y1scroll.set)
        y1scroll.pack(side=RIGHT, fill=Y)
        y1scroll.config(command=self.sallist.yview)
        self.saleschecks.pack(fill=BOTH, expand=1)

        self.displai()

    # функция отображения
    def displai(self):
        del self.salinfo[:]
        self.sallist.delete(0,END)
        for i in os.listdir('Checks'):
            if i.split('.')[-1]=='txt':
                self.sallist.insert(END,i)
                self.salinfo.append(i.split('.')[0])

    # получить данные о продажах
    def getdata(self,ev):
        indx=self.sallist.curselection()
        filename=self.sallist.get(indx)
        self.saleschecks.delete('1.0',END)
        openfile=open(f'Checks/{filename}','r')
        for i in openfile:
            self.saleschecks.insert(END,i)
        openfile.close()

    # поиск продаж
    def search(self):
        if self.salinv.get()=="":
            messagebox.showerror("Error","Invoice number is required",parent=self.root)
        else:
            if self.salinv.get() in self.salinfo:
                openfile = open(f'Checks/{self.salinv.get()}.txt', 'r')
                self.saleschecks.delete('1.0',END)
                for i in openfile:
                    self.saleschecks.insert(END, i)
                openfile.close()
            else:
                messagebox.showerror("Error", "Your Invoice No is invalid", parent=self.root)

    # очистить данные о продажах
    def clear(self):
        self.displai()
        self.saleschecks.delete('1.0',END)

if __name__ == "__main__":
    root = Tk()
    obj = sal(root)
    root.mainloop()