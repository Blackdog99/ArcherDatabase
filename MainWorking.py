from tkinter import *
from tkinter import ttk, filedialog
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

        # Configure the style for ttk widgets
        style = ttk.Style()
        style.configure('TEntry', font=('Helvetica', 10))  # Apply the style to ttk.Entry
        style.configure('TCombobox', font=('Helvetica', 10))  # Apply the style to ttk.Combobox


        frame = LabelFrame(self.root, text='Enter Values')
        frame.grid(row=0, column=1)

        # Barcode Entry
        Label(frame, text='Barcode:').grid(row=1, column=1, sticky=W)
        self.barcode = ttk.Entry(frame, style='TEntry')
        self.barcode.grid(row=1, column=2, padx=(5), pady=(5))

        # Title Entry - Updated to use ttk.Entry
        Label(frame, text='Title:').grid(row=2, column=1, sticky=W)
        self.title = ttk.Entry(frame, style='TEntry')
        self.title.grid(row=2, column=2, padx=(5), pady=(5))

        # Keyword 1 Entry - Updated to use ttk.Entry
        Label(frame, text='Keyword 1:').grid(row=3, column=1, sticky=W)
        self.keyword1 = ttk.Entry(frame, style='TEntry')
        self.keyword1.grid(row=3, column=2, padx=(5), pady=(5))

        # Keyword 2 Entry - Updated to use ttk.Entry
        Label(frame, text='Keyword 2:').grid(row=4, column=1, sticky=W)
        self.keyword2 = ttk.Entry(frame, style='TEntry')
        self.keyword2.grid(row=4, column=2, padx=(5), pady=(5))

        # Keyword 3 Entry - Updated to use ttk.Entry
        Label(frame, text='Keyword 3:').grid(row=5, column=1, sticky=W)
        self.keyword3 = ttk.Entry(frame, style='TEntry')
        self.keyword3.grid(row=5, column=2, padx=(5), pady=(5))

        # Physical Location Combobox
        physical_location_options = ['File 1:A', 'File 1:B', 'File 2:A', 'File 2:B', 'File 3:A', 'File 3:B'
                                    ,'Resource Box']  # Add more as needed
        Label(frame, text='Physical Location:').grid(row=6, column=1, sticky=W)
        self.physlocation = ttk.Combobox(frame, values=physical_location_options, style='TCombobox', width=20)
        self.physlocation.grid(row=6, column=2, padx=5, pady=5)
        self.physlocation.set('Select Physical Location')
        self.physlocation['state'] = 'readonly'

        # Function to open the file dialog and update the entry with the selected file path
        def browse_file():
            filepath = filedialog.askopenfilename()  # Opens the dialog and stores the selected file path
            if filepath:  # Checks if a file was selected
                self.vlocation.delete(0, "end")  # Clears the entry field
                self.vlocation.insert(0, filepath)  # Inserts the selected file path into the entry

        # Label for the Virtual Location entry
        Label(frame, text='Virtual Location:').grid(row=7, column=1, sticky=W)

        # Entry field for displaying the selected file path
        self.vlocation = ttk.Entry(frame, style='TEntry')
        self.vlocation.grid(row=7, column=2, padx=5, pady=(5))

        # Button to open the file dialog
        browse_btn = ttk.Button(frame, text="Browse",
                                command=browse_file)  # Calls the 'browse_file' function when clicked
        browse_btn.grid(row=7, column=3, padx=(5), pady=(5))  # Place it next to the entry field

        # Description Text
        Label(frame, text='Description:').grid(row=8, column=1, sticky=W)
        self.description = Text(frame, height=4, width=30)
        self.description.grid(row=8, column=2, padx=(5), pady=(5))

        # Add record button
        ttk.Button(frame, text='Add Record', command=self.add_record).grid(row=9, column=1)

        # Message Display
        self.message = Label(text='', fg='red')
        self.message.grid(row=8, column=1, columnspan=1, sticky="ew")

        # Initialize the Treeview
        self.tree = ttk.Treeview(frame, height=30, columns=(
        'Barcode', 'Title', 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Description', 'Physical Location',
        'Virtual Location'))
        self.tree.grid(row=9, column=0, columnspan=8, sticky="nsew")
        self.root.grid_rowconfigure(9, weight=1)  # Make the Treeview row expandable
        self.root.grid_columnconfigure(0, weight=1)  # Make the Treeview column expandable

        # Create the vertical scrollbar and associate it with the Treeview's Y-axis
        vert_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        vert_scrollbar.grid(row=9, column=8,
                            sticky="ns")  # Place scrollbar next to the Treeview, adjust column as needed

        # Configure the Treeview to use the scrollbar
        self.tree.configure(yscrollcommand=vert_scrollbar.set)

        # Configure Treeview columns and headings
        self.tree.heading('#0', text='Barcode')
        self.tree.column('#0', width=50)
        self.tree.heading('#1', text='Title')
        self.tree.column('#1', width=150)
        self.tree.heading('#2', text='Keyword 1')
        self.tree.column('#2', width=50)
        self.tree.heading('#3', text='Keyword 2')
        self.tree.column('#3', width=50)
        self.tree.heading('#4', text='Keyword 3')
        self.tree.column('#4', width=50)
        self.tree.heading('#5', text='Description')
        self.tree.column('#5', width=150)
        self.tree.heading('#6', text='Physical Location')
        self.tree.column('#6', width=150)
        self.tree.heading('#7', text='Virtual Location')
        self.tree.column('#7', width=150, stretch=True)


        # Menu Bar
        Chooser = Menu()
        itemone = Menu()
        itemtwo = Menu()

        # Add commands to item_one menu
        itemone.add_command(label='Add Record', command=self.add_record)
        itemone.add_command(label='Delete Record', command=self.dele)
        itemone.add_command(label='Edit Record', command=self.edit_box)

        # Add commands to item_two Menu
        itemtwo.add_command(label='Keyword Search', command=self.open_keyword_search_window)
        itemtwo.add_command(label='Barcode Search', command=self.open_barcode_search_window)
        itemtwo.add_command(label='Search Description', command=self.open_description_search_window)
        itemtwo.add_command(label='General Search', command=self.open_general_search_window)

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

    # def run_query(self, query, parameters=(), commit=False):
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         result = cursor.execute(query, parameters)
    #         if commit:
    #             conn.commit()
    #         return result

    # def run_query(self, query, parameters=(), commit=False):
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         try:
    #             cursor.execute(query, parameters)
    #             if commit:
    #                 conn.commit()
    #             if query.lstrip().upper().startswith("SELECT"):
    #                 return cursor.fetchall()
    #             else:
    #                 return cursor.rowcount  # Number of rows inserted/updated/deleted
    #         except Exception as e:
    #             conn.rollback()
    #             raise e
    #         finally:
    #             cursor.close()

    # def run_query(self, query, parameters=(), commit=False):
    #     print("Using the following query: " + query)
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         try:
    #             # Start transaction explicitly if commit is required
    #             if commit:
    #                 cursor.execute('BEGIN')
    #             cursor.execute(query, parameters)
    #             if commit:
    #                 conn.commit()
    #             if query.lstrip().upper().startswith("SELECT"):
    #                 return cursor.fetchall()
    #             else:
    #                 return cursor.rowcount  # Number of rows inserted/updated/deleted
    #         except Exception as e:
    #             conn.rollback()
    #             raise e
    #         finally:
    #             cursor.close()

    def run_query(self, query, parameters=(), commit=False):
        # Validate input query and parameters
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")
        if not isinstance(parameters, (tuple, list)):
            raise ValueError("Parameters must be a tuple or a list.")
        if not isinstance(commit, bool):
            raise ValueError("Commit must be a boolean.")

        print("Using the following query: " + query)

        # Connect to the database
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Start transaction explicitly if commit is required
                if commit:
                    cursor.execute('BEGIN')
                cursor.execute(query, parameters)

                if commit:
                    conn.commit()

                # Handling different types of queries
                if query.lstrip().upper().startswith("SELECT"):
                    return cursor.fetchall()  # For SELECT queries, return fetched data
                else:
                    return cursor.rowcount  # For INSERT, UPDATE, DELETE, return affected row count

        except sqlite3.DatabaseError as db_err:
            if conn:
                conn.rollback()  # Roll back the transaction on errors related to the database
            print("Database error:", db_err)
            raise

        except Exception as e:
            if conn:
                conn.rollback()  # Roll back the transaction on general errors
            print("Error executing the query:", e)
            raise

        finally:
            if cursor:
                cursor.close()  # Ensure the cursor is closed after operation



    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM archer'
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

    # Delete Record
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

    # Delete a record
    def dele(self):
        de = tkinter.messagebox.askquestion('Delete Record', 'Do you want to Delete a record')
        if de == 'yes':
            self.delete_record()

    # Edit a record
    def edit_box(self):
        self.message['text'] = ''
        selected_item = self.tree.selection()

        # Check if an item is selected
        if not selected_item:
            self.message['text'] = 'Please select a record to edit'
            return

        # Get the values of the selected item
        selected_values = self.tree.item(selected_item)['values']

        # Check if an item is selected and has enough values
        if not selected_values or len(selected_values) < 7:
            self.message['text'] = 'Selected record does not have enough values'
            return

        barcode = selected_values[0]
        title = selected_values[1]
        keyword1 = selected_values[2]
        keyword2 = selected_values[3]
        keyword3 = selected_values[4]
        plocation = selected_values[5]
        vlocation = selected_values[6]

        # Check if there is a description at index 7
        description = selected_values[5] if len(selected_values) > 5 else ''

        self.edit_root = Toplevel()
        self.edit_root.title('Edit Record')

        Label(self.edit_root, text='Old Barcode:').grid(row=0, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=barcode), state='readonly').grid(row=0,
                                                                                                          column=2)

        Label(self.edit_root, text='Old Title:').grid(row=1, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=title), state='readonly').grid(row=1,
                                                                                                          column=2)

        Label(self.edit_root, text='Old Keyword 1:').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=keyword1), state='readonly').grid(row=2,
                                                                                                             column=2)

        Label(self.edit_root, text='Old Keyword 2:').grid(row=3, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=keyword2), state='readonly').grid(row=3,
                                                                                                             column=2)

        Label(self.edit_root, text='Old Keyword 3:').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=keyword3), state='readonly').grid(row=4,
                                                                                                             column=2)

        Label(self.edit_root, text='Old Physical Location:').grid(row=5, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=plocation), state='readonly').grid(row=5,
                                                                                                              column=2)

        Label(self.edit_root, text='Old Virtual Location:').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=vlocation), state='readonly').grid(row=6,
                                                                                                              column=2)

        Label(self.edit_root, text='Old Description:').grid(row=7, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=description), state='readonly').grid(row=7,
                                                                                                                column=2)

        # New Barcode
        Label(self.edit_root, text='New Barcode:').grid(row=8, column=1, sticky=W)
        new_barcode = Entry(self.edit_root)
        new_barcode.grid(row=8, column=2)

        # New Title
        Label(self.edit_root, text='New Title:').grid(row=9, column=1, sticky=W)
        new_title = Entry(self.edit_root)
        new_title.grid(row=9, column=2)

        # New Keyword 1
        Label(self.edit_root, text='New Keyword 1:').grid(row=10, column=1, sticky=W)
        new_keyword1 = Entry(self.edit_root)
        new_keyword1.grid(row=10, column=2)

        # New Keyword 2
        Label(self.edit_root, text='New Keyword 2:').grid(row=11, column=1, sticky=W)
        new_keyword2 = Entry(self.edit_root)
        new_keyword2.grid(row=11, column=2)

        # New Keyword 3
        Label(self.edit_root, text='New Keyword 3:').grid(row=12, column=1, sticky=W)
        new_keyword3 = Entry(self.edit_root)
        new_keyword3.grid(row=12, column=2)

        # New Physical Location
        Label(self.edit_root, text='New Physical Location:').grid(row=13, column=1, sticky=W)
        new_plocation = Entry(self.edit_root)
        new_plocation.grid(row=13, column=2)

        # New Virtual Location
        Label(self.edit_root, text='New Virtual Location:').grid(row=14, column=1, sticky=W)
        new_vlocation = Entry(self.edit_root)
        new_vlocation.grid(row=14, column=2)

        # New Description
        Label(self.edit_root, text='New Description:').grid(row=15, column=1, sticky=W)
        new_description = Text(self.edit_root, height=4, width=30)
        new_description.insert(END, description)
        new_description.grid(row=15, column=2)

        # Save edit button
        Button(self.edit_root, text='Save Changes to Record', command=lambda:
        self.edit_record(
            new_barcode.get(),
            new_title.get(),
            new_keyword1.get(),
            new_keyword2.get(),
            new_keyword3.get(),
            new_plocation.get(),
            new_vlocation.get(),
            new_description.get("1.0", END),
            barcode  # Old barcode to identify the record for updating
        )
               ).grid(row=16, column=1, sticky=W)

        self.edit_root.mainloop()

    def show_all(self,db_name, table_name):
        """
        Prints all records from the specified SQLite table.

        Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to print records from.
        """
        # Connect to the SQLite database
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()  # Create a cursor object
            try:
                # Execute a query to select all records from the table
                cursor.execute(f"SELECT * FROM {table_name}")
                records = cursor.fetchall()  # Fetch all rows from the query result

                # Check if any records are found
                if records:
                    # Print each record
                    for record in records:
                        print(record)
                else:
                    print("No records found in the table.")

            except sqlite3.Error as e:
                # Handle any SQLite errors
                print(f"An error occurred: {e}")

            finally:
                cursor.close()  # Close the cursor

    def edit_record(self, new_barcode, new_title, new_keyword1, new_keyword2, new_keyword3, new_plocation, new_vlocation,
                    new_description, old_barcode):
        #self.show_all("archer.db","archer")
        print(f"Updating record {old_barcode} with new values.")
        new_description = new_description.strip()  # Ensuring description is stripped of leading/trailing whitespace
        query = '''
                UPDATE archer
                SET Barcode=?, Title=?, Keyword1=?, Keyword2=?, Keyword3=?, PhysicalLocation=?,
                VirtualLocation=?, Description=?
                WHERE Barcode=?
                '''
        parameters = (
            new_barcode, new_title, new_keyword1, new_keyword2, new_keyword3, new_plocation,
            new_vlocation, new_description, old_barcode
        )
        try:
            self.run_query(query, parameters, commit=True)
            self.edit_root.destroy()
            self.message['text'] = f'Record {old_barcode} updated successfully.'
            self.viewing_records()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self.message['text'] = 'Failed to update the record.'
        #self.show_all("archer.db","archer")

    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit Record', 'Do you want to Edit a Record?')
        if ed == 'yes':
            self.edit_box()

    def open_keyword_search_window(self):
        keyword_search_window = Toplevel(self.root)
        keyword_search_window.title('Keyword Search')
        keyword_search_window.geometry('600x400')

        Label(keyword_search_window, text='Enter Keyword:').pack(pady=10)

        search_entry = Entry(keyword_search_window)
        search_entry.pack(pady=10)

        search_button = Button(keyword_search_window, text='Search', command=lambda: self.perform_keyword_search(search_entry.get(), search_results_tree))
        search_button.pack(pady=10)

    # Setup the Treeview
        columns = ('Barcode', 'Title', 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Physical Location', 'Virtual Location', 'Description')
        search_results_tree = ttk.Treeview(keyword_search_window, columns=columns, show='headings')
        search_results_tree.pack(pady=20, fill=BOTH, expand=True)
        for col in columns:
            search_results_tree.heading(col, text=col)

    def perform_keyword_search(self, keyword, tree):
        for i in tree.get_children():
            tree.delete(i)
        query = '''
            SELECT * FROM archer
            WHERE Keyword1 LIKE ? OR Keyword2 LIKE ? OR Keyword3 LIKE ?
            '''
        parameters = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        records = self.run_query(query, parameters)
        for row in records:
            tree.insert('', 'end', values=row)

    def open_barcode_search_window(self):
        barcode_search_window = Toplevel(self.root)
        barcode_search_window.title('Barcode Search')
        barcode_search_window.geometry('600x400')

        Label(barcode_search_window, text='Enter Barcode:').pack(pady=10)

        search_entry = Entry(barcode_search_window)
        search_entry.pack(pady=10)

        search_button = Button(barcode_search_window, text='Search', command=lambda: self.perform_barcode_search(search_entry.get(), search_results_tree))
        search_button.pack(pady=10)

        # Setup the Treeview
        columns = ('Barcode', 'Title', 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Physical Location', 'Virtual Location',
                   'Description')
        search_results_tree = ttk.Treeview(barcode_search_window, columns=columns, show='headings')
        search_results_tree.pack(pady=20, fill=BOTH, expand=True)
        for col in columns:
            search_results_tree.heading(col, text=col)

    def perform_barcode_search(self, barcode, tree):
        print("Search Triggered for barcode: ", barcode)
        for i in tree.get_children():
            tree.delete(i)
        query = '''
                SELECT * FROM archer
                WHERE Barcode = ?
                '''
        parameters = (barcode,)  # Ensure this is a tuple by including the comma
        records = self.run_query(query, parameters)
        for row in records:
            tree.insert('', 'end', values=row)

    def open_keyword_search_window(self):
        keyword_search_window = Toplevel(self.root)
        keyword_search_window.title('Keyword Search')
        keyword_search_window.geometry('600x400')

        Label(keyword_search_window, text='Enter Keyword:').pack(pady=10)

        search_entry = Entry(keyword_search_window)
        search_entry.pack(pady=10)

        search_button = Button(keyword_search_window, text='Search',
                               command=lambda: self.perform_keyword_search(search_entry.get(), search_results_tree))
        search_button.pack(pady=10)

        # Setup the Treeview
        columns = ('Barcode', 'Title', 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Physical Location', 'Virtual Location',
                   'Description')
        search_results_tree = ttk.Treeview(keyword_search_window, columns=columns, show='headings')
        search_results_tree.pack(pady=20, fill=BOTH, expand=True)
        for col in columns:
            search_results_tree.heading(col, text=col)

    def perform_keyword_search(self, keyword, tree):
        for i in tree.get_children():
            tree.delete(i)
        query = '''
               SELECT * FROM archer
               WHERE Keyword1 LIKE ? OR Keyword2 LIKE ? OR Keyword3 LIKE ?
               '''
        parameters = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        records = self.run_query(query, parameters)
        for row in records:
            tree.insert('', 'end', values=row)

    def open_description_search_window(self):
        description_search_window = Toplevel(self.root)
        description_search_window.title('Description Search')
        description_search_window.geometry('600x400')

        Label(description_search_window, text='Enter Description Keywords:').pack(pady=10)

        search_entry = Entry(description_search_window)
        search_entry.pack(pady=10)

        search_button = Button(description_search_window, text='Search',
                               command=lambda: self.perform_description_search(search_entry.get(), search_results_tree))
        search_button.pack(pady=10)

        # Setup the Treeview
        columns = ('Barcode', 'Title', 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Physical Location', 'Virtual Location',
                   'Description')
        search_results_tree = ttk.Treeview(description_search_window, columns=columns, show='headings')
        search_results_tree.pack(pady=20, fill=BOTH, expand=True)
        for col in columns:
            search_results_tree.heading(col, text=col)

    def perform_description_search(self, description, tree):
        for i in tree.get_children():
            tree.delete(i)
        query = '''
                SELECT * FROM archer
                WHERE Description LIKE ?
                '''
        # This prepares the parameter to be '%' + description + '%'
        # which is SQL for "contains the phrase 'description'"
        parameters = ('%' + description + '%',)
        records = self.run_query(query, parameters)
        for row in records:
            tree.insert('', 'end', values=row)

    def open_general_search_window(self):
        general_search_window = Toplevel(self.root)
        general_search_window.title('General Search')
        general_search_window.geometry('600x400')

        Label(general_search_window, text='Enter Search Term:').pack(pady=10)

        search_entry = Entry(general_search_window)
        search_entry.pack(pady=10)

        search_button = Button(general_search_window, text='Search',
                               command=lambda: self.perform_general_search(search_entry.get(), search_results_tree))
        search_button.pack(pady=10)

        # Setup the Treeview
        columns = ('Barcode', 'Title', 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Physical Location', 'Virtual Location',
                   'Description')
        search_results_tree = ttk.Treeview(general_search_window, columns=columns, show='headings')
        search_results_tree.pack(pady=20, fill=BOTH, expand=True)
        for col in columns:
            search_results_tree.heading(col, text=col)

    def perform_general_search(self, term, tree):
        for i in tree.get_children():
            tree.delete(i)
        query = '''
                SELECT * FROM archer
                WHERE Title LIKE ? OR Keyword1 LIKE ? OR Keyword2 LIKE ? OR Keyword3 LIKE ? OR Description LIKE ?
                '''
        like_term = f'%{term}%'
        parameters = (like_term, like_term, like_term, like_term, like_term)
        records = self.run_query(query, parameters)
        for row in records:
            tree.insert('', 'end', values=row)

if __name__ == '__main__':
    root = Tk()
    root.geometry('800x600')  # Set the window size to 800x600
    application = Archer_Portal(root)
    root.mainloop()

    # Configure the root grid to expand
    root.grid_rowconfigure(0, weight=1)  # Makes the row containing your main content expandable
    root.grid_columnconfigure(0, weight=1)  # Makes the column containing your main content expandable

    root.mainloop()