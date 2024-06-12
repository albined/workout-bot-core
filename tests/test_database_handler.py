import unittest
import sqlite3
from datetime import datetime
from unittest.mock import patch
from workout_bot.data_access.database_handler import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.db_handler = DatabaseHandler(':memory:')

    def tearDown(self):
        self.db_handler.conn.close()

    def test_create_tables(self):
        # Verify that tables are created
        tables = ['Users', 'Challenges', 'Scores']
        for table in tables:
            with self.db_handler.conn:
                cur = self.db_handler.conn.cursor()
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
                self.assertIsNotNone(cur.fetchone())

    def test_add_user_and_user_exists(self):
        username = 'testuser'
        subscribed = True
        
        self.assertFalse(self.db_handler.user_exists(username))
        
        self.db_handler.add_user(username, subscribed)
        self.assertTrue(self.db_handler.user_exists(username))

    def test_add_user_duplicate(self):
        username = 'testuser'
        subscribed = True
        
        self.assertTrue(self.db_handler.add_user(username, subscribed))
        self.assertFalse(self.db_handler.add_user(username, subscribed))  # Should not add duplicate

    def test_set_user_subscription(self):
        username = 'testuser'
        subscribed = True
        self.db_handler.add_user(username, subscribed)
        
        self.db_handler.set_user_subscription(username, False)
        
        with self.db_handler.conn:
            cur = self.db_handler.conn.cursor()
            cur.execute("SELECT subscribed FROM Users WHERE username = ?", (username,))
            self.assertFalse(cur.fetchone()[0])

    def test_get_subscribed_users(self):
        usernames = ['user1', 'user2', 'user3']
        for username in usernames:
            self.db_handler.add_user(username, True)

        unsubscribed_user = 'user4'
        self.db_handler.add_user(unsubscribed_user, False)

        subscribed_users = self.db_handler.get_subscribed_users()
        self.assertEqual(len(subscribed_users), 3)
        self.assertTrue(all(user[0] in usernames for user in subscribed_users))

    def test_add_challenge(self):
        challenge_name = 'challenge1'
        challenge_basepoints = 100
        date = '2024-06-11'
        is_bonus = False

        self.db_handler.add_challenge(challenge_name, challenge_basepoints, date, is_bonus)
        
        with self.db_handler.conn:
            cur = self.db_handler.conn.cursor()
            cur.execute("SELECT * FROM Challenges WHERE challenge_name = ?", (challenge_name,))
            self.assertIsNotNone(cur.fetchone())

    def test_get_challenge_by_date(self):
        challenge_name = 'challenge1'
        challenge_basepoints = 100
        date = '2024-06-11'
        is_bonus = False

        self.db_handler.add_challenge(challenge_name, challenge_basepoints, date, is_bonus)

        challenges = self.db_handler.get_challenge_by_date(date)
        self.assertEqual(len(challenges), 1)
        self.assertEqual(challenges[0][1], challenge_name)

    def test_add_score_for_user_and_list_challenges_completed_by_user(self):
        username = 'testuser'
        self.db_handler.add_user(username, True)
        
        challenge_name = 'challenge1'
        challenge_basepoints = 100
        date = '2024-06-11'
        is_bonus = False
        self.db_handler.add_challenge(challenge_name, challenge_basepoints, date, is_bonus)
        
        with self.db_handler.conn:
            cur = self.db_handler.conn.cursor()
            cur.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
            user_id = cur.fetchone()[0]
            cur.execute("SELECT challenge_id FROM Challenges WHERE challenge_name = ?", (challenge_name,))
            challenge_id = cur.fetchone()[0]

        score = 50
        self.db_handler.add_score_for_user(user_id, challenge_id, score)

        completed_challenges = self.db_handler.list_challenges_completed_by_user(user_id, date)
        self.assertEqual(len(completed_challenges), 1)
        self.assertEqual(completed_challenges[0][0], challenge_name)
        self.assertEqual(completed_challenges[0][1], score)

if __name__ == '__main__':
    unittest.main()
