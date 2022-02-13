
import sqlite3
from pobieranie_danych import pobierz_dane

# utworzenie połączenia z bazą przechowywaną na dysku
# lub w pamięci (':memory:')
con = sqlite3.connect('test.db')

# dostęp do kolumn przez indeksy i przez nazwy
con.row_factory = sqlite3.Row

# utworzenie obiektu kursora
cur = con.cursor()

# tworzenie tabel
cur.execute("DROP TABLE IF EXISTS klasa;")

cur.execute("""
    CREATE TABLE IF NOT EXISTS klasa (
        id INTEGER PRIMARY KEY ASC,
        nazwa varchar(250) NOT NULL,
        profil varchar(250) DEFAULT ''
    )""")

cur.executescript("""
    DROP TABLE IF EXISTS uczen;
    CREATE TABLE IF NOT EXISTS uczen (
        id INTEGER PRIMARY KEY ASC,
        imie varchar(250) NOT NULL,
        nazwisko varchar(250) NOT NULL,
        klasa_id INTEGER NOT NULL,
        FOREIGN KEY(klasa_id) REFERENCES klasa(id)
    )""")

# wstawiamy jeden rekor danych
cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);', ('1A', 'matematyczny'))
cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);', ('1B', 'humanistyczny'))

# wykonujemy zapytanie SQL, które pobierze id klasy "1A" z tabeli "klasa"
cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('1A',))
klasa_id = cur.fetchone()[0]

# tupla "uczniowie" zawiera tuple z danymi poszczególnych uczniów
uczniowie = (
    (None, 'Tomasz', 'Nowak', klasa_id),
    (None, 'Jan', 'Kos', klasa_id),
    (None, 'Piotr', 'Kowalski', klasa_id)
)

# wstawiamy wiele rekordow
cur.executemany('INSERT INTO uczen VALUES(?,?,?,?)', uczniowie)

# zatwierdzamy zmiany w bazie
con.commit()

# pobieranie danych z bazy danych
def czytajdane():
    """Funkcja pobiera i wyświetla dane z bazy."""
    cur.execute(
        """
        SELECT uczen.id, imie,nazwisko,nazwa FROM uczen,klasa
        WHERE uczen.klasa_id=klasa.id
        """)
    uczniowie = cur.fetchall()
    for uczen in uczniowie:
        print(uczen['id'], uczen['imie'], uczen['nazwisko'], uczen['nazwa'])
    print()

# zmiana klasy ucznia o identyfikatorze 2
cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('1B',))
klasa_id = cur.fetchone()[0]
cur.execute('UPDATE uczen SET klasa_id=? WHERE id=?', (klasa_id, 2))

# usunięcie ucznia o identyfikatorze 3
cur.execute('DELETE FROM uczen WHERE id=?', (3,))

czytajdane()

dane_plik = pobierz_dane('C:\\Users\\Marcin\\Documents\\Python\\bazy danych\\uczniowie.csv')

cur.executemany(
    'INSERT INTO uczen (imie,nazwisko,klasa_id) VALUES(?,?,?)', dane_plik)



while True:
    print("1. Wypisanie rekordów znajdujących się w bazie danych")
    print("2. Dodanie rekordu do bazy danych ")
    print("3. Zmodyfikowanie rekordów w bazie danych")
    print("4. Usunięcie rekordu z bazy")
    print("5. Koniec programu")
    menu = str(input("Podaj cyfrę z menu, aby wybrać co chcesz zrobić: "))

    if menu == "1":
        czytajdane()

    elif menu == "2":
        rekord = input("Po przecinku podaj dane do dodania do bazy ")
        print()
        rekord = tuple(map(str, rekord.split(", ")))
        print(rekord)
        print()
        cur.execute('INSERT INTO uczen VALUES(NULL,?,?,?)', rekord)

    elif menu == "3":
        while True:
            print("Menu modyfikacji rekordu:")
            print("1. Zmiana imienia")
            print("2. Zmiana nazwiska")
            print("3. Zmiana klasy")
            print("4. Wyjście z menu modyfikacji rekordu")

            modd = str(input("Co chcesz zrobić? "))

            if modd == "1":
                new_name = str(input("Podaj nowe imie "))
                index = int(input("Podaj numer rekordu ucznia do zmiany imienia: "))
                cur.execute('UPDATE uczen SET imie=? WHERE id=?', (new_name, index,))

            elif modd == "2":
                new_name = str(input("Podaj nowe nazwisko "))
                index = int(input("Podaj numer rekordu ucznia do zmiany nazwiska: "))
                cur.execute('UPDATE uczen SET nazwisko=? WHERE id=?', (new_name, index,))

            elif modd == "3":
                new_name = str(input("Podaj nowa klase "))
                index = int(input("Podaj numer rekordu ucznia do zmiany klasy: "))
                cur.execute("SELECT id FROM klasa WHERE nazwa=?", (new_name,))
                id_klasy = cur.fetchone()[0]
                cur.execute('UPDATE uczen SET klasa_id=? WHERE id=?', (id_klasy, index,))

            elif modd == "4":
                break
            break
    elif menu == "4":
        indeks = input("Podaj indeks ucznia do usuniecia: ")
        cur.execute('DELETE FROM uczen WHERE id=?', (indeks))
    elif menu == "5":
        print("Koniec programu!!!")
        cur.close()
        exit()
    else:
        print("Błąd danych!! Podaj poprawne dane!")

