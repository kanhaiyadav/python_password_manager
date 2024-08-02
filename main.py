import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


decision = "yes"
FONT = "Bahnschrift SemiBold SemiConden"
FREQUENT_EMAIL_ID = "kanhaiya2004yadav@gmail.com"
BG = "#FFEADD"
BUTTON_BG = "#FCAEAE"
EXIT_BUTTON_BG = "#1D5B79"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '@']

    letters = [choice(letters) for _ in range(randint(6, 10))]
    symbols = [choice(symbols) for _ in range(randint(2, 4))]
    numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = letters + numbers + symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ------------------------------ EXIT PROGRAM -----------------------------------#
def terminate():
    window.destroy()


# ----------------------------- Searching for the website ----------------------#
def search_web():
    website = web_entry.get().lower()
    email = email_entry.get().lower()
    key = website + email
    if website == "" or email == "":
        messagebox.showerror(title="Error", message="Please make sure Website and Email / Username field in not empty.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(fp=file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No data file found")
        else:
            if key in data:
                email = data[key]["email"]
                password = data[key]["password"]
                messagebox.showinfo(title=data[key]["website"], message=f"Email: {email}\nPassword: {password}")
                pyperclip.copy(password)
            else:
                messagebox.showerror(title="Error", message="No details of the user on the website found!")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = web_entry.get().lower()
    email = email_entry.get().lower()
    key = website + email
    password = password_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            if key in data:
                global decision
                decision = messagebox.askquestion(
                    message=f"the user {email} is already present in data file.\nDo you want to overwrite?")
    except:
        pass

    finally:
        if decision == "yes":
            new_data = {
                key: {
                    "website": website,
                    "email": email,
                    "password": password
                }
            }
            if website == "" or email == "":
                messagebox.showerror(title="Oops!", message="Make sure all of the field are filled.")
            else:
                try:
                    with open("data.json", "r") as new_file:
                        data = json.load(fp=new_file)

                except FileNotFoundError:
                    with open("data.json", "w") as file:
                        json.dump(obj=new_data, fp=file, indent=4)

                else:
                    with open("data.json", "w") as file:
                        data.update(new_data)
                        json.dump(obj=data, fp=file, indent=4)

                finally:
                    web_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("MyPass - your personal password manager")
window.config(pady=50, padx=50, bg=BG)

canvas = tk.Canvas(width=200, height=200, bg=BG, highlightthickness=0)
logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

web_lbl = tk.Label(text="Website: ", bg=BG, font=(FONT, 13, "normal"), pady=10)
web_lbl.grid(column=0, row=2, sticky='e')
web_entry = tk.Entry(width=27, font=("calibri", 12, "normal"))
web_entry.focus()
web_entry.grid(column=1, row=2, columnspan=2, sticky="w")

search = tk.Button(text="Search", bg="#FCAEAE", width=11, command=search_web)
search.grid(column=2, row=2, sticky="e")

email_lbl = tk.Label(text="Email / username:", bg=BG, font=(FONT, 13, "normal"))
email_lbl.grid(column=0, row=3)
email_entry = tk.Entry(width=39, font=("calibri", 12, "normal"))
email_entry.insert(0, FREQUENT_EMAIL_ID)
email_entry.grid(column=1, row=3, columnspan=2)

password_lbl = tk.Label(text="Password:", bg=BG, font=(FONT, 13, "normal"))
password_lbl.grid(column=0, row=4, pady=10, sticky="e")
password_entry = tk.Entry(width=21, font=("calibri", 12, "normal"))
password_entry.grid(column=1, row=4, sticky="w")

pass_button = tk.Button(text="Generate Password", width=15, bg=BUTTON_BG, command=generate_password)
pass_button.grid(column=2, row=4, sticky="e")

add = tk.Button(text="Add", width=32, bg=BUTTON_BG, command=save_data)
add.grid(column=1, row=5, columnspan=2, sticky='w')

exit_button = tk.Button(text="Exit", width=8, bg=EXIT_BUTTON_BG, fg="white", command=terminate)
exit_button.grid(column=2, row=5, sticky='e')

window.mainloop()
