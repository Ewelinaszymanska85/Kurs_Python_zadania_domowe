class KalkulatorWalut:
    @staticmethod
    def usd_na_pln(kwota_usd):
        KURS = 4.0
        return kwota_usd * KURS


wynik = KalkulatorWalut.usd_na_pln(100)

print(wynik) 