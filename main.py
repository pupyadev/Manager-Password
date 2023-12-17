from PIL import ImageTk, Image
from tkinter import messagebox
import customtkinter as CTk
import sqlite3

db = sqlite3.connect("password_database.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS passwords (name text, login text, password text)")
db.commit()

CTk.set_default_color_theme("green")
app = CTk.CTk()
app.title("Manager Password")
app.resizable(width=False, height=False)
app.geometry("350x445")
app.iconbitmap("icon.ico")

#----------Основная логика-----------

#--Добавляем картику
image = Image.open("photo.png")
img = CTk.CTkImage(dark_image=image, size=(300, 143))
img_stack_app = CTk.CTkLabel(app, text="", image=img)
img_stack_app.place(x=25, y=7)

#--Кнопки
btn_add_password = CTk.CTkButton(app, text="Add Password", width=321, corner_radius=20, command=lambda: app_close())
btn_add_password.place(x=15, y=156)
btn_app_ok = CTk.CTkButton(app, text="Ok", width=321, corner_radius=20, command=lambda: add_password(input_name_password.get(), input_login_password.get(), input_password.get())) #.place(x=15, y=250)
btn_app_ok.place_forget()
btn_app_cancel = CTk.CTkButton(app, text="Cancel", width=321, corner_radius=20, command=lambda: show_app()) #.place(x=15, y=283)
btn_app_cancel.place_forget()

#--Вводы текста
input_name_password = CTk.CTkEntry(app, placeholder_text="Name", width=300, corner_radius=20) #.place(x=25, y=57)
input_name_password.place_forget()
input_login_password = CTk.CTkEntry(app, placeholder_text="Login", width=300, corner_radius=20) #.place(x=25, y=127)
input_login_password.place_forget()
input_password = CTk.CTkEntry(app, placeholder_text="Password", width=300, corner_radius=20) #.place(x=25, y=197)
input_password.place_forget()

#--Основная таблица
password_bar = CTk.CTkScrollableFrame(app, width=285, corner_radius=20)
password_bar.place(x=15, y=193)

#--Все функции

#-Функция отображения паролей на таблице
def refresh_table():
    for widget in password_bar.winfo_children():
        widget.destroy()

    for passwords in cursor.execute("SELECT * FROM passwords"):
        #Переменные
        name = passwords[0]
        login = passwords[1]
        password = passwords[2]

        mus_btn = CTk.CTkButton(password_bar, text="DELETE", corner_radius=20, text_color="black", fg_color="orange", hover_color="red", width=300, height=20, command=lambda n=name: delete_password(n))
        mus_btn.pack()
        name_text = CTk.CTkLabel(password_bar, text=f"Name:  {name}")
        name_text.pack()
        login_text = CTk.CTkLabel(password_bar, text=f"Login:  {login}")
        login_text.pack()
        password_text = CTk.CTkLabel(password_bar, text=f"Password:  {password}")
        password_text.pack()

#-Функция удаления пароля
def delete_password(name):
    answer = messagebox.askyesno("Предупреждение", "Вы точно хотите удалить данный пароль?")
    if answer:
        cursor.execute(f"DELETE FROM passwords WHERE name = ?", (name,))
        db.commit()

        refresh_table()

#-Функция стерания все с главного окна переходя к другому
def app_close():
    img_stack_app.place_forget()
    btn_add_password.place_forget()
    password_bar.place_forget()

    btn_app_ok.place(x=15, y=280)
    btn_app_cancel.place(x=15, y=313)
    input_name_password.place(x=25, y=57)
    input_login_password.place(x=25, y=127)
    input_password.place(x=25, y=197)

def show_app():
    img_stack_app.place(x=25, y=7)
    btn_add_password.place(x=15, y=156)
    password_bar.place(x=15, y=193)

    btn_app_ok.place_forget()
    btn_app_cancel.place_forget()
    input_name_password.place_forget()
    input_login_password.place_forget()
    input_password.place_forget()

    refresh_table()

#-Функция добавления пароля
def add_password(name, login, password):
    #Проверка на пустые поля
    if name == "":
        messagebox.showerror("Ошибка", "Введите текст в пустые поля")
    elif login == "":
        messagebox.showerror("Ошибка", "Введите текст в пустые поля")
    elif password == "":
        messagebox.showerror("Ошибка", "Введите текст в пустые поля")
    else:
        #Проверка на то что у нас есть такой пароль с таким же названием
        if cursor.execute("SELECT * FROM passwords WHERE name = ?", (name, )).fetchone() is None:
            cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (name, login, password))
            db.commit()
            messagebox.showinfo("Инфо", "Пароль был добавлен")
        else:
            messagebox.showerror("Ошибка", "Придумайте новое название пароля")

refresh_table()

app.mainloop()