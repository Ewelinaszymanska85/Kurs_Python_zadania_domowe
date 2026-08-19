# Wyszukiwanie po opisie (SQLAlchemy)

import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine("sqlite:///c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania_orm2.db")

class Base(DeclarativeBase):
    pass

class Zadanie(Base):
    __tablename__ = "zadania"
    id = Column(Integer, primary_key=True)
    tytul = Column(String, nullable=False)
    ukonczone = Column(Integer, default=0)
    priorytet = Column(Integer, default=1)
    data_utworzenia = Column(DateTime, default=datetime.datetime.utcnow)

def wyszukaj_zadania(fraza):
    with Session(engine) as db:
        return db.query(Zadanie).filter(Zadanie.tytul.contains(fraza)).all()


# Test
fraza = input("Podaj frazę do wyszukania: ")
wyniki = wyszukaj_zadania(fraza)

if wyniki:
    for z in wyniki:
        print(f"ID: {z.id} | {z.tytul} | priorytet: {z.priorytet}")
else:
    print("Nie znaleziono zadań.") 