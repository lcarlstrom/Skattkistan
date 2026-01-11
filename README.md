Skattkistan är en single-vault lösenordshanterare skapt för att underlätta lösenordsgeneration och hantering för användare.
Programmet har en enkel grafisk interface där användare kan definiera längden av önskat lösenord, generera detta med ett knapptryck, visa det genererade lösenordet, kopiera det oberoende av visningsläge och ta bort befintliga lösenord.

Vid körning av skriptet efterfrågas ett master lösenord.
Master lösenordet används till krypteringslogiken och för att få tillgång till lösenordshanteraren.
Master lösenordet säkerställer att dina lösenord är säkra även om password.txt blir stulen.

Vid första körning av skriptet kan master lösenordet vara vad som helst.
Följande inloggningar måste ske med samma lösenord. 

Master lösenordet sparas aldrig.

Användaren av lösenordshanteraren får ta del av ett grafiskt interface med versionsnummer, input-låda, generations-knapp och hjälp knapp.
Hjälp knappen visar en manual. 
I input-lådan bör ett integer värde matas in baserat på önskad lösenordslängd.
Efter input har fyllts klickar användaren på generations-knappen och får lösenord i den högre spalten.
Dessa lösenord syns initialt som asterisker med knappar vid sidan om för att visa/dölja, kopiera och ta bort lösenord.

Alla filer genererade av skriptet sparas i samma map som skriptet.
Lösenord (inte master) sparas krypterat i password.txt.
Masterpass salt sparas okrypterat i salt.bin.
Alla händelser och felmeddelanden sparas i en loggfil.   

Exempel-körning av skattkistan:

https://github.com/user-attachments/assets/1ddfa35f-9df5-455b-95dd-9b17c6068e3a

