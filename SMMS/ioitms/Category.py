from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class cat:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="white")
        self.root.focus_force()

        self.catid = StringVar()
        self.catname = StringVar()

        categdetailslbl = Label(self.root, text="Категория товаров", font=("times new roman", 20), bg="#BA4A00",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        catnamelbl = Label(self.root, text="Название категории", font=("times new roman", 15), bg="white").place(x=50, y=100)
        catnametxt = Entry(self.root, textvariable=self.catname, font=("times new roman", 15), bg="white").place(x=230, y=100,width=200)

        savebtn = Button(self.root, text="Сохранить", command=self.save, font=("times new roman", 15), bg="#2C3E50",fg="white", cursor="hand2").place(x=50, y=140, width=100, height=30)
        deletebtn = Button(self.root, text="Удалить", command=self.delete, font=("times new roman", 15), bg="#BA4A00",fg="white", cursor="hand2").place(x=170, y=140, width=100, height=30)

        # Category data table
        catframe = Frame(self.root, bd=3, relief=RIDGE)
        catframe.place(x=550, y=100, width=500, height=300)

        yscroll = Scrollbar(catframe, orient=VERTICAL)
        xscroll = Scrollbar(catframe, orient=HORIZONTAL)

        self.categorytable = ttk.Treeview(catframe, columns=(
            "cid", "name"),yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        xscroll.config(command=self.categorytable.xview)
        yscroll.config(command=self.categorytable.yview)

        self.categorytable.heading("cid", text="КID")
        self.categorytable.heading("name", text="Название")

        self.categorytable["show"] = "headings"

        self.categorytable.column("cid", width=90)
        self.categorytable.column("name", width=100)

        self.categorytable.pack(fill=BOTH, expand=1)
        self.categorytable.bind("<ButtonRelease-1>", self.getdata)
        #
        # self.displai()

        self.catimage=Image.open("IMAGES/category.jpg")
        self.catimage=self.catimage.resize((495,220),Image.Resampling.LANCZOS)
        self.catimage=ImageTk.PhotoImage(self.catimage)
        self.catimagelbl=Label(self.root,image=self.catimage,bd=2,relief=RAISED)
        self.catimagelbl.place(x=50,y=175)

        self.displai()

        # добавление категорий
    def save(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.catname.get() == "":
                messagebox.showerror("Error", "Name of the category is required", parent=self.root)
            else:
                cur.execute("Select * from Category where name=?", (self.catname.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "We already have the category,try another one",
                                         parent=self.root)
                else:
                    cur.execute(
                        "Insert into Category (name) values(?)",
                        (
                            self.catname.get(),
                        ))
                    conn.commit()
                    messagebox.showinfo("Success", "Category successfuly added", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # отобразить данные
    def displai(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            cur.execute("Select * from Category ")
            rows = cur.fetchall()
            self.categorytable.delete(*self.categorytable.get_children())
            for row in rows:
                self.categorytable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        # получить данные из таблицы
    def getdata(self, ev):
        f = self.categorytable.focus()
        content = (self.categorytable.item(f))
        row = content['values']
        self.catid.set(row[0])
        self.catname.set(row[1])

        # удалить категорию
    def delete(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.catid.get() == "":
                messagebox.showerror("Error", "Name of the category is required select it from the list", parent=self.root)
            else:
                cur.execute("Select * from Category where cid=?", (self.catid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "This name of the category is invalid", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Are you sure you want to delete this data?", parent=self.root)
                    if op == True:
                        cur.execute("delete from Category where cid=?", (self.catid.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Category successfully deleted", parent=self.root)
                        self.displai()
                        self.catid.set("")
                        self.catname.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = cat(root)
    root.mainloop()