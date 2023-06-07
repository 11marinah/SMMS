from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class prod:
    # рамка страницы товара
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="white")
        self.root.focus_force()

        #переменные
        self.prodsearchby = StringVar()
        self.prodsearchtext = StringVar()

        self.prodid = StringVar()
        self.prodcatname = StringVar()
        self.categlist = []
        self.prodsuppname = StringVar()
        self.suppllist=[]
        self.fetch_categoryandsupplier()
        self.prodname = StringVar()
        self.prodprice = StringVar()
        self.prodquantity = StringVar()
        self.prodavailability = StringVar()


        frsearch = LabelFrame(self.root, text="Поиск товаров", font=("goudy old style", 15, "bold"), bd=2,relief=RIDGE, bg="white")
        frsearch.place(x=480, y=10, width=600, height=80)

        searchcb = ttk.Combobox(frsearch, textvariable=self.prodsearchby, values=("Выбрать", "Category", "Supplier", "Name"),state='readonly', justify=CENTER, font=("times new roman", 15))
        searchcb.place(x=10, y=10, width=180)
        searchcb.current(0)

        searchtext = Entry(frsearch, textvariable=self.prodsearchtext, font=("times new roman", 15),bg="lightyellow").place(x=200, y=10)
        searchbtn = Button(frsearch, text="Поиск", command=self.search, font=("times new roman", 15), bg="#7D6608",fg="white", cursor="hand2").place(x=410, y=10, width=150, height=30)


        # таблица данных товаров
        prodframe = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        prodframe.place(x=10, y=10, width=450, height=480)

        proddetailslbl = Label(prodframe, text="Товары в супермаркете", font=("times new roman", 20), bg="#BA4A00",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        prodcatnamelbl = Label(self.root, text="Название категории", font=("times new roman", 15), bg="white").place(x=30, y=60)
        prodsuppnamelbl = Label(self.root, text="Имя поставщика", font=("times new roman", 15), bg="white").place(x=30, y=110)
        prodnamelbl = Label(self.root, text="Наименование товара", font=("times new roman", 15), bg="white").place(x=30, y=160)
        prodpricenamelbl = Label(self.root, text="Цена", font=("times new roman", 15), bg="white").place(x=30, y=210)
        prodquantitynamelbl = Label(self.root, text="Количество", font=("times new roman", 15), bg="white").place(x=30, y=260)
        prodavailabilitynamelbl = Label(self.root, text="Доступность", font=("times new roman", 15), bg="white").place(x=30, y=310)

        prodcatnamecb = ttk.Combobox(prodframe, textvariable=self.prodcatname, values=self.categlist,state='readonly', justify=CENTER, font=("times new roman", 15))
        prodcatnamecb.place(x=230,y=45,width=180)
        prodcatnamecb.current(0)

        prodsuppnamecb = ttk.Combobox(prodframe, textvariable=self.prodsuppname, values=self.suppllist,state='readonly', justify=CENTER, font=("times new roman", 15))
        prodsuppnamecb.place(x=230,y=95,width=180)
        prodsuppnamecb.current(0)

        prodnametxt=Entry(prodframe,textvariable=self.prodname,font=("times new roman",15),bg="lightyellow").place(x=230,y=145,width=180)
        prodpricetxt=Entry(prodframe,textvariable=self.prodprice,font=("times new roman",15),bg="lightyellow").place(x=230,y=195,width=180)
        prodquantitytxt=Entry(prodframe,textvariable=self.prodquantity,font=("times new roman",15),bg="lightyellow").place(x=230,y=245,width=180)

        prodavailabilitynamecb = ttk.Combobox(prodframe, textvariable=self.prodavailability, values=("Доступный","Недоступный"),state='readonly', justify=CENTER, font=("times new roman", 15))
        prodavailabilitynamecb.place(x=230,y=295,width=180)
        prodavailabilitynamecb.current(0)

        savebtn=Button(prodframe,text="Сохранить",command=self.save,font=("times new roman",15),bg="#2C3E50",fg="white",cursor="hand2").place(x=25,y=400,width=100,height=30)
        updatebtn=Button(prodframe,text="Обновление",command=self.update,font=("times new roman",15),bg="#7D6608",fg="white",cursor="hand2").place(x=130,y=400,width=110,height=30)
        deletebtn=Button(prodframe,text="Удалить",command=self.delete,font=("times new roman",15),bg="#BA4A00",fg="white",cursor="hand2").place(x=245,y=400,width=90,height=30)
        clearbtn=Button(prodframe,text="Очистить",command=self.clear,font=("times new roman",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=90,height=30)


        prod2frame = Frame(self.root, bd=3, relief=RIDGE)
        prod2frame.place(x=480, y=100, width=600, height=390)

        yscroll = Scrollbar(prod2frame, orient=VERTICAL)
        xscroll = Scrollbar(prod2frame, orient=HORIZONTAL)

        self.producttable = ttk.Treeview(prod2frame, columns=(
        "pid", "category", "supplier", "name", "price", "quantity", "availability"), yscrollcommand=yscroll.set,
                                          xscrollcommand=xscroll.set)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        xscroll.config(command=self.producttable.xview)
        yscroll.config(command=self.producttable.yview)

        self.producttable.heading("pid", text="ТID")
        self.producttable.heading("category", text="Категория")
        self.producttable.heading("supplier", text="Поставщик")
        self.producttable.heading("name", text="Название")
        self.producttable.heading("price", text="Цена")
        self.producttable.heading("quantity", text="Количество")
        self.producttable.heading("availability", text="Доступность")

        self.producttable["show"] = "headings"

        self.producttable.column("pid", width=90)
        self.producttable.column("category", width=100)
        self.producttable.column("supplier", width=100)
        self.producttable.column("name", width=100)
        self.producttable.column("price", width=90)
        self.producttable.column("quantity", width=100)
        self.producttable.column("availability", width=100)

        self.producttable.pack(fill=BOTH, expand=1)
        self.producttable.bind("<ButtonRelease-1>", self.getdata)

        self.displai()

    # получение данных о категории и поставщике
    def fetch_categoryandsupplier(self):
        self.categlist.append("Empty")
        self.suppllist.append("Empty")
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            cur.execute("Select name from Category")
            categ=cur.fetchall()
            if len(categ)>0:
                del self.categlist[:]
                self.categlist.append("Select")
                for i in categ:
                    self.categlist.append(i[0])
            cur.execute("Select name from Supplier")
            suppl = cur.fetchall()
            if len(suppl) > 0:
                del self.suppllist[:]
                self.suppllist.append("Select")
                for i in suppl:
                    self.suppllist.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # добавление функции
    def save(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.prodcatname.get() == "Select" or self.prodcatname.get() == "Empty" or self.prodsuppname.get()=="Select" or self.prodname.get()=="Select":
                messagebox.showerror("Error", "All fields are  required", parent=self.root)
            else:
                cur.execute("Select * from Products where name=?", (self.prodname.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "We already have the product,try another one", parent=self.root)
                else:
                    cur.execute(
                        "Insert into Products (category, supplier, name, price, quantity, availability) values(?,?,?,?,?,?)",
                        (
                            self.prodcatname.get(),
                            self.prodsuppname.get(),
                            self.prodname.get(),
                            self.prodprice.get(),
                            self.prodquantity.get(),
                            self.prodavailability.get(),
                        ))
                    conn.commit()
                    messagebox.showinfo("Success", "Products successfuly added", parent=self.root)
                    self.displai()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # функция отображения
    def displai(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            cur.execute("Select * from Products ")
            rows = cur.fetchall()
            self.producttable.delete(*self.producttable.get_children())
            for row in rows:
                self.producttable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # получить данные таблицы
    def getdata(self, ev):
        f = self.producttable.focus()
        content = (self.producttable.item(f))
        row = content['values']
        self.prodid.set(row[0])
        self.prodcatname.set(row[1])
        self.prodsuppname.set(row[2])
        self.prodname.set(row[3])
        self.prodprice.set(row[4])
        self.prodquantity.set(row[5])
        self.prodavailability.set(row[6])

        # обновление товара
    def update(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.prodcatname.get() == "":
                messagebox.showerror("Error", "Select product from the list", parent=self.root)
            else:
                cur.execute("Select * from Products where pid=?", (self.prodid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This product is invalid", parent=self.root)
                else:
                    cur.execute(
                        "update Products set category=?, supplier=?, name=?, price=?, quantity=?, availability=?  where pid=?",
                        (
                            self.prodcatname.get(),
                            self.prodsuppname.get(),
                            self.prodname.get(),
                            self.prodprice.get(),
                            self.prodquantity.get(),
                            self.prodavailability.get(),
                            self.prodid.get(),

                        ))
                    conn.commit()
                    messagebox.showinfo("Success", "Products successfuly updated", parent=self.root)
                    self.displai()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # удаление товара
    def delete(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.prodid.get() == "":
                messagebox.showerror("Error", "Select product from the list", parent=self.root)
            else:
                cur.execute("Select * from Products where pid=?", (self.prodid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This product is invalid", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Are you sure you want to delete this data?", parent=self.root)
                    if op == True:
                        cur.execute("delete from Products where pid=?", (self.prodid.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Products successfully deleted", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # очистить данные в текстовом поле или поле со списком
    def clear(self):
        self.prodid.set("")
        self.prodcatname.set("Select")
        self.prodsuppname.set("Select")
        self.prodname.set("")
        self.prodprice.set("")
        self.prodquantity.set("")
        self.prodavailability.set("Availability")
        self.prodsearchtext.set("")
        self.prodsearchby.set("Select")
        self.displai()

    # поиск товара
    def search(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.prodsearchby.get() == "Select":
                messagebox.showerror("Error", "Search by name,email or contact", parent=self.root)
            elif self.prodsearchtext.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute(
                    "Select * from Products where " + self.prodsearchby.get() + " LIKE '%" + self.prodsearchtext.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.producttable.delete(*self.producttable.get_children())
                    for row in rows:
                        self.producttable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "Data not found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = prod(root)
    root.mainloop()