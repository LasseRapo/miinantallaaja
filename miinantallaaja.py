"""
Ohjelmoinnin alkeet kurssin lopputyö: miinantallaaja eli miinaharava. Luonut Lasse "betoni" Rapo ja Aki Lotvonen.
Haravaston tarjoaa Mika Oja.
Peli tallentaa pelien tilastot "tilastot.json" nimiseen tiedostoon.
"""

import funktiot as f

def kaynnista():
    """
    Avaa pelin alkuvalikon.
    """
    print("Miinantallaaja, made by betoni and Aki.")
    print("Valitse toiminto:")
    print("(U)usi peli")
    print("(T)ilastot")
    print("(L)opeta peli")
    while True:
        toiminto = input("Tee valintasi: ").strip().lower()
        if toiminto == "u":
            f.uusi_peli()
        elif toiminto == "t":
            f.nayta_tilastot("tilastot.json")
        elif toiminto == "l":
            break
        else:
            print("Virheellinen valinta. Aloittaaksesi uuden pelin kirjoita U, "
                  "lukeaksi tilastoja kirjoita T, sulkeaksesi pelin kirjoita L")

if __name__ == "__main__":
    kaynnista()