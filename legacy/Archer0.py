from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sqlite3

class Archer_Portal():
    db_name = 'archer.db'

    def __init__(self, root):
        self.root = root
        self.root.title('Archer Data')

        # Logo and Title
        self.photo = PhotoImage(file='img_1.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=0)

        self.label1 = Label(font=('arial', 15, 'bold'), text='Archer Portal', fg='grey')
        self.label1.grid(row=8, column=0)

        # New record
        frame = LabelFrame(self.root, text='Enter Values')
        frame.grid(row=0, column=1)

        Label(frame, text='Barcode:').grid(row=1, column=1, sticky=W)
        self.barcode = Entry(frame)
        self.barcode.grid(row=1, column=2)

        Label(frame, text='Title:').grid(row=2, column=1, sticky=W)
        self.title = Entry(frame)
        self.title.grid(row=2, column=2)

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

        # Database display box
        self.tree = ttk.Treeview(height=10, column=['', '', '', '', '', '', ''])
        self.tree.grid(row=8, column=0, columnspan=8)
        self.tree.heading('#0', text='Barcode')
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='Title')
        self.tree.column('#1', width=50)
        self.tree.heading('#2', text='Keyword 1')
        self.tree.column('#2', width=50)
        self.tree.heading('#3', text='Keyword 2')
        self.tree.column('#3', width=50)
        self.tree.heading('#4', text='Keyword 3')
        self.tree.column('#4', width=50)
        self.tree.heading('#5', text='Description')
        self.tree.column('#5', width=150)
        self.tree.heading('#6', text='Physical Location')
        self.tree.column('#6', width=50)
        self.tree.heading('#7', text='Virtual Location')
        self.tree.column('#7', width=50, stretch=False)

        # Menu Bar
        Chooser = Menu()
        itemone = Menu()
        itemtwo = Menu()

        itemone.add_command(label='Add Record')
        itemone.add_command(label='Delete Record')

        itemtwo.add_command(label='Keyword Search', command=self.open_keyword_search_window)
        itemtwo.add_command(label='Barcode Search')
        itemtwo.add_command(label='Search Description')
        itemtwo.add_command(label='General Search')

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_cascade(label='Search', menu=itemtwo)

        root.config(menu=Chooser)

        # Initialize a separate instance variable for keyword search results tree
        self.keyword_search_tree = ttk.Treeview(height=10, column=['', '', '', '', '', '', ''])
        self.keyword_search_tree.grid(row=8, column=0, columnspan=8)
        self.keyword_search_tree.heading('#0', text='Barcode')
        self.keyword_search_tree.column('#0', width=50)
        self.keyword_search_tree.heading('#1', text='Title')
        self.keyword_search_tree.column('#1', width=50)
        self.keyword_search_tree.heading('#2', text='Keyword 1')
        self.keyword_search_tree.column('#2', width=50)
        self.keyword_search_tree.heading('#3', text='Keyword 2')
        self.keyword_search_tree.column('#3', width=50)
        self.keyword_search_tree.heading('#4', text='Keyword 3')
        self.keyword_search_tree.column('#4', width=50)
        self.keyword_search_tree.heading('#5', text='Description')
        self.keyword_search_tree.column('#5', width=150)
        self.keyword_search_tree.heading('#6', text='Physical Location')
        self.keyword_search_tree.column('#6', width=50)
        self.keyword_search_tree.heading('#7', text='Virtual Location')
        self.keyword_search_tree.column('#7', width=50, stretch=False)

        self.viewing_records()

    def open_keyword_search_window(self):
        keyword_search_window = Toplevel(self.root)
        keyword_search_window.title('Keyword Search')

        keyword_search_window.geometry('600x400')

        search_entry = Entry(keyword_search_window)
        search_entry.pack(pady=10)

        search_button = Button(keyword_search_window, text='Search',
                               command=lambda: self.perform_keyword_search(search_entry.get()))
        search_button.pack(pady=10)

        # Use the separate keyword search results tree
        self.keyword_search_tree.pack(pady=10)

    def perform_keyword_search(self, search_term):
        # Perform keyword search and update self.keyword_search_tree with results
        # ...

        # Example: Update with placeholder data
        self.update_keyword_search_results([('123', 'Title1', 'KW1', 'KW2', 'KW3', 'Desc1', 'Loc1', 'VLoc1'),
                                            ('456', 'Title2', 'KW4', 'KW5', 'KW6', 'Desc2', 'Loc2', 'VLoc2')])

    def update_keyword_search_results(self, results):
        # Clear previous results
        for element in self.keyword_search_tree.get_children():
            self.keyword_search_tree.delete(element)

        # Insert new results into the keyword_search_tree
        for data in results:
            self.keyword_search_tree.insert('', 1000, text=data[0], values=data[1:])

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn