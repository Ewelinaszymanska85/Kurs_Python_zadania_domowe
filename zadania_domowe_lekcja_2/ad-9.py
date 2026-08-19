import this

tekst = "".join([this.d.get(c, c) for c in this.s])
linie = tekst.split("\n")

print(linie[0])
print(linie[1]) 