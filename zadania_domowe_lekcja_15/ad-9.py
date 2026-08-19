# Dodanie tagów do zadań (SQLAlchemy)

import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship

engine = create_engine("sqlite:///c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania_tagi.db")

class Base(DeclarativeBase):
    pass

# Tabela pośrednia (wiele-do-wielu)
zadania_tagi = Table(
    "zadania_tagi",
    Base.metadata,
    Column("id_zadania", Integer, ForeignKey("zadania.id")),
    Column("id_taga", Integer, ForeignKey("tagi.id"))
)

class Zadanie(Base):
    __tablename__ = "zadania"
    id = Column(Integer, primary_key=True)
    tytul = Column(String, nullable=False)
    ukonczone = Column(Integer, default=0)
    priorytet = Column(Integer, default=1)
    data_utworzenia = Column(DateTime, default=datetime.datetime.utcnow)
    tagi = relationship("Tag", secondary=zadania_tagi, back_populates="zadania")

class Tag(Base):
    __tablename__ = "tagi"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String, nullable=False)
    zadania = relationship("Zadanie", secondary=zadania_tagi, back_populates="tagi")

Base.metadata.create_all(engine)

# Test
with Session(engine) as db:
    # Tworzymy tagi
    tag1 = Tag(nazwa="ważne")
    tag2 = Tag(nazwa="dom")
    tag3 = Tag(nazwa="praca")
    db.add_all([tag1, tag2, tag3])
    db.commit()

    # Tworzymy zadania z tagami
    zadanie1 = Zadanie(tytul="Napisać raport", priorytet=1, tagi=[tag3])
    zadanie2 = Zadanie(tytul="Posprzątać kuchnię", priorytet=2, tagi=[tag1, tag2])
    db.add_all([zadanie1, zadanie2])
    db.commit()

    # Wyświetlamy zadania z tagami
    zadania = db.query(Zadanie).all()
    for z in zadania:
        nazwy_tagow = ", ".join([t.nazwa for t in z.tagi])
        print(f"ID: {z.id} | {z.tytul} | tagi: {nazwy_tagow}") 