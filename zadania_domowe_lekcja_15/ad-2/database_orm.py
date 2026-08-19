from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine("sqlite:///c:/Projects python/Kurs Python/python_lesson/zadania domowe/lesson15/zadania_orm.db")


class Base(DeclarativeBase):
    pass


class Zadanie(Base):
    __tablename__ = "zadania"
    id = Column(Integer, primary_key=True)
    tytul = Column(String, nullable=False)
    ukonczone = Column(Integer, default=0)


Base.metadata.create_all(engine)


def dodaj_zadanie(tytul):
    with Session(engine) as db:
        zadanie = Zadanie(tytul=tytul)
        db.add(zadanie)
        db.commit()


def pokaz_zadania():
    with Session(engine) as db:
        return db.query(Zadanie).all()


def usun_zadanie(id_zadania):
    with Session(engine) as db:
        zadanie = db.query(Zadanie).filter(Zadanie.id == id_zadania).first()
        if zadanie:
            db.delete(zadanie)
            db.commit()


def wyszukaj_zadania(fraza):
    """Wyszukuje zadania, ktorych tytul zawiera podana fraze."""
    with Session(engine) as db:
        return db.query(Zadanie).filter(Zadanie.tytul.contains(fraza)).all()
