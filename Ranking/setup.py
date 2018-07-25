import sqlite3


def main():
    db = sqlite3.connect('Rankings.db')
    adder = db.cursor()
    adder.execute('''CREATE TABLE servers (ServerID int, Folder text, Question int)''')
    adder.execute('''CREATE TABLE ranks (UserID int, Points int, DailyGuess int, ServerID int)''')
    db.commit()
    db.close()


if __name__ == "__main__": main()