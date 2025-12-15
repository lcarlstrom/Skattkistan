# Det här skriptet genererar ett lösenord med en användardefinierad längd.


import string # För att enkelt kunna definiera ett objekt som innehåller A-Z + 0-9 + all punctuation.
import secrets # Bättre variant av "random" som generar mer kryptografiskt säkra lösenord

def passgen():
    length = int(input("Input your length as an integer: ")) # Sätt längden av lösenordet
    chars = string.ascii_letters + string.digits + string.punctuation # Alla karaktärer som vanligtvis är tillåtna i lösenord
    password = "".join(secrets.choice(chars) for i in range(length)) # Ta ett slumpat urval från "chars" "length" antal gånger
    return password


if __name__ == "__main__":
    result = passgen()
    print(result)