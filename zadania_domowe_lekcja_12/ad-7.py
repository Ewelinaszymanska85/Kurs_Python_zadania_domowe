class Data:
    def __init__(self, dzien, miesiac, rok):
        self.dzien = dzien
        self.miesiac = miesiac
        self.rok = rok

    @classmethod
    def ze_stringa(cls, data_str):
        dzien, miesiac, rok = data_str.split("-")
        return cls(int(dzien), int(miesiac), int(rok))

    def __str__(self):
        return f"{self.dzien:02d}-{self.miesiac:02d}-{self.rok}"


# Testowanie
data1 = Data(1, 1, 2020)
data2 = Data.ze_stringa("25-12-2023")

print(data1)
print(data2) 