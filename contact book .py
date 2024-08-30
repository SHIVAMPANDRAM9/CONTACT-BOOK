from tkinter import *
from tkinter import messagebox
import sqlite3 as sql 

conn = sql.connect('contacts.db')
cursor  = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (name TEXT ,phone TEXT , email TEXT )''')
conn.commit()

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name == "" or phone == "" or email =="":
        messagebox.showerror("Error","All fileds are required ")
    else:
        cursor.execute('INSERT INTO contacts VALUES (?, ?, ?)',(name, phone, email))
        conn.commit()
        list_contacts()  # Function call 
        clear_entries()

# function to delete a selected contact 
def delete_contact():
    try:
        selected_contact = contact_listbox.get(contact_listbox.curselection())
        cursor.execute('DELETE FROM contacts WHERE name=? AND phone=?AND email=?', selected_contact)
        conn.commit()        
        list_contacts() # Function call
    except:
        messagebox.showerror("Error","No contact selected")  

# function to ypdate a selected contact 
def update_contact():
    try:
        selected_contact = contact_listbox.get(contact_listbox.curselection())
        name, phone, email = selected_contact

        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()

        cursor.execute('UPDATE contacts SET name=?, phone=?, email=? WHERE name=? AND phone=? AND email=?',(new_name, new_phone,new_email, name, phone, email))
        conn.commit()
        list_contacts() # Function call 
    except:
        messagebox.showerror("Error", "No contact selected")  

def clear_entries():
    name_entry.delete(0, END)       
    phone_entry.delete(0, END)  
    email_entry.delete(0, END)   

def list_contacts():
    contact_listbox.delete(0, END)
    try:
        cursor.execute('SELECT * FROM contacts')
        for contact in cursor.fetchall():
            contact_listbox.insert(END, contact)
    except sql.Error as e:
        print(f"Database error: {e}")        
root = Tk()
root.title("Contact Book")    
root.geometry("500x400")

name_label = Label(root, text="Name")
name_label.pack()
name_entry = Entry(root)
name_entry.pack()

phone_label = Label(root, text="Phone")
phone_label.pack()
phone_entry = Entry(root)
phone_entry.pack()

email_label = Label(root, text="Email")
email_label.pack()
email_entry = Entry(root)
email_entry.pack()

add_button = Button(root, text="Add Contact", command=add_contact)
add_button.pack()

update_button = Button(root, text="Update Contact", command=update_contact)
update_button.pack()

delete_button = Button(root, text="Delete Contact", command=delete_contact)
delete_button.pack()

contact_listbox = Listbox(root)
contact_listbox.pack(fill=BOTH, expand=1)

list_contacts() # Function call

root.mainloop()