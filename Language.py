from tkinter import *
from tkinter import ttk , messagebox
import sqlite3
window = Tk()
window.title("Language Academy | Designed By Fatemeh Baghaei")
window.geometry("800x800")
window.resizable(False, False)
window.config(background="pink")
conn = sqlite3.connect("baghaei.db")
cursor = conn.cursor()

def create_user():
    def save():
        nameE = entry_name.get()
        phoneE = entry_phone.get()
        if nameE and phoneE:
            cursor.execute("INSERT INTO Users (name , phone) VALUES (?,?)",
                           (nameE , phoneE))
            conn.commit()
            messagebox.showinfo("موفق","زبان آموز با موفقیت اضافه شد")
            user_window.destroy()
        else:
            messagebox.showwarning( "خطا" , "لطفا همه فیلدها را پر کنید")

    user_window = Toplevel(window, height=300, width=400 , bg ='pink')
    user_window.pack_propagate(False)
    (Label(user_window, text=" : نام و نام خانوادگی" , font=("Arial", 12), anchor="e", justify="right",background='pink')
     .pack(pady=20))

    entry_name = Entry(user_window)
    entry_name.pack(pady=20)

    (Label(user_window, text=" :شماره تماس", font=("Arial", 12), anchor="e", justify="right",background='pink')
     .pack(pady=20))

    entry_phone = Entry(user_window)
    entry_phone.pack(pady=20)

    (Button(user_window, text="ذخیره" , command=save,background='green')
     .pack(pady=20))

#********************************************************
userID=None
def signin():
    def searchDb():
        global userID
        phoneE = entry_user_phone.get()
        if phoneE:
            cursor.execute("SELECT userID from Users WHERE phone=?",(phoneE,))
            result=cursor.fetchone()
            if result:
                messagebox.showinfo("موفق","زبان آموز با موفقیت وارد شد.")
                userID=result[0]
                signin_user_window.place_forget()
            else:
                messagebox.showinfo("خطا", "شماره تلفن یافت نشد.")

    signin_user_window=Frame(window,bg="pink",width=400,height=400)
    signin_user_window.pack_propagate(False)
    signin_user_window.place(x=200,y=200)
    Label(signin_user_window, bg='pink',text="شماره تماس زبان آموز").pack(pady=5)
    entry_user_phone=Entry(signin_user_window)
    entry_user_phone.pack(pady=5)

    Button(signin_user_window,text="ورود",bg='green',command=searchDb).pack(pady=5)
    def cancel():
        signin_user_window.place_forget()

    Button(signin_user_window,text="انصراف",background='yellow',command=cancel).pack(pady=5)

#********************************************************

def delete_user():
    def removeDb():
        phoneE = entry_user_phone.get()
        if phoneE:
            cursor.execute("DELETE from Users WHERE phone=?", (phoneE,))
            conn.commit()
            if cursor.rowcount==0:
                messagebox.showwarning("خطا","زبان آموز با این شماره تلفن یافت نشد")
            else:
                messagebox.showinfo("موفق","زبا آموز با موفقیت حذف شد")

                delete_user_window.place_forget()

    delete_user_window = Frame(window, bg="pink", width=400, height=200)
    delete_user_window.pack_propagate(False)
    delete_user_window.place(x=200, y=200)

    Label(delete_user_window, text="شماره تلفن زبان آموز:" ,background='pink').pack(pady=5)
    entry_user_phone = Entry(delete_user_window)
    entry_user_phone.pack(pady=5)

    Button(delete_user_window, text="حذف" ,command=removeDb ,background='red').pack(pady=10)

    def cancel():
        delete_user_window.place_forget()

    Button(delete_user_window, text="انصراف",background='yellow', command=cancel).pack(pady=10)
#********************************************************
def edit_user():
    def update_user():
        phone_id=entry_phone_id.get()
        name=entry_name.get()
        phone=entry_phone.get()
        if phone_id and name and phone:
            cursor.execute("UPDATE Users SET name=?, phone=? WHERE phone=?" ,(name,phone,phone_id))
            conn.commit()
            if cursor.rowcount==0:
                messagebox.showwarning("خطا", "زبان آموز با این شماره تلفن یافت نشد")
            else:
                messagebox.showinfo("موفق", "زبان آموز با موفقیت ویرایش شد")
                edit_user_window.destroy()

    edit_user_window=Toplevel(window , background='pink')
    edit_user_window.title("ویرایش زبان آموز")
    edit_user_window.geometry("300x300")

    Label(edit_user_window,text=":شماره تماس زبان آموز",background='pink').pack(pady=5)
    entry_phone_id=Entry(edit_user_window)
    entry_phone_id.pack(pady=5)
    Label(edit_user_window,text=":نام جدید",background='pink').pack(pady=5)
    entry_name=Entry(edit_user_window)
    entry_name.pack(pady=5)
    Label(edit_user_window, text=":شماره تماس جدید زبان آموز",background='pink').pack(pady=5)
    entry_phone = Entry(edit_user_window)
    entry_phone.pack(pady=5)
    Button(edit_user_window, text="ویرایش", command=update_user ,background='green').pack(pady=10)
 #********************************************************
def show_users():
    win = Toplevel(window, height=500, width=500 , bg ='pink')
    win.title("لیست زبان آموزان")
    win.geometry("500x400")

    tree = ttk.Treeview(win, columns=("id", "name", "phone"), show="headings")

    tree.heading("id", text="کد")
    tree.heading("name", text="نام")
    tree.heading("phone", text="شماره")

    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT userID,name,phone FROM Users")

    for row in cursor.fetchall():
        tree.insert("", END, values=row)
 #********************************************************
def search_user():
    win = Toplevel(window, height=300, width=400 , bg ='pink')
    win.geometry("300x200")

    Label(win, text="شماره تماس",background='pink').pack()

    ent = Entry(win)
    ent.pack()

    def search():

        cursor.execute(
            "SELECT name,phone FROM Users WHERE phone=?",
            (ent.get(),))

        row = cursor.fetchone()

        if row:
            messagebox.showinfo(
                "نتیجه",
                f"نام : {row[0]}\nشماره : {row[1]}"
            )
        else:
            messagebox.showwarning("خطا", "یافت نشد")

    Button(win, text="جستجو",background='yellow', command=search).pack()
 #*******************************************************
def report_users():
    cursor.execute("SELECT COUNT(*) FROM Users")

    count = cursor.fetchone()[0]

    messagebox.showinfo(
        "گزارش",
        f"تعداد زبان آموزان : {count}"
    )
#*********************************************
def create_leng():
    def save():
        nameA = entry_name.get()
        priceA = entry_phone.get()
        if nameA and priceA:
            cursor.execute("INSERT INTO Lang (name , price) VALUES (?,?)",
                           (nameA, priceA))
            conn.commit()
            messagebox.showinfo("موفق", "زبان با موفقیت اضافه شد")
            leng_window.destroy()
        else:
            messagebox.showwarning("خطا", "لطفا همه فیلدها را پر کنید")

    leng_window = Toplevel(window, height=300, width=400, bg='pink')
    leng_window.pack_propagate(False)
    (Label(leng_window, text=" : زبان", font=("Arial", 12), anchor="e", justify="right",
           background='pink')
     .pack(pady=20))

    entry_name = Entry(leng_window)
    entry_name.pack(pady=20)

    (Label(leng_window, text=" :قیمت دوره", font=("Arial", 12), anchor="e", justify="right", background='pink')
     .pack(pady=20))

    entry_phone = Entry(leng_window)
    entry_phone.pack(pady=20)

    (Button(leng_window, text="ذخیره", command=save, background='green')
     .pack(pady=20))

#********************************************************
def delete_leng():
    def removeDb():
        nameA = entry_leng_name.get()
        if nameA:
            cursor.execute("DELETE from Lang WHERE name=?", (nameA,))
            conn.commit()
            if cursor.rowcount==0:
                messagebox.showwarning("خطا","زبان  با این نام یافت نشد")
            else:
                messagebox.showinfo("موفق","زبان با موفقیت حذف شد")

                delete_leng_window.place_forget()

    delete_leng_window = Frame(window, bg="pink", width=400, height=200)
    delete_leng_window.pack_propagate(False)
    delete_leng_window.place(x=200, y=200)

    Label(delete_leng_window, text="نام زبان را وارد کنید:",background='pink').pack(pady=5)
    entry_leng_name = Entry(delete_leng_window)
    entry_leng_name.pack(pady=5)

    Button(delete_leng_window, text="حذف" ,command=removeDb,background='red').pack(pady=10)

    def cancel():
        delete_leng_window.place_forget()

    Button(delete_leng_window, text="انصراف" ,background='yellow', command=cancel).pack(pady=10)
#********************************************************
def edit_leng():
    def update_leng():
        name_id=entry_name_id.get()
        name = entry_name.get()
        price=entry_price.get()
        if name_id and price and name:
            cursor.execute("UPDATE Lang SET name=? , price=? WHERE name=?" ,(name,price,name_id))
            conn.commit()
            if cursor.rowcount==0:
                messagebox.showwarning("خطا", "زبان با این نام یافت نشد")
            else:
                messagebox.showinfo("موفق", "زبان با موفقیت ویرایش شد")
                edit_leng_window.destroy()

    edit_leng_window=Toplevel(window , background='pink')
    edit_leng_window.title("ویرایش زبان")
    edit_leng_window.geometry("300x300")
    Label(edit_leng_window,text=":زبان را وارد کنید",background='pink').pack(pady=5)
    entry_name_id=Entry(edit_leng_window)
    entry_name_id.pack(pady=5)
    Label(edit_leng_window,text=":نام جدید",background='pink').pack(pady=5)
    entry_name=Entry(edit_leng_window)
    entry_name.pack(pady=5)
    Label(edit_leng_window, text=":قیمت جدید دوره", background='pink').pack(pady=5)
    entry_price = Entry(edit_leng_window)
    entry_price.pack(pady=5)
    Button(edit_leng_window, text="ویرایش", command=update_leng ,background='green').pack(pady=10)

#********************************************************
def show_languages():
    win=Toplevel(window, background='pink')
    win.title("لیست زبان ها")
    win.geometry("500x400")

    tree=ttk.Treeview(win,columns=("id","name","price"),show="headings")

    tree.heading("id",text="کد")
    tree.heading("name",text="نام زبان")
    tree.heading("price",text="شهریه")

    tree.pack(fill=BOTH,expand=True)

    cursor.execute("SELECT langID,name,price FROM Lang")

    for row in cursor.fetchall():
        tree.insert("",END,values=row)
#********************************************************
def add_invoice():
    invoice_window = Toplevel(window, background='pink')
    invoice_window.title("ایجاد فاکتور جدید")
    invoice_window.geometry("500x500")

    cursor.execute("SELECT name, price FROM Lang")
    menu = cursor.fetchall()
    leng_price = {name: price for name, price in menu}

    Label(invoice_window, text=":انتخاب زبان", background='pink').pack(pady=5)
    combo_leng = ttk.Combobox(invoice_window, values=list(leng_price.keys()))
    combo_leng.pack(pady=5)

    Label(invoice_window, text=":قیمت زبان", background='pink').pack(pady=5)
    label_price = Label(invoice_window, text="0", background='pink')  # مقدار اولیه
    label_price.pack(pady=5)

    def update_price(event):
        leng_name = combo_leng.get()
        if leng_name in leng_price:
            label_price.config(text=f"{leng_price[leng_name]}")

    combo_leng.bind("<<ComboboxSelected>>", update_price)
    def remove_item():
        selected =tree.selection()
        if not selected:
            messagebox.showwarning("خطا","لطفا یک سطر انتخاب کنید")
            return
        item = selected[0]
        values=tree.item(item, 'values')
        value_cast=(values[0],int(values[1]),float(values[2]))
        tree.delete(item)
        invoice_items.remove(value_cast)
        total = sum(item[2] for item in invoice_items)
        totallbl.configure(text=total)

    def add_to_list():
        lang_name =combo_leng.get()
        quantity=int(entry_quantity.get())
        price=leng_price[lang_name]
        total_price=quantity * price
        invoice_items.append((lang_name,quantity,total_price))
        total =sum(item[2]for item in invoice_items)
        totallbl.configure(text=total)
        tree.insert('',END,values=[lang_name,quantity,total_price])

    def get_langID(lang):
         cursor.execute("SELECT langid FROM lang WHERE name=?",(lang,))
         menu1=cursor.fetchone()
         return  menu1[0]

    def submit_invoice():
        total =totallbl.cget("text")
        messagebox.showinfo("فاکتور",f"قیمت نهایی{total}")
        print("userID:", userID)
        cursor.execute("INSERT INTO Invoices (userID,total_price) VALUES (?,?)",(userID ,total))
        invoice_id=cursor.lastrowid

        for item in invoice_items:
            langid= get_langID(item[0])
            cursor.execute("INSERT INTO Invoice_item  (invoice_id ,lengID,quantity,price) VALUES (?,?,?,?)",(invoice_id,langid,item[1],item[2]))
            conn.commit()
            invoice_window.destroy()

    Label(invoice_window, text=":تعداد",background='pink').pack(pady=5)
    entry_quantity = Entry(invoice_window)
    entry_quantity.pack(pady=5)

    Button(invoice_window, text="افزودن فاکتور", background='green', command=add_to_list).pack(pady=6)
    f = Frame(invoice_window, width=500)
    f.pack(fill=BOTH, expand=1)
    f.grid_rowconfigure(0,weight=3)
    f.grid_rowconfigure(1,weight=1)
    columns=('langname','quantity','fee')
    tree=ttk.Treeview(f,columns=columns,show='headings')
    tree.heading('langname',text="نام زبان")
    tree.heading('quantity',text="تعداد")
    tree.heading('fee',text="قیمت")
    tree.grid(row=0,column=0,padx=10)

   # listbox = Listbox(f)
  #  listbox.pack(side=LEFT, fill=BOTH, expand=1, padx=10)
    f10=Frame(f,width=450)
    f10.grid(row=1,column=0,padx=10)

    rb=Button(f10,text="حذف",width=20,bg='red',command=remove_item)
    rb.grid(row=0,column=0,padx=10,sticky='snwe')
     # Button(f, text="حذف",bg='red',).pack(side=RIGHT, padx=1)
    Button(f10, text="ثبت فاکتور",width=20, background='green',command=submit_invoice).grid(row=0,column=1,padx=10)

    invoice_items=[]

    totallbl = Label(f10, text="--------------", background="gray")
    totallbl.grid(row=0,column=2,sticky='snwe',padx=10)
   # totallbl.pack(pady=20)

#********************************************************
def show_invoices():

        win = Toplevel(window)

        tree = ttk.Treeview(
            win,
            columns=("id", "user", "total"),
            show="headings"
        )

        tree.heading("id", text="شماره")

        tree.heading("user", text="کد زبان آموز")

        tree.heading("total", text="جمع")

        tree.pack(fill=BOTH, expand=True)

        cursor.execute(
            "SELECT invoicesID,userID,total_price FROM Invoices"
        )

        for row in cursor.fetchall():
            tree.insert("", END, values=row)

#****************************************************
def report_income():

    cursor.execute(
        "SELECT SUM(total_price) FROM Invoices"
    )

    total=cursor.fetchone()[0]

    if total==None:
        total=0

    messagebox.showinfo(
        "درآمد",
        f"کل درآمد : {total}"
    )
#**************************************
def add_teacher():

    def save():

        name = entry_name.get()
        phone = entry_phone.get()
        skill = entry_skill.get()

        if name and phone and skill:

            cursor.execute(
                "INSERT INTO Teachers(name,phone,skill) VALUES (?,?,?)",
                (name, phone, skill)
            )

            conn.commit()

            messagebox.showinfo(
                "موفق",
                "مدرس با موفقیت اضافه شد"
            )

            teacher_window.destroy()

        else:

            messagebox.showwarning(
                "خطا",
                "لطفا همه فیلدها را پر کنید"
            )

    teacher_window = Toplevel(window)
    teacher_window.title("افزودن مدرس")
    teacher_window.geometry("350x320")
    teacher_window.config(bg="pink")

    Label(
        teacher_window,
        text="نام و نام خانوادگی مدرس",
        bg="pink"
    ).pack(pady=5)

    entry_name = Entry(teacher_window, width=30)
    entry_name.pack()

    Label(
        teacher_window,
        text="شماره تماس",
        bg="pink"
    ).pack(pady=5)

    entry_phone = Entry(teacher_window, width=30)
    entry_phone.pack()

    Label(
        teacher_window,
        text="تخصص مدرس",
        bg="pink"
    ).pack(pady=5)

    entry_skill = Entry(teacher_window, width=30)
    entry_skill.pack()

    Button(
        teacher_window,
        text="ذخیره",
        bg="green",
        width=15,
        command=save
    ).pack(pady=20)
#**************************************************
def show_teachers():
    win = Toplevel(window, bg="pink")
    win.title("لیست مدرس ها")
    win.geometry("600x400")

    tree = ttk.Treeview(
        win,
        columns=("id", "name", "phone", "skill"),
        show="headings"
    )

    tree.heading("id", text="کد")
    tree.heading("name", text="نام مدرس")
    tree.heading("phone", text="شماره تماس")
    tree.heading("skill", text="تخصص")

    tree.column("id", width=60)
    tree.column("name", width=180)
    tree.column("phone", width=150)
    tree.column("skill", width=150)

    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT teacherID,name,phone,skill FROM Teachers")

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)
#************************************************
def edit_teacher():

    def update_teacher():

        phone_id = entry_phone_id.get()
        name = entry_name.get()
        phone = entry_phone.get()
        skill = entry_skill.get()

        if phone_id and name and phone and skill:

            cursor.execute(
                "UPDATE Teachers SET name=?, phone=?, skill=? WHERE phone=?",
                (name, phone, skill, phone_id)
            )

            conn.commit()

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "خطا",
                    "مدرس با این شماره پیدا نشد"
                )

            else:

                messagebox.showinfo(
                    "موفق",
                    "مدرس با موفقیت ویرایش شد"
                )

                teacher_window.destroy()

        else:

            messagebox.showwarning(
                "خطا",
                "همه فیلدها را پر کنید"
            )

    teacher_window = Toplevel(window)
    teacher_window.title("ویرایش مدرس")
    teacher_window.geometry("350x350")
    teacher_window.config(bg="pink")

    Label(teacher_window, text="شماره تماس مدرس", bg="pink").pack(pady=5)
    entry_phone_id = Entry(teacher_window)
    entry_phone_id.pack(pady=5)

    Label(teacher_window, text="نام جدید", bg="pink").pack(pady=5)
    entry_name = Entry(teacher_window)
    entry_name.pack(pady=5)

    Label(teacher_window, text="شماره تماس جدید", bg="pink").pack(pady=5)
    entry_phone = Entry(teacher_window)
    entry_phone.pack(pady=5)

    Label(teacher_window, text="تخصص جدید", bg="pink").pack(pady=5)
    entry_skill = Entry(teacher_window)
    entry_skill.pack(pady=5)

    Button(
        teacher_window,
        text="ویرایش",
        bg="green",
        command=update_teacher
    ).pack(pady=15)
#**********************************************************
def delete_teacher():

    def removeDb():

        phone = entry_phone.get()

        if phone:

            cursor.execute(
                "DELETE FROM Teachers WHERE phone=?",
                (phone,)
            )

            conn.commit()

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "خطا",
                    "مدرسی با این شماره پیدا نشد"
                )

            else:

                messagebox.showinfo(
                    "موفق",
                    "مدرس با موفقیت حذف شد"
                )

                teacher_window.destroy()

        else:

            messagebox.showwarning(
                "خطا",
                "شماره تماس را وارد کنید"
            )

    teacher_window = Toplevel(window)
    teacher_window.title("حذف مدرس")
    teacher_window.geometry("300x180")
    teacher_window.config(bg="pink")

    Label(
        teacher_window,
        text="شماره تماس مدرس",
        bg="pink"
    ).pack(pady=10)

    entry_phone = Entry(teacher_window)
    entry_phone.pack(pady=5)

    Button(
        teacher_window,
        text="حذف",
        bg="red",
        fg="white",
        command=removeDb
    ).pack(pady=15)
#*************************************
def show_courses():

    win = Toplevel(window)
    win.title("لیست دوره ها")
    win.geometry("700x400")
    win.config(bg="pink")

    tree = ttk.Treeview(
        win,
        columns=("id","name","lang","teacher","sessions","price"),
        show="headings"
    )

    tree.heading("id",text="کد")
    tree.heading("name",text="نام دوره")
    tree.heading("lang",text="کد زبان")
    tree.heading("teacher",text="کد مدرس")
    tree.heading("sessions",text="تعداد جلسات")
    tree.heading("price",text="شهریه")

    tree.pack(fill=BOTH,expand=True)

    cursor.execute("""
        SELECT courseID,name,langID,teacherID,sessions,price
        FROM Courses
    """)

    rows=cursor.fetchall()

    for row in rows:
        tree.insert("",END,values=row)
#*********************************************
def add_course():

    win = Toplevel(window)
    win.title("افزودن دوره")
    win.geometry("400x400")
    win.config(bg="pink")

    Label(win,text="نام دوره",bg="pink").pack(pady=5)
    entry_name = Entry(win)
    entry_name.pack()

    cursor.execute("SELECT name FROM Lang")
    langs = [row[0] for row in cursor.fetchall()]

    Label(win,text="زبان",bg="pink").pack(pady=5)
    combo_lang = ttk.Combobox(win, values=langs)
    combo_lang.pack()

    cursor.execute("SELECT name FROM Teachers")
    teachers = [row[0] for row in cursor.fetchall()]

    Label(win,text="مدرس",bg="pink").pack(pady=5)
    combo_teacher = ttk.Combobox(win, values=teachers)
    combo_teacher.pack()

    Label(win,text="تعداد جلسات",bg="pink").pack(pady=5)
    entry_sessions = Entry(win)
    entry_sessions.pack()

    Label(win,text="شهریه",bg="pink").pack(pady=5)
    entry_price = Entry(win)
    entry_price.pack()

    def save():

        cursor.execute(
            "SELECT langID FROM Lang WHERE name=?",
            (combo_lang.get(),)
        )
        lang = cursor.fetchone()

        cursor.execute(
            "SELECT teacherID FROM Teachers WHERE name=?",
            (combo_teacher.get(),)
        )
        teacher = cursor.fetchone()

        if not lang or not teacher:
            messagebox.showwarning(
                "خطا",
                "زبان یا مدرس انتخاب نشده است"
            )
            return

        cursor.execute(
            """INSERT INTO Courses
            (name,langID,teacherID,sessions,price)
            VALUES (?,?,?,?,?)""",
            (
                entry_name.get(),
                lang[0],
                teacher[0],
                entry_sessions.get(),
                entry_price.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "موفق",
            "دوره با موفقیت اضافه شد"
        )

        win.destroy()

    Button(
        win,
        text="ذخیره",
        bg="green",
        command=save
    ).pack(pady=15)
#**************************************************
def add_enrollment():

    win = Toplevel(window)
    win.title("ثبت نام زبان آموز")
    win.geometry("400x350")
    win.config(bg="pink")

    cursor.execute("SELECT name FROM Users")
    users = [row[0] for row in cursor.fetchall()]

    Label(win,text="زبان آموز",bg="pink").pack(pady=5)

    combo_user = ttk.Combobox(win,values=users)
    combo_user.pack()

    cursor.execute("SELECT name FROM Courses")
    courses = [row[0] for row in cursor.fetchall()]

    Label(win,text="دوره",bg="pink").pack(pady=5)

    combo_course = ttk.Combobox(win,values=courses)
    combo_course.pack()

    Label(win,text="تاریخ ثبت نام",bg="pink").pack(pady=5)

    entry_date = Entry(win)
    entry_date.pack()

    Label(win,text="وضعیت",bg="pink").pack(pady=5)

    combo_status = ttk.Combobox(
        win,
        values=["فعال","لغو شده","پایان یافته"]
    )

    combo_status.pack()

    def save():

        cursor.execute(
            "SELECT userID FROM Users WHERE name=?",
            (combo_user.get(),)
        )

        user = cursor.fetchone()

        cursor.execute(
            "SELECT courseID FROM Courses WHERE name=?",
            (combo_course.get(),)
        )

        course = cursor.fetchone()

        if not user or not course:

            messagebox.showwarning(
                "خطا",
                "اطلاعات صحیح نیست"
            )

            return

        cursor.execute(
            """
            INSERT INTO Enrollments
            (userID,courseID,enrollDate,status)
            VALUES (?,?,?,?)
            """,
            (
                user[0],
                course[0],
                entry_date.get(),
                combo_status.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "موفق",
            "ثبت نام انجام شد"
        )

        win.destroy()

    Button(
        win,
        text="ثبت نام",
        bg="green",
        command=save
    ).pack(pady=15)
#**********************************************
def add_enroll():

    win = Toplevel(window)
    win.title("ثبت نام زبان آموز")
    win.geometry("400x400")
    win.config(bg="pink")

    cursor.execute("SELECT name FROM Users")
    users = [row[0] for row in cursor.fetchall()]

    Label(win, text="زبان آموز", bg="pink").pack(pady=5)

    combo_user = ttk.Combobox(win, values=users)
    combo_user.pack()

    cursor.execute("SELECT name FROM Courses")
    courses = [row[0] for row in cursor.fetchall()]

    Label(win, text="دوره", bg="pink").pack(pady=5)

    combo_course = ttk.Combobox(win, values=courses)
    combo_course.pack()

    Label(win, text="تاریخ ثبت نام", bg="pink").pack(pady=5)

    entry_date = Entry(win)
    entry_date.pack()

    Label(win, text="وضعیت", bg="pink").pack(pady=5)

    combo_status = ttk.Combobox(
        win,
        values=["فعال", "لغو شده", "پایان یافته"]
    )
    combo_status.pack()

    def save():

        cursor.execute(
            "SELECT userID FROM Users WHERE name=?",
            (combo_user.get(),)
        )
        user = cursor.fetchone()

        cursor.execute(
            "SELECT courseID FROM Courses WHERE name=?",
            (combo_course.get(),)
        )
        course = cursor.fetchone()

        if not user or not course:

            messagebox.showwarning(
                "خطا",
                "لطفاً زبان آموز و دوره را انتخاب کنید"
            )
            return

        cursor.execute(
            """
            INSERT INTO Enrollments
            (userID, courseID, date, status)
            VALUES (?,?,?,?)
            """,
            (
                user[0],
                course[0],
                entry_date.get(),
                combo_status.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "موفق",
            "ثبت نام با موفقیت انجام شد"
        )

        win.destroy()

    Button(
        win,
        text="ثبت نام",
        bg="green",
        command=save
    ).pack(pady=15)
#********************************************
def show_enrollments():

    win = Toplevel(window)
    win.title("لیست ثبت نام ها")
    win.geometry("800x400")
    win.config(bg="pink")

    tree = ttk.Treeview(
        win,
        columns=("id","user","course","date","status"),
        show="headings"
    )

    tree.heading("id",text="کد")
    tree.heading("user",text="زبان آموز")
    tree.heading("course",text="دوره")
    tree.heading("date",text="تاریخ ثبت نام")
    tree.heading("status",text="وضعیت")

    tree.column("id",width=60)
    tree.column("user",width=180)
    tree.column("course",width=180)
    tree.column("date",width=150)
    tree.column("status",width=120)

    tree.pack(fill=BOTH,expand=True)

    cursor.execute("""
        SELECT
            Enrollments.enrollID,
            Users.name,
            Courses.name,
            Enrollments.date,
            Enrollments.status
        FROM Enrollments
        INNER JOIN Users
            ON Enrollments.userID = Users.userID
        INNER JOIN Courses
            ON Enrollments.courseID = Courses.courseID
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("",END,values=row)
#***************************************************
def edit_enroll():

    def update():

        cursor.execute(
            "SELECT userID FROM Users WHERE name=?",
            (combo_user.get(),)
        )
        user=cursor.fetchone()

        cursor.execute(
            "SELECT courseID FROM Courses WHERE name=?",
            (combo_course.get(),)
        )
        course=cursor.fetchone()

        cursor.execute(
            """
            UPDATE Enrollments
            SET
            userID=?,
            courseID=?,
            date=?,
            status=?
            WHERE enrollID=?
            """,
            (
                user[0],
                course[0],
                entry_date.get(),
                combo_status.get(),
                entry_id.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "موفق",
            "ثبت نام ویرایش شد"
        )

        win.destroy()

    win=Toplevel(window)
    win.geometry("350x420")
    win.config(bg="pink")

    Label(win,text="کد ثبت نام",bg="pink").pack()
    entry_id=Entry(win)
    entry_id.pack()

    cursor.execute("SELECT name FROM Users")
    users=[r[0] for r in cursor.fetchall()]

    Label(win,text="زبان آموز",bg="pink").pack()
    combo_user=ttk.Combobox(win,values=users)
    combo_user.pack()

    cursor.execute("SELECT name FROM Courses")
    courses=[r[0] for r in cursor.fetchall()]

    Label(win,text="دوره",bg="pink").pack()
    combo_course=ttk.Combobox(win,values=courses)
    combo_course.pack()

    Label(win,text="تاریخ",bg="pink").pack()
    entry_date=Entry(win)
    entry_date.pack()

    Label(win,text="وضعیت",bg="pink").pack()

    combo_status=ttk.Combobox(
        win,
        values=["فعال","لغو شده","پایان یافته"]
    )
    combo_status.pack()

    Button(
        win,
        text="ویرایش",
        bg="green",
        command=update
    ).pack(pady=15)
#****************************************************
def delete_enroll():

    def remove():

        if entry_id.get():

            cursor.execute(
                "DELETE FROM Enrollments WHERE enrollID=?",
                (entry_id.get(),)
            )

            conn.commit()

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "خطا",
                    "ثبت نام پیدا نشد"
                )

            else:

                messagebox.showinfo(
                    "موفق",
                    "ثبت نام حذف شد"
                )

                win.destroy()

    win = Toplevel(window)
    win.title("حذف ثبت نام")
    win.geometry("300x200")
    win.config(bg="pink")

    Label(win,text="کد ثبت نام",bg="pink").pack(pady=10)

    entry_id=Entry(win)
    entry_id.pack()

    Button(
        win,
        text="حذف",
        bg="red",
        command=remove
    ).pack(pady=15)
#****************************************************
def search_enroll():

    win = Toplevel(window)
    win.title("جستجوی ثبت نام")
    win.geometry("350x220")
    win.config(bg="pink")

    Label(
        win,
        text="کد ثبت نام",
        bg="pink"
    ).pack(pady=10)

    entry_id = Entry(win)
    entry_id.pack(pady=5)

    def search():

        cursor.execute("""
            SELECT
                Users.name,
                Courses.name,
                Enrollments.date,
                Enrollments.status
            FROM Enrollments
            JOIN Users
            ON Enrollments.userID=Users.userID
            JOIN Courses
            ON Enrollments.courseID=Courses.courseID
            WHERE Enrollments.enrollID=?
        """,(entry_id.get(),))

        row = cursor.fetchone()

        if row:

            messagebox.showinfo(
                "نتیجه جستجو",
                f"""زبان آموز : {row[0]}

دوره : {row[1]}

تاریخ ثبت نام : {row[2]}

وضعیت : {row[3]}"""
            )

        else:

            messagebox.showwarning(
                "خطا",
                "ثبت نام پیدا نشد"
            )

    Button(
        win,
        text="جستجو",
        bg="green",
        command=search
    ).pack(pady=15)
#***************************************************
def report_enroll():

    cursor.execute("SELECT COUNT(*) FROM Enrollments")

    count = cursor.fetchone()[0]

    messagebox.showinfo(
        "گزارش ثبت نام",
        f"تعداد ثبت نام ها : {count}"
    )
#***************************************
def report_courses():

    cursor.execute("SELECT COUNT(*) FROM Courses")

    count = cursor.fetchone()[0]

    messagebox.showinfo(
        "گزارش دوره ها",
        f"تعداد دوره ها : {count}"
    )
#***********************************************
def delete_course():

    def remove():

        cursor.execute(
            "DELETE FROM Courses WHERE courseID=?",
            (entry_id.get(),)
        )

        conn.commit()

        if cursor.rowcount==0:

            messagebox.showwarning(
                "خطا",
                "دوره پیدا نشد"
            )

        else:

            messagebox.showinfo(
                "موفق",
                "دوره حذف شد"
            )

            win.destroy()

    win=Toplevel(window)
    win.geometry("300x180")
    win.config(bg="pink")

    Label(win,text="کد دوره",bg="pink").pack(pady=10)

    entry_id=Entry(win)
    entry_id.pack()

    Button(
        win,
        text="حذف",
        bg="red",
        command=remove
    ).pack(pady=15)
#************************************************
def edit_course():

    def update():

        cursor.execute(
            "SELECT langID FROM Lang WHERE name=?",
            (combo_lang.get(),)
        )
        lang=cursor.fetchone()

        cursor.execute(
            "SELECT teacherID FROM Teachers WHERE name=?",
            (combo_teacher.get(),)
        )
        teacher=cursor.fetchone()

        cursor.execute(
            """
            UPDATE Courses
            SET
            name=?,
            langID=?,
            teacherID=?,
            sessions=?,
            price=?
            WHERE courseID=?
            """,
            (
                entry_name.get(),
                lang[0],
                teacher[0],
                entry_session.get(),
                entry_price.get(),
                entry_id.get()
            )
        )

        conn.commit()

        messagebox.showinfo(
            "موفق",
            "دوره ویرایش شد"
        )

        win.destroy()

    win=Toplevel(window)
    win.geometry("400x450")
    win.config(bg="pink")

    Label(win,text="کد دوره",bg="pink").pack()
    entry_id=Entry(win)
    entry_id.pack()

    Label(win,text="نام دوره",bg="pink").pack()
    entry_name=Entry(win)
    entry_name.pack()

    cursor.execute("SELECT name FROM Lang")
    langs=[r[0] for r in cursor.fetchall()]

    Label(win,text="زبان",bg="pink").pack()
    combo_lang=ttk.Combobox(win,values=langs)
    combo_lang.pack()

    cursor.execute("SELECT name FROM Teachers")
    teachers=[r[0] for r in cursor.fetchall()]

    Label(win,text="مدرس",bg="pink").pack()
    combo_teacher=ttk.Combobox(win,values=teachers)
    combo_teacher.pack()

    Label(win,text="تعداد جلسات",bg="pink").pack()
    entry_session=Entry(win)
    entry_session.pack()

    Label(win,text="شهریه",bg="pink").pack()
    entry_price=Entry(win)
    entry_price.pack()

    Button(
        win,
        text="ویرایش",
        bg="green",
        command=update
    ).pack(pady=15)
#**********************************************
def about():

    messagebox.showinfo(
        "درباره برنامه",
        """
سیستم مدیریت آموزشگاه زبان

طراحی و پیاده سازی:
فاطمه بقایی

دانشجوی رشته کامپیوتر

سال: 1405
        """
    )
#**********************************************

bg_image= PhotoImage(file="back.png")
bg_label = Label(window, image=bg_image , width=600 , height=600)
bg_label.pack(fill=BOTH, expand=True,side=TOP)

menubar = Menu(window)
window.configure(menu=menubar)
lang_menu = Menu(menubar, tearoff=0)
lang_menu.add_command(label= "افزودن زبان جدید" , command=create_leng )
lang_menu.add_command(label="ویرایش زبان",command=edit_leng)
lang_menu.add_command(label=  "حذف زبان " , command=delete_leng)
lang_menu.add_command(label=  "لیست زبان ها " , command=show_languages)
menubar.add_cascade(label= "زبان" , menu=lang_menu)
#********************************************************
user_menu = Menu(menubar , tearoff=0)
user_menu.add_command(label="ورود زبان آموز " , command=signin)
user_menu.add_command(label="افزودن زبان آموز جدید" , command=create_user)
user_menu.add_command(label="ویرایش زبان آموز", command=edit_user)
user_menu.add_command(label="حذف زبان آموز" , command=delete_user)
user_menu.add_command(label="لیست زبان آموزان",command=show_users)
user_menu.add_command(label="جستجوی زبان آموزان",command=search_user)
user_menu.add_command(label="گزارش زبان آموزان",command=report_users)
menubar.add_cascade(label= "زبان آموزان" , menu=user_menu)
#*********************************************************
teacher_menu = Menu(menubar, tearoff=0)
teacher_menu.add_command(label="افزودن مدرس", command=add_teacher)
teacher_menu.add_command(label="ویرایش مدرس", command=edit_teacher)
teacher_menu.add_command(label="حذف مدرس", command=delete_teacher)
teacher_menu.add_command(label="لیست مدرس‌ها", command=show_teachers)
menubar.add_cascade(label="مدرس", menu=teacher_menu)
#*************************************************
course_menu = Menu(menubar, tearoff=0)
course_menu.add_command(label="افزودن دوره", command=add_course)
course_menu.add_command(label="لیست دوره‌ها", command=show_courses)
course_menu.add_command(label="حذف دوره‌ها", command=delete_course)
course_menu.add_command(label="ویرایش دوره‌ها", command=edit_course)
menubar.add_cascade(label="دوره‌ها", menu=course_menu)
#****************************************
enroll_menu = Menu(menubar, tearoff=0)
enroll_menu.add_command(label="ثبت‌ نام", command=add_enroll)
enroll_menu.add_command(label="لیست ثبت‌ نام‌ها", command=show_enrollments)
enroll_menu.add_command(label="ویرایش ثبت‌ نام‌ها", command=edit_enroll)
enroll_menu.add_command(label="حذف ثبت‌ نام‌ها", command=delete_enroll)
enroll_menu.add_command(label="جستجوی ثبت نام",command=search_enroll)
menubar.add_cascade(label="ثبت‌ نام", menu=enroll_menu)
#************************************************
report_menu = Menu(menubar, tearoff=0)
report_menu.add_command(label="درآمد کل", command=report_income)
report_menu.add_command(label="تعداد ثبت‌ نام‌ها", command=report_enroll)
report_menu.add_command(label="تعداد دوره‌ها", command=report_courses)
menubar.add_cascade(label="گزارش‌ها", menu=report_menu)
#*************************************************
invoice_menu= Menu(menubar,tearoff=0)
invoice_menu.add_command(label="افزودن فاکنور",command= add_invoice)
invoice_menu.add_command(label="لیست فاکنور",command=show_invoices)
invoice_menu.add_command(label="درآمد کل",command=report_income)
menubar.add_cascade(label="فاکنور", menu= invoice_menu)
#***************************************************
help_menu = Menu(menubar, tearoff=0)

help_menu.add_command(
    label="درباره برنامه",
    command=about
)

menubar.add_cascade(
    label="راهنما",
    menu=help_menu
)
#***************************************
window.mainloop()