class MetaWalidujMetody(type):
    def __new__(mcs, name, bases, namespace):
        for nazwa, obiekt in namespace.items():
            if callable(obiekt) and not nazwa.startswith("__"):
                if obiekt.__doc__ is None:
                    raise TypeError(
                        f"Metoda '{nazwa}' wymaga docstringa."
                    )
        return super().__new__(mcs, name, bases, namespace)


# --- PRZYKŁAD POPRAWNY ---
class Poprawna(metaclass=MetaWalidujMetody):
    def metoda_ok(self):
        """To jest poprawny docstring."""
        return "OK"

    def inna_metoda(self):
        """Też ma dokumentację."""
        return "OK"


# --- PRZYKŁAD NIEPOPRAWNY ---
try:
    class Niepoprawna(metaclass=MetaWalidujMetody):
        def brak_docstringa(self):
            return "Błąd"
except TypeError as e:
    print(f"BŁĄD METAKLASY: {e}") 