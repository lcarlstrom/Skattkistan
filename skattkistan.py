# Skattkistan är en lösenordshanterare skapt för att underlätta lösenordsgeneration samt hantering för användare av alla slag.
# Programmet har en enkel grafisk interface där användare kan definiera längden av önskat lösenord, generera detta med ett knapptryck och
# sedan hantera dessa genererade lösenord genom att visa, kopiera eller ta bort existerande lösenord.

from tkinter import *                                               # Tkinter för att skapa GUI:n
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import string                                                       # För att enkelt kunna definiera ett objekt som innehåller A-Z + 0-9 + all punctuation.
import secrets                                                      # Bättre variant av "random" som generar mer kryptografiskt säkra lösenord
from datetime import datetime                                       # För att kunna inkludera datum i loggar
from cryptography.fernet import Fernet, InvalidToken                
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import sys
import sv_ttk
import darkdetect
import json


if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):      # Om skriptet körs som en executable
    os.chdir(os.path.dirname(sys.executable))                       # Sätt "working directory" till samma map som executable ligger i - fungerar lite annorlunda till nederliggande logik

else:                                                               # Om skriptet körs som ett vanligt python-script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))            # Sätt "working directory" till samma map som skriptet ligger i

# Logg-logik som behöver förekomma tidigt, varje funktion eller error som kallas eller sker ska loggas.

Eventerrorlist = []

try:
    with open("log.txt", "r") as file:
        for line in file.readlines():
            line = line.strip()
            Eventerrorlist.append(line)
except:
    open("log.txt", "x")

# Kryptering och nyckelkreation

try:
    with open("salt.bin", "rb") as file:                            # Öppna och läs av saltfilen
        salt = file.read()
except:
    with open("salt.bin", "wb") as file:                            # Om filen inte finns, skapa den och lägg till ett slumpat salt
        salt = os.urandom(16)
        file.write(salt)

def ask_masterpassword():                                           # Skapa en GUI som efterfrågar "Master Password" när funktionen kallas och returnerar detta lösenord, detta är huvudlösenordet för att komma in i applikationen
        masterpass = simpledialog.askstring("Master Password", "Enter your master password: ", show="*")
        if masterpass is None:                                      # Om masterpass är None (händer när man klickar på cancel) 
            Eventerrorlist.append(str(datetime.now()) + " Event" + " masterpass_cancel")
            with open("log.txt", "a") as file:
                for evnt in Eventerrorlist:
                    file.write(evnt + "\n")
            sys.exit(1)                                             # bryt funktionen
        return masterpass.encode()    

masterpass = ask_masterpassword()

kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

key = base64.urlsafe_b64encode(kdf.derive(masterpass))

cipher = Fernet(key)

# Huvud GUI:n

root = Tk()                                                         # Skapa ett tkinter fönster som kallas "Skattkistan"
root.title("Skattkistan")
root.geometry("1050x500")

group = Frame(root, bd=4, relief=RAISED)                            # Frame 1 innehåller längd-entry, manual, versionnummer och toggletheme.
group.place(relx=0.03, rely=0.1, relheight=0.8, relwidth=0.4)        

version = Label(group, text="version 2.0")
version.pack(side=TOP, anchor=W)

centeredwidgets = Frame(group)
centeredwidgets.pack(expand=True)

separate = ttk.Separator(root, orient="vertical")                   # Visuell separator för att skilja på frame 1 och 2
separate.place(relx=0.47, rely=0, relheight=1)

canvas_frame = Frame(root, bd=4, relief=SUNKEN)                     # För att få en snygg border på min canvas. Definieras här för att sätta ovanpå canvas. Vid border på en canvas kan dess barn överlappa bordern på grund av tkinters implementation. Detta undviker det problemet.
canvas_frame.place(relx=0.51, rely=0.1, relheight=0.8, relwidth=0.4)

canvas = Canvas(canvas_frame, bd=0, highlightthickness=0)           # En canvas behövs för att implementera en scrollbar för att skrolla igenom t.ex. en stor mängd lösenord
canvas.pack(fill=BOTH, expand=TRUE)

group2 = Frame(canvas)                                              # Frame två där skapade lösenord ska sparas
window1 = canvas.create_window((10, 10), window=group2, anchor=NW)  

# Manual/Hjälpfönster

helpwindow = None                                                   # Behövs för följande logik som begränsar fönster mängden till 1.

def showhelp():
    global helpwindow
    if helpwindow is None or not helpwindow.winfo_exists():         # Om hjälpfönstret inte finns
        helpwindow = Toplevel()                                     # skapa hjälpfönstret.
        helpwindow.transient(root)                                  # Gör fönstret ett barn av huvudfönstret                        
        helpwindow.title("Guide")
        helpwindow.geometry("750x175+150+150")
        helpmsg = Label(helpwindow, text = """Manual for Skattkistan version 2.0
        Correct use: input a whole number above 0 and below 50 
        into the entry-field titled "length" and press generate.
        Passwords will now generate into the right field.
        These are viewable, copyable and removeable.
        To view a password press "?" 
        To copy a password press "c" 
        To remove a password press "-" """)
        helpmsg.place(relx=0.2, rely=0.1, relheight=0.8, relwidth=0.6)
    Eventerrorlist.append(str(datetime.now()) + " Event" + " showhelp")

helpbutton = ttk.Button(centeredwidgets, text="Help", command=showhelp)

# Scrollbar

def on_configure(event):                                            # När något ändras uppdatera "scrollable" region   
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    

scrollbar = Scrollbar(root, command=canvas.yview)                   # Skapa en scrollbar 
scrollbar.pack(side=RIGHT, fill="y")                                # Placera scrollbaren längst till höger i GUI:n
canvas.configure(yscrollcommand= scrollbar.set)                     # Kopplar canvas till scrollbar så att scrollbar uppdateras när canvas scrollas
group2.bind("<Configure>", on_configure)                            # När storleken på group2 ändras kör funktionen on_configure för att uppdatera scrollregionen         

def mwheelscroll(event):                                            # Ser till att det att scrolla med scrollwheel men bara när användaren har musen efter seperatorn
    global separate                                                 # Importerar "seperate" variabel från tidigare kod eftersom funktionen inte har tillgång till den annars
    mousexcoord = root.winfo_pointerx()                         
    seperatorxcoord = separate.winfo_rootx()
    if mousexcoord > seperatorxcoord:                               # Tillåt bara scrollning när användaren har musen vid lösenordslistan
        top, bottom = canvas.yview()                    
        if top > 0.0 or bottom < 1.0:                               # Tillåt bara scrollning när listan är överfull
            if event.num == 4:                                      # Linux scroll-up
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:                                    # Linux scroll-down
                canvas.yview_scroll(1, "units")
            else:                                                   # Windows 
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind("<MouseWheel>", mwheelscroll)                             # Windows scrollwheel
root.bind("<Button-4>", mwheelscroll)                               # Linux scroll-up
root.bind("<Button-5>", mwheelscroll)                               # Linux scroll-down

# Längd entry box

txt_label = Label(centeredwidgets, text = "Length: ")                         # Definierar att det efterfrågas "Längd" vid input-fältet

def save_length(*args):                                             # Funktion för att spara längden som användaren definierar
    value = length.get()
    return value

length = StringVar()
length.trace_add("write", save_length)                              # Varje gång entryfältet "längd" skrivs till så kalla på funktionen
txt = Entry(centeredwidgets, textvariable=length)                             # "save_length" för att spara ned det senaste värdet.

# Lösenordsgeneration och inläsning

rowcount = 0                                                        # Adderas med 1 efter varje lösenordsgeneration för att lösenorden ska ordnas efter varandra i GUI:n
errorwindow = None                                                  # Behövs för följande logik som begränsar error-fönster mängden till 1.

savedpasswords = []
encryptedpass = []

try:                                                                # Testa att öppna filen för inläsning av lösenord
    with open("password.txt", "rb") as file:
        for line in file.readlines():
            line = line.strip()
            encryptedpass.append(line)
            decrypted = cipher.decrypt(line)
            savedpasswords.append(decrypted.decode())

except (FileNotFoundError, InvalidToken) as error:
    if type(error) == FileNotFoundError:                                                    # Om filen inte finns så skapa den
        file = open("password.txt", "wb")
        Eventerrorlist.append(str(datetime.now()) + " Error" + " FileNotFoundError")
    elif type(error) == InvalidToken:                                                       # Om lösenordet är fel (Fernet raisar "InvalidToken" när den försöker avkryptera med en inkorrekt nyckel, d.v.s en nyckel som skapades med fel lösenord)
        root.withdraw()                                                                     # skapa en messagebox som säger "Invalid master password"
        messagebox.showerror("Error", "Invalid master password")
        root.destroy()
        Eventerrorlist.append(str(datetime.now()) + " Error" + " InvalidToken")
        with open("log.txt", "a") as file:
            for evnt in Eventerrorlist:
                file.write(evnt + "\n")
        sys.exit(1)

def passgen(*args):
        try:
            global rowcount
            if savedpasswords:                                                              # Om listan av lösenord inte är tom
                password = savedpasswords.pop(0)                                            # Sätt lösenordet till första elementet i listan och sen ta bort elementet
                encrypted = encryptedpass.pop(0)
            else:    
                length = int(save_length())
                if 0 < length < 50:
                    length = length                                                         # Tillåt längden att bli det användardefinierade
                else:
                    length = "Invalid"                                                      # Gör längden till en str om den är 0 eller mindre för att raise TypeError vid password variabel
                                                                                            # fångar sedan detta för att printa ut unikt "Input length greater than 0" error msg till användaren
                chars = string.ascii_letters + string.digits + string.punctuation           # Alla karaktärer som vanligtvis är tillåtna i lösenord
                password = "".join(secrets.choice(chars) for i in range(length))            # Ta ett slumpat urval från "chars" "length" antal gånger
                encrypted = cipher.encrypt(password.encode())
                with open("password.txt", "ab") as file:
                    file.write(encrypted + b"\n")
            pwd_label = Label(group2, text = len(password) * "*")                           # Lägg till lösenordet i GUI:n i asterisk-format
            pwd_label.grid(column=0, row=rowcount)
            pwd_labels = []                                                                 # Skapa en lista av alla lösenord widgets
            pwd_labels.append(pwd_label)
            Eventerrorlist.append(str(datetime.now()) + " Event" + " passgen")
            
            def toggle_password():                                                          # Funktion för att visa lösenordet när användaren klickar på "?"
                for pwd_label in pwd_labels:                                                # För varje individuell widget i listan av widgets  
                    if pwd_label.cget("text") == len(password) * "*":                       # Om lösenordet nu visas som asterisker
                        pwd_label.config(text=password)                                     # Gör om asteriskerna till det faktiska lösenordet
                    else:                                                                   # Men om det inte är asterisker  
                        pwd_label.config(text=len(password) * "*")                          # Gör om det till asterisker
                Eventerrorlist.append(str(datetime.now()) + " Event" + " toggle_password")
            
            showbutton = ttk.Button(group2, text="?", command=toggle_password)              # Knapp för att visa lösenordet
            showbutton.grid(column=1, row = rowcount)
            
            def copy_password():                                                            # För varje individuell label, kopiera specifikt det lösenordet
                for pwd_label in pwd_labels:
                    root.clipboard_clear()
                    root.clipboard_append(password)
                Eventerrorlist.append(str(datetime.now()) + " Event" + " copy_password")

            copybutton = ttk.Button(group2, text="C", command=copy_password)                # Knapp för att kopiera lösenordet
            copybutton.grid(column=2, row= rowcount)

            def remove_password(encrypted):                                                 # Ta bört lösenordet
                pwd_label.destroy()
                showbutton.destroy()
                copybutton.destroy()
                deletebutton.destroy()
                canvas.update_idletasks()                                                   # Rita om GUI:n när lösenordet har tagits bort.

                with open("password.txt", "rb") as file:
                    passwords = file.readlines()

                with open("password.txt", "wb") as file:
                    for pword in passwords:
                        if pword.strip() != encrypted:
                            file.write(pword)

                Eventerrorlist.append(str(datetime.now()) + " Event" + " remove_password")

            deletebutton = ttk.Button(group2, text="-", command=lambda encrypted = encrypted: remove_password(encrypted))        # Knapp för att ta bort lösenordet - sätter en lokal lambda variable "encrypted" som fångar värdet av encrypted vid line 193
            deletebutton.grid(column=3, row= rowcount)

            rowcount += 1
            return password
        except (ValueError, TypeError) as error:                                            # Fånga när length blir matad med non-integer värden eller en längd av 0
                global errorwindow
                if errorwindow is None or not errorwindow.winfo_exists():                   # Se till att errorfönstret inte redan finns
                    errorwindow = Toplevel()
                    errorwindow.transient(root)                                             # Gör fönstret ett barn av root fönstret
                    errorwindow.title("Error")
                    errorwindow.geometry("350x30+300+250")
                    if type(error) == ValueError:                                           # Om input är ett non-integer värde                                       
                        errormsg = Label(errorwindow, text = "Please only input an integer value")
                        Eventerrorlist.append(str(datetime.now()) + " Error" + " ValueError")
                    elif type(error) == TypeError:                                          # Om input är 0
                        errormsg = Label(errorwindow, text = "Please input a length greater than 0 and less than 50")
                        Eventerrorlist.append(str(datetime.now()) + " Error" + " TypeError")
                    errormsg.pack(anchor=CENTER)
   
while savedpasswords:                                                                       # Om listan av sparade lösenord inte är tom
    passgen()                                                                               # kalla funktionen passgen() som kommer mata in listan i GUI:n.


buttongen = ttk.Button(centeredwidgets, text="Generate password", command=passgen)                    # Knapp för att generera lösenord
txt.bind("<Return>", passgen)                                                               # Tillåt att användaren klickar enter i input-fältet för generera ett lösenord.

txt_label.pack()                                                                            # Uppdaterad logik som tillsammans med centered widgets ser till att alla knappar i vänstra spalten
txt.pack()                                                                                  # är ordentligt centrerade
buttongen.pack()
helpbutton.pack()

#Preferences
try:
    with open("preferences.txt", "r") as file:
        prefdict = json.load(file)
except:
    prefdict = {}
    with open("preferences.txt", "w") as file:
        json.dump(prefdict, file)

#Tema
if "theme" in prefdict:                                                                     # Om det finns ett sparat tema så läs in det
    sv_ttk.set_theme(prefdict["theme"])
else:
    sv_ttk.set_theme(darkdetect.theme())                                                    # Annars sätt temat till samma som användarens maskin

def saveandtoggletheme():
    sv_ttk.toggle_theme()
    Eventerrorlist.append(str(datetime.now()) + " Event" + " ToggleTheme")
    prefdict["theme"] = str(sv_ttk.get_theme())
    with open("preferences.txt", "w") as file:
        json.dump(prefdict, file)

toggletheme = ttk.Button(group, text = "Toggle Theme", command = saveandtoggletheme)
toggletheme.pack(side=BOTTOM, anchor=W)

root.mainloop()

# Logg-hantering

Eventerrorlist.sort()

with open("log.txt", "w") as file:
    for evnt in Eventerrorlist:
        file.write(evnt + "\n")