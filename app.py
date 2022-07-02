
from datetime import date
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import pygame
from PIL import Image as ii, ImageTk
from pyzbar.pyzbar import decode
import time
import cv2
from tkinter import *
from tkinter import ttk
import pymysql
import pandas as pd
import smtplib
from email.message import EmailMessage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global cam1, cam2
cam1 = True
cam2 = False

global us_bg, us_fg, mid_bg, mid_fg, btn_p_bg, btn_p_fg, btn_s_bg, dk_bg
us_bg = "#2E2E3A"
us_fg = "#FFFFFF"
# mid_bg = "#31FFA1"
mid_bg = "#4ADE80"
mid_fg = "#111827"
# btn_p_bg = "#4ADE80"
btn_p_bg = "#55CB83"
btn_s_bg = "#111827"
# btn_p_fg = "#111827"
btn_p_fg = "#2E2E3A"
# dk_bg = "#1FAD53"
dk_bg = "#baffd3"


def db_conn_funct():
    global mycon, cur
    mycon = pymysql.connect(host='localhost', user='root',
                            password='', db='pbl', charset='utf8mb4')
    cur = mycon.cursor()
    print('connected !')


def db_disconn_funct():
    global mycon
    if mycon.open:
        mycon.close()
        print('disconn !')
    else:
        pass


# initilise
db_conn_funct()  # conn established
global root
root = Tk()
root.title('PBL PROJECT')
root.geometry("600x500")

def on_closing_window():
    global mycon, root
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mycon.close()
        root.destroy()

# functions :


def billing():

    hide_all_frames()

    billing_frame.pack(fill=BOTH, expand=1)
    billing_app_page()


def statistics():
    hide_all_frames()
    statistics_frame.pack(fill=BOTH, expand=1)
    stats_main_all()


def dashboard():
    hide_all_frames()
    dashboard_frame.pack(fill=BOTH, expand=1)
    dashboard_main_analysis()


def sales():
    hide_all_frames()
    sales_frame.pack(fill=BOTH, expand=1)
    sales_analysis_main()


def bill():
    hide_all_frames()
    bill_frame.pack(fill=BOTH, expand=1)
    bill_display_analysis()


def load_products():
    hide_all_frames()
    load_product_frame.pack(fill=BOTH, expand=1)  # add product frame
    product_frame_funct()


def add_products():
    hide_all_frames()
    add_product_frame.pack(fill=BOTH, expand=1)  # view frame
    view_product_screen()


def del_products():
    hide_all_frames()
    del_product_frame.pack(fill=BOTH, expand=1)
    edit_del_pro()


def about():
    hide_all_frames()
    about_us_frame.pack(fill=BOTH, expand=1)
    about_app_dev()


def hide_all_frames():

    billing_frame.pack_forget()
    statistics_frame.pack_forget()
    dashboard_frame.pack_forget()
    bill_frame.pack_forget()
    sales_frame.pack_forget()
    load_product_frame.pack_forget()
    add_product_frame.pack_forget()
    del_product_frame.pack_forget()
    about_us_frame.pack_forget()
    contact_us_frame.pack_forget()


# creating menu obj
menu_bar = Menu(root)
root.config(menu=menu_bar)

# creating menu items
billing_menu = Menu(menu_bar, tearoff=0)
stats_menu = Menu(menu_bar, tearoff=0)
product_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)

# cascading menu to main menu
menu_bar.add_cascade(label="billing", menu=billing_menu)
menu_bar.add_cascade(label="statistics", menu=stats_menu)
menu_bar.add_cascade(label="Product", menu=product_menu)
menu_bar.add_cascade(label="About", menu=about_menu)

# adding sub menu for Billing menu :
billing_menu.add_command(label="Billing", command=billing)

# adding sub menu for stats menu :
stats_menu.add_command(label="Dashboard", command=dashboard)
stats_menu.add_command(label="Bills", command=statistics)
stats_menu.add_command(label="Sales", command=sales)
stats_menu.add_command(label="Product Stats", command=bill)

# adding sub menu for product menu :
product_menu.add_command(label="add", command=load_products)
product_menu.add_command(label="view", command=add_products)
product_menu.add_command(label="edit/delete", command=del_products)

# adding sub menu for about menu:
about_menu.add_command(label="about app", command=about)

# Frames
billing_frame = Frame(root, width=600, height=500, bg="red")

statistics_frame = Frame(root, width=600, height=500, bg="green")
dashboard_frame = Frame(root, width=600, height=500, bg="green")
sales_frame = Frame(root, width=600, height=500, bg="green")
bill_frame = Frame(root, width=600, height=500, bg="green")

load_product_frame = Frame(root, width=600, height=500, bg="red")
add_product_frame = Frame(root, width=600, height=500, bg="yellow")
del_product_frame = Frame(root, width=600, height=500, bg="blue")

about_us_frame = Frame(root, width=600, height=500, bg="red")
contact_us_frame = Frame(root, width=600, height=500, bg="green")

def billing_app_page():
    global song, cap, c_bill_txt, cphn_txt, addproduct_e, cname_txt, discount_txt, total_bill_txt, addquantity_e, capp, cap, mstr_df_prd, cam1, cam2, sac4_e, sac3_e, sac2_e, sac1_e, cur, mycon, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all
    db_conn_funct()
    quant_list_bill = pd.DataFrame()
    total_list_bill = pd.DataFrame()

    mstr_df_prd = pd.DataFrame({'pname': [], 'mrp': [], 'barcode': [], 'pid': [
    ], 'quantity': [], 'total': [], 'profit': [], 'total_profit': []})

    bc_list_bill_all = []
    name_list_bill = pd.DataFrame()
    pid_list_bill = pd.DataFrame()
    mrp_list_bill = pd.DataFrame()
    bc_list_bill = pd.DataFrame()

    cam1 = True

    if cam2:
        cam2 = False
        capp.release()

    F1 = LabelFrame(billing_frame, fg=us_fg, bg=us_bg)
    F1.place(x=0, y=0, relwidth=1)
    fc1 = LabelFrame(F1, fg=us_fg, bg=us_bg, borderwidth=0, relief="raised")
    fc1.grid(row=0, column=0, padx=40, pady=3)

    fc2 = LabelFrame(F1, fg=us_fg, bg=us_bg, relief="raised", borderwidth=0)
    fc2.grid(row=0, column=1, padx=37, pady=3)

    fc3 = LabelFrame(F1, fg=us_fg, bg=us_bg, relief="raised")
    fc3.grid(row=0, column=2, padx=40, pady=3)

    cname_lbl = Label(fc1, text="Customer Name:",
                      bg=us_bg, borderwidth=0, fg=us_fg, font=('Helvetica', 15, 'bold'))
    cname_lbl.grid(row=0, column=0, padx=10)
    cname_txt = Entry(fc1, width=15, font='arial 15')
    cname_txt.grid(row=0, column=1, padx=10)

    cphn_lbl = Label(fc2, text="Email:", bg=us_bg, fg=us_fg,
                     font=('Helvetica', 15, 'bold'), borderwidth=0)
    cphn_lbl.grid(row=0, column=2, padx=10)
    cphn_txt = Entry(fc2, width=23, font='arial 15')
    cphn_txt.grid(row=0, column=3, padx=10)

    c_bill_lbl = Label(fc3, text="Bill Number:", bg=us_bg, fg=us_fg,
                       font=('Helvetica', 15, 'bold'))
    c_bill_lbl.grid(row=0, column=4, padx=10)
    c_bill_txt = Entry(fc3, width=15, font=(
        'Helvetica', 15, 'bold'), state='disable')
    c_bill_txt.grid(row=0, column=5, padx=10)

    # ******************************************************************************

    # middle window - barcode and item details

    F2 = LabelFrame(billing_frame, fg=mid_fg, bg=mid_bg)
    F2.place(x=0, y=43, relwidth=1)

    barcode = LabelFrame(F2, fg=us_fg, bg=us_bg)
    barcode.grid(row=0, column=0, padx=5, pady=3)

    items = LabelFrame(F2, fg=mid_fg, bg=mid_bg, height=500)
    items.grid(row=0, column=1, padx=20, pady=3)

    # labels
    barcode_lbl = Label(barcode, text="Barcode", bg=us_bg, font=(
        'Helvetica', 15, 'bold'), width=50, height=20)
    barcode_lbl.grid(row=0, column=0, padx=10)

    lmain = Label(barcode_lbl)
    lmain.grid(row=0, column=0, padx=30, pady=50)

# ============================= bill id gen ======================================
    bill_qry = "select `bill_id` from bill_details;"
    bill_list_df = pd.read_sql(bill_qry, mycon)
    bill_list_all = bill_list_df['bill_id'].tolist()
    import string
    import random
    bill_id_new = ''.join(random.choices(
        string.ascii_letters + string.digits, k=8))
    while bill_id_new in bill_list_all:
        bill_id_new = ''.join(random.choices(
            string.ascii_letters + string.digits, k=8))

    c_bill_txt.configure(state='normal')
    if len(c_bill_txt.get()) > 0:
        c_bill_txt.delete(0, END)

    c_bill_txt.insert(0, bill_id_new)
    c_bill_txt.configure(state='disable')
    # print(bill_id_new)

# ===================================================================

    cap = cv2.VideoCapture(0)

    manual_mode = LabelFrame(items, fg=us_fg, bg=us_bg)
    manual_mode.grid(row=0, column=0, padx=0, pady=11)

    items_bill_live = LabelFrame(items, fg=mid_fg, bg=mid_bg)
    items_bill_live.grid(row=1, column=0, padx=25, pady=3)

    Label(manual_mode, text="PRODUCT ID", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    addproduct_e = Entry(manual_mode, width=15, font='arial 15')
    addproduct_e.grid(row=1, column=0, padx=5, pady=8)

    Label(manual_mode, text="QUANTITY", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=1)
    addquantity_e = Entry(manual_mode, width=15, font='arial 15')
    addquantity_e.grid(row=1, column=1, padx=5, pady=8)

    details = LabelFrame(items_bill_live, fg=mid_fg, bg=mid_bg, height=510)
    details.grid(row=1, column=0)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    name_detail.grid(row=0, column=0)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    cost_detail.grid(row=0, column=3)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    mrp_detail.grid(row=0, column=1)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    quant_detail.grid(row=0, column=2)

    def mult_view(*args):
        sac4_e.yview(*args)
        sac3_e.yview(*args)
        sac2_e.yview(*args)
        sac1_e.yview(*args)

    vsb = Scrollbar(details)
    vsb.grid(row=0, column=4, sticky='ns')
    vsb.configure(command=mult_view)

    Label(name_detail, text="NAME", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac1_e = Text(name_detail, width=18, height=15, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac1_e.grid(row=1, column=0)

    Label(quant_detail, text="QUANTITY", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac2_e = Text(quant_detail, width=13, height=15,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac2_e.grid(row=1, column=0)

    Label(mrp_detail, text="MRP", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac3_e = Text(mrp_detail, width=15, height=15, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac3_e.grid(row=1, column=0)

    Label(cost_detail, text="TOTAL", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac4_e = Text(cost_detail, width=15, height=15, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac4_e.grid(row=1, column=0)

    # bottom window - bill details and action buttons

    F3 = LabelFrame(billing_frame, fg=us_fg, bg=us_bg, relief="raised")
    F3.place(x=0, y=558, relwidth=1)
    discount = LabelFrame(F3, fg=us_fg, bg=us_bg, relief="raised")
    discount.grid(row=0, column=0, padx=40, pady=3)

    total_bill = LabelFrame(F3, fg=us_fg, bg=us_bg, relief="raised")
    total_bill.grid(row=0, column=1, padx=37, pady=3)

    generate_btn = LabelFrame(F3, fg=us_fg, bg=us_bg,  borderwidth='0')
    generate_btn.grid(row=0, column=4, padx=40, pady=3)

    total_btn = LabelFrame(F3, fg=us_fg, bg=us_bg, borderwidth='0')
    total_btn.grid(row=0, column=3, padx=40, pady=3)

    discount_lbl = Label(discount, text="Discount",
                         bg=us_bg, fg=us_fg, font=('Helvetica', 15, 'bold'))
    discount_lbl.grid(row=0, column=0, padx=10)
    discount_txt = Entry(discount, width=15, font='arial 15')
    discount_txt.grid(row=1, column=0, padx=10)

    discount_txt.insert(0, int(0))

    total_bill_lbl = Label(total_bill, text="Total Amount",
                           bg=us_bg, fg=us_fg, font=('Helvetica', 15, 'bold'))
    total_bill_lbl.grid(row=0, column=0, padx=10)

    total_bill_txt = Entry(total_bill, width=15,
                           font='arial 15', state='disable')
    total_bill_txt.grid(row=1, column=0, padx=10)

    global barcode_all_list
    barcode_qry = "select `barcode` from product;"
    barcode_all_df = pd.read_sql(barcode_qry, mycon)
    barcode_all_list = barcode_all_df['barcode'].tolist()

    global cnt123

    cnt123 = False

    def asd123():
        global cnt123
        cnt123 = True
        messagebox.showinfo("PRODUCT NOT AVAILABLE", "Pls add the product to inventory first !")
        cnt123 = False

    def show_frame():
        _, img = cap.read()
        img = cv2.resize(img, (400, 350))
        frame = img
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        hhh = ii.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=hhh)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

        for barcode in decode(img):
            global mycon, song, master_barcode_list, cur, barcode_all_df, bill_id_new, mstr_df_prd, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all

            myData = barcode.data.decode('utf-8')

            if myData in barcode_all_list:

                one_row_qry = "select `pname`, `mrp`, `barcode`, `pid`,`profit`, `quantity` as 'quant_main' from product where `barcode` = %s;" % (
                    myData,)
                temp_df_pro = pd.read_sql(one_row_qry, mycon)
                temp_df_pro['quantity'] = [int(1)]
                total_new = int(temp_df_pro['mrp'].to_string(index=False))
                temp_df_pro['total'] = [total_new]

                total_profit_new = int(
                    temp_df_pro['profit'].to_string(index=False))
                temp_df_pro['total_profit'] = [total_profit_new]

                master_barcode_list = mstr_df_prd['barcode'].tolist()
                ind_main = mstr_df_prd[mstr_df_prd['barcode']
                                       == myData].index.values
                if myData not in master_barcode_list:
                    q_new_temp = 1
                else:
                    q_new_temp = int(
                        float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False))) + 1

                pid_qry_bill = "select `barcode` , `quantity` as 'quant_main' from product;"
                pid_qry_bill_df = pd.read_sql(pid_qry_bill, mycon)
                pid_qry_bill_list = pid_qry_bill_df['barcode'].tolist()
                quant_ind = pid_qry_bill_list.index(myData)

                if myData in master_barcode_list:
                    if int(float(pid_qry_bill_df['quant_main'].iloc[quant_ind])) - q_new_temp >= 0:
                        pygame.mixer.init()
                        pygame.mixer.music.load("scanner_sound.mp3")
                        pygame.mixer.music.play()
                        ind_main = mstr_df_prd[mstr_df_prd['barcode']
                                               == myData].index.values
                        q_new_temp = int(
                            float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False))) + 1
                        mstr_df_prd.loc[ind_main, 'quantity'] = q_new_temp
                        total_new = int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(
                            index=False)))*(int(float(mstr_df_prd['mrp'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total'] = [total_new]

                        total_new = int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(
                            index=False))) * (int(float(mstr_df_prd['profit'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total_profit'] = [total_new]
                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")

                else:
                    if int(float(temp_df_pro['quant_main'].to_string(index=False))) > 0:
                        pygame.mixer.init()
                        pygame.mixer.music.load("scanner_sound.mp3")
                        pygame.mixer.music.play()
                        mstr_df_prd = mstr_df_prd.append(
                            temp_df_pro, ignore_index=True)

                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")

            else:
                if cnt123 == False:
                    asd123()

            time.sleep(1.2)

    def add_product_tobill():
        global mycon, cur, barcode_all_df, master_barcode_list, bill_id_new, mstr_df_prd, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all, addproduct_e, addquantity_e
        pid_qry_bill = "select `pid`, `quantity` as 'quant_main' from product;"
        pid_qry_bill_df = pd.read_sql(pid_qry_bill, mycon)
        pid_qry_bill_list = pid_qry_bill_df['pid'].tolist()

        if len(addproduct_e.get()) > 0 and len(addquantity_e.get()) > 0:
            if (addproduct_e.get()) in pid_qry_bill_list and int(addquantity_e.get()) > 0:
                if addproduct_e.get() in (mstr_df_prd['pid'].tolist()):
                    ind_main = mstr_df_prd[mstr_df_prd['pid']
                                           == addproduct_e.get()].index.values
                    q_new = int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(
                        index=False))) + int(addquantity_e.get())

                    quant_ind = pid_qry_bill_list.index(
                        str(addproduct_e.get()))

                    if int(float(pid_qry_bill_df['quant_main'].iloc[quant_ind])) - q_new >= 0:

                        mstr_df_prd.loc[ind_main, 'quantity'] = q_new
                        total_new = q_new * \
                            (int(
                                float(mstr_df_prd['mrp'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total'] = [total_new]
                        total_new = q_new * \
                            (int(
                                float(mstr_df_prd['profit'].iloc[ind_main].to_string(index=False))))
                        mstr_df_prd.loc[ind_main, 'total_profit'] = [total_new]

                        sac1_e.configure(state="normal")

                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')

                        addproduct_e.delete(0, END)
                        addquantity_e.delete(0, END)
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")

                else:

                    quant_ind = pid_qry_bill_list.index(
                        str(addproduct_e.get()))
                    if int(float(pid_qry_bill_df['quant_main'].iloc[quant_ind])) - int(addquantity_e.get()) >= 0:
                        one_row_qry = "select `pname`, `mrp`, `barcode`, `pid`,`profit`, `quantity` as 'quant_main' from product where `pid` = '%s';" % (
                            addproduct_e.get(),)
                        temp_df_pro = pd.read_sql(one_row_qry, mycon)
                        temp_df_pro['quantity'] = [int(addquantity_e.get())]
                        if int(float(temp_df_pro['quant_main'].to_string(index=False))) > 0:
                            total_new = int(temp_df_pro['mrp'].to_string(
                                index=False)) * int(addquantity_e.get())
                            temp_df_pro['total'] = [total_new]

                            total_new = int(temp_df_pro['profit'].to_string(
                                index=False)) * int(addquantity_e.get())
                            temp_df_pro['total_profit'] = [total_new]

                            mstr_df_prd = mstr_df_prd.append(
                                temp_df_pro, ignore_index=True)

                            sac1_e.configure(state="normal")
                            sac1_e.delete('1.0', END)
                            sac1_e.insert(
                                '1.0', mstr_df_prd['pname'].to_string(index=False))
                            sac1_e.configure(state="disable")

                            sac2_e.configure(state="normal")
                            sac2_e.delete('1.0', END)
                            sac2_e.insert(
                                '1.0', mstr_df_prd['quantity'].to_string(index=False))
                            sac2_e.configure(state='disable')

                            sac3_e.configure(state="normal")
                            sac3_e.delete('1.0', END)
                            sac3_e.insert(
                                '1.0', mstr_df_prd['mrp'].to_string(index=False))
                            sac3_e.configure(state="disable")

                            sac4_e.configure(state="normal")
                            sac4_e.delete('1.0', END)
                            sac4_e.insert(
                                '1.0', mstr_df_prd['total'].to_string(index=False))
                            sac4_e.configure(state='disable')

                            addproduct_e.delete(0, END)
                            addquantity_e.delete(0, END)
                        else:
                            messagebox.showinfo(
                                "PRODUCT NOT AVAILABLE", "The Quantity of Product is Zero")
                    else:
                        messagebox.showinfo(
                            "PRODUCT NOT AVAILABLE", "The Quantity of Product is not enough")

            else:
                messagebox.showinfo(
                    "PRODUCT NOT FOUND", "The product with pid "+addproduct_e.get()+" not found !")
                addproduct_e.delete(0, END)
                addquantity_e.delete(0, END)
        else:
            messagebox.showinfo("INVALID INPUT", "Fill all details first !")

    def remove_item_frombill():
        global mycon, cur, barcode_all_df, master_barcode_list, bill_id_new, mstr_df_prd, bill_id_new, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all, addproduct_e, addquantity_e
        if len(addquantity_e.get()) > 0 and len(addproduct_e.get()) > 0:
            if addproduct_e.get() in mstr_df_prd['pid'].tolist():
                ind_main = mstr_df_prd[mstr_df_prd['pid']
                                       == addproduct_e.get()].index.values
                q_now_ibbill = int(
                    float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False)))
                if q_now_ibbill - int(addquantity_e.get()) >= 0:

                    q_new = q_now_ibbill - int(addquantity_e.get())
                    mstr_df_prd.loc[ind_main, 'quantity'] = [q_new]
                    total_new = q_new * \
                        (int(
                            float(mstr_df_prd['mrp'].iloc[ind_main].to_string(index=False))))
                    mstr_df_prd.loc[ind_main, 'total'] = [total_new]

                    total_new = q_new * \
                        (int(
                            float(mstr_df_prd['profit'].iloc[ind_main].to_string(index=False))))
                    mstr_df_prd.loc[ind_main, 'total_profit'] = [total_new]

                    sac1_e.configure(state="normal")
                    sac1_e.delete('1.0', END)
                    sac1_e.insert(
                        '1.0', mstr_df_prd['pname'].to_string(index=False))
                    sac1_e.configure(state="disable")

                    sac2_e.configure(state="normal")
                    sac2_e.delete('1.0', END)
                    sac2_e.insert(
                        '1.0', mstr_df_prd['quantity'].to_string(index=False))
                    sac2_e.configure(state='disable')

                    sac3_e.configure(state="normal")
                    sac3_e.delete('1.0', END)
                    sac3_e.insert(
                        '1.0', mstr_df_prd['mrp'].to_string(index=False))
                    sac3_e.configure(state="disable")

                    sac4_e.configure(state="normal")
                    sac4_e.delete('1.0', END)
                    sac4_e.insert(
                        '1.0', mstr_df_prd['total'].to_string(index=False))
                    sac4_e.configure(state='disable')

                    addproduct_e.delete(0, END)
                    addquantity_e.delete(0, END)

                    if int(float(mstr_df_prd['quantity'].iloc[ind_main].to_string(index=False))) == 0:

                        mstr_df_prd = mstr_df_prd.drop(
                            mstr_df_prd.index[ind_main])
                        mstr_df_prd.reset_index(drop=True, inplace=True)

                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)
                        sac1_e.insert(
                            '1.0', mstr_df_prd['pname'].to_string(index=False))
                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)
                        sac2_e.insert(
                            '1.0', mstr_df_prd['quantity'].to_string(index=False))
                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)
                        sac3_e.insert(
                            '1.0', mstr_df_prd['mrp'].to_string(index=False))
                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)
                        sac4_e.insert(
                            '1.0', mstr_df_prd['total'].to_string(index=False))
                        sac4_e.configure(state='disable')
                    else:
                        pass

                    if mstr_df_prd.empty:
                        sac1_e.configure(state="normal")
                        sac1_e.delete('1.0', END)

                        sac1_e.configure(state="disable")

                        sac2_e.configure(state="normal")
                        sac2_e.delete('1.0', END)

                        sac2_e.configure(state='disable')

                        sac3_e.configure(state="normal")
                        sac3_e.delete('1.0', END)

                        sac3_e.configure(state="disable")

                        sac4_e.configure(state="normal")
                        sac4_e.delete('1.0', END)

                        sac4_e.configure(state='disable')

                else:
                    messagebox.showinfo("NOT ENOUGH ITEMS",
                                        "Not enough items to remove !")
                    addproduct_e.delete(0, END)
                    addquantity_e.delete(0, END)
            else:
                messagebox.showinfo(
                    "INVALID INPUT", "No such product found in order list !")
                addproduct_e.delete(0, END)
                addquantity_e.delete(0, END)
        else:
            messagebox.showinfo("INVALID INPUT", "Fill all details first !")

    def total_amt_bill_gen():
        global mstr_df_prd, total_bill_txt,  discount_txt
        total_amt_display = mstr_df_prd['total'].sum()
        total_bill_txt.configure(state='normal')
        if len(total_bill_txt.get()) > 0:
            total_bill_txt.delete(0, END)
        if len(discount_txt.get()) > 0:
            if int(discount_txt.get()) <= 100:
                percent_dis = int(discount_txt.get())*0.01
                total_amt_display = round(total_amt_display*(1 - percent_dis))

            else:
                messagebox.showinfo(
                    "INVALID INPUT", "Discount must be atmost 100")

        else:
            messagebox.showinfo(
                "INVALID INPUT", "Fill both tax and discount first !")

        total_bill_txt.insert(0, total_amt_display)
        total_bill_txt.configure(state='disable')

    def generate_bill_main():
        global mycon, sac1_e, sac2_e, sac3_e, sac4_e, cap, c_bill_txt, cphn_txt, addproduct_e, discount_txt, cname_txt, cur, barcode_all_df, master_barcode_list, bill_id_new, mstr_df_prd, bc_list_bill, pid_list_bill, quant_list_bill, name_list_bill, mrp_list_bill, total_list_bill, bc_list_bill_all, addproduct_e, addquantity_e, total_bill_txt, barcode_all_list
        is_df_notnull = bool(1 ^ int(mstr_df_prd.empty))
        if is_df_notnull and len(cname_txt.get()) > 0 and len(discount_txt.get()) > 0:
            generate_btn_lbl.configure(state='disable')
            # ======== total bill ========================

            total_amt_display = mstr_df_prd['total'].sum()
            total_bill_txt.configure(state='normal')

            if len(total_bill_txt.get()) > 0:
                total_bill_txt.delete(0, END)
            if len(discount_txt.get()) > 0:
                if int(discount_txt.get()) <= 100:
                    percent_dis = int(discount_txt.get()) * 0.01
                    total_amt_display = round(
                        total_amt_display * (1 - percent_dis))

                else:
                    messagebox.showinfo(
                        "INVALID INPUT", "Discount must be atmost 100")

            else:
                messagebox.showinfo(
                    "INVALID INPUT", "Fill both tax and discount first !")

            total_bill_txt.insert(0, total_amt_display)

            total_bill_txt.configure(state='disable')

        # ==========================================================================
            pname_list = mstr_df_prd['pname'].tolist()
            quantity_list = mstr_df_prd['quantity'].tolist()
            proxquant_list1 = mstr_df_prd['total_profit'].tolist()
            bc_list = mstr_df_prd['barcode'].tolist()
            mrpxquant1 = mstr_df_prd['total'].tolist()
            items_count_all = mstr_df_prd['quantity'].sum()
            pid_list_all = mstr_df_prd['pid'].tolist()
            proxquant_list = []
            mrpxquant = []
            for asd in range(mstr_df_prd.shape[0]):

                mrp_new = int(mrpxquant1[asd])*(int(discount_txt.get())/100)
                mrp_main = int(mrpxquant1[asd]) * \
                    (100 - int(discount_txt.get()))//100
                p_new = proxquant_list1[asd] - mrp_new
                proxquant_list.append(p_new)
                mrpxquant.append(mrp_main)

            total_profit_bill = sum(proxquant_list)
            qry_asd = "select * from stats;"
            stats_now = pd.read_sql(qry_asd, mycon)

            qry_asd = "select `quantity`, `sold`, `pid` from product;"
            product_now = pd.read_sql(qry_asd, mycon)

            num_of_rows = mstr_df_prd.shape[0]

            date_now = date.today()

            if len(cphn_txt.get()) == 0:

                qry3 = "INSERT INTO `bill_details` (`bill_id`, `items`, `bill_price`, `bill_profit`, `bill_date`, `c_name`, `c_email`, `discount`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', NULL, '%s');" % (
                    bill_id_new, items_count_all, total_amt_display, total_profit_bill, date_now, cname_txt.get(),
                    discount_txt.get(),)
            else:
                qry3 = "INSERT INTO `bill_details` (`bill_id`, `items`, `bill_price`, `bill_profit`, `bill_date`, `c_name`, `c_email`, `discount`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                    bill_id_new, items_count_all, total_amt_display, total_profit_bill, date_now, cname_txt.get(),
                    cphn_txt.get(), discount_txt.get(),)

            cur.execute(qry3)
            mycon.commit()

            for jj in range(num_of_rows):
                qry1 = "INSERT INTO `sales` (`bill_id`, `pname`, `quantity`, `profit_pp`, `barcode`) VALUES ('%s', '%s', '%s', '%s', '%s');" % (
                    bill_id_new, pname_list[jj], quantity_list[jj], proxquant_list[jj], bc_list[jj],)
                cur.execute(qry1)
                mycon.commit()

                if pname_list[jj] in stats_now['pname'].tolist():
                    ind_main = stats_now[stats_now['pname']
                                         == pname_list[jj]].index.values
                    sold_new = int(float(stats_now['sold'].iloc[ind_main].to_string(
                        index=False))) + int(quantity_list[jj])
                    net_rev_new = int(float(stats_now['net_revenue'].iloc[ind_main].to_string(
                        index=False))) + int(mrpxquant[jj])
                    net_pro_new = int(float(stats_now['net_profit'].iloc[ind_main].to_string(
                        index=False))) + int(proxquant_list[jj])

                    qry2 = "UPDATE `stats` SET `sold`='%s',`net_revenue`='%s',`net_profit`='%s' WHERE `pname` = '%s';" % (
                        sold_new, net_rev_new, net_pro_new, pname_list[jj],)
                else:
                    qry2 = "INSERT INTO `stats` (`pname`, `sold`, `net_revenue`, `net_profit`) VALUES ('%s', '%s', '%s', '%s')" % (
                        pname_list[jj], quantity_list[jj], mrpxquant[jj], proxquant_list[jj],)

                cur.execute(qry2)
                mycon.commit()

                ind_main = product_now[product_now['pid']
                                       == pid_list_all[jj]].index.values
                quant_new = int(float(product_now['quantity'].iloc[ind_main].to_string(
                    index=False))) - quantity_list[jj]

                sold_new = int(float(product_now['sold'].iloc[ind_main].to_string(
                    index=False))) + quantity_list[jj]

                qry4 = "UPDATE `product` SET `quantity`='%s',`sold`='%s' WHERE `pid` = '%s';" % (
                    quant_new, sold_new, pid_list_all[jj])
                cur.execute(qry4)
                mycon.commit()

            quant_list_bill = pd.DataFrame()
            total_list_bill = pd.DataFrame()
            try:
                billdf_pdf = mstr_df_prd[[
                    'pname', 'mrp', 'quantity', 'total'].copy()]

                if mstr_df_prd.shape[0] == 1:
                    billdf_pdf['DISCOUNT'] = str(discount_txt.get()) + "%"
                    billdf_pdf['total_all'] = "₹" + str(total_amt_display)
                    billdf_pdf['Bill Id'] = bill_id_new

                else:

                    dt_temp = ['~' for jj in range(mstr_df_prd.shape[0] - 1)]
                    dt_temp2 = ['~' for jj in range(mstr_df_prd.shape[0] - 1)]
                    dt_temp3 = ['~' for jj in range(mstr_df_prd.shape[0] - 1)]

                    dd_tmp = 'discount : ' + str(discount_txt.get()) + "%"
                    tt_tmp = 'total : ₹' + str(total_amt_display)
                    bd_tmp = 'bill id : ' + str(bill_id_new)
                    dt_temp.append(tt_tmp)
                    dt_temp2.append(bd_tmp)
                    dt_temp3.append(dd_tmp)

                    billdf_pdf['DISCOUNT'] = dt_temp3
                    billdf_pdf['total_all'] = dt_temp
                    billdf_pdf['Bill ID'] = dt_temp2

                billdf_pdf.index += 1

                billdf_pdf = billdf_pdf.rename(
                    {'pname': 'ITEM NAME', 'mrp': 'RATE', 'total': 'VALUE', 'total_all': 'BILL TOTAL'}, axis=1)
                billdf_pdf['VALUE_sub'] = billdf_pdf['VALUE'] * \
                    (int(discount_txt.get())*0.01)
                billdf_pdf['VALUE'] -= billdf_pdf['VALUE_sub']
                billdf_pdf = billdf_pdf.drop('VALUE_sub', 1)

                fig, ax = plt.subplots(figsize=(12, 4))
                ax.axis('tight')
                ax.axis('off')
                the_table = ax.table(
                    cellText=billdf_pdf.values, colLabels=billdf_pdf.columns, loc='top')

                pp = PdfPages("foo.pdf")

                pp.savefig(fig, bbox_inches='tight')

                pp.close()

                # ========== email ===================

                EMAIL_ADDRESS = 'YOUR EMAIL GOES HERE'
                EMAIL_PASSWORD = 'YOUR PASSWORD GOES HERE'
                order_number = bill_id_new  # bill number
                msg = EmailMessage()
                msg['Subject'] = str(
                    cname_txt.get()) + ' your bill for bill number ' + order_number + ' is attached'
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = str(cphn_txt.get())

                msg.set_content('thank you for shopping with us !')

                files = ["foo.pdf"]  # sample pdf

                for file in files:
                    with open(file, 'rb') as f:
                        file_data = f.read()
                        file_name = bill_id_new + " | Bill Details.pdf"
                    msg.add_attachment(
                        file_data, maintype='application', subtype='octet-stream', filename=file_name)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)

            except Exception as ex_tmp:
                print(ex_tmp)

            # ====================================

            if len(cphn_txt.get()) > 0:
                cphn_txt.delete(0, END)
            cname_txt.delete(0, END)
            discount_txt.delete(0, END)
            discount_txt.insert(0, int(0))

            mstr_df_prd = pd.DataFrame({'pname': [], 'mrp': [], 'barcode': [], 'pid': [
            ], 'quantity': [], 'total': [], 'profit': [], 'total_profit': []})

            bc_list_bill_all = []
            name_list_bill = pd.DataFrame()
            pid_list_bill = pd.DataFrame()
            mrp_list_bill = pd.DataFrame()
            bc_list_bill = pd.DataFrame()

            sac1_e.configure(state="normal")
            sac1_e.delete('1.0', END)

            sac1_e.configure(state="disable")

            sac2_e.configure(state="normal")
            sac2_e.delete('1.0', END)

            sac2_e.configure(state='disable')

            sac3_e.configure(state="normal")
            sac3_e.delete('1.0', END)

            sac3_e.configure(state="disable")

            sac4_e.configure(state="normal")
            sac4_e.delete('1.0', END)

            sac4_e.configure(state='disable')

            total_bill_txt.configure(state='normal')
            total_bill_txt.delete(0, END)
            total_bill_txt.configure(state='disable')

            messagebox.showinfo("BILL ID "+bill_id_new,
                                "Bill generated successfully !")

            bill_qry = "select `bill_id` from bill_details;"
            bill_list_df = pd.read_sql(bill_qry, mycon)
            bill_list_all = bill_list_df['bill_id'].tolist()

            bill_id_new = ''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
            while bill_id_new in bill_list_all:
                bill_id_new = ''.join(random.choices(
                    string.ascii_letters + string.digits, k=8))

            c_bill_txt.configure(state='normal')
            if len(c_bill_txt.get()) > 0:
                c_bill_txt.delete(0, END)

            c_bill_txt.insert(0, bill_id_new)
            c_bill_txt.configure(state='disable')

            generate_btn_lbl.configure(state='normal')

        else:

            messagebox.showinfo("CANNOT GENERATE BILL",
                                "Fill all the details/ add some items first !")

    show_frame()

    generate_btn_lbl = Button(generate_btn, text="Generate Bill", width=20, font=(
        'arial', 14, 'bold'), command=generate_bill_main, bg=btn_p_bg, fg=btn_p_fg,  borderwidth='4')
    generate_btn_lbl.grid(row=0, column=0, pady=5, padx=3)

    total_btn_lbl = Button(total_btn, text="TOTAL AMOUNT", width=20, font=(
        'arial', 14, 'bold'), command=total_amt_bill_gen,  borderwidth='4')
    total_btn_lbl.grid(row=0, column=0, pady=5, padx=3)

    Button(manual_mode, text="ADD ITEM", width=15,  borderwidth='4', font=('arial', 12, 'bold'),
           command=add_product_tobill).grid(row=0, column=2, pady=3, padx=5)

    Button(manual_mode, text="REMOVE", width=15,  borderwidth='4', font=('arial', 12, 'bold'),
           command=remove_item_frombill).grid(row=1, column=2, pady=3, padx=5)


def product_frame_funct():
    global nd11, qd11, md11, cd11, pid11, bd11, fpdf, cur, mycon, is_barcode_in_db, cam1, cam2, song

    is_barcode_in_db = False
    db_conn_funct()  # db connection open
    show_all_query = "select * from product;"
    fpdf = pd.read_sql(show_all_query, mycon)

    global capp, cap, cnt_temp_chutiya, cam_toggle_product

    if cam1:
        cam1 = False
        cap.release()

    cam2 = True
    cam_toggle_product = True

    F2 = LabelFrame(load_product_frame, fg=mid_fg, bg=mid_bg)
    F2.place(x=0, y=0, relwidth=1)

    barcode = LabelFrame(F2, fg=mid_fg, bg=mid_fg,
                         relief="raised", borderwidth=0)
    barcode.grid(row=0, column=1, padx=5, pady=3)

    details = LabelFrame(F2, fg=us_fg, bg=dk_bg, height=510, borderwidth=0)
    details.grid(row=0, column=0, padx=20, pady=26)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    name_detail.grid(row=0, column=0, padx=15, pady=25)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    cost_detail.grid(row=1, column=1, padx=15, pady=25)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    mrp_detail.grid(row=1, column=0, padx=15, pady=25)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    quant_detail.grid(row=0, column=1, padx=15, pady=25)

    pid_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    pid_detail.grid(row=2, column=0, padx=15, pady=25)

    barcode_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    barcode_detail.grid(row=2, column=1, padx=15, pady=25)

    Label(name_detail, text="PRODUCT NAME", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    nd11 = Entry(name_detail, width=15, font='arial 15')
    nd11.grid(row=1, column=0, padx=15, pady=20)

    Label(quant_detail, text="QUANTITY", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    qd11 = Entry(quant_detail, width=15, font='arial 15')
    qd11.grid(row=1, column=0, padx=15, pady=20)

    Label(mrp_detail, text="MRP", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    md11 = Entry(mrp_detail, width=15, font='arial 15')
    md11.grid(row=1, column=0, padx=15, pady=20)

    Label(cost_detail, text="COST", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    cd11 = Entry(cost_detail, width=15, font='arial 15')
    cd11.grid(row=1, column=0, padx=15, pady=20)

    Label(pid_detail, text="PID", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    pid11 = Entry(pid_detail, width=15, font='arial 15')
    pid11.grid(row=1, column=0, padx=15, pady=20)

    Label(barcode_detail, text="BARCODE", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    bd11 = Entry(barcode_detail, width=15, font='arial 15', state="disable")
    bd11.grid(row=1, column=0, padx=15, pady=20)

    barcode_lbl = Label(barcode, text="Barcode", bg=us_bg, fg=us_fg, font=(
        'Helvetica', 15, 'bold'), width=50, height=20)
    barcode_lbl.grid(row=0, column=0, padx=100)

    lmain = Label(barcode_lbl)
    lmain.grid(row=0, column=0, padx=60, pady=50)

    capp = cv2.VideoCapture(0)

    def show_frame():
        global bd11, myData, is_barcode_in_db, song, nd11, qd11, md11, cd11, pid11, fpdf, cur, mycon

        _, img = capp.read()
        img = cv2.resize(img, (400, 350))
        frame = cv2.flip(img, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        hhh = ii.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=hhh)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)

        for barcode in decode(img):

            myData = barcode.data.decode('utf-8')
            bd11.configure(state="normal")
            bd11.delete(0, END)
            bd11.insert(0, myData)
            bd11.configure(state="disable")
            show_all_query111 = "select * from product where `barcode` = '%s';" % (
                myData,)
            fpdf111 = pd.read_sql(show_all_query111, mycon)
            if myData in fpdf111['barcode'].tolist():

                if len(nd11.get()) > 0:
                    nd11.delete(0, END)
                if len(md11.get()) > 0:
                    md11.delete(0, END)
                if len(cd11.get()) > 0:
                    cd11.delete(0, END)
                if len(pid11.get()) > 0:
                    pid11.delete(0, END)
                if len(bd11.get()) > 0:
                    bd11.configure(state="normal")
                    bd11.delete(0, END)
                    bd11.configure(state="disable")
                if len(qd11.get()) > 0:
                    qd11.delete(0, END)

                is_barcode_in_db = False
            else:
                is_barcode_in_db = True
                pygame.mixer.init()
                pygame.mixer.music.load("scanner_sound.mp3")
                pygame.mixer.music.play()

            time.sleep(1.2)

    show_frame()

    def update_product_db():
        global nd11, qd11, md11, cd11, pid11, bd11, fpdf, cur, mycon, is_barcode_in_db
        show_all_query = "select * from product;"
        fpdf = pd.read_sql(show_all_query, mycon)

        if len(nd11.get()) > 0 and len(qd11.get()) > 0 and len(md11.get()) > 0 and len(cd11.get()) > 0 and len(pid11.get()) > 0 and len(bd11.get()) > 0:
            nd, qd, md, cd, pid, bd = str(nd11.get()), int(qd11.get()), int(
                md11.get()), int(cd11.get()), str(pid11.get()), str(bd11.get())
            date_now = date.today()
            profit_product = (int(md) - int(cd))

            pid_db = fpdf['pid'].tolist()

            if pid in pid_db:
                nd11.delete(0, END)

                md11.delete(0, END)

                cd11.delete(0, END)

                pid11.delete(0, END)
                bd11.configure(state="normal")
                bd11.delete(0, END)
                bd11.configure(state="disable")
                qd11.delete(0, END)
                messagebox.showinfo("PRODUCT ALREADY IN INVENTORY",
                                    "Pls go to Edit/Delete Page to update existing data !")

            else:
                sold = 0
                qry_add_product = "INSERT INTO `product` (`pname`, `barcode`, `mrp`, `cost`, `quantity`, `profit`, `sold`, `date_added`,`pid`) VALUES ('%s','%s', %s, %s, %s, %s, %s,'%s','%s') ;" % (
                    nd, bd, md, cd, qd, profit_product, sold, date_now, pid,)
                cur.execute(qry_add_product)
                mycon.commit()
                nd11.delete(0, END)

                md11.delete(0, END)

                cd11.delete(0, END)

                pid11.delete(0, END)
                bd11.configure(state="normal")
                bd11.delete(0, END)
                bd11.configure(state="disable")
                qd11.delete(0, END)
                messagebox.showinfo("SUCCESS", "Product added to inventory !")
                fpdf = pd.read_sql(show_all_query, mycon)

        else:
            messagebox.showinfo(
                "Alert", "Pls fill all the details before adding to inventory")
    Button(details, text="ADD PRODUCT", width=17, font=('arial', 15, 'bold'),
           background=btn_p_bg, borderwidth=4, relief=RAISED, foreground=btn_p_fg, command=update_product_db).grid(row=3, column=0, pady=14, padx=5, columnspan=2)


def view_product_screen():
    global pid_view_e, mycon, cur, sac1_e, sac2_e, sac3_e, sac4_e, sac5_e, sac6_e, sac7_e, cam1, cam2
    db_conn_funct()
    global capp, cap
    if cam1:
        cam1 = False
        cap.release()

    if cam2:
        cam2 = False
        capp.release()

      # db connection open
    show_all_query = "select * from product;"
    fpdf = pd.read_sql(show_all_query, mycon)

    F1 = LabelFrame(add_product_frame, fg=mid_fg, bg=mid_bg)
    F1.place(x=0, y=0, relwidth=1)

    fc1 = LabelFrame(F1, fg=us_fg, bg=us_bg, borderwidth=0, relief="raised")
    fc1.grid(row=0, column=0, padx=40, pady=3)

    F2 = LabelFrame(F1, fg=us_fg, bg=us_bg)
    F2.grid(row=1, column=0, padx=40, pady=10)

    details = LabelFrame(F2, fg=us_fg, bg=us_bg, height=510)
    details.grid(row=0, column=0)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    name_detail.grid(row=0, column=0)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    cost_detail.grid(row=0, column=1)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    mrp_detail.grid(row=0, column=2)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    quant_detail.grid(row=0, column=3)

    pid_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    pid_detail.grid(row=0, column=4)

    barcode_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    barcode_detail.grid(row=0, column=5)

    date_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    date_detail.grid(row=0, column=6)

    # ++++++++++++++++++++++++++++++++++

    def mult_view(*args):
        sac7_e.yview(*args)
        sac6_e.yview(*args)
        sac5_e.yview(*args)
        sac4_e.yview(*args)
        sac3_e.yview(*args)
        sac2_e.yview(*args)
        sac1_e.yview(*args)

    vsb = Scrollbar(F2)
    vsb.grid(row=0, column=1, sticky='ns')
    vsb.configure(command=mult_view)

    Label(name_detail, text="NAME", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac1_e = Text(name_detail, width=17, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac1_e.grid(row=1, column=0)

    Label(barcode_detail, text="BARCODE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac2_e = Text(barcode_detail, width=17, height=19,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac2_e.grid(row=1, column=0)

    Label(mrp_detail, text="MRP", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac3_e = Text(mrp_detail, width=13, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac3_e.grid(row=1, column=0)

    Label(cost_detail, text="COST", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac4_e = Text(cost_detail, width=13, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac4_e.grid(row=1, column=0)

    Label(quant_detail, text="QUANTITY", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac5_e = Text(quant_detail, width=13, height=19,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac5_e.grid(row=1, column=0)

    Label(pid_detail, text="PID", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac6_e = Text(pid_detail, width=13, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac6_e.grid(row=1, column=0)

    Label(date_detail, text="DATE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac7_e = Text(date_detail, width=16, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac7_e.grid(row=1, column=0)

    pname11 = fpdf['pname'].to_string(index=False)
    barcode11 = fpdf['barcode'].to_string(index=False)
    mrp11 = fpdf['mrp'].to_string(index=False)
    cost11 = fpdf['cost'].to_string(index=False)
    quantity11 = fpdf['quantity'].to_string(index=False)
    pid11 = fpdf['pid'].to_string(index=False)
    date_added11 = fpdf['date_added'].to_string(index=False)

    sac1_e.configure(state="normal")
    sac1_e.delete('1.0', END)
    sac1_e.insert('1.0', pname11)
    sac1_e.configure(state="disable")

    sac2_e.configure(state="normal")
    sac2_e.delete('1.0', END)
    sac2_e.insert('1.0', barcode11)
    sac2_e.configure(state='disable')

    sac3_e.configure(state="normal")
    sac3_e.delete('1.0', END)
    sac3_e.insert('1.0', mrp11)
    sac3_e.configure(state="disable")

    sac4_e.configure(state="normal")
    sac4_e.delete('1.0', END)
    sac4_e.insert('1.0', cost11)
    sac4_e.configure(state='disable')

    sac5_e.configure(state="normal")
    sac5_e.delete('1.0', END)
    sac5_e.insert('1.0', quantity11)
    sac5_e.configure(state='disable')

    sac6_e.configure(state="normal")
    sac6_e.delete('1.0', END)
    sac6_e.insert('1.0', pid11)
    sac6_e.configure(state="disable")

    sac7_e.configure(state="normal")
    sac7_e.delete('1.0', END)
    sac7_e.insert('1.0', date_added11)
    sac7_e.configure(state="disable")

    def save_inv_tocsv():
        fpdf.to_csv('inventory.csv')
        messagebox.showinfo("SUCCESS", "Inventory Saved as inventory.csv")

    def view_products_simple():
        global pid_view_e, pname11, barcode11, mrp11, cost11, quantity11, pid11, date_added11, sac1_e, sac2_e, sac3_e, sac4_e, sac5_e, sac6_e, sac7_e
        pid11 = str(pid_view_e.get())
        qry_main = "select * from product where `pid` = '%s' ;" % (pid11)
        fpdf = pd.read_sql(qry_main, mycon)
        if fpdf.empty:
            pid_view_e.delete(0, END)
            messagebox.showinfo(
                "INVALID PID", "No product with such PID found !")
        else:
            pname11 = fpdf['pname'].to_string(index=False)
            barcode11 = fpdf['barcode'].to_string(index=False)
            mrp11 = fpdf['mrp'].to_string(index=False)
            cost11 = fpdf['cost'].to_string(index=False)
            quantity11 = fpdf['quantity'].to_string(index=False)
            pid11 = fpdf['pid'].to_string(index=False)
            date_added11 = fpdf['date_added'].to_string(index=False)

            sac1_e.configure(state="normal")
            sac1_e.delete('1.0', END)
            sac1_e.insert('1.0', pname11)
            sac1_e.configure(state="disable")

            sac2_e.configure(state="normal")
            sac2_e.delete('1.0', END)
            sac2_e.insert('1.0', barcode11)
            sac2_e.configure(state='disable')

            sac3_e.configure(state="normal")
            sac3_e.delete('1.0', END)
            sac3_e.insert('1.0', mrp11)
            sac3_e.configure(state="disable")

            sac4_e.configure(state="normal")
            sac4_e.delete('1.0', END)
            sac4_e.insert('1.0', cost11)
            sac4_e.configure(state='disable')

            sac5_e.configure(state="normal")
            sac5_e.delete('1.0', END)
            sac5_e.insert('1.0', quantity11)
            sac5_e.configure(state='disable')

            sac6_e.configure(state="normal")
            sac6_e.delete('1.0', END)
            sac6_e.insert('1.0', pid11)
            sac6_e.configure(state="disable")

            sac7_e.configure(state="normal")
            sac7_e.delete('1.0', END)
            sac7_e.insert('1.0', date_added11)
            sac7_e.configure(state="disable")

    manual_mode = LabelFrame(fc1, fg=us_fg, bg=us_bg, borderwidth=0)
    manual_mode.grid(row=0, column=0, padx=15, pady=15)

    Label(manual_mode, text="PRODUCT ID", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    pid_view_e = Entry(manual_mode, width=15, font='arial 15')
    pid_view_e.grid(row=1, column=0, padx=5, pady=8)

    Button(manual_mode, text="SEARCH", width=15, font=('arial', 12, 'bold'),
           command=view_products_simple, borderwidth='4',
           background=btn_p_bg,
           foreground=btn_p_fg).grid(row=0, column=2, pady=3, padx=5)
    Button(manual_mode, text="SAVE AS CSV", borderwidth=4, width=15, font=('arial', 12,
           'bold'), command=save_inv_tocsv).grid(row=1, column=2, pady=3, padx=5)


def edit_del_pro():
    global mycon, cur, pid_checkrrr, cam1, cam2
    global capp, cap
    if cam1:
        cam1 = False
        cap.release()

    if cam2:
        cam2 = False
        capp.release()

    db_conn_funct()

    F1 = LabelFrame(del_product_frame, fg=mid_fg, bg=mid_bg)
    F1.place(x=0, y=0, relwidth=1)
    fc1 = LabelFrame(F1, fg=us_fg, bg=us_bg)
    fc1.grid(row=0, column=0, padx=80, pady=24)

    fc2 = LabelFrame(F1, fg=us_fg, bg=dk_bg)
    fc2.grid(row=1, column=0, padx=250, pady=3)

    manual_mode = LabelFrame(fc1, fg=us_fg, bg=us_bg,
                             borderwidth=0, relief="raised")
    manual_mode.grid(row=0, column=0, padx=15, pady=15)

    Label(manual_mode, text="PRODUCT ID", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    pid_checkrrr = Entry(manual_mode, width=15, font='arial 15')
    pid_checkrrr.grid(row=1, column=0, padx=5, pady=8)

    details = LabelFrame(fc2, fg=mid_fg, bg=dk_bg,
                         height=510, relief="raised", borderwidth=0)
    details.grid(row=0, column=0, padx=20, pady=26)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    name_detail.grid(row=0, column=0, padx=15, pady=25)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    cost_detail.grid(row=1, column=0, padx=15, pady=25)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    mrp_detail.grid(row=0, column=2, padx=15, pady=25)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    quant_detail.grid(row=0, column=1, padx=15, pady=25)

    pid_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    pid_detail.grid(row=1, column=1, padx=15, pady=25)

    barcode_detail = LabelFrame(details, fg=us_fg, bg=us_bg, relief="raised")
    barcode_detail.grid(row=1, column=2, padx=15, pady=25)

    global nd11, bd11, pd101, cd11, md11, qd11, pid111

    Label(name_detail, text="PRODUCT NAME", fg=us_fg, bg=us_bg, font=('Helvetica', 15, 'bold')).grid(row=0, column=0,
                                                                                                     pady=10)
    nd11 = Entry(name_detail, width=15, font='arial 15', state="disable")
    nd11.grid(row=1, column=0, padx=15, pady=20)

    Label(quant_detail, text="QUANTITY", fg=us_fg, bg=us_bg, font=('Helvetica', 15, 'bold')).grid(row=0, column=0,
                                                                                                  pady=10)
    qd11 = Entry(quant_detail, width=15, font='arial 15', state="disable")
    qd11.grid(row=1, column=0, padx=15, pady=20)

    Label(mrp_detail, text="MRP", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    md11 = Entry(mrp_detail, width=15, font='arial 15', state="disable")
    md11.grid(row=1, column=0, padx=15, pady=20)

    Label(cost_detail, text="COST", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    cd11 = Entry(cost_detail, width=15, font='arial 15', state="disable")
    cd11.grid(row=1, column=0, padx=15, pady=20)

    Label(pid_detail, text="PID", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    pd101 = Entry(pid_detail, width=15, font='arial 15', state="disable")
    pd101.grid(row=1, column=0, padx=15, pady=20)

    Label(barcode_detail, text="BARCODE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=10)
    bd11 = Entry(barcode_detail, width=15, font='arial 15', state="disable")
    bd11.grid(row=1, column=0, padx=15, pady=20)

    def search_product_to_del():
        global pid_checkrrr, nd11, bd11, pd101, cd11, md11, qd11, mycon, pid111
        pid111 = str(pid_checkrrr.get())

        qry_main = "select * from product where `pid` = '%s' ;" % (pid111)
        fpdf = pd.read_sql(qry_main, mycon)
        if fpdf.empty:
            pid_checkrrr.delete(0, END)
            messagebox.showinfo(
                "INVALID PID", "No product with such PID found !")
        else:
            pname11 = fpdf['pname'].to_string(index=False)
            barcode11 = fpdf['barcode'].to_string(index=False)
            mrp11 = fpdf['mrp'].to_string(index=False)
            cost11 = fpdf['cost'].to_string(index=False)
            quantity11 = fpdf['quantity'].to_string(index=False)
            pid11 = fpdf['pid'].to_string(index=False)

            nd11.configure(state="normal")
            nd11.delete(0, END)
            nd11.insert(0, pname11)

            bd11.configure(state="normal")
            bd11.delete(0, END)
            bd11.insert(0, barcode11)

            pd101.configure(state="normal")
            pd101.delete(0, END)
            pd101.insert(0, pid11)

            cd11.configure(state="normal")
            cd11.delete(0, END)
            cd11.insert(0, cost11)

            md11.configure(state="normal")
            md11.delete(0, END)
            md11.insert(0, mrp11)

            qd11.configure(state="normal")
            qd11.delete(0, END)
            qd11.insert(0, quantity11)

    def del_rec_perma():
        global nd11, bd11, pd101, cd11, md11, qd11, mycon, pid111, pid_checkrrr

        pid111 = str(pd101.get())

        qry_main = "delete from product where `pid` = '%s';" % (pid111,)
        cur.execute(qry_main)
        mycon.commit()

        nd11.delete(0, END)
        bd11.delete(0, END)
        pd101.delete(0, END)
        cd11.delete(0, END)
        md11.delete(0, END)
        qd11.delete(0, END)
        messagebox.showinfo("SUCCESS", "Product deleted from Inventory!")

    def upadte_records_db():
        global nd11, bd11, pd101, cd11, md11, qd11, mycon, pid111, pid_checkrrr

        pid111 = str(pid_checkrrr.get())

        nd111 = str(nd11.get())
        bd111 = str(bd11.get())
        pd1011 = str(pd101.get())
        cd111 = int(cd11.get())
        md111 = int(md11.get())
        qd111 = int(qd11.get())

        prt = int(md111) - int(cd111)
        date_now = date.today()
        qry_main = "UPDATE `product` SET `pname`='%s',`barcode`='%s',`mrp`=%s,`cost`=%s,`quantity`=%s,`profit`=%s,`date_added`='%s',`pid`='%s' WHERE `pid` = '%s';" % (
            nd111, bd111, md111, cd111, qd111, prt, date_now, pd1011, pid111,)
        cur.execute(qry_main)
        mycon.commit()

        nd11.delete(0, END)
        bd11.delete(0, END)
        pd101.delete(0, END)
        cd11.delete(0, END)
        md11.delete(0, END)
        qd11.delete(0, END)
        messagebox.showinfo(
            "SUCCESS", "Product details successfully updated !")

    Button(manual_mode, text="SEARCH", width=15, font=('arial', 12, 'bold'),
           command=search_product_to_del, borderwidth='4',
           background=btn_p_bg,
           foreground=btn_p_fg).grid(row=0, column=1, pady=3, padx=5, rowspan=2)

    Button(details, text="UPDATE", width=15, font=('arial', 12, 'bold'),
           command=upadte_records_db, borderwidth='4').grid(row=3, column=0, pady=14, padx=5, columnspan=2)
    Button(details, text="DELETE", width=15, font=('arial', 12, 'bold'),
           command=del_rec_perma, borderwidth='4').grid(row=3, column=1, pady=14, padx=5, columnspan=2)

# ==============================================================================


def about_app_dev():
    global cam1, cam2, capp, cap

    if cam1:
        cam1 = False
        cap.release()

        # print("cap released")
    if cam2:
        cam2 = False
        capp.release()

    # =======================

    def resize_image_abtus(event):
        new_width = event.width
        new_height = event.height
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # avoid garbage collection

    image = ii.open("bg.png")
    copy_of_image = image.copy()
    photo = ImageTk.PhotoImage(image)
    label = ttk.Label(about_us_frame, image=photo)
    label.bind('<Configure>', resize_image_abtus)
    label.pack(fill=BOTH, expand=YES)

# ******************************************************************************
# ------------ stats -------------------------


def stats_main_all():  # bill all function
    global cam1, cam2, capp, cap
    global sac1_e, sac2_e, sac3_e, sac4_e, sac5_e, sac6_e, sac7_e
    if cam1:
        cam1 = False
        cap.release()

    if cam2:
        cam2 = False
        capp.release()

    F1 = LabelFrame(statistics_frame, fg=mid_fg, bg=mid_bg)
    F1.place(x=0, y=0, relwidth=1)

    F2 = LabelFrame(F1, fg=mid_fg, bg=mid_bg)
    F2.grid(row=1, column=0, padx=5, pady=3)

    details = LabelFrame(F2, fg=us_fg, bg=us_bg, height=510)
    details.grid(row=0, column=0)

    name_detail = LabelFrame(details,  fg=us_fg, bg=us_bg)
    name_detail.grid(row=0, column=0)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    cost_detail.grid(row=0, column=1)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    mrp_detail.grid(row=0, column=2)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    quant_detail.grid(row=0, column=3)

    pid_detail = LabelFrame(details,  fg=us_fg, bg=us_bg)
    pid_detail.grid(row=0, column=4)

    barcode_detail = LabelFrame(details,  fg=us_fg, bg=us_bg)
    barcode_detail.grid(row=0, column=5)

    date_detail = LabelFrame(details,  fg=us_fg, bg=us_bg)
    date_detail.grid(row=0, column=6)

    # ++++++++++++++++++++++++++++++++++

    def mult_view(*args):
        sac7_e.yview(*args)
        sac6_e.yview(*args)
        sac5_e.yview(*args)
        sac4_e.yview(*args)
        sac3_e.yview(*args)
        sac2_e.yview(*args)
        sac1_e.yview(*args)

    vsb = Scrollbar(F2)
    vsb.grid(row=0, column=1, sticky='ns')
    vsb.configure(command=mult_view)

    Label(name_detail, text="BILL ID",  fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac1_e = Text(name_detail, width=17, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac1_e.grid(row=1, column=0)

    Label(barcode_detail, text="ITEMS", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac2_e = Text(barcode_detail, width=10, height=19,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac2_e.grid(row=1, column=0)

    Label(mrp_detail, text="BILL AMT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac3_e = Text(mrp_detail, width=13, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac3_e.grid(row=1, column=0)

    Label(cost_detail, text="BILL PROFIT", fg=us_fg, bg=us_bg,
          font=('Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac4_e = Text(cost_detail, width=13, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac4_e.grid(row=1, column=0)

    Label(quant_detail, text="DATE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac5_e = Text(quant_detail, width=17, height=19,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac5_e.grid(row=1, column=0)

    Label(pid_detail, text="CUSTOMER", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac6_e = Text(pid_detail, width=28, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac6_e.grid(row=1, column=0)

    Label(date_detail, text="DISCOUNT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac7_e = Text(date_detail, width=10, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac7_e.grid(row=1, column=0)

    qry_main = 'select * from bill_details;'
    main_df_all = pd.read_sql(qry_main, mycon)

    bill_id_all = main_df_all['bill_id'].to_string(index=False)
    items_all = main_df_all['items'].to_string(index=False)
    bill_price_all = main_df_all['bill_price'].to_string(index=False)
    bill_profit_all = main_df_all['bill_profit'].to_string(index=False)
    bill_date_all = main_df_all['bill_date'].to_string(index=False)
    c_name_all = main_df_all['c_name'].to_string(index=False)
    dis_all = main_df_all['discount'].to_string(index=False)

    sac1_e.configure(state="normal")
    sac1_e.delete('1.0', END)
    sac1_e.insert('1.0', bill_id_all)
    sac1_e.configure(state="disable")

    sac2_e.configure(state="normal")
    sac2_e.delete('1.0', END)
    sac2_e.insert('1.0', items_all)
    sac2_e.configure(state='disable')

    sac3_e.configure(state="normal")
    sac3_e.delete('1.0', END)
    sac3_e.insert('1.0', bill_price_all)
    sac3_e.configure(state="disable")

    sac4_e.configure(state="normal")
    sac4_e.delete('1.0', END)
    sac4_e.insert('1.0', bill_profit_all)
    sac4_e.configure(state='disable')

    sac5_e.configure(state="normal")
    sac5_e.delete('1.0', END)
    sac5_e.insert('1.0', bill_date_all)
    sac5_e.configure(state='disable')

    sac6_e.configure(state="normal")
    sac6_e.delete('1.0', END)
    sac6_e.insert('1.0', c_name_all)
    sac6_e.configure(state="disable")

    sac7_e.configure(state="normal")
    sac7_e.delete('1.0', END)
    sac7_e.insert('1.0', dis_all)
    sac7_e.configure(state="disable")

    fc1 = LabelFrame(F1,  fg=us_fg, bg=us_bg)
    fc1.grid(row=0, column=0, padx=40, pady=3)

    def save_inv_tocsv():
        main_df_all.to_csv('bills.csv')
        messagebox.showinfo("SUCCESS", "Saved as bills.csv")

    def view_products_simple():
        global sac1_e, sac2_e, sac3_e, sac4_e, sac5_e, sac6_e, sac7_e
        pid11 = str(pid_view_e.get())
        qry_main = "select * from bill_details where `bill_id` = '%s' ;" % (
            pid11,)
        main_df_all = pd.read_sql(qry_main, mycon)
        if main_df_all.empty:
            pid_view_e.delete(0, END)
            messagebox.showinfo("INVALID Bill ID",
                                "No Bill with such BILL ID found !")
        else:
            bill_id_all = main_df_all['bill_id'].to_string(index=False)
            items_all = main_df_all['items'].to_string(index=False)
            bill_price_all = main_df_all['bill_price'].to_string(index=False)
            bill_profit_all = main_df_all['bill_profit'].to_string(index=False)
            bill_date_all = main_df_all['bill_date'].to_string(index=False)
            c_name_all = main_df_all['c_name'].to_string(index=False)
            dis_all = main_df_all['discount'].to_string(index=False)

            sac1_e.configure(state="normal")
            sac1_e.delete('1.0', END)
            sac1_e.insert('1.0', bill_id_all)
            sac1_e.configure(state="disable")

            sac2_e.configure(state="normal")
            sac2_e.delete('1.0', END)
            sac2_e.insert('1.0', items_all)
            sac2_e.configure(state='disable')

            sac3_e.configure(state="normal")
            sac3_e.delete('1.0', END)
            sac3_e.insert('1.0', bill_price_all)
            sac3_e.configure(state="disable")

            sac4_e.configure(state="normal")
            sac4_e.delete('1.0', END)
            sac4_e.insert('1.0', bill_profit_all)
            sac4_e.configure(state='disable')

            sac5_e.configure(state="normal")
            sac5_e.delete('1.0', END)
            sac5_e.insert('1.0', bill_date_all)
            sac5_e.configure(state='disable')

            sac6_e.configure(state="normal")
            sac6_e.delete('1.0', END)
            sac6_e.insert('1.0', c_name_all)
            sac6_e.configure(state="disable")

            sac7_e.configure(state="normal")
            sac7_e.delete('1.0', END)
            sac7_e.insert('1.0', dis_all)
            sac7_e.configure(state="disable")

    manual_mode = LabelFrame(fc1,  fg=us_fg, bg=us_bg, borderwidth=0)
    manual_mode.grid(row=0, column=0, padx=15, pady=15)

    Label(manual_mode, text="BILL ID",  fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    pid_view_e = Entry(manual_mode, width=15, font='arial 15')
    pid_view_e.grid(row=1, column=0, padx=5, pady=8)

    Button(manual_mode, text="SEARCH", width=15, borderwidth='4', background=btn_p_bg,
           foreground=btn_p_fg, font=('arial', 12, 'bold'), command=view_products_simple).grid(row=0,
                                                                                               column=2,
                                                                                               pady=3,
                                                                                               padx=5)

    Button(manual_mode, text="SAVE AS CSV", borderwidth='4', width=15, font=('arial', 12,
           'bold'), command=save_inv_tocsv).grid(row=1, column=2, pady=3, padx=5)


def dashboard_main_analysis():
    global cam1, cam2, capp, cap, mycon, cur

    if cam1:
        cam1 = False
        cap.release()

    if cam2:
        cam2 = False
        capp.release()

    F1 = LabelFrame(dashboard_frame, fg=mid_fg, bg=mid_bg)
    F1.place(x=0, y=0, relwidth=1)

    F2 = LabelFrame(F1, fg=us_fg, bg=dk_bg, borderwidth=0)
    F2.grid(row=0, column=0, padx=30, pady=25)

    F3 = LabelFrame(F1, fg=mid_fg, bg=us_bg)
    F3.grid(row=1, column=0, pady=25, padx=5)

    rev_month = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    rev_month.grid(row=0, column=0, pady=8, padx=10)

    prof_month = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    prof_month.grid(row=0, column=1, pady=8, padx=10)

    sold_month = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    sold_month.grid(row=0, column=2, pady=8, padx=10)

    top_pro_month = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    top_pro_month.grid(row=0, column=4, pady=8, padx=10)

    rev_today = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    rev_today.grid(row=1, column=0, pady=8, padx=10)

    prof_today = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    prof_today.grid(row=1, column=1, pady=8, padx=10)

    sold_today = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    sold_today.grid(row=1, column=2, pady=8, padx=10)

    stock_avail = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    stock_avail.grid(row=1, column=3, pady=8, padx=10)

    supr_cust = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    supr_cust.grid(row=1, column=4, pady=8, padx=10)

    cust_count = LabelFrame(F2, fg=us_fg, bg=us_bg, relief="raised")
    cust_count.grid(row=0, column=3, pady=8, padx=10)

    Label(rev_month, text="MONTHLY REVENUE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    rev_month_txt = Entry(rev_month, width=17,
                          font='arial 15', state="disable")
    rev_month_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(prof_month, text="MONTHLY PROFIT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    prof_month_txt = Entry(prof_month, width=17,
                           font='arial 15', state="disable")
    prof_month_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(sold_month, text="MONTHLY SALES", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    sold_month_txt = Entry(sold_month, width=17,
                           font='arial 15', state="disable")
    sold_month_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(top_pro_month, text="AVERAGE BILL AMT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    top_pro_month_txt = Entry(top_pro_month, width=17,
                              font='arial 15', state="disable")
    top_pro_month_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(rev_today, text="TODAY'S REVENUE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=15)
    rev_today_txt = Entry(rev_today, width=17,
                          font='arial 15', state="disable")
    rev_today_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(prof_today, text="TODAY'S PROFIT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    prof_today_txt = Entry(prof_today, width=17,
                           font='arial 15', state="disable")
    prof_today_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(sold_today, text="TODAY'S SALES", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    sold_today_txt = Entry(sold_today, width=17,
                           font='arial 15', state="disable")
    sold_today_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(stock_avail, text="STOCK", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    stock_avail_txt = Entry(stock_avail, width=17,
                            font='arial 15', state="disable")
    stock_avail_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(cust_count, text="CUSTOMERS", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    cust_count_txt = Entry(cust_count, width=17,
                           font='arial 15', state="disable")
    cust_count_txt.grid(row=1, column=0, pady=8, padx=10)

    Label(supr_cust, text="PRO CUSTOMERS", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0, pady=8, padx=10)
    supr_cust_txt = Entry(supr_cust, width=17,
                          font='arial 15', state="disable")
    supr_cust_txt.grid(row=1, column=0, pady=8, padx=10)

    # -------- adding values ---------

    today_date = date.today()
    month_this = today_date.month

    qry_main = "select SUM(`bill_price`) as 'rev_monthly' from bill_details where MONTH(`bill_date`) = '%s';" % (
        month_this,)
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['rev_monthly'].to_string(index=False)

    rev_month_txt.configure(state=NORMAL)
    if len(rev_month_txt.get()) > 0:
        rev_month_txt.delete(0, END)
    rev_month_txt.insert(0, rev_month_this)
    rev_month_txt.configure(state=DISABLED)

    qry_main = "select SUM(`bill_profit`) as 'prof_monthly' from bill_details where MONTH(`bill_date`) = '%s';" % (
        month_this,)
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['prof_monthly'].to_string(index=False)

    prof_month_txt.configure(state=NORMAL)
    if len(prof_month_txt.get()) > 0:
        prof_month_txt.delete(0, END)
    prof_month_txt.insert(0, rev_month_this)
    prof_month_txt.configure(state=DISABLED)

    qry_main = "select SUM(`items`) as 'items_sold' from bill_details where MONTH(`bill_date`) = '%s';" % (
        month_this,)
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['items_sold'].to_string(index=False)

    sold_month_txt.configure(state=NORMAL)
    if len(sold_month_txt.get()) > 0:
        sold_month_txt.delete(0, END)
    sold_month_txt.insert(0, rev_month_this)
    sold_month_txt.configure(state=DISABLED)

    qry_main = "select ROUND(AVG(`bill_price`)) as 'avg_bill_amt' from bill_details;"
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['avg_bill_amt'].to_string(index=False)

    top_pro_month_txt.configure(state=NORMAL)
    if len(top_pro_month_txt.get()) > 0:
        top_pro_month_txt.delete(0, END)
    top_pro_month_txt.insert(0, rev_month_this)
    top_pro_month_txt.configure(state=DISABLED)

    qry_main = "select SUM(`bill_price`) as 'rev_daily' from bill_details where `bill_date` = '%s';" % (
        today_date,)
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['rev_daily'].to_string(index=False)

    rev_today_txt.configure(state=NORMAL)
    if len(rev_today_txt.get()) > 0:
        rev_today_txt.delete(0, END)
    rev_today_txt.insert(0, rev_month_this)
    rev_today_txt.configure(state=DISABLED)

    qry_main = "select SUM(`bill_profit`) as 'prof_daily' from bill_details where `bill_date` = '%s';" % (
        today_date,)
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['prof_daily'].to_string(index=False)

    prof_today_txt.configure(state=NORMAL)
    if len(prof_today_txt.get()) > 0:
        prof_today_txt.delete(0, END)
    prof_today_txt.insert(0, rev_month_this)
    prof_today_txt.configure(state=DISABLED)

    qry_main = "select SUM(`items`) as 'items_sold_today' from bill_details where `bill_date` = '%s';" % (
        today_date,)
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['items_sold_today'].to_string(index=False)

    sold_today_txt.configure(state=NORMAL)
    if len(sold_today_txt.get()) > 0:
        sold_today_txt.delete(0, END)
    sold_today_txt.insert(0, rev_month_this)
    sold_today_txt.configure(state=DISABLED)

    qry_main = "select SUM(`quantity`) as 'stock_available' from product;"
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['stock_available'].to_string(index=False)

    stock_avail_txt.configure(state=NORMAL)
    if len(stock_avail_txt.get()) > 0:
        stock_avail_txt.delete(0, END)
    stock_avail_txt.insert(0, rev_month_this)
    stock_avail_txt.configure(state=DISABLED)

    qry_main = "select COUNT(DISTINCT `c_email`) as 'cust_total' from bill_details;"
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['cust_total'].to_string(index=False)

    cust_count_txt.configure(state=NORMAL)
    if len(cust_count_txt.get()) > 0:
        cust_count_txt.delete(0, END)
    cust_count_txt.insert(0, rev_month_this)
    cust_count_txt.configure(state=DISABLED)

    qry_main = "select count(DISTINCT `c_email`) as pro_cust_cnt from bill_details where `bill_price` > (select ROUND(AVG(`bill_price`)) from bill_details);"
    df_main = pd.read_sql(qry_main, mycon)
    rev_month_this = df_main['pro_cust_cnt'].to_string(index=False)

    supr_cust_txt.configure(state=NORMAL)
    if len(supr_cust_txt.get()) > 0:
        supr_cust_txt.delete(0, END)
    supr_cust_txt.insert(0, rev_month_this)
    supr_cust_txt.configure(state=DISABLED)

    grp1 = LabelFrame(F3, fg=us_fg, bg=us_bg)  # top 5 items
    grp1.grid(row=0, column=0)

    grp2 = LabelFrame(F3, fg=us_fg, bg=us_bg)  # daily sales graph (line)
    grp2.grid(row=0, column=1, padx=14)

    grp3 = LabelFrame(F3, fg=us_fg, bg=us_bg)  # weekly sale (pie)
    grp3.grid(row=0, column=2)

    # chart 1 _______________

    qry_data1 = "select `pname`, `sold` from stats order by `sold` desc limit 5;"
    df_top5 = pd.read_sql(qry_data1, mycon)

    figure1 = plt.Figure(figsize=(4, 3), dpi=100)
    ax1 = figure1.add_subplot(111)
    figure1.autofmt_xdate(rotation=15, ha='center')
    ax1.bar(df_top5['pname'].tolist(), df_top5['sold'].tolist())
    bar1 = FigureCanvasTkAgg(figure1, grp1)
    bar1.get_tk_widget().grid(row=0, column=0)
    ax1.set_title('TOP 5 BESTSELLERS')
    ax1.tick_params(axis='x', labelsize=6)
    ax1.tick_params(axis='y', labelsize=6)

# ====== graph ===========

    qry_data2 = "select DAY(`bill_date`) as 'today_date', SUM(`bill_price`) as 'today_sale', SUM(`bill_profit`) as 'today_profit' from bill_details group by DAY(`bill_date`);"
    df_mosa = pd.read_sql(qry_data2, mycon)

    figure2 = plt.Figure(figsize=(4, 3), dpi=100)
    ax2 = figure2.add_subplot(111)
    figure2.autofmt_xdate(rotation=15, ha='center')
    ax2.plot(df_mosa['today_date'].tolist(),
             df_mosa['today_sale'].tolist(), label='revenue')
    ax2.plot(df_mosa['today_date'].tolist(
    ), df_mosa['today_profit'].tolist(), color='green', label='profit')

    bar2 = FigureCanvasTkAgg(figure2, grp2)
    bar2.get_tk_widget().grid(row=0, column=0)
    ax2.set_title('DAILY REVENUE & PROFIT')
    ax2.tick_params(axis='x', labelsize=6)
    ax2.tick_params(axis='y', labelsize=6)

    ax2.set_xticks(df_mosa['today_date'].tolist())
    ax2.set_xlabel('Days of month : ' + today_date.strftime("%B"))
    ax2.legend()
# ===================== graph 3 =========================

    qry_data3 = "select DAYNAME(`bill_date`) as 'week_date', SUM(`bill_price`) as 'week_sale',SUM(`bill_profit`) as 'week_profit' from bill_details group by DAYNAME(`bill_date`) order by DAYOFWEEK(`bill_date`) ;"
    df_wesa = pd.read_sql(qry_data3, mycon)

    x_asdasd = np.arange(len(df_wesa))

    figure3 = plt.Figure(figsize=(4, 3), dpi=100)
    ax3 = figure3.add_subplot(111)
    figure3.autofmt_xdate(rotation=15, ha='center')
    ax3.bar(x_asdasd-0.2, df_wesa['week_sale'],
            color='blue', width=0.4, label='revenue')
    ax3.bar(x_asdasd+0.2, df_wesa['week_profit'],
            color='green', width=0.4, label='profit')
    bar3 = FigureCanvasTkAgg(figure3, grp3)
    bar3.get_tk_widget().grid(row=0, column=0)
    ax3.set_title('WEEKLY ANALYSIS')
    ax3.tick_params(axis='x', labelsize=6)
    ax3.tick_params(axis='y', labelsize=6)

    ax3.set_xticks(df_wesa.index, df_wesa['week_date'])
    ax3.legend()


def sales_analysis_main():
    global cam1, cam2, capp, cap
    global sac1_e, sac3_e, sac4_e, sac5_e, sac6_e
    if cam1:
        cam1 = False
        cap.release()

    if cam2:
        cam2 = False
        capp.release()

    F1 = LabelFrame(sales_frame, fg=mid_fg, bg=mid_bg)
    F1.place(x=0, y=0, relwidth=1)

    F2 = LabelFrame(F1, fg=mid_fg, bg=mid_bg)
    F2.grid(row=1, column=0, padx=60, pady=10)

    details = LabelFrame(F2, fg=mid_fg, bg=mid_bg, height=510)
    details.grid(row=0, column=0)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    name_detail.grid(row=0, column=0)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    cost_detail.grid(row=0, column=1)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    mrp_detail.grid(row=0, column=2)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    quant_detail.grid(row=0, column=3)

    pid_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    pid_detail.grid(row=0, column=4)

    # ++++++++++++++++++++++++++++++++++

    def mult_view(*args):

        sac6_e.yview(*args)
        sac5_e.yview(*args)
        sac4_e.yview(*args)
        sac3_e.yview(*args)
        sac1_e.yview(*args)

    vsb = Scrollbar(F2)
    vsb.grid(row=0, column=1, sticky='ns')
    vsb.configure(command=mult_view)

    Label(name_detail, text="BILL ID", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac1_e = Text(name_detail, width=17, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac1_e.grid(row=1, column=0)

    Label(mrp_detail, text="ITEM NAME", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac3_e = Text(mrp_detail, width=23, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac3_e.grid(row=1, column=0)

    Label(cost_detail, text="QUANTITY", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac4_e = Text(cost_detail, width=17, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac4_e.grid(row=1, column=0)

    Label(quant_detail, text="PROFIT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac5_e = Text(quant_detail, width=17, height=19,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac5_e.grid(row=1, column=0)

    Label(pid_detail, text="BARCODE", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac6_e = Text(pid_detail, width=23, height=19, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac6_e.grid(row=1, column=0)

    qry_main = 'select * from sales;'
    main_df_all = pd.read_sql(qry_main, mycon)

    bill_id_all = main_df_all['bill_id'].to_string(index=False)
    bill_price_all = main_df_all['pname'].to_string(index=False)
    bill_profit_all = main_df_all['quantity'].to_string(index=False)
    bill_date_all = main_df_all['profit_pp'].to_string(index=False)
    c_name_all = main_df_all['barcode'].to_string(index=False)

    bis_list = []
    bis_list[:0] = bill_id_all.split('\n')
    bis_list_main = bis_list

    if len(bis_list_main) > 1:

        bpa_list = []
        bpa_list[:0] = bill_price_all.split('\n')

        bpra_list = []
        bpra_list[:0] = bill_profit_all.split('\n')

        bda_list = []
        bda_list[:0] = bill_date_all.split('\n')

        cna_list = []
        cna_list[:0] = c_name_all.split('\n')

        # -------------- operation --------------

        for a in range(len(bis_list)):
            a = len(bis_list) - (a + 1)
            if a != 0:
                if bis_list[a] != bis_list[a - 1]:
                    bis_list_main = bis_list_main[:a] + \
                        ['--------------------------'] + bis_list_main[a:]
                    bpa_list = bpa_list[:a] + \
                        ['------------------------------------'] + bpa_list[a:]
                    bpra_list = bpra_list[:a] + \
                        ['--------------------------'] + bpra_list[a:]
                    bda_list = bda_list[:a] + \
                        ['--------------------------'] + bda_list[a:]
                    cna_list = cna_list[:a] + \
                        ['------------------------------------'] + cna_list[a:]

        # ------------- back to string ---------------------

        bill_id_all = '\n'.join([str(ele) for ele in bis_list_main])
        bill_price_all = '\n'.join([str(ele) for ele in bpa_list])
        bill_profit_all = '\n'.join([str(ele) for ele in bpra_list])
        bill_date_all = '\n'.join([str(ele) for ele in bda_list])
        c_name_all = '\n'.join([str(ele) for ele in cna_list])

    sac1_e.configure(state="normal")
    sac1_e.delete('1.0', END)
    sac1_e.insert('1.0', bill_id_all)
    sac1_e.configure(state="disable")

    sac3_e.configure(state="normal")
    sac3_e.delete('1.0', END)
    sac3_e.insert('1.0', bill_price_all)
    sac3_e.configure(state="disable")

    sac4_e.configure(state="normal")
    sac4_e.delete('1.0', END)
    sac4_e.insert('1.0', bill_profit_all)
    sac4_e.configure(state='disable')

    sac5_e.configure(state="normal")
    sac5_e.delete('1.0', END)
    sac5_e.insert('1.0', bill_date_all)
    sac5_e.configure(state='disable')

    sac6_e.configure(state="normal")
    sac6_e.delete('1.0', END)
    sac6_e.insert('1.0', c_name_all)
    sac6_e.configure(state="disable")

    fc1 = LabelFrame(F1, fg=us_fg, bg=us_bg, relief="raised")
    fc1.grid(row=0, column=0, padx=40, pady=3)

    def save_inv_tocsv():
        main_df_all.to_csv('sales.csv')
        messagebox.showinfo("SUCCESS", "Saved as sales.csv")

    def view_products_simple():
        global sac1_e,  sac3_e, sac4_e, sac5_e, sac6_e
        pid11 = str(pid_view_e.get())
        qry_main = "select * from sales where `bill_id` = '%s' ;" % (pid11,)
        main_df_all = pd.read_sql(qry_main, mycon)
        if main_df_all.empty:
            pid_view_e.delete(0, END)
            messagebox.showinfo("INVALID Bill ID",
                                "No Bill with such BILL ID found !")
        else:
            bill_id_all = main_df_all['bill_id'].to_string(index=False)
            bill_price_all = main_df_all['pname'].to_string(index=False)
            bill_profit_all = main_df_all['quantity'].to_string(index=False)
            bill_date_all = main_df_all['profit_pp'].to_string(index=False)
            c_name_all = main_df_all['barcode'].to_string(index=False)

            sac1_e.configure(state="normal")
            sac1_e.delete('1.0', END)
            sac1_e.insert('1.0', bill_id_all)
            sac1_e.configure(state="disable")

            sac3_e.configure(state="normal")
            sac3_e.delete('1.0', END)
            sac3_e.insert('1.0', bill_price_all)
            sac3_e.configure(state="disable")

            sac4_e.configure(state="normal")
            sac4_e.delete('1.0', END)
            sac4_e.insert('1.0', bill_profit_all)
            sac4_e.configure(state='disable')

            sac5_e.configure(state="normal")
            sac5_e.delete('1.0', END)
            sac5_e.insert('1.0', bill_date_all)
            sac5_e.configure(state='disable')

            sac6_e.configure(state="normal")
            sac6_e.delete('1.0', END)
            sac6_e.insert('1.0', c_name_all)
            sac6_e.configure(state="disable")

    manual_mode = LabelFrame(fc1, fg=us_fg, bg=us_bg, borderwidth=0)
    manual_mode.grid(row=0, column=0, padx=15, pady=15)

    Label(manual_mode, text="BILL ID", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    pid_view_e = Entry(manual_mode, width=15, font='arial 15')
    pid_view_e.grid(row=1, column=0, padx=5, pady=8)

    Button(manual_mode, text="SEARCH", borderwidth='4',
           background=btn_p_bg,
           foreground=btn_p_fg, width=15, font=('arial', 12, 'bold'), command=view_products_simple).grid(row=0,
                                                                                                         column=2,
                                                                                                         pady=3,
                                                                                                         padx=5)

    Button(manual_mode, text="SAVE AS CSV", width=15, borderwidth=4, font=('arial', 12,
           'bold'), command=save_inv_tocsv).grid(row=1, column=2, pady=3, padx=5)


def bill_display_analysis():
    global cam1, cam2, capp, cap
    global sac1_e, sac2_e, sac3_e, sac4_e, sac5_e, sac6_e, sac7_e
    if cam1:
        cam1 = False
        cap.release()

    if cam2:
        cam2 = False
        capp.release()

    F1 = LabelFrame(bill_frame, fg=mid_fg, bg=mid_bg)
    F1.place(x=0, y=0, relwidth=1)

    F2 = LabelFrame(F1, fg=mid_fg, bg=mid_bg)
    F2.grid(row=1, column=0, padx=100, pady=3)

    details = LabelFrame(F2, fg=us_fg, bg=us_bg, height=510)
    details.grid(row=0, column=0)

    name_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    name_detail.grid(row=0, column=0)

    cost_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    cost_detail.grid(row=0, column=1)

    mrp_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    mrp_detail.grid(row=0, column=2)

    quant_detail = LabelFrame(details, fg=us_fg, bg=us_bg)
    quant_detail.grid(row=0, column=3)

    # ++++++++++++++++++++++++++++++++++

    def mult_view(*args):
        sac5_e.yview(*args)
        sac4_e.yview(*args)
        sac3_e.yview(*args)
        sac1_e.yview(*args)

    vsb = Scrollbar(F2)
    vsb.grid(row=0, column=1, sticky='ns')
    vsb.configure(command=mult_view)

    Label(name_detail, text="PRODUCT", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac1_e = Text(name_detail, width=30, height=25, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac1_e.grid(row=1, column=0)

    Label(mrp_detail, text="SOLD", fg=us_fg, bg=us_bg, font=(
        'Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac3_e = Text(mrp_detail, width=20, height=25, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac3_e.grid(row=1, column=0)

    Label(cost_detail, text="NET REVENUE", fg=us_fg, bg=us_bg,
          font=('Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac4_e = Text(cost_detail, width=20, height=25, font='arial 15',
                  yscrollcommand=vsb.set, state="disable")
    sac4_e.grid(row=1, column=0)

    Label(quant_detail, text="NET PROFIT", fg=us_fg, bg=us_bg,
          font=('Helvetica', 15, 'bold')).grid(row=0, column=0)
    sac5_e = Text(quant_detail, width=20, height=25,
                  font='arial 15', yscrollcommand=vsb.set, state="disable")
    sac5_e.grid(row=1, column=0)

    qry_main = 'select * from stats;'
    main_df_all = pd.read_sql(qry_main, mycon)

    bill_id_all = main_df_all['pname'].to_string(index=False)
    bill_price_all = main_df_all['sold'].to_string(index=False)
    bill_profit_all = main_df_all['net_revenue'].to_string(index=False)
    bill_date_all = main_df_all['net_profit'].to_string(index=False)

    sac1_e.configure(state="normal")
    sac1_e.delete('1.0', END)
    sac1_e.insert('1.0', bill_id_all)
    sac1_e.configure(state="disable")

    sac3_e.configure(state="normal")
    sac3_e.delete('1.0', END)
    sac3_e.insert('1.0', bill_price_all)
    sac3_e.configure(state="disable")

    sac4_e.configure(state="normal")
    sac4_e.delete('1.0', END)
    sac4_e.insert('1.0', bill_profit_all)
    sac4_e.configure(state='disable')

    sac5_e.configure(state="normal")
    sac5_e.delete('1.0', END)
    sac5_e.insert('1.0', bill_date_all)
    sac5_e.configure(state='disable')

# ===========================================


billing_frame.pack(fill=BOTH, expand=1)
billing_app_page()
# running

root.protocol("WM_DELETE_WINDOW", on_closing_window)
root.mainloop()


# の実演はすべて終了
