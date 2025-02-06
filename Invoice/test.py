import tkinter as tk 
from tkinter import ttk
from tkinter import *
import mysql.connector
from tkinter import messagebox
import random
from datetime import datetime
import mysql.connector


import random

connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="siddharth1402",
        database="project"
    )

c=connection.cursor()


class Window1(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("1200x600")
        self.title('INVOICE Page')
        self.configure(bg="#dec8c8")

        # MySQL connection and query retrieval
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="siddharth1402",
            database="project"
        )
        self.c = self.connection.cursor()

        # Variables
        inv_id = random.randint(100, 100000)
        self.inv_id_ent = IntVar()
        self.inv_id_ent.set(inv_id)
        self.cust_ct = StringVar()
        self.cust_name = StringVar()
        self.prd_id_ent = IntVar()
        self.prd_qty_ent = IntVar()
        self.date_pr = StringVar()
        self.date_pr.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.total_list = []
        self.grd_total = 0
        self.products = []
        self.prd_qty_ent = IntVar()

        # Functions
        def default_bill():
            self.display_txt.insert(END, "\t\t\t            Starbucks")
            self.display_txt.insert(END, "\n\t\t\t        6th Avenue Street")
            self.display_txt.insert(END, "\n\t\t\t   Contact- +919456387601")
            self.display_txt.insert(END, "\n===========================================================================================================")
            self.display_txt.insert(END, f"\nInvoice ID: {self.inv_id_ent.get()}")
            self.display_txt.insert(END, f"\nTime : {self.date_pr.get()}")

        def gen_bill():
            self.display_txt.insert(END, f"\nCustomer Name: {self.cust_name.get()}")
            self.display_txt.insert(END, f"\nCustomer Contact: {self.cust_ct.get()}")
            self.display_txt.insert(END, "\n===========================================================================================================")
            self.display_txt.insert(END, "Product Name\t\t                     \t\t Quantity                \t\tPrice             \t\t       Total")
            self.display_txt.insert(END, "\n===========================================================================================================")

        def add_prd():
            qty = self.prd_qty_ent.get()
            prdid_data = self.prd_id_ent.get()
            self.c.execute("SELECT One_price FROM products WHERE Product_id = %s", (prdid_data,))
            price_row = self.c.fetchone()

            if price_row is None:
                messagebox.showerror("Error", "Product ID does not exist")
                return

            price = price_row[0]
            total = qty * price
            self.c.execute("SELECT Product_name FROM products WHERE Product_id = %s", (prdid_data,))
            prdname_row = self.c.fetchone()

            if prdname_row is None:
                messagebox.showerror("Error", "Product ID does not exist")
                return

            prdname = prdname_row[0]
            self.total_list.append(total)
            self.products.append({'product_id': prdid_data, 'quantity': qty})
            self.display_txt.insert(END, f"\n{prdname}\t\t                     \t\t{qty}                    \t\t{price}              \t\t\t\t      Rs. {total}")

        def commit():
            for product in self.products:
                invid = self.inv_id_ent.get()
                cust_name_data = self.cust_name.get()
                cust_ct_data = self.cust_ct.get()
                qty = product['quantity']
                prdid_data = product['product_id']

                self.c.execute("SELECT One_price FROM products WHERE Product_id = %s", (prdid_data,))
                price_row = self.c.fetchone()

                if price_row is None:
                    messagebox.showerror("Error", "Product ID does not exist")
                    return

                price = price_row[0]
                total = qty * price

                self.c.execute("SELECT Product_name FROM products WHERE Product_id = %s", (prdid_data,))
                prdname_row = self.c.fetchone()

                if prdname_row is None:
                    messagebox.showerror("Error", "Product ID does not exist")
                    return

                prdname = prdname_row[0]

                print("Inserting into invoice table:")
                print("Invoice ID:", invid)
                print("Product Name:", prdname)
                print("Price:", price)
                print("Quantity:", qty)
                print("Product ID:", prdid_data)
                print("Customer Name:", cust_name_data)
                print("Customer Contact:", cust_ct_data)

                sql1 = "INSERT INTO invoice(invoice_id, Product_name, Price, Quantity, Product_id, Customer_name, Customer_contact) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (invid, prdname, total, qty, prdid_data, cust_name_data, cust_ct_data)

                try:
                    self.c.execute(sql1, val)
                    self.connection.commit()
                    print("Insert successful.")
                except Exception as e:
                    print("Error inserting into database:", str(e))

        def close_window():
            self.destroy()

        def total():
            grd_total = 0
            for item in self.total_list:
                grd_total += item
            self.display_txt.insert(END, "\n===========================================================================================================")
            self.display_txt.insert(END, f"\t\t\t\t Grand Total :{grd_total}")
            self.display_txt.insert(END, "\n===========================================================================================================")

        # GUI layout
        detframe = LabelFrame(self, text="Product Details", padx=20, pady=200, bd=5, background="white")
        detframe.grid(row=0, column=1, padx=5, pady=5, sticky=N)

        bill_frame = LabelFrame(self, text="Bill Area", font=('Ariel', 10), bd=3, background="#dec8c8", relief=GROOVE, )
        bill_frame.grid(row=0, column=0, padx=0, pady=5, sticky=N)
        self.display_txt = Text(bill_frame, bg="white", height=32, width=107, bd=5, relief=FLAT)
        self.display_txt.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        Cust_name_lbl = Label(detframe, text="Customer Name : ", background='white')
        Cust_name_lbl.grid(row=1, column=0)
        Cust_name_entry = Entry(detframe, textvariable=self.cust_name)
        Cust_name_entry.grid(row=1, column=1)

        Cust_ct_lbl = Label(detframe, text="Customer Contact : ", background='white')
        Cust_ct_lbl.grid(row=2, column=0)
        Cust_ct_entry = Entry(detframe, textvariable=self.cust_ct)
        Cust_ct_entry.grid(row=2, column=1)

        prd_id_lbl = Label(detframe, text="Product ID : ", background='white')
        prd_id_lbl.grid(row=3, column=0)
        prd_id_entry = Entry(detframe, textvariable=self.prd_id_ent)
        prd_id_entry.grid(row=3, column=1)

        prd_qty_lbl = Label(detframe, text="Product Quantity : ", background='white')
        prd_qty_lbl.grid(row=4, column=0)
        prd_qty_entry = Entry(detframe, textvariable=self.prd_qty_ent)
        prd_qty_entry.grid(row=4, column=1)

        gen_button = Button(detframe, text='Show Invoice', padx=15, fg='black', bg='#debfa6', command=gen_bill)
        gen_button.grid(row=6, column=0)
        space1 = Label(detframe, text="               ", background='white')
        space1.grid(row=5, column=0)

        total_button = Button(detframe, text='Total', padx=15, fg='black', bg='#debfa6', command=total)
        total_button.grid(row=7, column=0)
        add_button = Button(detframe, text='Add Product', padx=15, fg='black', bg='#debfa6', command=add_prd)
        add_button.grid(row=8, column=0)
        close_button = Button(detframe, text='Back', padx=15, fg='black', bg='#debfa6', command=close_window)
        close_button.grid(row=9, column=0)
        commit_button = Button(detframe, text='Commit Transaction', padx=15, fg='black', bg='#debfa6', command=commit)
        commit_button.grid(row=10, column=0)

        default_bill()

   
        root.mainloop()


class Window2(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("1200x600")
        self.title('Report Page')
        self.configure(bg="#dec8c8")
        #mysql connection and query retrieval 
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="siddharth1402",
                database="project"
            )

        c=connection.cursor()
        
        #----------------------------variables
        invid=StringVar()
        cust_ct=StringVar()
        pname_ent=StringVar()
        prdid_ent=StringVar()
        prdqty_ent=StringVar()
        prddel_ent=StringVar()
        #=======================-------------------------------------------------
        def reset():
            for record in self.trv.get_children():
                self.trv.delete(record)
        def displaydata():
            reset()
            inputdata=invid.get()
            c.execute('SELECT * from invoice WHERE invoice_id=%s',(inputdata,))
            item =c.fetchall()

            for i in item:
                self.trv.insert('','end',value=(i[0],i[1],i[2],i[3]))
        

        def displaydata_custct():
            reset()
            pname_data=pname_ent.get()
            prdid_data=prdid_ent.get()
            prdqty_data=prdqty_ent.get()
            
            c.execute("select * from products where Product_id = %s",(prdid_data,))
            existing_data=c.fetchone()

            if existing_data:
                messagebox.showerror("Duplicate Data . Please enter new data ")
                return

            sql = "INSERT INTO products (Product_id,Quantity,Product_name) VALUES (%s, %s, %s)"
            val = (prdid_data, prdqty_data, pname_data)
            c.execute(sql, val)

            connection.commit()
            pname_ent.set("")
            prdid_ent.set("")
            prdqty_ent.set("")
            # if c.rowcount>0:
            #     messagebox.showinfo("Data successfully Entered!")
            #     item =c.fetchall()

            #     for i in item:
            #         trv.insert('','end',value=(i[0],i[1],i[2]))
            # else:
            #     messagebox.showerror("No Data Entered . Something Went Wrong")

            
            
            
        # def compinvoice():
        #     reset()
        #     # c.execute('SELECT * from Products')
        #     # item =c.fetchall()
            
        #     # for i in item:
        #     #     trv.insert('','end',value=(i[0],i[1],i[2]))

        #     c.execute('SELECT * from Products')
        #     item =c.fetchall()

        #     # for i in item:
        #     #     trv.insert('','end',value=(i[0],i[1],i[2]))

        #     for x in item:
        #         reorder = "Yes" if x[1] <= 10 else "No"  # Check if quantity is less than 10
        #         trv.insert('', 'end', values=(x[0], x[1], x[2], reorder))
        def close_window():
            self.destroy()
        def reset():
            # Delete all entries in the Treeview widget
            for record in self.trv.get_children():
                self.trv.delete(record)
        def compinvoice():
            reset()  # Clear existing entries in the Treeview widget

            # Fetch the latest data from the database
            c.execute('SELECT * from Products')
            items = c.fetchall()

            for item in items:
                product_id = item[0]
                quantity = item[1]
                product_name = item[2]

                reorder_status = "Yes" if quantity <= 10 else "No"
                self.trv.insert('', 'end', values=(product_id, quantity, product_name, reorder_status))

        def search():
            prddel_data=prddel_ent.get()
            # for i in item:
            #     trv.insert('','end',value=(i[0],i[1],i[2]))
            
            c.execute("SELECT * from products WHERE Product_id=%s",(prddel_data,))
            item =c.fetchall()

            for i in item:
                self.trv.insert('','end',value=(i[0],i[1],i[2]))

        def on_enter_press(event):
            displaydata()

        def enter_press(evnt):
            displaydata_custct()

        self.prdframe = LabelFrame(self,text="Product Details",padx=20,pady=200,bd=5,background="white")
        self.prdframe.grid(row=0,column=1,padx=5,pady=5,sticky=N)



        pnamelbl=Label(self.prdframe,text="Product Name:                ",background='white')
        pnamelbl.grid(row=0,column=0)
        pnameentry = Entry(self.prdframe,textvariable=pname_ent)
        pnameentry.grid(row=0,column=1)
        pnameentry.bind('<Return>',on_enter_press)

        #functions prd
        #invoice frame
        # def getinpdta():
        #     inputdata=invid.get()
        #     displaydata(inputdata)
        #spacee + Buttons
        # space1=Label(prdframe,text="               ",background='white')
        # space1.grid(row=1,column=0)
        # invbutton=Button(prdframe,text='Submit',padx=10,fg='black',bg='#debfa6',command=displaydata)
        # invbutton.grid(row=2,column=0)
        # space2=Label(prdframe,text="               ",background='white')
        # space2.grid(row=4,column=0)

        prdidlbl=Label(self.prdframe,text="Product ID : ",background='white')
        prdidlbl.grid(row=1,column=0)
        prdidentry = Entry(self.prdframe,textvariable=prdid_ent)
        prdidentry.grid(row=1,column=1)
        prdidentry.bind('<Return>',enter_press)

        prdqtylbl=Label(self.prdframe,text="Product Quantity : ",background='white')
        prdqtylbl.grid(row=2,column=0)
        prdqtyentry = Entry(self.prdframe,textvariable=prdqty_ent)
        prdqtyentry.grid(row=2,column=1)
        prdqtyentry.bind('<Return>',enter_press)




        custctbutton=Button(self.prdframe,text='Submit',padx=15,fg='black',bg='#debfa6',command=displaydata_custct)
        custctbutton.grid(row=5,column=0)

        space2=Label(self.prdframe,text="               ",background='white')
        space2.grid(row=6,column=0)

        prddellbl=Label(self.prdframe,text="Product ID : ",background='white')
        prddellbl.grid(row=7,column=0)
        prddelentry = Entry(self.prdframe,textvariable=prddel_ent)
        prddelentry.grid(row=7,column=1)

        delbutton=Button(self.prdframe,text='Submit',padx=15,fg='black',bg='#debfa6',command=search)
        delbutton.grid(row=8,column=0)

        space3=Label(self.prdframe,text="               ",background='white')
        space3.grid(row=9,column=0)

        genbutton=Button(self.prdframe,padx=10,pady=5,text='Show All Purchases',fg='black',bg='#debfa6',command=compinvoice)
        genbutton.grid(row=10,column=0)

        close_button=Button(self.prdframe,text='Back',padx=15,fg='black',bg='#debfa6',command=close_window)
        close_button.grid(row=11,column=0)

        #treeview
        self.trv=ttk.Treeview(self,columns=(1,2,3,4),show="headings",height="15")
        self.trv.grid(row=0,column=0,padx=0,pady=0,sticky=N)
        self.trv.heading(1,text="Product ID")
        self.trv.heading(2,text="Product Quantity")
        self.trv.heading(3,text="Product Name")
        self.trv.heading(4,text="Reorder Status")

        #scrollbars
        self.scrolly=Scrollbar(self,orient=VERTICAL,command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrolly.set)
        self.scrolly.grid(row=0,column=2,sticky='ns')

        self.scrollx=Scrollbar(self,orient=HORIZONTAL,command=self.trv.xview)
        self.trv.configure(xscrollcommand=self.scrollx.set)
        self.scrollx.grid(row=1,column=0,sticky='ew')

class Window3(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("1200x600")
        self.title('Report Page')
        self.configure(bg="#dec8c8")
        #mysql connection and query retrieval 
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="siddharth1402",
                database="project"
            )

        c=connection.cursor()
        #----------------------------variables
        invid=StringVar()
        cust_ct=StringVar()
        pname_ent=StringVar()
        prdid_ent=StringVar()
        prdqty_ent=StringVar()
        prddel_ent=StringVar()
        trans_ent=StringVar()
        #=======================-------------------------------------------------
        def reset():
            for record in trv.get_children():
                trv.delete(record)
        # def displaydata():
        #     reset()
        #     inputdata=invid.get()
        #     c.execute('SELECT * from invoice WHERE invoice_id=%s',(inputdata,))
        #     item =c.fetchall()

        #     for i in item:
        #         trv.insert('','end',value=(i[0],i[1],i[2],i[3]))
        

        # def displaydata_custct():
        #     reset()
        #     # pname_data=pname_ent.get()
        #     # prdid_data=prdid_ent.get()
        #     # prdqty_data=prdqty_ent.get()
        #     trans_data=trans_ent.get()
            
        #     c.execute("select * from products where Product_id = %s",(trans_data,))
        #     existing_data=c.fetchone()

        #     # if existing_data:
        #     #     messagebox.showerror("Duplicate Data . Please enter new data ")
        #     #     return

        #     # sql = "INSERT INTO products (Product_id,Quantity,Product_name) VALUES (%s, %s, %s)"
        #     # val = (prdid_data, prdqty_data, pname_data)
        #     # c.execute(sql, val)

        #     connection.commit()
            
            # if c.rowcount>0:
            #     messagebox.showinfo("Data successfully Entered!")
            #     item =c.fetchall()

            #     for i in item:
            #         trv.insert('','end',value=(i[0],i[1],i[2]))
            # else:
            #     messagebox.showerror("No Data Entered . Something Went Wrong")

            # c.execute('SELECT * from Products')
            # item =c.fetchall()

            # for i in item:
            #     trv.insert('','end',value=(i[0],i[1],i[2]))

            # for x in item:
            #     reorder = "Yes" if x[1] < 10 else "No"  # Check if quantity is less than 10
            #     trv.insert('', 'end', values=(x[0], x[1], x[2], reorder))
            
            
        def disp_payments():
            reset()
            c.execute('SELECT * from payments')
            item =c.fetchall()
            
            for i in item:
                trv.insert('','end',value=(i[0],i[1],i[2],i[3],i[4]))

        def search():
            prddel_data=prddel_ent.get()
            trans_data=trans_ent.get()
            # for i in item:
            #     trv.insert('','end',value=(i[0],i[1],i[2]))
            
            c.execute("SELECT * from payments WHERE Transaction_id=%s",(trans_data,))
            item =c.fetchall()

            for i in item:
                trv.insert('','end',value=(i[0],i[1],i[2],i[3],i[4]))

        def on_enter_press(event):
            displaydata()

        def enter_press(evnt):
            displaydata_custct()

        def close_window():
            self.destroy()

        prdframe = LabelFrame(self,text="Product Details",padx=20,pady=200,bd=5,background="white")
        prdframe.grid(row=0,column=1,padx=5,pady=5,sticky=N)



        pnamelbl=Label(prdframe,text="Transaction ID:                ",background='white')
        pnamelbl.grid(row=0,column=0)
        pnameentry = Entry(prdframe,textvariable=trans_ent)
        pnameentry.grid(row=0,column=1)
        pnameentry.bind('<Return>',on_enter_press)



        # prdidlbl=Label(prdframe,text="Product ID : ",background='white')
        # prdidlbl.grid(row=1,column=0)
        # prdidentry = Entry(prdframe,textvariable=prdid_ent)
        # prdidentry.grid(row=1,column=1)
        # prdidentry.bind('<Return>',enter_press)

        # prdqtylbl=Label(prdframe,text="Product Quantity : ",background='white')
        # prdqtylbl.grid(row=2,column=0)
        # prdqtyentry = Entry(prdframe,textvariable=prdqty_ent)
        # prdqtyentry.grid(row=2,column=1)
        # prdqtyentry.bind('<Return>',enter_press)




        custctbutton=Button(prdframe,text='Submit',padx=15,fg='black',bg='#debfa6',command=search)
        custctbutton.grid(row=5,column=0)

        space2=Label(prdframe,text="               ",background='white')
        space2.grid(row=6,column=0)

        genbutton=Button(prdframe,padx=10,pady=5,text='Show All Transaction',fg='black',bg='#debfa6',command=disp_payments)
        genbutton.grid(row=10,column=0)

        close_button=Button(prdframe,text='Back',padx=15,fg='black',bg='#debfa6',command=close_window)
        close_button.grid(row=9,column=0)




        # space=Label(invframe,text="               ",background='white')
        #customer contact

        #display frame 
        dispframe = LabelFrame(self,text="Display",padx=300,pady=400,bd=5,background="white")
        dispframe.grid(row=0,column=2)
        # genbill=Button(dispframe,text='testing')
        # genbill.pack()




        display_txt = Text(self, bg="white", height=40, width=100, bd=5)
        display_txt.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Allow row 0 to grow to fill the available vertical space
        self.grid_columnconfigure(0, weight=1)  # Allow column 0 to grow to fill the available horizontal space


        trv=ttk.Treeview(display_txt,columns=(1,2,3,4,5),height=27,show="headings",)
        trv.column(1,anchor=CENTER,stretch=NO,width=155) 
        trv.column(2,anchor=CENTER,stretch=NO,width=210)
        trv.column(3,anchor=CENTER,stretch=NO,width=190)
        trv.column(4,anchor=CENTER,stretch=NO,width=190)
        trv.column(5,anchor=CENTER,stretch=NO,width=100)
        # trv.column(4,anchor=CENTER,stretch=NO,width=209)

        trv.heading(1,text="Transaction ID")
        trv.heading(2,text="Transaction Status")
        trv.heading(3,text="Date Of Transaction")
        trv.heading(4,text="Invoice ID")
        trv.heading(5,text="Charges")





        trv.grid(row=0,column=0,columnspan=10,rowspan=2)



        root.mainloop()

class Window4(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("1200x600")
        self.title('Report Page')
        self.configure(bg="#dec8c8")
        #mysql connection and query retrieval 
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="siddharth1402",
                database="project"
            )

        c=connection.cursor()
        #----------------------------variables
        invid=StringVar()
        cust_ct=StringVar()
        pname_ent=StringVar()
        prdid_ent=StringVar()
        prdqty_ent=StringVar()
        prddel_ent=StringVar()
        #=======================-------------------------------------------------
        def reset():
            for record in trv.get_children():
                trv.delete(record)

        def close_window():
            self.destroy()
        def displaydata():
            reset()
            inputdata=invid.get()
            c.execute('SELECT * from invoice WHERE invoice_id=%s',(inputdata,))
            item =c.fetchall()

            for i in item:
                trv.insert('','end',value=(i[0],i[1],i[2],i[3]))
        

        def displaydata_custct():
            reset()
            pname_data=pname_ent.get()
            prdid_data=prdid_ent.get()
            prdqty_data=prdqty_ent.get()
            
            c.execute("select * from products where Product_id = %s",(prdid_data,))
            existing_data=c.fetchone()

            if existing_data:
                messagebox.showerror("Duplicate Data . Please enter new data ")
                return

            sql = "INSERT INTO products (Product_id,Quantity,Product_name) VALUES (%s, %s, %s)"
            val = (prdid_data, prdqty_data, pname_data)
            c.execute(sql, val)

            connection.commit()
            pname_ent.set("")
            prdid_ent.set("")
            prdqty_ent.set("")
            # if c.rowcount>0:
            #     messagebox.showinfo("Data successfully Entered!")
            #     item =c.fetchall()

            #     for i in item:
            #         trv.insert('','end',value=(i[0],i[1],i[2]))
            # else:
            #     messagebox.showerror("No Data Entered . Something Went Wrong")

            
            
            
        # def compinvoice():
        #     reset()
        #     # c.execute('SELECT * from Products')
        #     # item =c.fetchall()
            
        #     # for i in item:
        #     #     trv.insert('','end',value=(i[0],i[1],i[2]))

        #     c.execute('SELECT * from Products')
        #     item =c.fetchall()

        #     # for i in item:
        #     #     trv.insert('','end',value=(i[0],i[1],i[2]))

        #     for x in item:
        #         reorder = "Yes" if x[1] <= 10 else "No"  # Check if quantity is less than 10
        #         trv.insert('', 'end', values=(x[0], x[1], x[2], reorder))
        def reset():
            # Delete all entries in the Treeview widget
            for record in trv.get_children():
                trv.delete(record)
        def compinvoice():
            reset()  # Clear existing entries in the Treeview widget

            # Fetch the latest data from the database
            c.execute('SELECT * from Products')
            items = c.fetchall()

            for item in items:
                product_id = item[0]
                quantity = item[1]
                product_name = item[2]

                reorder_status = "Yes" if quantity <= 10 else "No"
                trv.insert('', 'end', values=(product_id, quantity, product_name, reorder_status))

        def search():
            prddel_data=prddel_ent.get()
            # for i in item:
            #     trv.insert('','end',value=(i[0],i[1],i[2]))
            
            c.execute("SELECT * from products WHERE Product_id=%s",(prddel_data,))
            item =c.fetchall()

            for i in item:
                trv.insert('','end',value=(i[0],i[1],i[2]))

        def on_enter_press(event):
            displaydata()

        def enter_press(evnt):
            displaydata_custct()

        prdframe = LabelFrame(self,text="Product Details",padx=20,pady=200,bd=5,background="white")
        prdframe.grid(row=0,column=1,padx=5,pady=5,sticky=N)



        pnamelbl=Label(prdframe,text="Product Name:                ",background='white')
        pnamelbl.grid(row=0,column=0)
        pnameentry = Entry(prdframe,textvariable=pname_ent)
        pnameentry.grid(row=0,column=1)
        pnameentry.bind('<Return>',on_enter_press)

        #functions prd
        #invoice frame
        # def getinpdta():
        #     inputdata=invid.get()
        #     displaydata(inputdata)
        #spacee + Buttons
        # space1=Label(prdframe,text="               ",background='white')
        # space1.grid(row=1,column=0)
        # invbutton=Button(prdframe,text='Submit',padx=10,fg='black',bg='#debfa6',command=displaydata)
        # invbutton.grid(row=2,column=0)
        # space2=Label(prdframe,text="               ",background='white')
        # space2.grid(row=4,column=0)

        prdidlbl=Label(prdframe,text="Product ID : ",background='white')
        prdidlbl.grid(row=1,column=0)
        prdidentry = Entry(prdframe,textvariable=prdid_ent)
        prdidentry.grid(row=1,column=1)
        prdidentry.bind('<Return>',enter_press)

        prdqtylbl=Label(prdframe,text="Product Quantity : ",background='white')
        prdqtylbl.grid(row=2,column=0)
        prdqtyentry = Entry(prdframe,textvariable=prdqty_ent)
        prdqtyentry.grid(row=2,column=1)
        prdqtyentry.bind('<Return>',enter_press)




        custctbutton=Button(prdframe,text='Submit',padx=15,fg='black',bg='#debfa6',command=displaydata_custct)
        custctbutton.grid(row=5,column=0)

        space2=Label(prdframe,text="               ",background='white')
        space2.grid(row=6,column=0)

        prddellbl=Label(prdframe,text="Product ID : ",background='white')
        prddellbl.grid(row=7,column=0)
        prddelentry = Entry(prdframe,textvariable=prddel_ent)
        prddelentry.grid(row=7,column=1)

        delbutton=Button(prdframe,text='Submit',padx=15,fg='black',bg='#debfa6',command=search)
        delbutton.grid(row=8,column=0)

        space3=Label(prdframe,text="               ",background='white')
        space3.grid(row=9,column=0)

        genbutton=Button(prdframe,padx=10,pady=5,text='Show All Products',fg='black',bg='#debfa6',command=compinvoice)
        genbutton.grid(row=10,column=0)

        close_button=Button(prdframe,text='Back',padx=15,fg='black',bg='#debfa6',command=close_window)
        close_button.grid(row=9,column=0)


        # space=Label(invframe,text="               ",background='white')
        #customer contact

        #display frame 
        dispframe = LabelFrame(self,text="Display",padx=300,pady=400,bd=5,background="white")
        dispframe.grid(row=0,column=2)
        # genbill=Button(dispframe,text='testing')
        # genbill.pack()


        #----------------------------------------------------------------------------------------------------------------------------
        #text display area
        # display_txt=Text(dispframe,bg="white",height=40,width=100,bd=5)
        # display_txt.grid(row=2,column=3,padx=2,pady=3)
        #text display area
        #text display area
        #text display area

        display_txt = Text(self, bg="white", height=40, width=100, bd=5)
        display_txt.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)  # Allow row 0 to grow to fill the available vertical space
        self.grid_columnconfigure(0, weight=1)  # Allow column 0 to grow to fill the available horizontal space
        #----------------------------------------------------------------------------------------------------------------------------
        #functions()
        # def geninvdefault():
        #     # display_txt.insert(END,"\t\t\t\t\tINVOICE")
        #     display_txt.insert(END,"=============================================================================================================")
        #     display_txt.insert(END,"\n\tInvoice ID\t\t\tProduct\t\t\tPrice\t\t\tQuantity")
        #     display_txt.insert(END,"\n=============================================================================================================")

        # geninvdefault()


        #tree viewe display data


        trv=ttk.Treeview(display_txt,columns=(1,2,3,4),height=27,show="headings",)
        trv.column(1,anchor=CENTER,stretch=NO,width=135) 
        trv.column(2,anchor=CENTER,stretch=NO,width=298)
        trv.column(3,anchor=CENTER,stretch=NO,width=208)
        trv.column(4,anchor=CENTER,stretch=NO,width=208)
        # trv.column(4,anchor=CENTER,stretch=NO,width=209)

        trv.heading(1,text="Product ID")
        trv.heading(2,text="Quantity")
        trv.heading(3,text="Product Name")
        trv.heading(4,text="Reorder")




        trv.grid(row=0,column=0,columnspan=10,rowspan=2)


        root.mainloop()

class Window5(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.geometry("1200x600")
        self.title('Report Page')
        self.configure(bg="#dec8c8")
        
        # MySQL connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="siddharth1402",
            database="project"
        )

        c = connection.cursor()
        inv_id_ent = StringVar()

        # Create frames
        prdframe = LabelFrame(self, text="Product Details", padx=20, pady=200, bd=5, background="white")
        prdframe.grid(row=0, column=1, padx=5, pady=5, sticky=N)

        dispframe = LabelFrame(self, text="Display", padx=300, pady=400, bd=5, background="white")
        dispframe.grid(row=0, column=2)

        display_txt = Text(self, bg="white", height=40, width=100, bd=5)
        display_txt.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Display Treeview
        trv = ttk.Treeview(display_txt, columns=(1, 2, 3, 4, 5, 6, 7), height=27, show="headings")
        trv.column(1, anchor=CENTER, stretch=NO, width=100)
        trv.column(2, anchor=CENTER, stretch=NO, width=155)
        trv.column(3, anchor=CENTER, stretch=NO, width=100)
        trv.column(4, anchor=CENTER, stretch=NO, width=100)
        trv.column(5, anchor=CENTER, stretch=NO, width=100)
        trv.column(6, anchor=CENTER, stretch=NO, width=155)
        trv.column(7, anchor=CENTER, stretch=NO, width=155)

        trv.heading(1, text="Invoice ID")
        trv.heading(2, text="Product Name")
        trv.heading(3, text="Price")
        trv.heading(4, text="Quantity")
        trv.heading(5, text="Product ID")
        trv.heading(6, text="Customer Name")
        trv.heading(7, text="Customer Contact")

        trv.grid(row=0, column=0, columnspan=10, rowspan=2)
        def disp_invoice():
            reset()
            c.execute('SELECT * FROM invoice')
            items = c.fetchall()

            for item in items:
                trv.insert('', 'end', values=item)

        
    # Function to reset the treeview
        def reset():
            for record in trv.get_children():
                trv.delete(record)

    # Function to display data from the 'invoice' table
        

    # Function to search invoice based on Invoice ID
        def search():
            inv_id_data = inv_id_ent.get()
        
            c.execute("SELECT * from invoice WHERE invoice_id=%s", (inv_id_data,))
            item = c.fetchone()

            if item:
                trv.insert('', 'end', values=item)
            else:
                messagebox.showerror("Error", "No invoice found for the provided Invoice ID.")

        # Button to display invoice data
        genbutton = tk.Button(prdframe, padx=10, pady=5, text='Show All Invoices', fg='black', bg='#debfa6', command=disp_invoice)
        genbutton.grid(row=10, column=0)

        pnamelbl = tk.Label(prdframe, text="Invoice ID:                ", background='white')
        pnamelbl.grid(row=0, column=0)
        pnameentry = tk.Entry(prdframe, textvariable=inv_id_ent)
        pnameentry.grid(row=0, column=1)
        custctbutton = tk.Button(prdframe, text='Submit', padx=15, fg='black', bg='#debfa6', command=search)
        custctbutton.grid(row=5, column=0)


        root.mainloop()


root=tk.Tk()
root.geometry("1200x600")
root.title('Homepage')
root.configure(bg="#dec8c8")
bg=PhotoImage(file=r"C:\Users\nsidd\OneDrive\Desktop\Coding\DBMS Project\final\file.png")
pic_label=Label(root,image=bg)
pic_label.place(x=0,y=0,relwidth=1,relheight=1)
        
def invoice():
    invoice_page = Window1(root)

def report():
    report_page = Window2(root)

def transaction():
    transaction_page = Window3(root)

def product():
    product_page = Window4(root)

def orders():
    order_page=Window5(root)



inv_button = Button(root, text="INVOICE", command=invoice, padx=10, pady=10, bg="#debfa6")
inv_button.pack(pady=20)

rep_button = Button(root, text="REPORT", command=report, padx=10, pady=10, bg="#debfa6")
rep_button.pack(pady=20)

trns_button = Button(root, text="TRANSACTION", command=transaction, padx=10, pady=10, bg="#debfa6")
trns_button.pack(pady=20)

trns_button = Button(root, text="PRODUCTS",command=product, padx=10, pady=10, bg="#debfa6")
trns_button.pack(pady=20)

trns_button = Button(root, text="ORDERS",command=orders, padx=10, pady=10, bg="#debfa6")
trns_button.pack(pady=20)

root.mainloop()
