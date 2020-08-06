from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import time
import sqlite3


class SchoolPortal():
    db = 'schoolportal.db'

    def __init__(self, root):
        self.root = root
        self.root.title('school portal')

        # adding portal logo and title
        self.logo = ImageTk.PhotoImage(
            Image.open('images/icon.png').resize((120, 90)))
        self.logo_label = Label(image=self.logo)
        self.logo_label.grid(row=0, column=0)

        self.app_title = Label(font=('arial', 15, 'bold'),
                               text='school database system',
                               fg="dark red")
        self.app_title.grid(row=1, column=0)

        # adding input section
        self.entry_frame = LabelFrame(text='add a record')
        self.entry_frame.grid(row=0, column=1)

        Label(self.entry_frame, text='Firstname').grid(row=0,
                                                       column=1,
                                                       sticky=W)
        self.first_name = Entry(self.entry_frame)
        self.first_name.grid(row=0, column=2)

        Label(self.entry_frame, text='Lastname').grid(row=1,
                                                      column=1,
                                                      sticky=W)
        self.last_name = Entry(self.entry_frame)
        self.last_name.grid(row=1, column=2)

        Label(self.entry_frame, text='Email').grid(row=2, column=1, sticky=W)
        self.email = Entry(self.entry_frame)
        self.email.grid(row=2, column=2)

        Label(self.entry_frame, text='Gender').grid(row=3, column=1, sticky=W)
        self.gender = Entry(self.entry_frame)
        self.gender.grid(row=3, column=2)

        Label(self.entry_frame, text='Age').grid(row=4, column=1, sticky=W)
        self.age = Entry(self.entry_frame)
        self.age.grid(row=4, column=2)

        # adding form submit button
        ttk.Button(self.entry_frame,
                   text='Add',
                   command=self.add_records_button).grid(row=5,
                                                         column=1,
                                                         columnspan=2,
                                                         pady=7)

        # adding action insight message
        self.action_message = Label(self.entry_frame, text='')
        self.action_message.grid(row=6, column=1, columnspan=2)

        # adding database view area
        self.database_view = ttk.Treeview(height=10,
                                          column=['', '', '', '', ''])
        self.database_view.grid(row=7, column=0, columnspan=2)

        self.database_view.heading('#0', text='ID')
        self.database_view.column('#0', width=50)

        self.database_view.heading('#1', text='First Name')
        self.database_view.column('#1', width=105)

        self.database_view.heading('#2', text='Last Name')
        self.database_view.column('#2', width=105)

        self.database_view.heading('#3', text='Email')
        self.database_view.column('#3', width=130)

        self.database_view.heading('#4', text='Gender')
        self.database_view.column('#4', width=80)

        self.database_view.heading('#5', text='Age')
        self.database_view.column('#5', width=60, stretch=False)

        # add current time and day
        def current_time_and_day():
            today = datetime.now()
            today = '{:%B %d, %Y}'.format(today)
            self.dateinfo.config(text=today)

            current_time = time.strftime('%I:%M %p')
            self.timeinfo.config(text=current_time)
            self.timeinfo.after(200, current_time_and_day)

        self.dateinfo = Label(font=('arial', 12), fg='green')
        self.dateinfo.grid(row=8, column=1, columnspan=2, sticky=E, padx=10)

        self.timeinfo = Label(font=('arial', 12), fg='green')
        self.timeinfo.grid(row=8, column=0, sticky=W)

        current_time_and_day()

        # add menu

        menu_bar = Menu()
        item = Menu()

        item.add_command(label='add record', command=self.add_records_button)
        item.add_command(label='edit record', command=self.edit_student_record)
        item.add_command(label='delete record', command=self.delete_student)
        item.add_separator()
        item.add_command(label='help', command=self.help)
        item.add_command(label='exit', command=self.ex)

        menu_bar.add_cascade(label='file', menu=item)
        menu_bar.add_cascade(label='add', command=self.add_records_button)
        menu_bar.add_cascade(label='edit', command=self.edit_student_record)
        menu_bar.add_cascade(label='delete', command=self.delete_student)
        menu_bar.add_cascade(label='help',  command=self.help)
        menu_bar.add_cascade(label='exit', command=self.ex)

        root.config(menu=menu_bar)
        self.view_db_records()

    # querying the database
    def run_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE if not EXISTS students
                (ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                first_name STR, 
                last_name STR, 
                email STR, 
                gender STR, 
                age INTEGER )""")
            query_result = cursor.execute(query, parameters)
            connection.commit()

        return query_result

    # add all database student records to the view section
    def view_db_records(self):
        records = self.database_view.get_children()
        for element in records:
            self.database_view.delete(element)
        query = 'SELECT * from students'

        db_table = self.run_db_query(query)

        for data in db_table:
            self.database_view.insert('', 1000, text=data[0], values=data[1:])

    # validating new record input
    def validate_input(self):
        return (len(self.first_name.get()) != 0
                and len(self.last_name.get()) != 0
                and len(self.email.get()) != 0 and len(self.gender.get()) != 0
                and len(self.age.get()) != 0)

    # adding a new record to the students database
    def add_new_student(self):
        query = "INSERT INTO students VALUES (NULL,?,?,?,?,?)"
        parameters = (self.first_name.get(), self.last_name.get(),
                      self.email.get(), self.gender.get(), self.age.get())
        self.run_db_query(query, parameters)
        self.action_message.config(
            text=f'{self.first_name.get()} has been succefully added',
            fg='green')

        # clear input section after adding a new record
        self.first_name.delete(0, END)
        self.last_name.delete(0, END)
        self.email.delete(0, END)
        self.gender.delete(0, END)
        self.age.delete(0, END)

        self.view_db_records()

    def add_records_button(self):
        if not self.validate_input():
            self.action_message.config(text='please complete all fields',
                                       fg='red')
        else:
            add = messagebox.askquestion(
                'ADD RECORD', 'Are you sure you want to add this person ?')
            if add == 'yes':
                self.add_new_student()

    # deleting a record from the students table
    def delete_student(self):
        try:
            self.database_view.item(
                self.database_view.selection())['values'][1]
        except IndexError as e:
            messagebox.showerror(
                'ERROR', 'please select the student you want to delete')
            return
        validation_popup = messagebox.showwarning(
            'DELETE RECORD', 'this student will be deleted')
        if validation_popup == 'ok':

            id_value = self.database_view.item(
                self.database_view.selection())['text']
            print(id_value)
            query = "DELETE FROM students WHERE ID = ?"
            self.run_db_query(query, (id_value, ))
            self.action_message.config(
                text=f'record with ID: {id_value} sucessfully deleted',
                fg='green')

            self.view_db_records()

    # editing a record in the students databease
    def edit_student_record(self):
        try:
            self.database_view.item(
                self.database_view.selection())['values'][0]
        except IndexError as e:
            messagebox.showerror('ERROR',
                                 'select the student record you want to edit')
            return

        first_name = self.database_view.item(
            self.database_view.selection())['values'][0]

        last_name = self.database_view.item(
            self.database_view.selection())['values'][1]

        email = self.database_view.item(
            self.database_view.selection())['values'][2]

        gender = self.database_view.item(
            self.database_view.selection())['values'][3]

        age = self.database_view.item(
            self.database_view.selection())['values'][4]

        # create a new widget where the changes will be made
        self.edit_root = Toplevel()
        self.edit_root.title('Edit Students Record')

        Label(self.edit_root, text='Old Firstname').grid(row=0,
                                                         column=1,
                                                         sticky=W)
        Entry(self.edit_root,
              textvariable=StringVar(self.edit_root, value=first_name),
              state='readonly').grid(row=0, column=2)
        Label(self.edit_root, text='New Firstname').grid(row=1,
                                                         column=1,
                                                         sticky=W)
        new_first_name = Entry(self.edit_root)
        new_first_name.grid(row=1, column=2)

        Label(self.edit_root, text='Old Lastname').grid(row=2,
                                                        column=1,
                                                        sticky=W)
        Entry(self.edit_root,
              textvariable=StringVar(self.edit_root, value=last_name),
              state='readonly').grid(row=2, column=2)
        Label(self.edit_root, text='New Lastname').grid(row=3,
                                                        column=1,
                                                        sticky=W)
        new_last_name = Entry(self.edit_root)
        new_last_name.grid(row=3, column=2)

        Label(self.edit_root, text='Old Email').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root,
              textvariable=StringVar(self.edit_root, value=email),
              state='readonly').grid(row=4, column=2)
        Label(self.edit_root, text='New Email').grid(row=5, column=1, sticky=W)
        new_email = Entry(self.edit_root)
        new_email.grid(row=5, column=2)

        Label(self.edit_root, text='Current Gender').grid(row=6,
                                                          column=1,
                                                          sticky=W)
        Entry(self.edit_root,
              textvariable=StringVar(self.edit_root, value=gender),
              state='readonly').grid(row=6, column=2)
        Label(self.edit_root, text='Change in Gender').grid(row=7,
                                                            column=1,
                                                            sticky=W)
        new_gender = Entry(self.edit_root)
        new_gender.grid(row=7, column=2)

        Label(self.edit_root, text='Old Age').grid(row=8, column=1, sticky=W)
        Entry(self.edit_root,
              textvariable=StringVar(self.edit_root, value=age),
              state='readonly').grid(row=8, column=2)
        Label(self.edit_root, text='New Age').grid(row=9, column=1, sticky=W)
        new_age = Entry(self.edit_root)
        new_age.grid(row=9, column=2)

        save_changes_button = Button(
            self.edit_root,
            text='save changes',
            command=lambda: self.edit_record(
                first_name, last_name, new_first_name.get(), new_last_name.get(
                ), new_email.get(), new_gender.get(), new_age.get()))
        save_changes_button.grid(row=10, column=1, columnspan=2)

        self.edit_root.mainloop()

    # update database with changes
    def edit_record(self, firstname, lastname, newfname, newlname, newemail,
                    newgender, newage):
        validation_popup = messagebox.showinfo(
            '', 'Press OK to CONFIRM these changes')
        if validation_popup == 'ok':
            query = """
                UPDATE students SET first_name=?, last_name=?, email=?, 
                gender=?, age=? WHERE first_name=? AND last_name=?
                """
            parameters = (newfname, newlname, newemail, newgender, newage,
                          firstname, lastname)
            self.run_db_query(query, parameters)
            self.edit_root.destroy()
            self.action_message.config(text=f'{firstname} updated succesfully',
                                       fg='green')
            self.view_db_records()

    def help(self):
        messagebox.showinfo('LOG', 'contact us at Example@gmail.com')
    
    def ex(self):
        if messagebox.askyesno('Exit', 'Are you sure you want to quit'):
            quit()


def main():
    root = Tk()
    root.geometry('530x465+500+200')
    application = SchoolPortal(root)
    root.mainloop()


main()
