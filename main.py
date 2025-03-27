import sqlite3
import os
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "store.db")

os.environ["INVOICE_LANG"] = "en"
provider_name = os.getenv("PROVIDER_NAME", "your-store")
bank_account = os.getenv("BANK_ACCOUNT", "0000-0000-0000-0000")
bank_code = os.getenv("BANK_CODE", "0000")

provider = Provider(provider_name, bank_account=bank_account, bank_code=bank_code)
creator = Creator("Kushal Desai")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice (
        invoice_no INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL NOT NULL,
        customer TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS item (
        serial_no INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (invoice_no) REFERENCES invoice(invoice_no)
    )
""")

conn.commit()

root = Tk()
root.title("Bill Generator")
root.geometry("800x500")

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Customer Name:").grid(row=0, column=0, padx=5, sticky=E)
customer_name = Entry(frame, width=20, font=("Arial", 12))
customer_name.grid(row=0, column=1, padx=5)

Label(frame, text="Address:").grid(row=0, column=2, padx=5, sticky=E)
customer_address = Entry(frame, width=25, font=("Arial", 12))
customer_address.grid(row=0, column=3, padx=5)

Label(frame, text="Mobile Number:").grid(row=0, column=4, padx=5, sticky=E)
customer_mobile = Entry(frame, width=15, font=("Arial", 12))
customer_mobile.grid(row=0, column=5, padx=5)

Label(root, text="Item Name:", font=("Arial", 12)).pack()
item_name = Entry(root, width=40, font=("Arial", 12))
item_name.pack()

Label(root, text="Price:", font=("Arial", 12)).pack()
item_price = Entry(root, width=20, font=("Arial", 12))
item_price.pack()

Label(root, text="Quantity:", font=("Arial", 12)).pack()
item_quantity = Entry(root, width=20, font=("Arial", 12))
item_quantity.pack()

invoice_items = []
bill = None
total = 0

def add_item():
    global bill, total
    name = item_name.get()
    price = item_price.get()
    qty = item_quantity.get()
    customer = customer_name.get()

    if not name or not price or not qty:
        messagebox.showwarning("Warning", "Please fill all item details!")
        return

    try:
        price = float(price)
        qty = int(qty)
    except ValueError:
        messagebox.showerror("Error", "Invalid price or quantity format!")
        return

    if bill is None:
        cursor.execute("INSERT INTO invoice (total, customer) VALUES (?, ?)", (0, customer))
        conn.commit()
        bill = cursor.lastrowid  

    cursor.execute("INSERT INTO item (invoice_no, item_name, price, quantity) VALUES (?, ?, ?, ?)", (bill, name, price, qty))
    conn.commit()

    invoice_items.append(Item(qty, price, description=name))
    total += price * qty  
    messagebox.showinfo("Success", f"Added {name} (Qty: {qty})")

    item_name.delete(0, END)
    item_price.delete(0, END)
    item_quantity.delete(0, END)

def generate_invoice():
    global total, bill
    customer = customer_name.get()
    address = customer_address.get()
    mobile = customer_mobile.get()

    if not customer or not address or not mobile:
        messagebox.showwarning("Warning", "Please enter customer details!")
        return

    if not invoice_items:
        messagebox.showwarning("Warning", "No items added!")
        return

    cursor.execute("UPDATE invoice SET total = ? WHERE invoice_no = ?", (total, bill))
    conn.commit()

    cursor.execute("SELECT MAX(invoice_no) FROM invoice")
    invoice_number = cursor.fetchone()[0]

    client = Client(customer, mobile, address)
    invoice = Invoice(client, provider, creator)

    for item in invoice_items:
        invoice.add_item(item)

    invoice.currency = "Rs"
    invoice.number = invoice_number  

    docu = SimpleInvoice(invoice)
    invoice_path = f"invoices/invoice_{invoice_number}.pdf"
    os.makedirs("invoices", exist_ok=True)
    docu.gen(invoice_path, generate_qr_code=False)

    messagebox.showinfo("Invoice Generated", f"Invoice PDF Created: invoice_{invoice_number}.pdf")
    root.destroy()  

Button(root, text="Add Item", font=("Arial", 12), command=add_item).pack(pady=10)
Button(root, text="Generate Invoice", font=("Arial", 12), command=generate_invoice).pack(pady=10)

root.mainloop()
conn.close()