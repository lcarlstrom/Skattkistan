# <img src="https://i.imgur.com/AZSA6Jp.png" width="24" height="24" style="vertical-align: middle;" /> Skattkistan


## Syfte

Skattkistan är en single-vault lösenordshanterare skapt för att underlätta lösenordsgeneration och hantering för användare.
Programmet har en enkel grafisk interface och lösenordskryptering.

## Funktion

Skriptet skapar en grafisk interface för ett huvud-lösenord och själva lösenordshanteraren.
Huvud-lösenordet kan initialt vara vad som helst - följande inloggningar måste ske med samma lösenord om sparade lösenord finns.
Användare kan generera kryptografiskt säkra lösenord med den inbyggda generationslogiken och hantera befinitliga lösenord.
Om användaren är osäker hur skriptet ska användas finns en inbyggd manual.

Skriptet skapar fyra filer:
- password.txt
- salt.bin
- preferences.txt
- log.txt

## Systemkrav

Skriptet har aktiv support för linux och windows miljöer. Övriga miljöer är inte testade.

## Instruktioner
### Python
```bash
git clone https://github.com/lcarlstrom/Skattkistan
cd Skattkistan
pip install -r requirements.txt
chmod +x skattkistan.py
./skattkistan.py
```
### .exe
```bash
git clone https://github.com/lcarlstrom/Skattkistan
cd Skattkistan
skattkistan.exe
````

## Flaggor
- Help-knapp visar användarmanual
- Versionsnummer finns i top-vänstra hörnet

## Exempel-körning av skattkistan

https://github.com/user-attachments/assets/1ddfa35f-9df5-455b-95dd-9b17c6068e3a

## Flödesschema av skriptets logik:

![My First Board - Frame 1](https://github.com/user-attachments/assets/d8dcda11-073f-43a6-adea-2302991b31e3)


