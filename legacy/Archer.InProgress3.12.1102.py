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

        Label(frame, text='Keyword 1:').grid(row=3, column=1, sticky=W)
        self.keyword1 = Entry(frame)
        self.keyword1.grid(row=3, column=2)

        Label(frame, text='Keyword 2:').grid(row=4, column=1, sticky=W)
        self.keyword2 = Entry(frame)
        self.keyword2.grid(row=4, column=2)

        Label(frame, text='Keyword 3:').grid(row=5, column=1, sticky=W)
        self.keyword3 = Entry(frame)
        self.keyword3.grid(row=5, column=2)

        Label(frame, text='Physical Location:').grid(row=6, column=1, sticky=W)
        self.physlocation = Entry(frame)
        self.physlocation.grid(row=6, column=2)

        Label(frame, text='Virtual Location:').grid(row=7, column=1, sticky=W)
        self.vlocation = Entry(frame)
        self.vlocation.grid(row=7, column=2)

        Label(frame, text='Description:').grid(row=8, column=1, sticky=W)
        self.description = Text(frame, height=4, width=30)
        self.description.grid(row=8, column=2)

        # Add record button
        ttk.Button(frame, text='Add Record', command=self.add_record).grid(row=9, column=1)

        # Message Display
        self.message = Label(text='', fg='red')
        self.message.grid(row=0, column=1)

        # Database display box
        self.tree = ttk.Treeview(height=10, column=['', '', '', '', '', '', ''])
        self.tree.grid(row=9, column=0, columnspan=8)
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

        # Add commands to item_one menu
        itemone.add_command(label='Add Record')
        itemone.add_command(label='Delete Record', command =self.dele)
        itemone.add_command(label='Edit Record', command =self.edit_box)

        # Add commands to item_two Menu
        itemtwo.add_command(label='Keyword Search', command=self.open_keyword_search_window)
        itemtwo.add_command(label='Barcode Search')
        itemtwo.add_command(label='Search Description')
        itemtwo.add_command(label='General Search')

        # cascade menus
        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_cascade(label='Search', menu=itemtwo)

        # Configure menu
        root.config(menu=Chooser)

        # Create the 'archer' table
        self.create_table()

        # Display records
        self.viewing_records()

    def open_keyword_search_window(self):
        keyword_search_window = Toplevel(self.root)
        keyword_search_window.title('Keyword Search')

        # Keyword Search Window Size
        keyword_search_window.geometry('600x400')

        # Search Term Entry
        search_entry = Entry(keyword_search_window)
        search_entry.pack(pady=10)

        # Button to trigger search
        search_button = Button(keyword_search_window, text='Search',
                               command=lambda: self.perform_keyword_search(search_entry.get()))
        search_button.pack(pady=10)

        # Treeview for displaying search results
        search_results_tree = ttk.Treeview(height=10, column=['', '', '', '', '', '', ''])
        search_results_tree.grid(row=9, column=0, columnspan=8)
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

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'select * FROM archer'
        db_table = self.run_query(query)
        for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:])

    def create_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        query = '''
                CREATE TABLE IF NOT EXISTS archer (
                    Barcode INTEGER PRIMARY KEY,
                    Title TEXT,
                    Keyword1 TEXT,
                    Keyword2 TEXT,
                    Keyword3 TEXT,
                    Description TEXT,
                    PhysicalLocation TEXT,
                    VirtualLocation TEXT
                );
                '''
        try:
            self.run_query(query)
            print("Table 'archer' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def perform_keyword_search(self, keyword):
        # Implement keyword search logic here
        pass

    def add_record(self):
        if self.validation():
            query = 'INSERT INTO archer VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            parameters = (
                self.barcode.get(),
                self.title.get(),
                self.keyword1.get(),
                self.keyword2.get(),
                self.keyword3.get(),
                self.description.get("1.0", END),
                self.physlocation.get(),
                self.vlocation.get()
            )
            self.run_query(query, parameters)
            self.message['text'] = f'Record {self.barcode.get()} added successfully.'

            # Clear fields
            self.barcode.delete(0, END)
            self.title.delete(0, END)
            self.keyword1.delete(0, END)
            self.keyword2.delete(0, END)
            self.keyword3.delete(0, END)
            self.physlocation.delete(0, END)
            self.vlocation.delete(0, END)
            self.description.delete("1.0", END)
        else:
            self.message['text'] = 'Some fields need to be filled...'

        # Refresh the displayed records
        self.viewing_records()

    def validation(self):
        return (
            len(self.barcode.get()) != 0 and
            len(self.title.get()) != 0 and
            len(self.keyword1.get()) != 0 and
            len(self.physlocation.get()) != 0 and
            len(self.vlocation.get()) != 0 and
            len(self.description.get("1.0", END)) != 0
        )

        #----------Delete Record
    def delete_record(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.message['text'] ='Please select a record to delete'
            return
        self.message['text'] = ''
        number = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM archer WHERE barcode= ?'
        self.run_query(query,(number,))
        self.message['text'] = 'Record {} has been deleted'.format(number)

        self.viewing_records()

        #----------------Delete a record
    def dele(self):
        de = tkinter.messagebox.askquestion('Delete Record', 'Do you want to Delete a record')
        if de == 'yes':
            self.delete_record()


        #------------------Edit a record
    def edit_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            self.message['text'] ='Please select a record to edit'
            return

        bcode = self.tree.item(self.tree.selection())['values'][0]
        title = self.tree.item(self.tree.selection())['values'][1]
        keyword1 = self.tree.item(self.tree.selection())['values'][2]
        keyword2 = self.tree.item(self.tree.selection())['values'][3]
        keyword3 = self.tree.item(self.tree.selection())['values'][4]
        plocation = self.tree.item(self.tree.selection())['values'][5]
        vlocation = self.tree.item(self.tree.selection())['values'][6]
        description = self.tree.item(self.tree.selection())['values'][7]

        self.edit_root = Toplevel()
        self.edit_root.title('Edit Record')

        Label(self.edit_root, text = 'Old Barcode:').grid(row = 0, column = 1, sticky = W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root,value=bcode),state='readonly').grid(row = 0,
        column =2)
        Label(self.edit_root, text = 'New Barcode:').grid(row =1, column = 1, sticky = W)
        new_bcode = Entry(self.edit_root)
        new_bcode.grid(row = 1, column =2)

        Label(self.edit_root, text='Old Title:').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=title), state='readonly').grid(row=2,
        column=2)
        Label(self.edit_root, text='New Title:').grid(row=3, column=1, sticky=W)
        new_title = Entry(self.edit_root)
        new_title.grid(row=3, column=2)

        Label(self.edit_root, text='Old Keyword 1:').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=keyword1), state='readonly').grid(row=4,
        column=2)
        Label(self.edit_root, text='New Keyword 1:').grid(row=5, column=1, sticky=W)
        new_keyword1 = Entry(self.edit_root)
        new_keyword1.grid(row=5, column=2)

        Label(self.edit_root, text='Old Keyword 2:').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=keyword2), state='readonly').grid(row=6,
        column=2)
        Label(self.edit_root, text='New Keyword 2:').grid(row=7, column=1, sticky=W)
        new_keyword2 = Entry(self.edit_root)
        new_keyword2.grid(row=7, column=2)

        Label(self.edit_root, text='Old Keyword 3:').grid(row=8, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=keyword3), state='readonly').grid(row=8,
        column=2)
        Label(self.edit_root, text='New Keyword 3:').grid(row=9, column=1, sticky=W)
        new_keyword3 = Entry(self.edit_root)
        new_keyword3.grid(row=9, column=2)

        Label(self.edit_root, text='Old Physical Location:').grid(row=10, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=plocation), state='readonly').grid(row=10,
        column=2)
        Label(self.edit_root, text='New Physical Location:').grid(row=11, column=1, sticky=W)
        new_plocation = Entry(self.edit_root)
        new_plocation.grid(row=11, column=2)

        Label(self.edit_root, text='Old Virtual Location:').grid(row=12, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=vlocation), state='readonly').grid(row=12,
        column=2)
        Label(self.edit_root, text='New Virtual Location:').grid(row=13, column=1, sticky=W)
        new_vlocation = Entry(self.edit_root)
        new_vlocation.grid(row=13, column=2)

        Label(self.edit_root, text='Old Description:').grid(row=14, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=description), state='readonly').grid(row=14,
        column=2)
        Label(self.edit_root, text='New Description:').grid(row=15, column=1, sticky=W)
        new_description = Entry(self.edit_root)
        new_description.grid(row=15, column=2)


        #-----------------Save edit button
        Button(self.edit_root,text = 'Save Changes to Record', command = lambda :
        self.edit_record(new_bcode.get(),new_title.get(),new_keyword1.get(),new_keyword2.get(),new_keyword3.get(),
        new_plocation.get(),new_vlocation.get(),new_description.get()))\
            .grid(row=16, column=1, sticky=W)

        self.edit_root.mainloop()
    def edit_record(self,new_bcode,bcode,new_title,title,new_keyword1,keyword1,new_keyword2,keyword2,
                    new_keyword3,keyword3,new_plocation,plocation,new_vlocation,vlocation,new_description,description):
        query = 'UPDATE archer SET Barcode=?, Title=?, Keyword1=?, Keyword2=?, Keyword3=?, PhysicalLocation=?, '
                 'VirtualLocation=?, Description=? WHERE Barcode=? AND Title=? AND Keyword1=? AND Keyword2=?' \
                 AND Keyword3=? AND PhysicalLocation=? AND VirtualLocation=? AND Description=?
        parameters = (new_bcode, new_title, new_keyword1, new_keyword2, new_keyword3, new_vlocation,
        new_description, description,bcode,title,keyword1,keyword2,keyword3,plocation,vlocation,description)
        self.run_query(query,paramaters)
        self.edit_root.destroy()
        self.message['text'] ='{} details were changed to {}'.format(bcode,new_bcode)


    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit Record','Do you want to Edit a Record?')
        if ed == 'yes':
            self.edit_box()



if __name__ == '__main__':
    root = Tk()
    root.geometry('530x465+500+200')
    application = Archer_Portal(root)
    root.mainloop()
