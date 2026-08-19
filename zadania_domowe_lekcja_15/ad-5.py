# Dodanie daty utworzenia (SQLAlchemy)

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

Base.metadata.create_all(engine)

# Test
with Session(engine) as db:
    zadanie = Zadanie(tytul="Testowe zadanie", priorytet=2)
    db.add(zadanie)
    db.commit()

with Session(engine) as db:
    zadania = db.query(Zadanie).all()
    for z in zadania:
        print(f"ID: {z.id} | {z.tytul} | priorytet: {z.priorytet} | data: {z.data_utworzenia}")