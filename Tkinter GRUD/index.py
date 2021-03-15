from tkinter import ttk
from tkinter import *

import sqlite3



class Product:

    db_name = 'database.db'
    
    def __init__(self, window):

        self.wind = window
        self.wind.title("Product Aplication")

        # Creatin a Frame Container
        frame = LabelFrame(self.wind, text = 'Register a new product or object')
        frame.grid(row=0, column = 0, columnspan = 3, pady = 10)
        
        # Name input
        Label(frame, text ='Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row =1, column = 1, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # Price Input
        Label(frame, text='Price: ').grid(row=2, column=0)
        self.price=Entry(frame)
        self.price.grid(row = 2, column=1, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # Description Input
        Label(frame, text='Description: ').grid(row=3, column=0)
        self.description =Entry(frame)
        self.description.grid(row=3, column=1, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # amount Input
        Label(frame, text='Amount: ').grid(row=4, column=0)
        self.amount = Entry(frame)
        self.amount.grid(row=4, column =1, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # Button Add Product
        ttk.Button(frame, text='Save Product', command = self.add_product).grid(row=5, columnspan= 12, sticky= W + E )
        
        # Output Messages
        self.message = Label(text='',fg='red')
        self.message.grid(row = 6, column = 0, columnspan=2, sticky= W + E)


        # Table
        self.tree= ttk.Treeview(height = 15, columns =('#1','#2','#3'))
        self.tree.grid(row=7, column= 0, columnspan = 2, pady = 9,ipadx= 70,ipady= 5)
        self.tree.heading('#0', text='Name', anchor=CENTER)
        self.tree.heading('#1', text='Price', anchor =CENTER)
        self.tree.heading('#2', text='Description', anchor=CENTER)
        self.tree.heading('#3', text='Amount', anchor=CENTER)
        # filling the Row
        self.get_products()

        # Buttons
        ttk.Button(text = 'DELETE', command= self.delete_product).grid(row= 8, column= 0, sticky = W+E)
        ttk.Button(text ='EDIT', command= self.edit_produt).grid(row=8, column=1, sticky= W+E)

        #

    def run_query(self, query, parameters =()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result =cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # query
        query = 'SELECT *FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
           
            self.tree.insert('',0, text=row[1], value = (row[2],row[3],row[4]))
            
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 and len(self.description.get()) !=0 and len(self.amount.get()) !=0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL,?,?,?,?)'
            parameters = (self.name.get(), self.price.get(),self.description.get(),self.amount.get())
            self.run_query(query, parameters)
            self.message['text']= 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.description.delete(0, END)
            self.amount.delete(0,END)


        else:
            self.message['text'] = 'Name, Price, description and amount  are Required'
        
        self.get_products()

    def delete_product(self):
        self.message['text']=''
        try:

            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Please Select a Record'
            return
        self.message['text']=''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text']= 'Record {} deleted Successfully'. format(name)
        self.get_products()
    
    def edit_produt(self):
        self.message['text']=''
        try:

            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Please Select a Record'
            return

        name  = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        old_description= self.tree.item(self.tree.selection())['values'][1]
        old_amount = self.tree.item(self.tree.selection())['values'][2]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit product'

        # old name
        Label(self.edit_wind, text= 'Old Name: ').grid(row=0, column= 1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value= name), state = 'readonly').grid(row=0, column = 2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        #  new name
        Label(self.edit_wind, text= 'New Name').grid(row=1, column=1 )
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)
        
        # old price
        Label(self.edit_wind, text= 'Old Price').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value= old_price), state='readonly').grid(row=2, column= 2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # new price
        Label(self.edit_wind, text='New Price').grid(row=3, column= 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)
        
        # old desctiption
        Label(self.edit_wind, text='Old Description').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_description), state='readonly').grid(row=4, column=2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # new description
        Label(self.edit_wind, text='New Description').grid(row=5,column=1)
        new_description = Entry(self.edit_wind)
        new_description.grid(row=5,column=2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # old amount
        Label(self.edit_wind, text='Old Amount').grid(row=6,column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_amount), state='readonly').grid(row=6, column=2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)

        # new amount
        Label(self.edit_wind,text='New Amount').grid(row=7,column=1)
        new_amount = Entry(self.edit_wind)
        new_amount.grid(row = 7, column=2, ipadx= 70,ipady= 5 ,pady=5, columnspan=10)


        Button(self.edit_wind, text= 'Update', command= lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price, new_description.get(), old_description, new_amount.get(), old_amount)).grid(row= 8, column=1,ipadx= 70,ipady= 5 ,pady=5, sticky= W +E)

    def edit_records(self, new_name, name, new_price, old_price,new_description, old_description, new_amount, old_amount):
        query = 'UPDATE product SET name = ?, price= ?, description= ?, amount= ? WHERE name= ? AND price = ? AND description = ? AND amount = ?'
        parameters= ( new_name, new_price,new_description,new_amount, name, old_price,old_description, old_amount )
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} update Successfully'.format(name)
        self.get_products()



if __name__=='__main__':
    window = Tk()
    application = Product(window)
    window.resizable(width=False, height=False)
    window.mainloop()
     