import time

csc = True
kolone, vrste, vrednosti, matrica = [], [], [], []

def baciKockicu(klica):
    vrednostKockice = 0
    for i in range(9):
        klica = klica**2 % 253
        vrednostKockice = vrednostKockice*2 + klica%2
    vrednostKockice = int(vrednostKockice % 6 + 1)
    return klica, vrednostKockice

def baciKockice(klica, kockice, kockiceZaBacanje):
    for kockica in kockiceZaBacanje:
        klica, kockice[kockica-1] = baciKockicu(klica)
    return klica

def napraviRetkuMatricu():
    'Vraca praznu retku matricu, csc = True'
    global csc, matrica, kolone, vrste, vrednosti
    csc = True
    kolone = [0, 0, 0, 0]
    vrste = []
    vrednosti = []
    matrica = [kolone, vrste, vrednosti]

def napraviObicnuMatricu():
    'Pretvara matricu iz retke u obicnu, csc = False'
    global csc, matrica, kolone, vrste, vrednosti
    csc = False
    pomocna = []
    for i in range(10):
        pomocna.append([0, 0, 0])
    for kolona in range(3):
        pocetak, kraj = kolona, kolona+1
        for vrsta in range(pocetak, kraj):
            pomocna[vrsta][kolona] = vrednosti[vrsta]
    matrica = pomocna

def upisiURetku(vrsta, kolona, vrednost):
    'Upisuje element u retku matricu, csc = True'
    global kolone, vrste, vrednosti
    pocetak, kraj = kolone[kolona], kolone[kolona+1]
    for i in range(pocetak, kraj):
        if vrsta > vrste[i]:
            vrste.insert(i, vrsta)
            vrednosti.insert(i, vrednost)
            break
    else:
        vrste.insert(pocetak, vrsta)
        vrednosti.insert(pocetak, vrednost)
    for i in range(kolona+1, 4):
        kolone[i] += 1

def upisiUObicnu(vrsta, kolona, vrednost):
    'Upisuje u obicnu matricu, csc = False'
    global matrica
    matrica[vrsta][kolona] = vrednost

def upisiUMatricu(vrsta, kolona, vrednost):
    'Upisuje u matricu, nezavisno da li je retka ili obicna pozivanjem funkcija UpisiUObicnu() i UpisiURetku()'
    global csc, vrednosti
    if csc == True:
        upisiURetku(vrsta, kolona, vrednost)
        if len(vrednosti) == 14:
            napraviObicnuMatricu()
    else:
        upisiUObicnu(vrsta, kolona, vrednost)

def vrednostIzRetke(vrsta, kolona):
    'Pretrazuje retku matricu, ukoliko element postoji, vraca njegovu vrednost, u suprotnom vraca 0'
    global kolone, vrste, vrednosti
    pocetak, kraj = kolone[kolona], kolone[kolona+1]
    for i in range(pocetak, kraj):
        if vrste[i] == vrsta:
            return vrednosti[i]
    return 0

def vrednostIzMatrice(vrsta, kolona):
    'Pretrazuje matricu, nezavisno jel retka ili ne, i vraca vrednost trazenog elementa'
    global csc, matrica
    if csc == True:
        return vrednostIzRetke(vrsta, kolona)
    else:
        return matrica[vrsta][kolona]

def izbrojSveKockice(kockice):
    'Vraca listu sa brojem pojavljivanja svih strana kocke'
    izbrojeno = []
    for i in range(1, 7):
        izbrojeno.append(kockice.count(i))
    return izbrojeno

def izbroj(kockice, broj):
    'Vraca broj pojavljivanja trazene strane kocke'
    return kockice.count(broj)

def kenta(kockice, bacanje):
    'Proverava jel kenta, ako jeste vraca vrednost, ako nije vraca 0'
    izbrojeno = izbrojSveKockice(kockice)
    brojac = 0
    for i in range(6):
        if izbrojeno[i] == 1:
            brojac += 1
            if brojac == 5:
                return 76-10*bacanje
        else:
            brojac = 0
    return 0

def ful(kockice):
    'Proverava jel ful, ako jeste vraca vrednost, ako nije vraca 0'
    izbrojeno = izbrojSveKockice(kockice)
    if 3 in izbrojeno and 2 in izbrojeno:
        return 30 + sum(kockice)
    return 0

def poker(kockice):
    'Proverava jel poker, ako jeste vraca vrednost, ako nije vraca 0'
    izbrojeno = izbrojSveKockice(kockice)
    if 4 in izbrojeno:
        return 40 + 4*(izbrojeno.index(4)+1)
    elif 5 in izbrojeno:
        return 40 + 4 * (izbrojeno.index(5) + 1)
    return 0

def jamb(kockice):
    'Proverava jel jamb, ako jeste vraca vrednost, ako nije vraca 0'
    izbrojeno = izbrojSveKockice(kockice)
    if 5 in izbrojeno:
        return 50 + sum(kockice)
    return 0

def vrednostPriUnosu(kockice, bacanje, vrsta, kolona):
    'Vraca vrednost ako polje moze biti popunjeno, vraca 0 ako moze biti samo precrtano'
    if bacanje != 1 and kolona == 2:
        return 0
    if vrsta in range(0, 6):
        return (vrsta+1) * izbroj(kockice, vrsta+1)
    elif vrsta == 6:
        return kenta(kockice, bacanje)
    elif vrsta == 7:
        return ful(kockice)
    elif vrsta == 8:
        return poker(kockice)
    else:
        return jamb(kockice)

def nadjiPraznaPolja():
    'Parseuje matricu i vraca listu praznih polja'
    praznaPolja = []
    for i in range(10):
        if vrednostIzMatrice(i, 0) == 0:
            praznaPolja.append((i, 0))
            break
    for i in range(9, -1, -1):
        if vrednostIzMatrice(i, 1) == 0:
            praznaPolja.append((i, 1))
            break
    for i in range(10):
        if vrednostIzMatrice(i, 2) == 0:
            praznaPolja.append((i, 2))
    return praznaPolja

def transformisiNaziv(koordinate):
    naziviKolona = ['Na dole', 'Na gore', ['Rucne', 'Rucna', 'Rucni']]
    naziviVrsta = ['Jedinice', 'Dvojke', 'Trojke', 'Cetvorke', 'Petice', 'Sestice', 'Kenta', 'Ful', 'Poker', 'Jamb']

    vrsta = koordinate[0]
    kolona = koordinate[1]

    if kolona == 2:
        if vrsta in range(0, 6):
            return (naziviVrsta[vrsta], naziviKolona[kolona][0])
        elif vrsta == 6:
            return (naziviVrsta[vrsta], naziviKolona[kolona][1])
        else:
            return (naziviVrsta[vrsta], naziviKolona[kolona][2])
    else:
        return (naziviVrsta[vrsta], naziviKolona[kolona])

def prikaziKockice(kockice):
    nazivKocke = ['Prva', 'Druga', 'Treca', 'Cetvrta', 'Peta']
    print('\nVase kocke:')
    for i in range(5):
        print('{:<7} - {}'.format(nazivKocke[i], kockice[i]))

def odabirOpcije(brojOpcija, brojIzbora = 1):
    if brojIzbora == 1:
        while True:
            try:
                izbor = int(input())
                if izbor not in range(1, brojOpcija+1):
                    raise ValueError
                return izbor
            except ValueError:
                print('Opcija koju ste odabrali ne postoji!')
    else:
        while True:
            try:
                izbori = [int(value) for value in input().split()]
                if len(izbori) > brojIzbora:
                    raise ValueError
                for izbor in izbori:
                    if izbor not in range(1, brojOpcija+1):
                        raise ValueError
                return izbori
            except ValueError:
                print('Opcije koje ste odabrali ne postoje!')

def sumaPrvih6():
    sveKolone = []
    for i in range(3):
        jednaKolona = 0
        for j in range(6):
            vrednost = vrednostIzMatrice(j, i)
            if vrednost == -1:
                vrednost = 0
            jednaKolona += vrednost
        sveKolone.append(jednaKolona)
    return sveKolone

def SumaSvih():
    sveKolone = []
    for i in range(3):
        jednaKolona = 0
        for j in range(10):
            vrednost = vrednostIzMatrice(j, i)
            if vrednost == -1:
                vrednost = 0
            jednaKolona += vrednost
        sveKolone.append(jednaKolona)
    return sveKolone

'Ako ne treba da se dodaje 30 ako je zbir prvih 6 veci od ja mislim 36 onda ove dve funkcije mogu da se spoje u jednu, u suprotnom pozivati prvu funkciju za prvih 6 iz druge, i dodati poslednja 4'

def VrednostIzMatrice(vrsta, kolona):
    vrednost = vrednostIzMatrice(vrsta, kolona)
    if vrednost == -1:
        return '/'
    elif vrednost == 0:
        return ' '
    return vrednost

def opcija2():
    naziviKolona = ['Jamb', 'Na dole', 'Na gore', 'Rucna']
    naziviVrsta = ['Jedinice', 'Dvojke', 'Trojke', 'Cetvorke', 'Petice', 'Sestice', 'Kenta', 'Ful', 'Poker', 'Jamb']
    zbir6 = sumaPrvih6()
    zbirSvih = SumaSvih()
    for i in range(10):
        if i == 0:
            print('.............................................')
            print(':{:10}:{:10}:{:10}:{:10}:'.format(naziviKolona[0], naziviKolona[1], naziviKolona[2], naziviKolona[3]))
            print(':..........:..........:..........:..........:')
        print(':{:10}:{:^10}:{:^10}:{:^10}:'.format(naziviVrsta[i], VrednostIzMatrice(i, 0), VrednostIzMatrice(i, 1), VrednostIzMatrice(i, 2)))
        if i == 5:
            print(':..........:..........:..........:..........:')
            print(':{:10}:{:^10}:{:^10}:{:^10}:'.format('Suma', zbir6[0], zbir6[1], zbir6[2]))
            print(':..........:..........:..........:..........:')
        elif i == 9:
            print(':..........:..........:..........:..........:')
            print(':{:10}:{:^10}:{:^10}:{:^10}:'.format('Suma', zbirSvih[0], zbirSvih[1], zbirSvih[2]))
            print(':..........:..........:..........:..........:')

def opcija3(klica):
    kockice = [0, 0, 0, 0, 0]
    izbor = [1, 2, 3, 4, 5]
    brojBacanja = 0
    for bacanje in range(1, 4):
        brojBacanja = bacanje
        klica = baciKockice(klica, kockice, izbor)
        prikaziKockice(kockice)
        if bacanje != 3:
            print('Opcija 1: Bacite kockice ponovo\nOpcija 2: Nastavi igru dalje')
            izbor = odabirOpcije(2)
            if izbor == 2:
                break
            else:
                print('Odaberite koje kockice zelite da bacite ponovo:')
                izbor = odabirOpcije(5, 5)
    praznaPolja = nadjiPraznaPolja()
    zaPopunjavanje = []
    zaPrecrtavanje = []
    for praznoPolje in praznaPolja:
        if vrednostPriUnosu(kockice, brojBacanja, praznoPolje[0], praznoPolje[1]) == 0:
            zaPrecrtavanje.append(praznoPolje)
        else:
            zaPopunjavanje.append(praznoPolje)
    i = 1
    if len(zaPopunjavanje) != 0:
        print('Polja koja mozete popuniti:')
    for praznoPolje in zaPopunjavanje:
        nazivPolja = transformisiNaziv(praznoPolje)
        print('{:^2} - {:>8} {:<8}'.format(i, nazivPolja[1], nazivPolja[0]))
        i += 1
    if len(zaPrecrtavanje) != 0:
        print('\nPolja koja mozete precrtati:')
    for praznoPolje in zaPrecrtavanje:
        nazivPolja = transformisiNaziv(praznoPolje)
        print('{:^2} - {:>8} {:<8}'.format(i, nazivPolja[1], nazivPolja[0]))
        i += 1
    praznaPolja = zaPopunjavanje + zaPrecrtavanje
    izbor = odabirOpcije(len(praznaPolja))
    poljeZaUpis = praznaPolja[izbor-1]
    vrednost = vrednostPriUnosu(kockice, brojBacanja, poljeZaUpis[0], poljeZaUpis[1])
    if vrednost == 0:
        vrednost = -1
    upisiUMatricu(poljeZaUpis[0], poljeZaUpis[1], vrednost)
    return klica

matrica = napraviRetkuMatricu()
klica = time.time()
while True:
    print('Opcije:\nOpcija 1: Napravi prazan talon\nOpcija 2: Prikazi talon\nOpcija 3: Baci kockice\nOpcija 4: Prekini igru')
    izbor = odabirOpcije(4)
    if izbor == 1:
        napraviRetkuMatricu()
        print('Napravljen prazan talon!\n')
    elif izbor == 2:
        opcija2()
    elif izbor == 3:
        klica = opcija3(klica)
    else:
        exit(0)