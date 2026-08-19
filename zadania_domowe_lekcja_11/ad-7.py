class Telewizor:
    def __init__(self):
        self.__kanal = 1
        self.__glosnosc = 10
        self.__wlaczony = False

    def wlacz(self):
        self.__wlaczony = True
        print("Telewizor włączony.")

    def wylacz(self):
        self.__wlaczony = False
        print("Telewizor wyłączony.")

    def zmien_kanal(self, numer):
        if self.__wlaczony:
            self.__kanal = numer
            print(f"Zmieniono kanał na {self.__kanal}.")
        else:
            print("Nie można zmienić kanału – telewizor jest wyłączony.")

    def glosniej(self):
        if self.__wlaczony:
            if self.__glosnosc < 100:
                self.__glosnosc += 1
            else:
                print("Maksymalna głośność to 100.")
        else:
            print("Nie można zmienić głośności – telewizor jest wyłączony.")

    def ciszej(self):
        if self.__wlaczony:
            if self.__glosnosc > 0:
                self.__glosnosc -= 1
            else:
                print("Minimalna głośność to 0.")
        else:
            print("Nie można zmienić głośności – telewizor jest wyłączony.")

    def info(self):
        stan = "włączony" if self.__wlaczony else "wyłączony"
        print(f"Stan: {stan}, kanał: {self.__kanal}, głośność: {self.__glosnosc}")


# Testowanie
tv = Telewizor()
tv.info()

tv.zmien_kanal(5)   # nie zadziała – TV wyłączony
tv.wlacz()
tv.zmien_kanal(5)   # zadziała
tv.glosniej()
tv.info()

tv.wylacz()
tv.ciszej()         # nie zadziała – TV wyłączony 