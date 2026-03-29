import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name = "sah_p2p.db"):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sah_p2p.db")
        self.createTables()

    def getConnection(self):
        return sqlite3.connect(self.db_path)

    def createTables(self):
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Jucatori (
            Username TEXT PRIMARY KEY,
            Password TEXT NOT NULL,
            ScorTotal REAL DEFAULT 0.0
             )
        ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS IstoricMeciuri (
            Jucator1 TEXT,
            Jucator2 TEXT,
            VictoriiJ1 INTEGER DEFAULT 0,
            VictoriiJ2 INTEGER DEFAULT 0,
            Remize INTEGER DEFAULT 0,
            PRIMARY KEY (Jucator1, Jucator2)
            )
                       ''')

        conn.commit()
        conn.close()

    def registerUser(self, username, password):
        conn = self.getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Jucatori (Username, Password) VALUES (?, ?)''', (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Eroare la inregistrare {e}")
            return False
        finally:
            conn.close()

    def loginUser(self, username, password):
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Jucatori WHERE Username = ? AND Password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def getPlayerScore(self, username):
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute('''SELECT ScorTotal FROM Jucatori WHERE Username = ?''', (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0]
        return 0.0

    def getRivalScore(self, player1, player2):
        conn = self.getConnection()
        cursor = conn.cursor()
        p1, p2 =sorted([player1, player2])
        cursor.execute("SELECT VictoriiJ1, VictoriiJ2, Remize FROM IstoricMeciuri"
                       " WHERE Jucator1 = ? AND Jucator2 = ?", (p1, p2))
        row = cursor.fetchone()
        conn.close()

        if row:
            v1, v2, remize = row
            return f"Scor: {p1}\t{v1 + 0.5 * remize} - {v2 + 0.5 * remize}\t{p2}"
        else:
            return f"Scor: {p1}\t0 - 0\t{p2}"

    def updateResult(self, player1, player2, winner):
        conn = self.getConnection()
        cursor = conn.cursor()

        # p1 și p2 sunt numele sortate alfabetic!
        p1, p2 = sorted([player1, player2])

        cursor.execute("SELECT * FROM IstoricMeciuri WHERE Jucator1 = ? AND Jucator2 = ?", (p1, p2))
        meci = cursor.fetchone()

        # AICI ERA GREȘEALA: Trebuie să comparăm cu p1 și p2!
        v1_add = 1 if winner == p1 else 0
        v2_add = 1 if winner == p2 else 0
        rem_add = 1 if winner == "Remiza" else 0

        if meci is None:
            cursor.execute('''INSERT INTO IstoricMeciuri
                           (Jucator1, Jucator2, VictoriiJ1, VictoriiJ2, Remize)
                           VALUES(?, ?, ?, ?, ?)''',
                           (p1, p2, v1_add, v2_add, rem_add))
        else:
            # ȘI AICI: Folosim p1 și p2!
            if winner == p1:
                cursor.execute('''UPDATE IstoricMeciuri SET VictoriiJ1 = VictoriiJ1 + 1
                               WHERE Jucator1 = ? AND Jucator2 = ?''', (p1, p2))
            elif winner == p2:
                cursor.execute('''UPDATE IstoricMeciuri SET VictoriiJ2 = VictoriiJ2 + 1
                               WHERE Jucator1 = ? AND Jucator2 = ?''', (p1, p2))
            elif winner == "Remiza":
                cursor.execute('''UPDATE IstoricMeciuri SET Remize = Remize + 1
                               WHERE Jucator1 = ? AND Jucator2 = ?''', (p1, p2))

        if winner == "Remiza":
            cursor.execute('''UPDATE Jucatori SET ScorTotal = ScorTotal + 0.5
                           WHERE Username IN (?, ?)''', (p1, p2))
        else:
            cursor.execute('''UPDATE Jucatori SET ScorTotal = ScorTotal + 1
                          WHERE Username = ?''', (winner,))

        conn.commit()
        conn.close()

