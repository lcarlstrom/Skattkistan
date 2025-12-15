# Detta skript använder tkinter modulen för att skapa en användarinterface som slutligen
# ska slås ihop med ett password-gen skript. Password-gen skriptet genererar lösenord baserat
# användardefinerad längd och målet är att eventuellt skapa ett program dylikt "bitwarden".

from tkinter import *
from tkinter import ttk

root = Tk()                 # Skapa ett tkinter fönster som kallas "Skattkistan"
root.title("Skattkistan")
root.geometry("800x500")

group = Frame(root, bg="#f5f5f5", bd=4, relief=RAISED)          # Frame 1 som ska inkludera längd-definitionen samt
group.place(relx=0.03, rely=0.1, relheight=0.8, relwidth=0.4)     # lösen-generationswidgeten. 

txt_label = Label(group, text = "Längd: ")   # Definierar att det efterfrågas "Längd" vid input-fältet
txt_label.place(relx=0.35, rely=0.28, relwidth=0.3)

def save_length(*args):         # Funktion för att spara längden som användaren definierar
    value = length.get()

length = StringVar()
length.trace_add("write", save_length)      # Varje gång entryfältet "längd" skrivs till så kalla på funktionen
txt = Entry(group, textvariable=length)      # "save_length" för att spara ned det senaste värdet.
txt.place(relx=0.35, rely=0.35, relwidth=0.3)

buttongen = ttk.Button(group, text="Generera ett lösenord") # Knapp för att generera lösenord
buttongen.place(relx=0.30, rely=0.43, relwidth=0.4)

separate = ttk.Separator(root, orient="vertical")           # Visuell separator för att skilja på frame 1 och 2
separate.place(relx=0.47, rely=0, relwidth=0.2, relheight=1)

group2 = Frame(root, bg="#f5f5f5", bd=4, relief=SUNKEN)     # Frame två där skapade lösenord ska sparas
group2.place(relx=0.51, rely=0.1, relheight=0.8, relwidth=0.4)


root.mainloop()