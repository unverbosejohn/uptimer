import sqlite3

import config

class Database:
    def __init__(self, db_file, schema_file):
        self.conn = None
        
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_schema(schema_file)
        except sqlite3.Error as e:
            print(e)

    def create_schema(self, schema_file):
        with open(schema_file, 'r') as f:
            sql_script = f.read()
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.executescript(sql_script)
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while setting up the database schema: {e}")


    def close(self):
        if self.conn:
            self.conn.close()
