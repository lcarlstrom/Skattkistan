# Skattkistan är en lösenordshanterare skapt för att underlätta lösenordsgeneration samt hantering för användare av alla slag.
# Programmet har en enkel grafisk interface där användare kan definiera längden av önskat lösenord, generera detta med ett knapptryck och
# sedan hantera dessa genererade lösenord genom att visa, kopiera eller ta bort existerande lösenord.

from tkinter import *                                               # Tkinter för att skapa GUI:n
from tkinter import ttk
import string                                                       # För att enkelt kunna definiera ett objekt som innehåller A-Z + 0-9 + all punctuation.
import secrets                                                      # Bättre variant av "random" som generar mer kryptografiskt säkra lösenord

root = Tk()                                                         # Skapa ett tkinter fönster som kallas "Skattkistan"
root.title("Skattkistan")
root.geometry("800x500")

group = Frame(root, bg="#f5f5f5", bd=4, relief=RAISED)            # Frame 1 som ska inkludera längd-definitionen samt
group.place(relx=0.03, rely=0.1, relheight=0.8, relwidth=0.4)       # lösen-generationswidgeten. 
version = Label(group, text="version 1.6", bg="#f5f5f5")
version.place(relx=0.01, rely=0.01, relwidth=0.2)

helpwindow = None                                                   # Hjälpfönstret finns inte förens det skapas

def showhelp():
    global helpwindow
    if helpwindow is None or not helpwindow.winfo_exists():         # Om hjälpfönstret inte finns
        helpwindow = Toplevel()                                     # skapa hjälpfönstret.
        helpwindow.transient(root)                                  # Gör fönstret ett barn av huvudfönstret                        
        helpwindow.grab_set()                                       # Tvinga input innan det går att interagera med andra fönster
        helpwindow.title("Guide")
        helpwindow.geometry("600x175")
        helpmsg = Label(helpwindow, text = """Manual for Skattkistan version 1.6 
        Correct use: input whole number(s) into the entry-field 
        titled "length" and press generate.
        Passwords will now generate into the right field.
        These are viewable, copyable and removeable.
        To view a password press "?" 
        To copy a password press "c" 
        To remove a password press "-" """)
        helpmsg.place(relx=0.2, rely=0.1, relheight=0.8, relwidth=0.6)

helpbutton = ttk.Button(group, text="Help", command=showhelp)
helpbutton.place(relx=0.40, rely=0.50, relwidth=0.2)

separate = ttk.Separator(root, orient="vertical")                   # Visuell separator för att skilja på frame 1 och 2
separate.place(relx=0.47, rely=0, relwidth=0.2, relheight=1)

canvas = Canvas(root, bg="#f5f5f5", bd=4, relief=SUNKEN)          # Skapar en canvas där min frame finns och alla mina widgets
canvas.place(relx=0.51, rely=0.1, relheight=0.8, relwidth=0.4)

group2 = Frame(canvas, bg="#f5f5f5")                                              # Frame två där skapade lösenord ska sparas
window1 = canvas.create_window((10, 10), window=group2, anchor=NW)  
def windowsize(event):                                              # Resize fönstret så att frame "group2" endast ligger inuti canvas
    canvas.itemconfig(window1, width=canvas.winfo_width() - 20, height=canvas.winfo_height() - 20)

def on_configure(event):                                            # När något ändras uppdatera "scrollable" region   
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollbar = Scrollbar(root, command=canvas.yview)                   # Skapa en scrollbar 
scrollbar.pack(side=RIGHT, fill="y")                                # Placera scrollbaren längst till höger i GUI:n
canvas.configure(yscrollcommand= scrollbar.set)                     # Kopplar canvas till scrollbar så att scrollbar uppdateras när canvas scrollas
group2.bind("<Configure>", on_configure)                            # När storleken på group2 ändras kör funktionen on_configure för att uppdatera scrollregionen         

txt_label = Label(group, text = "Length: ", bg="#f5f5f5")                         # Definierar att det efterfrågas "Längd" vid input-fältet
txt_label.place(relx=0.35, rely=0.28, relwidth=0.3)

def save_length(*args):                                             # Funktion för att spara längden som användaren definierar
    value = length.get()
    return value

length = StringVar()
length.trace_add("write", save_length)                              # Varje gång entryfältet "längd" skrivs till så kalla på funktionen
txt = Entry(group, textvariable=length)                             # "save_length" för att spara ned det senaste värdet.
txt.place(relx=0.35, rely=0.35, relwidth=0.3)

rowcount = 0                                                        # Adderas med 1 efter varje lösenordsgeneration för att lösenorden ska ordnas efter varandra i GUI:n
errorwindow = None                                                  # Errorfönstret finns inte innan det skapas.

def passgen():
        try:
            global rowcount
            length = int(save_length())
            chars = string.ascii_letters + string.digits + string.punctuation           # Alla karaktärer som vanligtvis är tillåtna i lösenord
            password = "".join(secrets.choice(chars) for i in range(length))            # Ta ett slumpat urval från "chars" "length" antal gånger
            pwd_label = Label(group2, text = len(password) * "*", bg="#f5f5f5")                       # Lägg till lösenordet i GUI:n i asterisk-format
            pwd_label.grid(column=0, row=rowcount)
            pwd_labels = []                                                             # Skapa en lista av alla lösenord widgets
            pwd_labels.append(pwd_label)
            
            def toggle_password():                                                      # Funktion för att visa lösenordet när användaren klickar på "?"
                for pwd_label in pwd_labels:                                            # För varje individuell widget i listan av widgets  
                    if pwd_label.cget("text") == len(password) * "*":                   # Om lösenordet nu visas som asterisker
                        pwd_label.config(text=password)                                 # Gör om asteriskerna till det faktiska lösenordet
                    else:                                                               # Men om det inte är asterisker  
                        pwd_label.config(text=len(password) * "*")                      # Gör om det till asterisker
            showbutton = ttk.Button(group2, text="?", command=toggle_password)          # Knapp för att visa lösenordet
            showbutton.grid(column=1, row = rowcount)
            
            def copy_password():                                                        # För varje individuell label, kopiera specifikt det lösenordet
                 for pwd_label in pwd_labels:
                    root.clipboard_clear()
                    root.clipboard_append(password)
            copybutton = ttk.Button(group2, text="C", command=copy_password)            # Knapp för att kopiera lösenordet
            copybutton.grid(column=2, row= rowcount)

            def remove_password():                                                      # För varje individuell label, ta bort lösenordet och alla knappar
                 for pwd_label in pwd_labels:
                      pwd_label.destroy()
                      showbutton.destroy()
                      copybutton.destroy()
                      deletebutton.destroy()
                     # if len(group2.winfo_children()) == 0:                            # Om det inte finns några labels kvar
                     #      group2.destroy()                                            # Ta bort frame "group2", annars stannar label1 kvar
            deletebutton = ttk.Button(group2, text="-", command=remove_password)        # Knapp för att ta bort lösenordet
            deletebutton.grid(column=3, row= rowcount)

            rowcount += 1
            return password
        except ValueError:                                                              # Fånga när length blir matad med non-integer värden, int(save_length()) av en string blir ValueError
                  global errorwindow
                  if errorwindow is None or not errorwindow.winfo_exists():             # Se till att errorfönstret inte redan finns
                    errorwindow = Toplevel()
                    errorwindow.transient(root)                                         # Gör fönstret ett barn av root fönstret
                    errorwindow.grab_set()                                              # Tvinga input innan interaktion med andra fönster
                    errorwindow.title("Error")
                    errorwindow.geometry("250x30")
                    errormsg = Label(errorwindow, text = "Please only input an integer value")
                    errormsg.pack(anchor=CENTER)
   

buttongen = ttk.Button(group, text="Generate password", command=passgen)                # Knapp för att generera lösenord
buttongen.place(relx=0.30, rely=0.43, relwidth=0.4)


root.mainloop()


