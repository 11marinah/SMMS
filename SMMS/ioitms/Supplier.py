from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class supp:
    # рамка страницы поставщика
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="white")
        self.root.focus_force()

        # переменные
        self.suppsearchby = StringVar()
        self.suppsearchtext = StringVar()
        self.suppinv = StringVar()
        self.suppcontact = StringVar()
        self.suppname = StringVar()
        self.suppdescr = StringVar()

        # данные поставщика
        frsearch = LabelFrame(self.root, text="Поиск поставщика", font=("times new roman", 15, "bold"), bd=2,relief=RIDGE, bg="white")
        frsearch.place(x=250, y=30, width=600, height=70)
        searchcb = ttk.Combobox(frsearch, textvariable=self.suppsearchby, values=("Select","Invoice", "Name", "Contact"),state='readonly', justify=CENTER, font=("times new roman", 15))
        searchcb.place(x=10, y=10, width=180)
        searchcb.current(0)
        searchtext = Entry(frsearch, textvariable=self.suppsearchtext, font=("times new roman", 15),bg="lightyellow").place(x=200, y=10)
        searchbtn = Button(frsearch, text="Поиск", command=self.search, font=("times new roman", 15), bg="#7D6608",fg="white", cursor="hand2").place(x=410, y=10, width=150, height=30)
        suppldetailslbl = Label(self.root, text="Информация о поставщике", font=("times new roman", 15), bg="#BA4A00",fg="white").place(x=50, y=100, width=1000)
        suppinvlbl = Label(self.root, text="Номер счета-фактуры", font=("times new roman", 15), bg="white").place(x=50, y=150)
        suppinvtxt = Entry(self.root, textvariable=self.suppinv, font=("times new roman", 15), bg="lightyellow").place(x=250, y=150, width=180)
        suppnamelbl = Label(self.root, text="Имя", font=("times new roman", 15), bg="white").place(x=50, y=190)
        suppnametxt = Entry(self.root, textvariable=self.suppname, font=("times new roman", 15), bg="lightyellow").place(x=250, y=190, width=180)
        suppcontactlbl = Label(self.root, text="Номер телефона", font=("times new roman", 15), bg="white").place(x=50, y=230)
        suppcontacttxt = Entry(self.root, textvariable=self.suppcontact, font=("times new roman", 15),bg="lightyellow").place(x=250, y=230, width=180)
        suppdescrlbl = Label(self.root, text="Описание", font=("times new roman", 15), bg="white").place(x=50, y=270)
        self.suppdescrtxt = Text(self.root,  font=("times new roman", 15),bg="lightyellow")
        self.suppdescrtxt.place(x=250, y=270, width=280,height=100)
        savebtn = Button(self.root, text="Сохранить", command=self.save, font=("times new roman", 15), bg="#2C3E50",fg="white", cursor="hand2").place(x=50, y=420, width=110, height=30)
        updatebtn = Button(self.root, text="Обновление", command=self.update, font=("times new roman", 15), bg="#7D6608",fg="white", cursor="hand2").place(x=170, y=420, width=110, height=30)
        deletebtn = Button(self.root, text="Удалить", command=self.delete, font=("times new roman", 15), bg="#BA4A00",fg="white", cursor="hand2").place(x=290, y=420, width=110, height=30)
        clearbtn = Button(self.root, text="Очистить", command=self.clear, font=("times new roman", 15), bg="#607d8b",fg="white", cursor="hand2").place(x=410, y=420, width=110, height=30)

        # таблица данных поставщика
        suppframe = Frame(self.root, bd=3, relief=RIDGE)
        suppframe.place(x=550, y=150, width=500, height=300)
        yscroll = Scrollbar(suppframe, orient=VERTICAL)
        xscroll = Scrollbar(suppframe, orient=HORIZONTAL)
        self.suppliertable = ttk.Treeview(suppframe, columns=(
        "invoice", "name", "contact", "desc"),yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        xscroll.config(command=self.suppliertable.xview)
        yscroll.config(command=self.suppliertable.yview)

        self.suppliertable.heading("invoice", text="Номер счета-фактуры")
        self.suppliertable.heading("name", text="Имя")
        self.suppliertable.heading("contact", text="Номер телефона")
        self.suppliertable.heading("desc", text="Описание")
        self.suppliertable["show"] = "headings"
        self.suppliertable.column("invoice", width=120)
        self.suppliertable.column("name", width=80)
        self.suppliertable.column("contact", width=100)
        self.suppliertable.column("desc", width=100)
        self.suppliertable.pack(fill=BOTH, expand=1)
        self.suppliertable.bind("<ButtonRelease-1>", self.getdata)
        self.displai()

    # добавление данных поставщика
    def save(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.suppinv.get() == "":
                messagebox.showerror("Error", "Invoice is required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where invoice=?", (self.suppinv.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This invoice is already assigned,try another one", parent=self.root)
                else:
                    cur.execute(
                        "Insert into Supplier (invoice, name, contact, desc) values(?,?,?,?)",
                        (
                            self.suppinv.get(),
                            self.suppname.get(),
                            self.suppcontact.get(),
                            self.suppdescrtxt.get('1.0',END),
                        ))
                    conn.commit()
                    messagebox.showinfo("Success", "Supplier successfuly added", parent=self.root)
                    self.displai()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # показать данные поставщика
    def displai(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            cur.execute("Select * from Supplier ")
            rows = cur.fetchall()
            self.suppliertable.delete(*self.suppliertable.get_children())
            for row in rows:
                self.suppliertable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            # получить данные
    def getdata(self, ev):
        f = self.suppliertable.focus()
        content = (self.suppliertable.item(f))
        row = content['values']
        # print(row)
        self.suppinv.set(row[0])
        self.suppname.set(row[1])
        self.suppcontact.set(row[2])
        self.suppdescrtxt.delete('1.0', END)
        self.suppdescrtxt.insert(END, row[3])

        # обновить данные поставщиков
    def update(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.suppinv.get() == "":
                messagebox.showerror("Error", "invoice is required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where invoice=?", (self.suppinv.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This invoice is invalid", parent=self.root)
                else:
                    cur.execute(
                        "update Supplier set name=?, contact=?, desc=?  where invoice=?",
                        (
                            self.suppname.get(),
                            self.suppcontact.get(),
                            self.suppdescrtxt.get('1.0',END),
                            self.suppinv.get(),
                        ))
                    conn.commit()
                    messagebox.showinfo("Success", "Supplier successfuly updated", parent=self.root)
                    self.displai()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            # удалить данные поставщиков
    def delete(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.suppinv.get() == "":
                messagebox.showerror("Error", "invoice is required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where invoice=?", (self.suppinv.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This invoice is invalid", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Are you sure you want to delete this data?", parent=self.root)
                    if op == True:
                        cur.execute("delete from Supplier where invoice=?", (self.suppinv.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Supplier successfully deleted", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            # очистить функцию
    def clear(self):
        self.suppinv.set("")
        self.suppname.set("")
        self.suppcontact.set("")
        self.suppdescrtxt.delete('1.0', END)
        self.displai()

        # поиск поставщика
    def search(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.suppsearchby.get() == "Select":
                messagebox.showerror("Error", "Search by Invoice, name or contact", parent=self.root)
            elif self.suppsearchtext.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute(
                    "Select * from Supplier where " + self.suppsearchby.get() + " LIKE '%" + self.suppsearchtext.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.suppliertable.delete(*self.suppliertable.get_children())
                    for row in rows:
                        self.suppliertable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "Data not found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = supp(root)
    root.mainloop()