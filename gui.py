from tkinter import Tk, Label, Entry, Button, messagebox, CENTER, BOTTOM, LEFT, TOP, RIGHT, LabelFrame, GROOVE, \
    StringVar, \
    Toplevel, SOLID, \
    font, Frame
import re
import random
import mysql.connector as mc

connection = mc.connect(host='localhost', user='root', password='', database='pyproj')
db_cursor = connection.cursor()
create_sql = 'CREATE TABLE IF NOT EXISTS `blocked_urls`' \
             '( `url_id` int(11) NOT NULL AUTO_INCREMENT, `url_text` varchar(100) NOT NULL,' \
             ' `url_ip` varchar(45) DEFAULT NULL, PRIMARY KEY (`url_id`))' \
             ' ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'

db_cursor.execute(create_sql)


# db connection code goes here

root = Tk()
root.title("Phishing detection using Machine Learning")
root.geometry('500x300')
root.minsize(500, 300)
url = StringVar(root)


def add_space(master, h, side=TOP):
    LabelFrame(master, height=h).pack(side=side)


def alert():
    messagebox.showinfo('Alerting Authorities', 'Cyber Cell has been notified of malicious URL')


def insert_to_db(url_val, master=None):
    ip = ".".join('%s' % random.randint(10, 190) for i in range(4))
    db_cursor.execute("INSERT INTO blocked_urls (url_text, url_ip) VALUES ('{0}','{1}');".format(url_val, ip))
    for widget in master.winfo_children():
        widget.destroy()
    table = fetch_table()

    for i in range(len(table)):
        for j in range(len(table[i])):
            Label(master, text=table[i][j], justify=LEFT, padx=10, pady=7).grid(column=j, row=i)

    connection.commit()
    db_cursor.close()
    connection.close()


def button_frame(master, url_val=None, top=None):
    add_space(master, 80, side=RIGHT)
    btn1 = Button(master, text="Send Alert", command=alert, padx=10, pady=5, bd=2, bg='grey', relief=GROOVE,
                  font=('Arial', 10, 'bold')).pack(side=LEFT)
    add_space(master, 80, side=RIGHT)
    btn2 = Button(master, text="Block URL", command=lambda: insert_to_db(url_val, top), padx=10, pady=5, bd=2,
                  bg='orange', relief=GROOVE,
                  font=('Arial', 10, 'bold')).pack(side=LEFT)
    add_space(master, 80, side=RIGHT)
    # btn3 = Button(master, text="Reset", command=reset).pack()
    # btn4 = Button(master, text="close", command=top.destroy).pack(side=LEFT)


# def display_table(master):
#     master.pack_forget()
#     db_cursor.execute('SELECT * FROM blocked_urls;')
#     rows = db_cursor.fetchall()
#
#     for row in rows:
#         for i in range(0, 3):
#             Label(master, text=row[i], relief='solid', padx=10, pady=10, bd=1).pack(side=LEFT)

# fetch table
def fetch_table():
    db_cursor.execute('SELECT * FROM blocked_urls;')
    rows = db_cursor.fetchall()
    return rows


def open_window():
    # root.iconify()
    url_value = url.get()

    top = Toplevel()
    top.title('Checking : ' + url_value)
    top.geometry('500x300')
    top.minsize(500, 500)

    url_font = font.Font(family='Arial', size=12, weight='bold')
    ui_font = font.Font(family='Arial', size=10, weight='bold')

    add_space(top, 20)

    # predict_url

    # url_status = predicted_value[0].lower()
    url_status = ''

    if url_status == 'good':
        lbl_url = Label(top, text='Entered URL : ' + url_value + ' is legitimate', padx=20, pady=20,
                        relief=SOLID, font=url_font, bg='green',
                        fg='white')
    elif url_status == 'bad':
        lbl_url = Label(top, text='Entered URL : ' + url_value + ' is malicious', padx=20, pady=20,
                        relief=SOLID, font=url_font, bg='red',
                        fg='white')
    else:
        lbl_url = Label(top, text='A Problem was encountered', padx=20, pady=20,
                        relief=SOLID, font=url_font, bg='black',
                        fg='white')
    lbl_url.pack()
    # add_space(top, 20)

    table_frame = Frame(top, relief='solid', bd=1)

    btn_frame = Frame(top)
    button_frame(btn_frame, url_val=url_value, top=table_frame)
    btn_frame.pack()

    add_space(top, 20)

    Label(top, text='Blocked URLs', padx=20, pady=10, font=ui_font).pack()

   # out put table

    table_frame.pack()


def validate():
    url_valid = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url.get())
    if not url_valid:
        messagebox.showerror(title='Wrong URL Entered', message='Please check the URL you have entered')
        # open_window()  # for debugging
    else:
        open_window()


# if not db:
#     messagebox.showerror(title='Database Connection Error', message='Cannot connect to database')

credits_text = 'Made for Python Project - SYMCA SEM IV - by Jyotishree Badugu,' \
               'Sheroy Divecha, Meet Divecha, Dinky Shah & Shivam Verma'
credit = Label(root, text=credits_text, pady=20, wraplength=400, justify=CENTER, width=100).pack()

entry_label = Label(root, padx=10, pady=10, text="Enter URL").pack()
entry_textbox = Entry(root, width=50, textvariable=url).pack()

LabelFrame(root, height=10).pack()
submit = Button(root, text='Check URL', padx=10, pady=5, bd=2, command=validate, bg='orange', relief=GROOVE,
                font=('Arial', 10, 'bold')).pack()

root.mainloop()
