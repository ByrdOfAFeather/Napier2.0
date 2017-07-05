# TODO setup bot specific ranking (admin) values
import sqlite3


def main():
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('''CREATE TABLE ranks (UserID int, Points int, DailyGuess int)''')
    db.commit()
    db.close()

if __name__ == "__main__": main()