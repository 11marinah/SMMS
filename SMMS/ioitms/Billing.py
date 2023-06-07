from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class bil:
    #рамка страницы выставления счетов
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="white")

        self.icon_title=PhotoImage(file="IMAGES/shopping-cart.png")
        title=Label(self.root,text="Супермаркет ioitms",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#6E2C00",fg="white",anchor="w",padx="20").place(x=0,y=0,relwidth=1,height=70)

            #время
        blogoutbtn=Button(self.root,text="Выйти",font=("times new roman",15,"bold"),command=self.logout,bg="#D4AC0D",cursor="hand2").place(x=1150,y=10,width=150,height=50)
        self.bclocklbl=Label(self.root,text="Универсальный магазин в вашем районе\t\t Дата: DD-MM-YYYY\t\t Время: HH:MM:SS",font=("times new roman",15),bg="#2C3E50",fg="white")
        self.bclocklbl.place(x=0,y=70,relwidth=1,height=30)

        #переменные
        self.bproductsearch=StringVar()
        self.clientname=StringVar()
        self.clientcontact=StringVar()

        self.bproductid = StringVar()
        self.bproductname = StringVar()
        self.bproductprice = StringVar()
        self.bproductquantity = StringVar()
        self.bproductavailability = StringVar()
        self.instock = StringVar()
        self.calculatorinput = StringVar()

        self.cartlist=[]
        self.printcheck=0

        #Таблица данных товаров Рамка
        productframe = Frame(self.root, bd=5, relief=RIDGE,bg="white")
        productframe.place(x=10, y=110, width=410, height=570)
        productframelbl = Label(productframe, text="Товары", font=("times new roman", 20), bg="#BA4A00",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X)

        #рамка поиска товаров
        productframesearch = Frame(productframe, bd=3, relief=RIDGE,bg="white")
        productframesearch.place(x=2, y=40, width=400, height=90)
        productframesearchlbl = Label(productframesearch, text="Поиск товаров ", font=("times new roman", 16,"bold"), bg="white",fg="black").place(x=5,y=5)

        bproductnamelbl = Label(productframesearch, text="Название", font=("times new roman", 16,"bold"), bg="white",fg="black").place(x=1,y=40)
        bproductnametxt = Entry(productframesearch,textvariable=self.bproductsearch, font=("times new roman", 16), bg="lightyellow").place(x=150,y=47,width=140,height=22)

        searchbtn = Button(productframesearch, text="Поиск", command=self.search, font=("times new roman", 15), bg="#BA4A00",fg="white", cursor="hand2").place(x=295, y=47, width=95, height=22)
        Displaybtn = Button(productframesearch, text="Отобразить все", command=self.displai, font=("times new roman", 15), bg="#BA4A00",fg="white", cursor="hand2").place(x=255, y=5, width=135, height=22)

        #Рамка сведений о товарах
        bproducttableframe = Frame(productframe, bd=3, relief=RIDGE)
        bproducttableframe.place(x=2, y=150, width=400, height=400)

        yscroll = Scrollbar(bproducttableframe, orient=VERTICAL)
        xscroll = Scrollbar(bproducttableframe, orient=HORIZONTAL)

        self.bproducttable = ttk.Treeview(bproducttableframe, columns=(
        "pid", "name", "price", "quantity", "availability"),yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        xscroll.config(command=self.bproducttable.xview)
        yscroll.config(command=self.bproducttable.yview)

        self.bproducttable.heading("pid", text="ТID")
        self.bproducttable.heading("name", text="Название")
        self.bproducttable.heading("price", text="Цена")
        self.bproducttable.heading("quantity", text="Количество")
        self.bproducttable.heading("availability", text="Доступность")

        self.bproducttable["show"] = "headings"

        self.bproducttable.column("pid", width=40)
        self.bproducttable.column("name", width=90)
        self.bproducttable.column("price", width=60)
        self.bproducttable.column("quantity", width=80)
        self.bproducttable.column("availability", width=100)

        self.bproducttable.pack(fill=BOTH, expand=1)
        self.bproducttable.bind("<ButtonRelease-1>", self.getdata)

        bproducttablenotelbl = Label(productframe, text="Чтобы удалить товары из корзины, введите количество 0", font=("times new roman", 10),anchor='w', bg="#BA4A00",fg="white",bd=1,relief=RIDGE).pack(side=BOTTOM,fill=X)


        #рамка таблицы данных клиента
        clientframe = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        clientframe.place(x=420, y=110, width=500, height=120)
        clientframelbl = Label(clientframe, text="Клиентские данные", font=("times new roman", 20), bg="#F39C12", fg="white",bd=3, relief=RIDGE).pack(side=TOP, fill=X)

        clientamelbl = Label(clientframe, text="Имя", font=("times new roman", 16, "bold"), bg="white",fg="black").place(x=5, y=40)
        clientnametxt = Entry(clientframe, textvariable=self.clientname, font=("times new roman", 16),bg="lightyellow").place(x=180, y=45, width=180, height=20)

        clientcontactlbl = Label(clientframe, text="Номер телефона", font=("times new roman", 16, "bold"), bg="white",fg="black").place(x=5, y=75)
        clientcontacttxt = Entry(clientframe, textvariable=self.clientcontact, font=("times new roman", 16),bg="lightyellow").place(x=180, y=75, width=180, height=20)

        #тележка и рамка калькулятора
        cartcalculatorframe = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        cartcalculatorframe.place(x=420, y=230, width=500, height=450)
        cartcalculatorframelbl = Label(cartcalculatorframe, text="Калькулятор и корзина", font=("times new roman", 20), bg="gray", fg="white",bd=3, relief=RIDGE).pack(side=TOP, fill=X)

        #рамка калькулятора
        calculatorframe = Frame(cartcalculatorframe, bd=5, relief=RIDGE, bg="white")
        calculatorframe.place(x=2, y=40, width=245, height=310)

        calculatorinputtxt = Entry(calculatorframe, textvariable=self.calculatorinput, font=("arial", 20,"bold"), width=15,bd=7, relief=GROOVE,state='readonly')
        calculatorinputtxt.grid(row=0,columnspan=4)

        btn7 = Button(calculatorframe, text='7', font=("arial", 15),command=lambda :self.getinput(7), width=4,bd=4,pady=11, cursor="hand2").grid(row=1,column=0)
        btn8 = Button(calculatorframe, text='8', font=("arial", 15),command=lambda :self.getinput(8), width=4,bd=4,pady=11, cursor="hand2").grid(row=1,column=1)
        btn9 = Button(calculatorframe, text='9', font=("arial", 15),command=lambda :self.getinput(9), width=4,bd=4,pady=11, cursor="hand2").grid(row=1,column=2)
        btnadd = Button(calculatorframe, text="+", font=("arial", 15),command=lambda :self.getinput('+'), width=4,bd=4,pady=11, cursor="hand2").grid(row=1,column=3)

        btn4 = Button(calculatorframe, text='4', font=("arial", 15),command=lambda :self.getinput(4), width=4,bd=4,pady=11, cursor="hand2").grid(row=2,column=0)
        btn5 = Button(calculatorframe, text='5', font=("arial", 15),command=lambda :self.getinput(5), width=4,bd=4,pady=11, cursor="hand2").grid(row=2,column=1)
        btn6 = Button(calculatorframe, text='6', font=("arial", 15),command=lambda :self.getinput(6), width=4,bd=4,pady=11, cursor="hand2").grid(row=2,column=2)
        btnsub = Button(calculatorframe, text="-", font=("arial", 15),command=lambda :self.getinput('-'), width=4,bd=4,pady=11, cursor="hand2").grid(row=2,column=3)

        btn1 = Button(calculatorframe, text='1', font=("arial", 15),command=lambda :self.getinput(1), width=4,bd=4,pady=11, cursor="hand2").grid(row=3,column=0)
        btn2 = Button(calculatorframe, text='2', font=("arial", 15),command=lambda :self.getinput(2), width=4,bd=4,pady=11, cursor="hand2").grid(row=3,column=1)
        btn3 = Button(calculatorframe, text='3', font=("arial", 15),command=lambda :self.getinput(3), width=4,bd=4,pady=11, cursor="hand2").grid(row=3,column=2)
        btnmlt = Button(calculatorframe, text="*", font=("arial", 15),command=lambda :self.getinput('*'), width=4,bd=4,pady=11, cursor="hand2").grid(row=3,column=3)

        btn0 = Button(calculatorframe, text='0', font=("arial", 15),command=lambda :self.getinput(0), width=4, bd=4, pady=11, cursor="hand2").grid(row=4,column=0)
        btnc = Button(calculatorframe, text='C', font=("arial", 15) ,command=self.clearcalc, width=4, bd=4, pady=11, cursor="hand2").grid(row=4,column=1)
        btneql = Button(calculatorframe, text='=', font=("arial", 15),command=self.results, width=4, bd=4, pady=11, cursor="hand2").grid(row=4, column=2)
        btndiv = Button(calculatorframe, text="/", font=("arial", 15),command=lambda :self.getinput('/'), width=4, bd=4, pady=11, cursor="hand2").grid(row=4, column=3)

        #рамка корзин
        cartframe = Frame(cartcalculatorframe, bd=5, relief=RIDGE, bg="white")
        cartframe.place(x=245, y=40, width=245, height=310)
        self.cartframelbl = Label(cartframe, text="Корзина \t Всего товара: [0]", font=("times new roman", 13), bg="gray",fg="white",bd=1,relief=RIDGE)
        self.cartframelbl.pack(side=TOP,fill=X)


        yscroll = Scrollbar(cartframe, orient=VERTICAL)
        xscroll = Scrollbar(cartframe, orient=HORIZONTAL)

        self.carttable = ttk.Treeview(cartframe, columns=(
            "pid", "name", "price", "quantity"), yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        xscroll.config(command=self.carttable.xview)
        yscroll.config(command=self.carttable.yview)

        self.carttable.heading("pid", text="ТID")
        self.carttable.heading("name", text="Название")
        self.carttable.heading("price", text="Цена")
        self.carttable.heading("quantity", text="Количество")

        self.carttable["show"] = "headings"

        self.carttable.column("pid", width=30)
        self.carttable.column("name", width=60)
        self.carttable.column("price", width=40)
        self.carttable.column("quantity", width=80)

        self.carttable.pack(fill=BOTH, expand=1)
        self.carttable.bind("<ButtonRelease-1>", self.getcarttdata)

        #виджет корзины
        cartwidgetframe = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        cartwidgetframe.place(x=425, y=585, width=490, height=90)


        cartproductnamelbl = Label(cartwidgetframe, text="Название товара", font=("times new roman", 14, "bold"), bg="white",fg="black").place(x=5, y=2)
        cartproductnametxt = Entry(cartwidgetframe,textvariable=self.bproductname, font=("times new roman", 14), bg="lightyellow",state='readonly').place(x=5,y=32,width=130,height=22)

        cartproductpricelbl = Label(cartwidgetframe, text="Цена за кол-во", font=("times new roman", 14, "bold"), bg="white",fg="black").place(x=170, y=2)
        cartproductpricetxt = Entry(cartwidgetframe,textvariable=self.bproductprice, font=("times new roman", 14), bg="lightyellow",state='readonly').place(x=170,y=32,width=180,height=22)

        cartproductquantitylbl = Label(cartwidgetframe, text="Количество", font=("times new roman", 14, "bold"), bg="white",fg="black").place(x=360, y=2)
        cartproductquantitytxt = Entry(cartwidgetframe,textvariable=self.bproductquantity, font=("times new roman", 14), bg="lightyellow").place(x=360,y=32,width=110,height=22)

        self.cartproductavailabilitylbl = Label(cartwidgetframe, text="В наличии", font=("times new roman", 14, "bold"), bg="white",fg="black")
        self.cartproductavailabilitylbl.place(x=5, y=55,width=130,height=22)

        cartaddbtn=Button(cartwidgetframe,text="Добавить в корзину", command=self.addcart,font=("times new roman",15),bg="#F39C12",fg="white",cursor="hand2").place(x=170,y=55,width=180,height=22)
        cartclearbtn=Button(cartwidgetframe,text="Очистить", command=self.clearcart,font=("times new roman",15),bg="#F39C12",fg="white",cursor="hand2").place(x=360,y=55,width=110,height=22)

        # рамка чек клиента
        clientcheckframe = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        clientcheckframe.place(x=920, y=110, width=420, height=455)
        clientchecklbl = Label(clientcheckframe, text="Чек клиента",font=("times new roman", 20), bg="#D4AC0D", fg="white",bd=3, relief=RIDGE).pack(side=TOP, fill=X)

        yscroll=Scrollbar(clientcheckframe,orient=VERTICAL)
        yscroll.pack(side=RIGHT,fill=Y)

        self.clientchecktxt=Text(clientcheckframe,yscrollcommand=yscroll.set)
        self.clientchecktxt.pack(fill=BOTH,expand=1)
        yscroll.config(command=self.clientchecktxt.yview)

        clientcheckmenuframe = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        clientcheckmenuframe .place(x=920, y=565, width=420, height=115)

        self.clientcheckamountlbl = Label(clientcheckmenuframe, text="Сумма чека \n [0]", font=("times new roman", 14, "bold"), bg="#D4AC0D",fg="white")
        self.clientcheckamountlbl.place(x=5, y=5,width=110,height=50)
        self.clientcheckdiscountlbl = Label(clientcheckmenuframe, text="Скидка \n [5%]",font=("times new roman", 14, "bold"), bg="#D4AC0D", fg="white")
        self.clientcheckdiscountlbl.place(x=120, y=5, width=100, height=50)
        self.clientchecknetpaylbl = Label(clientcheckmenuframe, text="Чистая заработная\nплата [0]",font=("times new roman", 14, "bold"), bg="#D4AC0D", fg="white")
        self.clientchecknetpaylbl.place(x=225, y=5, width=180, height=50)

        printclientckeckbtn= Button(clientcheckmenuframe, text="Печать", command=self.printthecheck,cursor="hand2", font=("times new roman", 14, "bold"), bg="#2C3E50",fg="white")
        printclientckeckbtn.place(x=5, y=60, width=110,height=45)
        clearclientckeckbtn = Button(clientcheckmenuframe, text="Очистить", command=self.clearallincart,cursor="hand2",font=("times new roman", 14, "bold"), bg="#2C3E50", fg="white")
        clearclientckeckbtn.place(x=120, y=60, width=100, height=45)
        saveclientckeckbtn = Button(clientcheckmenuframe, text="Сохраните чек", command=self.savecheck,cursor="hand2",font=("times new roman", 14, "bold"), bg="#2C3E50", fg="white")
        saveclientckeckbtn.place(x=225, y=60, width=180, height=45)

        # нижний колонтитул
        footerlbl = Label(self.root,text="Система управления супермаркетом ioitms | Copyright © 2023",font=("times new roman", 10), bg="#2C3E50", fg="white").pack(side=BOTTOM, fill=X)

        self.displai()
        self.dateandtime()

        # функции
    def getinput(self,nbr):
        xnbr=self.calculatorinput.get()+str(nbr)
        self.calculatorinput.set(xnbr)

        #очистить данные в калькуляторе
    def clearcalc(self):
        self.calculatorinput.set('')

        #результаты калькулятора
    def results(self):
        result=self.calculatorinput.get()
        self.calculatorinput.set(eval(result))

        # отображать данные
    def displai(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            # self.bproducttable = ttk.Treeview(bproducttableframe, columns=("pid", "name", "price", "quantity",
            # "availability"), yscrollcommand=yscroll.set,xscrollcommand=xscroll.set)
            cur.execute("Select pid, name, price, quantity,availability from Products where availability='Доступный'")
            rows = cur.fetchall()
            self.bproducttable.delete(*self.bproducttable.get_children())
            for row in rows:
                self.bproducttable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        # функция поиска
    def search(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            if self.bproductsearch.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute(
                    "Select pid, name, price, quantity,availability from Products where name LIKE '%" + self.bproductsearch.get() + "%' and availability='Доступный'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.bproducttable.delete(*self.bproducttable.get_children())
                    for row in rows:
                        self.bproducttable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "Data not found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        #получить данные из таблицы
    def getdata(self, ev):
        f = self.bproducttable.focus()
        content = (self.bproducttable.item(f))
        row = content['values']
        self.bproductid.set(row[0])
        self.bproductname.set(row[1])
        self.bproductprice.set(row[2])
        self.cartproductavailabilitylbl.config(text=f"В наличии [{str(row[3])}]")
        self.instock.set(row[3])
        self.bproductquantity.set('1')

    # получить данные корзины
    def getcarttdata(self, ev):
        f = self.carttable.focus()
        content = (self.carttable.item(f))
        row = content['values']
        self.bproductid.set(row[0])
        self.bproductname.set(row[1])
        self.bproductprice.set(row[2])
        self.bproductquantity.set(row[3])
        self.cartproductavailabilitylbl.config(text=f"В наличии [{str(row[4])}]")
        self.instock.set(row[4])

        # добавьте товар в корзину
    def addcart(self):
        if self.bproductid.get()=='':
            messagebox.showerror('Error','Select product  from the list',parent=self.root)
        elif int(self.bproductquantity.get()) > int(self.instock.get()):
            messagebox.showerror('Error', 'We dont have enough quantity', parent=self.root)
        elif self.bproductquantity.get()=='':
            messagebox.showerror('Error','The quantity is required',parent=self.root)
        else:
            # calculateprice=int(self.bproductquantity.get())*float(self.bproductprice.get())
            # calculateprice=float(calculateprice)
            calculateprice=self.bproductprice.get()
            cartdata=[self.bproductid.get(),self.bproductname.get(),calculateprice,self.bproductquantity.get(),self.instock.get() ]
            #Cart update
            present = 'no'
            indx = 0
            for row in self.cartlist:
                if self.bproductid.get() == row[0]:
                    present = 'yes'
                    break
                indx += 1
            if present=='yes':
                op=messagebox.askyesno('Confirm','Product already exist \n Click Yes to update product or No to remove the product')
                if op==True:
                    if self.bproductquantity.get()=="0":
                        self.cartlist.pop(indx)
                    else:
                        # self.cartlist[indx][2]=calculateprice
                        self.cartlist[indx][3] =self.bproductquantity.get()
            else:
                self.cartlist.append(cartdata)
            self.cartdisplai()
            self.updatecheck()

        # обновить чек
    def updatecheck(self):
        self.checkamount=0
        self.checknetpay=0
        self.checkdiscount=0
        for row in self.cartlist:
            self.checkamount=self.checkamount+(float(row[2])*int(row[3]))

        self.checkdiscount=(self.checkamount*5)/100
        self.checknetpay =self.checkamount-self.checkdiscount

        self.clientcheckamountlbl.config(text=f'Сумма чека\n{str(self.checkamount)}')
        self.clientchecknetpaylbl.config(text=f'Чистая заработная\nплата {str(self.checknetpay)}')
        self.cartframelbl.config(text=f'Корзина \t Всего товаров: [{str(len(self.cartlist))}]')

    # показать корзину
    def cartdisplai(self):
        try:
            self.carttable.delete(*self.carttable.get_children())
            for row in self.cartlist:
                self.carttable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # сохранить чек
    def savecheck(self):
        if self.clientname.get() == '' or self.clientcontact.get() == '':
            messagebox.showerror('Error', 'Clients name and contact are requires', parent=self.root)
        elif len(self.cartlist) == 0:
            messagebox.showerror('Error', 'Select the products from the cart list ', parent=self.root)
        else:
            #верхняя часть чека
            self.checktoppart()
            #средняя часть чека
            self.checkmiddlepart()
            #нижняя часть чека
            self.checkbottompart()


            fp = (open(f'Checks/{str(self.checkinvoice)}.txt', 'w'))
            fp.write(self.clientchecktxt.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', 'Check saved', parent=self.root)
            self.printcheck = 1

    # верхняя часть чека
    def checktoppart(self):
        self.checkinvoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        checktopparttxt = f'''
\t\t ioitms Supermarket
Phone No. 89156******,Kigali-250789
{str("=" * 47)}
Client name: {self.clientname.get()}
Phone number: {self.clientcontact.get()}
Check Number: {str(self.checkinvoice)} \t\t\t Date: {str(time.strftime("%d-%m-%Y"))}
{str("=" * 47)}
Product name\t\tQuantity\t\tPrice(Rwf) 
{str("=" * 47)}        
        '''
        self.clientchecktxt.delete('1.0', END)
        self.clientchecktxt.insert('1.0', checktopparttxt)

    # нижняя часть чека
    def checkbottompart(self):
        checkbottomparttxt = f'''
{str("=" * 47)}
check amount:\t\t\t{self.checkamount}Rwf
Discount:\t\t\t{self.checkdiscount}Rwf
Net pay:\t\t\t{self.checknetpay}Rwf
{str("=" * 47)}\n
\tThank you for shopping with us!!
        '''
        self.clientchecktxt.insert(END, checkbottomparttxt)

        #средняя часть чека
    def checkmiddlepart(self):
        conn = sqlite3.connect(database=r'ioitms.db')
        cur = conn.cursor()
        try:
            for row in self.cartlist:
                pid = row[0]
                proname = row[1]
                proquantity = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    availability = 'Недоступен'
                if int(row[3]) != int(row[4]):
                    availability = 'Доступный'

                proprice = float(row[2]) * int(row[3])
                proprice = str(proprice)
                self.clientchecktxt.insert(END, "\n " + proname + "\t\t" + row[3] + "\t\t" + proprice)
                # update Products table
                cur.execute('Update Products set  quantity=?, availability=?  where pid=?', (
                    proquantity,
                    availability,
                    pid
                ))
                conn.commit()
            conn.close()
            self.displai()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # функция очистки корзины
    def clearcart(self):
        self.bproductid.set('')
        self.bproductname.set('')
        self.bproductprice.set('')
        self.bproductquantity.set('')
        self.cartproductavailabilitylbl.config(text=f"В наличии []")
        self.instock.set('')

    # функция для очистки всего в корзине
    def clearallincart(self):
        self.printcheck == 0
        del self.cartlist[:]
        self.clientname.set('')
        self.clientcontact.set('')
        self.clientchecktxt.delete('1.0',END)
        self.cartframelbl.config(text=f'Корзина \t Всего товара: [0]')
        self.clearcart()
        self.displai()
        self.cartdisplai()

    # функция для отображения даты и времени
    def dateandtime(self):
        btime=time.strftime("%I:%M:%S")
        bdate=time.strftime("%d-%m-%Y")
        self.bclocklbl.config(text=f"Универсальный магазин в вашем районе\t\t Дата: {str(bdate)}\t\t Время: {str(btime)}")
        self.bclocklbl.after(200,self.dateandtime)

    # распечатать чек функция
    def printthecheck(self):
        if self.printcheck==1:
            messagebox.showinfo('Print',"Please wait while we are printing the check",parent=self.root)
            printedfile=tempfile.mktemp('.txt')
            open(printedfile,'w').write(self.clientchecktxt.get('1.0',END))
            os.startfile(printedfile,'print')
        else:
            messagebox.showerror('Error',"Please generate the check first",parent=self.root)

    #функция выхода
    def logout(self):
        self.root.destroy()
        os.system("python Login.py")

if __name__ == "__main__":
    root = Tk()
    obj = bil(root)
    root.mainloop()
