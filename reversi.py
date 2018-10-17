import random

# oznake polja na ploci
PRAZNO, CRNO, BIJELO, RUB = '.', '*', 'o', '?'

# gore dolje lijevo desno gore-desno dolje desno dolje-lijevo gore-lijevo
SMJEROVI = (-10, 10, -1, 1, -9, 11, 9, -11) 

def polja():
    """Lista svih polja na ploci."""
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def pocetna_ploca():
    ploca = [RUB] * 100
    for i in polja():
        ploca[i] = PRAZNO
    # srednja 4 polja su ispunjena, dva bijela i dva crna
    ploca[44], ploca[45] = BIJELO, CRNO
    ploca[54], ploca[55] = CRNO, BIJELO
    return ploca

def ispis(ploca):
    print('  1 2 3 4 5 6 7 8')
    for red in range(1, 9):
        print(red, end=" ")
        for polje in range(10*red + 1, 10*red + 9):
            print(ploca[polje], end=" ")
        print()
    print()

def protivnik(igrac):
    """Vraca drugog igraca."""
    return CRNO if igrac is BIJELO else BIJELO

def pronadji_put(polje, igrac, ploca, smjer):
    """
    Pronadji put, u zadanom smjeru, do polja igraca tako da su izmedju polja protivnika.
    Vraca zavrsno polje puta. Ili None ako put ne postoji.
    """
    polje += smjer
    if ploca[polje] == igrac:
        return None
    prot = protivnik(igrac)
    while ploca[polje] == prot:
        polje += smjer
    if ploca[polje] in (RUB, PRAZNO):
        return None
    return polje

def odigraj_potez(potez, igrac, ploca):
    """Uredi plocu nakon poteza igraca."""
    for smjer in SMJEROVI:
        dodjeli_polja(potez, igrac, ploca, smjer)

def dodjeli_polja(polje, igrac, ploca, smjer):
    """Dodjeli igracu polja od pocetnog do krajnjeg u danom smjeru."""
    kraj = pronadji_put(polje, igrac, ploca, smjer)
    if not kraj:
        return
    while polje != kraj:
        ploca[polje] = igrac
        polje += smjer

def dozovoljen(potez, igrac, ploca):
    """Je li potez igracu dozvoljen?"""
    if potez not in polja():  # ako je na ploci
        return False
    if ploca[potez] != PRAZNO: # ako je to polje prazno
        return False
    for d in SMJEROVI:        # i ako postoji put
        if pronadji_put(potez, igrac, ploca, d):
            return True
    return False

def dozvoljeni_potezi(igrac, ploca):
    """Lista dozvoljenih poteza igraca."""
    return [sq for sq in polja() if dozovoljen(sq, igrac, ploca)]

def ima_potez(igrac, ploca):
    """Ima li igrac iti jedan dozvoljeni potez?"""
    return len(dozvoljeni_potezi(igrac, ploca)) > 0

def igraj(black_strategy, white_strategy):
    """Odigraj igru."""
    ploca = pocetna_ploca()
    igrac = CRNO
    while igrac is not None:
        if igrac == CRNO:
            potez = black_strategy(igrac, ploca)
        else:
            potez = white_strategy(igrac, ploca)
        odigraj_potez(potez, igrac, ploca)
        igrac = slijedeci(ploca, igrac)
        #ispis(ploca)
    return ploca

def slijedeci(ploca, igrac):
    """Vraca igraca koji treba odigrati slijedeci potez."""
    drugi = protivnik(igrac)
    if ima_potez(drugi, ploca):
        return drugi
    elif ima_potez(igrac, ploca):
        return igrac
    return None

def rezultat(ploca):
    """Vraca rezultat, koliko ima bijeli koliko crnih polja."""
    bijeli, crni = 0, 0
    for polje in polja():
        igrac = ploca[polje]
        if igrac == BIJELO: bijeli += 1
        elif igrac == CRNO: crni += 1
    return bijeli, crni

def racunalo(igrac, ploca):
    """Jednostavna straegija koja random slijedeci potez."""
    return random.choice(dozvoljeni_potezi(igrac, ploca))

def covjek(igrac, ploca):
    ispis(ploca)
    while True:
        potez = input('> ')
        if potez and dozovoljen(int(potez), igrac, ploca):
            return int(potez)
        elif potez:
            print('Neispravan potez, pokusaj ponovo.')

# pokreni igru 
ploca = igraj(racunalo, covjek)
# prikazi rezultat
bijeli, crni = rezultat(ploca)
print('Bijeli:', bijeli, 'Crni:', crni)
if bijeli > crni:
    print('Bijeli pobjednik!')
elif crni > bijeli:
    print('Crni pobjednik!')
else:
    print('Nerješeno!')
ispis(ploca)


