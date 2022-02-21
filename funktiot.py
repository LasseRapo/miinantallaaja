import haravasto as h
import random as r
import time
import json
import datetime

tila = {
    "kentta": [],
    "pinta": []
}

tilastot = []
vuorot = 0

def nayta_tilastot(tiedosto):
    """
    Tulostaa pelin tilastot.
    """
    try:
        with open(tiedosto) as lahde:
            pelien_tilastot = json.load(lahde)
            for peli in pelien_tilastot:
                print(peli[0])
    except (IOError, json.JSONDecodeError):
        print("Ei tilastoja")

def tallenna_tilastot(tilastot, tiedosto):
    """
    Tallentaa pelin tilastot erilliseen tiedostoon.
    """
    with open(tiedosto, "w") as kohde:
        json.dump(tilastot, kohde, indent=2)

def uusi_peli():
    """
    Pyytää käyttäjältä kentän koon ja aloittaa uuden pelin. Pelin päätyttyä tallentaa tulokset.
    """
    tila["kentta"].clear()
    tila["pinta"].clear()
    global vuorot
    vuorot = 0

    h.lataa_kuvat("spritet")
    kentan_korkeus = kysy_korkeus()
    kentan_leveys = kysy_leveys()
    miinojen_lkm = kysy_miinat(kentan_korkeus, kentan_leveys)
    luo_kentta(kentan_korkeus, kentan_leveys, miinojen_lkm)
    h.luo_ikkuna(40 * kentan_leveys, 40 * kentan_korkeus)
    h.aseta_piirto_kasittelija(piirra_kentta)
    h.aseta_hiiri_kasittelija(kasittele_hiiri)
    aloitus_aika = time.time()
    h.aloita()

    kulunut_aika = time.time() - aloitus_aika
    minuuttia, sekuntia = divmod(round(kulunut_aika), 60)
    paivamaara = datetime.datetime.now()
    if voitto:
        tilastot.append(["{} voitto, {} x {}, {} miinaa, {:02d}:{:02d} min, {} vuoroa"
                        .format(paivamaara.strftime("%d-%m-%Y %H:%M:"), kentan_leveys, kentan_korkeus, miinojen_lkm,
                                minuuttia, sekuntia, vuorot)])
    else:
        tilastot.append(["{} häviö, {} x {}, {} miinaa, {:02d}:{:02d} min, {} vuoroa"
                        .format(paivamaara.strftime("%d-%m-%Y %H:%M:"), kentan_leveys, kentan_korkeus, miinojen_lkm,
                                minuuttia, sekuntia, vuorot)])
    tallenna_tilastot(tilastot, "tilastot.json")

def kysy_korkeus():
    while True:
        try:
            korkeus = int(input("Anna kentän korkeus ruutuina: "))
        except ValueError:
            print("Anna korkeus kokonaislukuna")
        else:
            return korkeus

def kysy_leveys():
    while True:
        try:
            leveys = int(input("Anna kentän leveys ruutuina: "))
        except ValueError:
            print("Anna leveys kokonaislukuna")
        else:
            return leveys

def kysy_miinat(korkeus, leveys):
    while True:
        try:
            miinat = int(input("Anna miinojen lukumäärä: "))
        except ValueError:
            print("Anna miinojen määrä kokonaislukuna")
        else:
            if miinat >= korkeus * leveys:
                print("Liikaa miinoja")
            elif miinat <= 0:
                print("Miinoja täytyy olla vähintään 1")
            else:
                return miinat

def kasittele_hiiri(x, y, hiiri, m_nappain):
    """
    Tarkastaa mitä hiiren nappia painettiin ja missä kohdassa.
    """
    x_k = x // 40
    y_k = y // 40
    if hiiri == h.HIIRI_VASEN:
        global vuorot
        vuorot += 1
        if tila["pinta"][y_k][x_k] == " ":
            if tila["kentta"][y_k][x_k] == "x":
                tila["pinta"][y_k][x_k] = tila["kentta"][y_k][x_k]
                piirra_kentta
                unlucky()
            elif tila["kentta"][y_k][x_k] == 0:
                tulva(x_k, y_k)
                piirra_kentta
                chicken_dinner()
            else:
                tila["pinta"][y_k][x_k] = tila["kentta"][y_k][x_k]
                piirra_kentta
                chicken_dinner()
        else:
            pass
    elif hiiri == h.HIIRI_OIKEA:
        if tila["pinta"][y_k][x_k] == " ":
            tila["pinta"][y_k][x_k] = "f"
            piirra_kentta
        elif tila["pinta"][y_k][x_k] == "f":
            tila["pinta"][y_k][x_k] = " "
            piirra_kentta
    elif hiiri == h.HIIRI_KESKI:
        pass

def unlucky():
    """
    Osuit miinaan ja hävisit pelin.
    """
    h.lopeta()
    global voitto
    voitto = False
    print("Hups osuit miinaan, hävisit pelin!")

def chicken_dinner():
    """
    Tarkistaa onko pelaaja ansainnut herkullisen kana-aterian.
    """
    korkeus = len(tila["pinta"])
    leveys = len(tila["pinta"][0])
    tunnetut = 0
    for i in tila["pinta"]:
        for j in i:
            if j == "f" or j == " ":
                pass
            else:
                tunnetut += 1
    
    miinat = 0
    for i in tila["kentta"]:
        for j in i:
            if j == "x":
                miinat += 1
            else:
                pass
    tyhjat_ruudut = korkeus * leveys - miinat
    
    if tunnetut == tyhjat_ruudut:
        h.lopeta()
        global voitto
        voitto = True
        print("Winner winner chicken dinner!")
    else:
        pass
    

def tulva(x, y):
    """
    Algoritmi, joka tutkii toisiinsa yhteydessä olevat tuntemattomat ruudut kartalta.
    """
    k_parit = [
    (x, y)
    ]
    n_parit = []
    
    while k_parit:
        xy = k_parit.pop()
        tila["pinta"][xy[1]][xy[0]] = 0
        tila["kentta"][xy[1]][xy[0]] = " "
        if xy[0] > 0 and xy[1] > 0:
            for rivi, i in enumerate(tila["kentta"][xy[1]-1:xy[1]+2]):
                for sarake, j in enumerate(i[xy[0]-1:xy[0]+2]):
                    if j == 0:
                        k_parit.append((xy[0]+sarake-1, xy[1]+rivi-1))
                    elif j == "x" or j == " ":
                        pass
                    else:
                        n_parit.append((xy[0]+sarake-1, xy[1]+rivi-1))
        
        elif xy[0] > 0 and xy[1] == 0:
            for rivi, i in enumerate(tila["kentta"][:2]):
                for sarake, j in enumerate(i[xy[0]-1:xy[0]+2]):
                    if j == 0:
                        k_parit.append((xy[0]+sarake-1, xy[1]+rivi))
                    elif j == "x" or j == " ":
                        pass
                    else:
                        n_parit.append((xy[0]+sarake-1, xy[1]+rivi))
        
        elif xy[0] == 0 and xy[1] > 0:
            for rivi, i in enumerate(tila["kentta"][xy[1]-1:xy[1]+2]):
                for sarake, j in enumerate(i[:2]):
                    if j == 0:
                        k_parit.append((xy[0]+sarake, xy[1]+rivi-1))
                    elif j == "x" or j == " ":
                        pass
                    else:
                        n_parit.append((xy[0]+sarake, xy[1]+rivi-1))
        
        elif xy[0] == 0 and xy[1] == 0:
            for rivi, i in enumerate(tila["kentta"][:2]):
                for sarake, j in enumerate(i[:2]):
                    if j == 0:
                        k_parit.append((xy[0]+sarake, xy[1]+rivi))
                    elif j == "x" or j == " ":
                        pass
                    else:
                        n_parit.append((xy[0]+sarake, xy[1]+rivi))
    
    while n_parit:
        n_xy = n_parit.pop()
        tila["pinta"][n_xy[1]][n_xy[0]] = tila["kentta"][n_xy[1]][n_xy[0]]

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    h.tyhjaa_ikkuna()
    h.piirra_tausta()
    h.aloita_ruutujen_piirto()
    for y, i in enumerate(tila["pinta"]):
        for x, j in enumerate(i):
            h.lisaa_piirrettava_ruutu(str(j), x * 40, y * 40)
    h.piirra_ruudut()

def miinoita(kentta, vapaat_ruudut, miinojen_lkm):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinojen_lkm):
        m = r.choice(vapaat_ruudut)
        kentta[m[1]][m[0]] = "x"
        vapaat_ruudut.remove(m)
    while vapaat_ruudut:
        lahimiinat = 0
        ruutu = vapaat_ruudut.pop()
        x, y = ruutu
        
        if x > 0 and y > 0:
            for i in kentta[y-1:y+2]:
                for j in i[x-1:x+2]:
                    if j == "x":
                        lahimiinat += 1
            kentta[y][x] = lahimiinat
        
        elif x > 0 and y == 0:
            for i in kentta[:2]:
                for j in i[x-1:x+2]:
                    if j == "x":
                        lahimiinat += 1
            kentta[y][x] = lahimiinat
        
        elif x == 0 and y > 0:
            for i in kentta[y-1:y+2]:
                for j in i[:2]:
                    if j == "x":
                        lahimiinat += 1
            kentta[y][x] = lahimiinat
        
        elif x == 0 and y == 0:
            for i in kentta[:2]:
                for j in i[:2]:
                    if j == "x":
                        lahimiinat += 1
            kentta[y][x] = lahimiinat
    
def luo_kentta(korkeus, leveys, miinojen_lkm):
    """
    Valmistelee kentän.
    """
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
    
    tila["kentta"] = kentta
    
    for rivi in range(korkeus):
        tila["pinta"].append([])
        for sarake in range(leveys):
            tila["pinta"][-1].append(" ")
    
    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))

    miinoita(kentta, jaljella, miinojen_lkm)