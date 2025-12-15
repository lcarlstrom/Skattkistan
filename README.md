Detta skript använder tkinter modulen för att skapa en användarinterface som slutligen
ska slås ihop med ett password-gen skript. Password-gen skriptet genererar lösenord baserat
på användardefinerad längd och målet är att eventuellt skapa ett program dylikt "bitwarden".

GUI:n innehåller ett fält för användaren att skriva in längd samt en knapp som genererar lösenord
baserat på denna längd. Vid implementering av lösengenerationslogiken ska output visas i 
i listformat i höger spalt och kunna visas (default syns som asterisker), kopieras, samt tas bort.