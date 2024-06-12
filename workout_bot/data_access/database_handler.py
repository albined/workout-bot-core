import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_name='workout_database.db') -> None:
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        subscribed BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS Challenges (
                        challenge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        challenge_name TEXT NOT NULL,
                        challenge_basepoints INTEGER NOT NULL,
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        is_bonus BOOLEAN DEFAULT FALSE
                    )
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS Scores (
                        score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        challenge_id INTEGER,
                        score INTEGER NOT NULL,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES Users(user_id),
                        FOREIGN KEY (challenge_id) REFERENCES Challenges(challenge_id)
                    )
                """)

    def drop_tables(self):
        with self.conn:
            self.conn.execute("DROP TABLE IF EXISTS Users")
            self.conn.execute("DROP TABLE IF EXISTS Challenges")
            self.conn.execute("DROP TABLE IF EXISTS Scores")

    def clear_database(self):
        self.drop_tables()
        self.create_tables()

    def get_user_scores_over_time(self, user_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''
                SELECT c.challenge_name, s.score, s.completed_at 
                FROM Scores s 
                JOIN Challenges c ON s.challenge_id = c.challenge_id 
                WHERE s.user_id = ? 
                ORDER BY s.completed_at
            ''', (user_id,))
            return cur.fetchall()
        
    def user_exists(self, username):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''
                SELECT 1 FROM Users WHERE username = ?
            ''', (username,))
            return cur.fetchone() is not None
        
    def add_user(self, username, subscribed):
        if not self.user_exists(username):
            with self.conn:
                self.conn.execute('''
                    INSERT INTO Users (username, subscribed) VALUES (?, ?)
                ''', (username, subscribed))
                return True
        return False
    
    def set_user_subscription(self, username, subscribed):
        with self.conn:
            self.conn.execute('''
                UPDATE Users SET subscribed = ? WHERE username = ?
            ''', (subscribed, username))

    def get_subscribed_users(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''
                SELECT username FROM Users WHERE subscribed = TRUE
            ''')
            return cur.fetchall()
        
    def add_challenge(self, challenge_name, challenge_basepoints, date, time, is_bonus):
        with self.conn:
            self.conn.execute('''
                INSERT INTO Challenges (challenge_name, challenge_basepoints, date, time, is_bonus) VALUES (?, ?, ?, ?, ?)
            ''', (challenge_name, challenge_basepoints, date, time, is_bonus))

    def get_challenge_by_date(self, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''
                SELECT * FROM Challenges WHERE date = ?
            ''', (date,))
            return cur.fetchall()
        
    def list_challenges_completed_by_user(self, user_id, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''
                SELECT c.challenge_name, s.score, s.completed_at 
                FROM Scores s
                JOIN Challenges c ON s.challenge_id = c.challenge_id
                WHERE s.user_id = ? AND DATE(s.completed_at) = ?
                ORDER BY s.completed_at
            ''', (user_id, date))
            return cur.fetchall()

    def add_score_for_user(self, user_id, challenge_id, score, completed_at=None):
        if completed_at is None:
            completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self.conn:
            self.conn.execute('''
                INSERT INTO Scores (user_id, challenge_id, score, completed_at) VALUES (?, ?, ?, ?)
            ''', (user_id, challenge_id, score, completed_at))
