# Skattkistan är en lösenordshanterare skapt för att underlätta lösenordsgeneration samt hantering för användare av alla slag.
# Programmet har en enkel grafisk interface där användare kan definiera längden av önskat lösenord, generera detta med ett knapptryck och
# sedan hantera dessa genererade lösenord genom att visa, kopiera eller ta bort existerande lösenord.

from tkinter import *  # Tkinter för att skapa GUI:n
from tkinter import ttk
import string # För att enkelt kunna definiera ett objekt som innehåller A-Z + 0-9 + all punctuation.
import secrets # Bättre variant av "random" som generar mer kryptografiskt säkra lösenord

root = Tk()                 # Skapa ett tkinter fönster som kallas "Skattkistan"
root.title("Skattkistan")
root.geometry("800x500")

group = Frame(root, bg="#f5f5f5", bd=4, relief=RAISED)          # Frame 1 som ska inkludera längd-definitionen samt
group.place(relx=0.03, rely=0.1, relheight=0.8, relwidth=0.4)     # lösen-generationswidgeten. 

separate = ttk.Separator(root, orient="vertical")           # Visuell separator för att skilja på frame 1 och 2
separate.place(relx=0.47, rely=0, relwidth=0.2, relheight=1)

group2 = Frame(root, bg="#f5f5f5", bd=4, relief=SUNKEN)         # Frame två där skapade lösenord ska sparas
group2.place(relx=0.51, rely=0.1, relheight=0.8, relwidth=0.4)

txt_label = Label(group, text = "Längd: ")   # Definierar att det efterfrågas "Längd" vid input-fältet
txt_label.place(relx=0.35, rely=0.28, relwidth=0.3)

def save_length(*args):         # Funktion för att spara längden som användaren definierar
    value = length.get()
    return value

length = StringVar()
length.trace_add("write", save_length)      # Varje gång entryfältet "längd" skrivs till så kalla på funktionen
txt = Entry(group, textvariable=length)      # "save_length" för att spara ned det senaste värdet.
txt.place(relx=0.35, rely=0.35, relwidth=0.3)

rowcount = 0                # Adderas med 1 efter varje lösenordsgeneration för att lösenorden ska ordnas efter varandra i GUI:n

def passgen():
        try:
            global rowcount
            length = int(save_length())
            chars = string.ascii_letters + string.digits + string.punctuation # Alla karaktärer som vanligtvis är tillåtna i lösenord
            password = "".join(secrets.choice(chars) for i in range(length)) # Ta ett slumpat urval från "chars" "length" antal gånger
            pwd_label = Label(group2, text = len(password) * "*")      # Lägg till lösenordet i GUI:n i asterisk-format
            pwd_label.grid(column=0, row=rowcount)
            pwd_labels = []                       # Skapa en lista av alla lösenords widgets
            pwd_labels.append(pwd_label)
            def toggle_password():                  # Funktion för att visa lösenordet när användaren klickar på "?"
                for pwd_lab in pwd_labels:        # För varje individuell widget i listan av widgets  
                    if pwd_lab.cget("text").startswith("*"):    # Om texten i widgeten börjar med asterisker
                        pwd_lab.config(text=password) # Gör om asteriskerna till det faktiska lösenordet
                    else:                             # Men om det inte är asterisker  
                        pwd_lab.config(text=len(password) * "*")    # Gör om det till asterisker
            showbutton = ttk.Button(group2, text="?", command=toggle_password) # Knapp för att visa lösenordet
            showbutton.grid(column=1, row = rowcount)
            def copy_password():                            # För varje individuell label, kopiera specifikt det lösenordet
                 for pwd_lab in pwd_labels:
                    root.clipboard_clear()
                    root.clipboard_append(password)
            showbutton = ttk.Button(group2, text="C", command=copy_password) # Knapp för att kopiera lösenordet
            showbutton.grid(column=2, row= rowcount)

            rowcount += 1
            return password
        except ValueError:                  # Fånga när length blir matad med non-integer värden, int(save_length()) av en string blir ValueError
                  newwindow = Tk()
                  newwindow.title("Error")
                  newwindow.geometry("250x30")
                  errormsg = Label(newwindow, text = "Please only input an integer value")
                  errormsg.pack(anchor=CENTER)
     

buttongen = ttk.Button(group, text="Generera ett lösenord", command=passgen) # Knapp för att generera lösenord
buttongen.place(relx=0.30, rely=0.43, relwidth=0.4)

root.mainloop()


