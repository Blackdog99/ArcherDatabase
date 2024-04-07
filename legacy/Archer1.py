from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sqlite3

class Archer_Portal():
    db_name = 'archer.db'

    def __init__(self, root) :
        self.root = root
        self.root.title('Archer Data')

    #-------------Logo and Title

        self.photo = PhotoImage(file='img_1.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0,column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='Archer Portal',fg='grey')
        self.label1.grid(row=8,column=0)

    #-----------------New record

        frame = LabelFrame(self.root, text='Enter Values')
        frame.grid(row=0,column=1)

        Label(frame,text='Barcode:').grid(row=1,column=1,sticky=W)
        self.barcode = Entry(frame)
        self.barcode.grid(row=1,column=2)


        Label(frame,text='Title:').grid(row=2,column=1,sticky=W)
        self.title = Entry(frame)
        self.title.grid(row=2,column=2)

        Label(frame, text='Keyword 1:').grid(row=2, column=1, sticky=W)
        self.keyword1 = Entry(frame)
        self.keyword1.grid(row=2, column=2)

        Label(frame, text='Keyword 2:').grid(row=3, column=1, sticky=W)
        self.keyword2 = Entry(frame)
        self.keyword2.grid(row=3, column=2)

        Label(frame, text='Keyword 3:').grid(row=4, column=1, sticky=W)
        self.keyword3 = Entry(frame)
        self.keyword3.grid(row=4, column=2)

        Label(frame, text='Physical Location:').grid(row=5, column=1, sticky=W)
        self.physlocation = Entry(frame)
        self.physlocation.grid(row=5, column=2)

        Label(frame, text='Virtual Location:').grid(row=6, column=1, sticky=W)
        self.vlocation = Entry(frame)
        self.vlocation.grid(row=6, column=2)

        Label(frame, text='Description:').grid(row=7, column=1, sticky=W)
        self.description = Text(frame, height=4, width=30)
        self.description.grid(row=7, column=2)


        #-----------------Database display box

        self.tree = ttk.Treeview(height=10,column=['','','','','','',''])
        self.tree.grid(row=8, column=0, columnspan=8)
        self.tree.heading('#0',text='Barcode')
        self.tree.column('#0', width=50)
        self.tree.heading('#1',text='Title')
        self.tree.column('#1', width=50)
        self.tree.heading('#2',text='Keyword 1')
        self.tree.column('#2', width=50)
        self.tree.heading('#3',text='Keyword 2')
        self.tree.column('#3', width=50)
        self.tree.heading('#4',text='Keyword 3')
        self.tree.column('#4', width=50)
        self.tree.heading('#5',text='Description')
        self.tree.column('#5', width=150)
        self.tree.heading('#6',text='Physical Location')
        self.tree.column('#6', width=50)
        self.tree.heading('#7',text='Virtual Location')
        self.tree.column('#7', width=50, stretch=False)


        #------------------Menu Bar
        Chooser = Menu()
        itemone = Menu()
        itemtwo = Menu()

        #-----------------Add commands to item_one menu
        itemone.add_command(label='Add Record')
        itemone.add_command(label='Delete Record')

        #-----------------Add commands to item_two Menu
        itemtwo.add_command(label='Keyword Search', command=self.open_keyword_search_window)
        itemtwo.add_command(label='Barcode Search')
        itemtwo.add_command(label='Search Description')
        itemtwo.add_command(label='General Search')


        #------------------cascade menus
        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_cascade(label='Search', menu=itemtwo)


        #------------------Configure menu
        root.config(menu=Chooser)


        self.viewing_records()
    def open_keyword_search_window(self):
        keyword_search_window = Toplevel(self.root)
        keyword_search_window.title('Keyword Search')

        #-------------------Keyword Search Window Size
        keyword_search_window.geometry('600x400')

        #--------------------Search Term Entry
        search_entry = Entry(keyword_search_window)
        search_entry.pack(pady=10)

        #--------------Button to trigger search
        search_button = Button(keyword_search_window, text='Search',
        command=lambda: self.perform_keyword_search(search_entry.get()))
        search_button.pack(pady=10)

        #---------------treeview for displaying search results
        search_results_tree = ttk.Treeview(height=10, column=['', '', '', '', '', '', ''])
        search_results_tree.grid(row=8, column=0, columnspan=8)
        search_results_tree.heading('#0', text='Barcode')
        search_results_tree.column('#0', width=50)
        search_results_tree.heading('#1', text='Title')
        search_results_tree.column('#1', width=50)
        search_results_tree.heading('#2', text='Keyword 1')
        search_results_tree.column('#2', width=50)
        search_results_tree.heading('#3', text='Keyword 2')
        search_results_tree.column('#3', width=50)
        search_results_tree.heading('#4', text='Keyword 3')
        search_results_tree.column('#4', width=50)
        search_results_tree.heading('#5', text='Description')
        search_results_tree.column('#5', width=150)
        search_results_tree.heading('#6', text='Physical Location')
        search_results_tree.column('#6', width=50)
        search_results_tree.heading('#7', text='Virtual Location')
        search_results_tree.column('#7', width=50, stretch=False)

        #----------------View Database Table
    def run_query(self,query,paramaters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query,paramaters)
            conn.commit()
        return query_result

    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'select * FROM Archer'
        db_table = self.run_query(query)
        for data in db_table:
            self.tree.insert('',1000,text=data[0],values=data[1])

if __name__ == '__main__':
    root = Tk()
    root.geometry('530x465+500+200')
    application = Archer_Portal(root)
    root.mainloop()