from tkinter import *
from dotenv import set_key
import os

def save_env_and_start():
    set_key(".env", "DB_NAME", "store.db")
    set_key(".env", "PROVIDER_NAME", store_name.get())
    set_key(".env", "BANK_ACCOUNT", bank_account.get())
    set_key(".env", "BANK_CODE", bank_code.get())
    set_key(".env", "FIRST_RUN", "false")  # Disable setup on next run

    setup.destroy()
    os.system("python billing_app_main.py")  # Change filename if needed

setup = Tk()
setup.title("Initial Store Setup")
setup.geometry("350x300")

Label(setup, text="Store Name").pack(pady=5)
store_name = Entry(setup, font=("Arial", 12))
store_name.pack(pady=5)

Label(setup, text="Bank Account").pack(pady=5)
bank_account = Entry(setup, font=("Arial", 12))
bank_account.pack(pady=5)

Label(setup, text="Bank Code").pack(pady=5)
bank_code = Entry(setup, font=("Arial", 12))
bank_code.pack(pady=5)

Button(setup, text="Save & Launch App", font=("Arial", 12), command=save_env_and_start).pack(pady=20)
setup.mainloop()
