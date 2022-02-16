import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types

import config


class SQLighter:
    def __init__(self, database_file):
        """connect to db and save the connection"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subsctioptions(self, status=True):
        """Get all active subs"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subs` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Is it in the base"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subs` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            return self.cursor.execute("INSERT INTO `subs` (`user_id`, `status`) VALUES (?, ?)",
                                       (user_id, status)).fetchall()

    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `subs` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        self.connection.close()
