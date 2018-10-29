import random
import tkinter as tk
from tkinter import ttk

# oznake polja na ploci
PRAZNO, CRNO, BIJELO, RUB, DOZVOLJEN = ' ', '*', 'o', '?', '.'

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
    print()
    print('  1 2 3 4 5 6 7 8')
    for red in range(1, 9):
        print(red, end=" ")
        for polje in range(10*red + 1, 10*red + 9):
            print(ploca[polje], end=" ")
        print()
    print()

def protivnik(igrac):
    """Vraca drugog igraca."""
    if igrac == BIJELO:
        return CRNO
    else:
        return BIJELO

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

def odigraj_potez(potez, igrac, ploca, buttons):
    """Uredi plocu nakon poteza igraca."""
    for smjer in SMJEROVI:
        dodjeli_polja(potez, igrac, ploca, buttons, smjer)

def dodjeli_polja(polje, igrac, ploca, buttons, smjer):
    """Dodjeli igracu polja od pocetnog do krajnjeg u danom smjeru."""
    kraj = pronadji_put(polje, igrac, ploca, smjer)
    if not kraj:
        return
    while polje != kraj:
        ploca[polje] = igrac
        buttons[polje].set(igrac)
        polje += smjer

def dozvoljen(potez, igrac, ploca):
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
    return [polje for polje in polja() if dozvoljen(polje, igrac, ploca)]

def ima_potez(igrac, ploca):
    """Ima li igrac iti jedan dozvoljeni potez?"""
    return len(dozvoljeni_potezi(igrac, ploca)) > 0

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
        if igrac == BIJELO:
            bijeli += 1
        elif igrac == CRNO:
            crni += 1
    return bijeli, crni

def racunalo(igrac, ploca):
    """Jednostavna strategija koja random slijedeci potez."""
    return random.choice(dozvoljeni_potezi(igrac, ploca))

# prikazi rezultat
def ispis_rezultat(ploca):
    bijeli, crni = rezultat(ploca)
    print()
    print('Bijeli:', bijeli, 'Crni:', crni)
    if bijeli > crni:
        print('Bijeli pobjednik!')
    elif crni > bijeli:
        print('Crni pobjednik!')
    else:
        print('Neriješeno!')
    ispis(ploca)


covjek_igrac = CRNO
racunalo_igrac = BIJELO

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

def covjek_odigrao(potez, igrac, ploca, buttons):
    odigraj_potez(potez, igrac, ploca, buttons)
    igrac = slijedeci(ploca, igrac)
    while igrac == racunalo_igrac:
        potez = racunalo(igrac, ploca)
        odigraj_potez(potez, igrac, ploca, buttons)
        igrac = slijedeci(ploca, igrac)
    if igrac == None:
        ispis_rezultat(ploca)

def on_click(potez, ploca, buttons):
    if potez and dozvoljen(potez, covjek_igrac, ploca):
        covjek_odigrao(potez, covjek_igrac, ploca, buttons)
        oznaci_dozvoljen(covjek_igrac, ploca, buttons)
    elif ima_potez(covjek_igrac, ploca):
        print('Neispravan potez, pokusaj ponovo.')

def oznaci_dozvoljen(igrac, ploca, buttons):
    for polje in polja():
        if ploca[polje] == PRAZNO:
            buttons[polje].set(PRAZNO)
    for polje in dozvoljeni_potezi(igrac, ploca):
        buttons[polje].set(DOZVOLJEN)

def init_frame(ploca):
    buttons = [RUB] * 100
    for red in range(1, 9):
        c = 0
        for polje in range(10*red + 1, 10*red + 9):
            btn_text = tk.StringVar()
            button = ttk.Button(frame, textvariable=btn_text, width=1, command= lambda p=polje: on_click(p, ploca, buttons))
            btn_text.set(ploca[polje])
            button.grid(row=red, column=c)
            buttons[polje]=btn_text
            c += 1
    oznaci_dozvoljen(covjek_igrac, ploca, buttons)

ploca = pocetna_ploca()
init_frame(ploca)

print('bijeli: ', BIJELO, ' crni: ', CRNO, 'dozvoljena polja: ', DOZVOLJEN)
print('ti si: ', covjek_igrac)
print()

root.mainloop()
