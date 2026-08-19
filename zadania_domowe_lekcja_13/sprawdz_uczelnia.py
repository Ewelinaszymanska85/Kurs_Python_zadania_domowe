import sqlite3

conn = sqlite3.connect("uczelnia.db")
kursor = conn.cursor()

print("Tabele:", kursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print("Studenci:", kursor.execute("SELECT * FROM studenci").fetchall())
print("Audytoria:", kursor.execute("SELECT * FROM audytoria").fetchall())
print("Przypisania:", kursor.execute("SELECT * FROM przypisania").fetchall())

conn.close()
