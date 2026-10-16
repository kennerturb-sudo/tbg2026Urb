ruumi_tyyp = input("Mis tüüpi ruumiga on tegemist (toitlustus, kaubandus, teenindus, sport, üritus)? ").lower()
ruumi_suurus = float(input("Kui suur ruum on (m2)? "))
teenindajad = int(input("Mitu teenindajat ruumis on? "))

if ruumi_tyyp == "toitlustus" or ruumi_tyyp == "kaubandus":
    protsent = 0.50
elif ruumi_tyyp == "teenindus":
    protsent = 0.25
elif ruumi_tyyp == "sport":
    protsent = 0.25
elif ruumi_tyyp == "üritus":
    protsent = 0.50
else:
    print("Sellist ruumi tüüpi ei ole!")
    exit()

# Arvutame ruumi lubatud inimeste arvu
inimeste_arv = ruumi_suurus * protsent / 4

# Lahutame teenindajad
inimeste_arv = inimeste_arv - teenindajad

# Inimeste arv ei saa olla negatiivne
if inimeste_arv < 0:
    inimeste_arv = 0

# Spordiruumis võib olla maksimaalselt 100 inimest
if ruumi_tyyp == "sport":
    inimeste_arv = min(inimeste_arv, 100 - teenindajad)
    if inimeste_arv < 0:
        inimeste_arv = 0

# Üritusel võib olla maksimaalselt 200 inimest
elif ruumi_tyyp == "üritus":
    inimeste_arv = min(inimeste_arv, 200 - teenindajad)
    if inimeste_arv < 0:
        inimeste_arv = 0

print(f"{ruumi_suurus} m2 ruumi on lubatud maksimaalselt "
      f"{inimeste_arv} inimest juhul kui ruumis on "
      f"{teenindajad} teenindajat.")