from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import os
import sqlite3
class ab:
    #о программном фрейме
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x500+220+130")
        self.root.title("Система управления супермаркетом")
        self.root.config(bg="#935116")
        self.root.focus_force()
        infostitlelbl = Label(self.root, text="Информация о программе", font=("times new roman", 20), bg="#D4AC0D",fg="#2C3E50",bd=3,relief=RIDGE).place(x=10, y=20, width=1220, height=40)

    #объяснение на английском языке
        infostitleenlbl = Label(self.root, text="Сохранить-The button used to add\n"
                                           "Обновить-The button used to update\n"
                                           "Удалить-The button used to delete\n"
                                           "Очистить-The button used to empty or clear enties\n"
                                           "Добавить в корзину-The button used to add products into the cart\n"
                                           "Поиск-The button used to search\n"
                                           "Печать-The button used to print the check\n"
                                           "сохранить чек-The button used to save the receipts\n\n"
                                           "When logging in the username is the user id \n"
                                           "if the user doesn't remember the pass word \n"
                                           "he need to enter his user name and then \n"
                                           "click on forgot password in order to receive the code \n"
                                           "on his email which will allow him to reset the password"
                                           ,
                           font=("times new roman", 14), bg="#D4AC0D",fg="#1C2833",bd=3,relief=RIDGE,justify="left").place(x=10, y=80, width=530, height=400)

    #объяснение на русском языке
        infostitlerulbl = Label(self.root, text="Сохранить - кнопка, используемая для добавления\n"
                                           "Обновить - кнопка, используемая для обновления\n"
                                           "Удалить - кнопка, используемая для удаления\n"
                                           "Очистить - кнопка, используемая для очистки элементов\n"
                                           "Добавить в корзину - кнопка, используемая для добавления товаров в корзину\n"
                                           "Поиск - кнопка, используемая для поиска\n"
                                           "Печать - кнопка, используемая для печати чека\n"
                                           "сохранить чек - кнопка, используемая для сохранения квитанций\n\n"
                                           "При входе в систему имя пользователя является идентификатором пользователя \n"
                                           "если пользователь не помнит пароль \n"
                                           "ему нужно ввести свое имя пользователя, а затем \n"
                                           "нажмите на забытый пароль, чтобы получить код \n"
                                           "на его электронную почту, которая позволит ему сбросить пароль"
                                           ,
                           font=("times new roman", 14), bg="#D4AC0D",fg="#1C2833",bd=3,relief=RIDGE,justify="left").place(x=560, y=80, width=670, height=400)

if __name__ == "__main__":
    root = Tk()
    obj = ab(root)
    root.mainloop()