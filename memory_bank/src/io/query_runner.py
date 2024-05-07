import sqlite3
from datetime import datetime

class QueryRunner(object):

    def __init__(self, config):
        self.config = config
        self.database_file_name = "%s\\%s.db" % (
            self.config.get("database_directory"),
            self.config.get("database_name")
        )

    def run_sql(self, sql_str):
        conn = sqlite3.connect(self.database_file_name)
        conn.execute(sql_str)
        conn.commit()

    def fetch_sql(self, sql_str):
        conn = sqlite3.connect(self.database_file_name)
        query = conn.execute(sql_str)
        results = query.fetchall()
        return results

    def create_all_tables(self):
        self.create_memories_table()

    def create_memories_table(self):
        sql_str = "CREATE TABLE memories(date DATE, text VARCHAR, hour INT, minute INT)"
        try:
            self.run_sql(sql_str)
        except sqlite3.OperationalError:
            pass

    def insert_memory(self, memory_text, date=None, hour=None, minute=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if hour and minute is None:
            sql_str = "INSERT INTO memories ('date', 'text') VALUES ('%s', '%s')" % (date, memory_text)
        elif minute is None:
            sql_str = "INSERT INTO memories ('date', 'text', 'hour') VALUES ('%s', '%s', '%s')" % (date, memory_text, hour)
        elif hour is None:
            raise Exception("cannot have a minute without hour")
        else:
            sql_str = "INSERT INTO memories ('date', 'text', 'hour', 'minute') VALUES ('%s', '%s', '%s', '%s')" % (date, memory_text, hour, minute)
        self.run_sql(sql_str)

    def get_memories(self, date=None):
        sql_str = "SELECT * FROM memories"
        if date is not None:
            sql_str += " WHERE date = '%s'" % date
        return self.fetch_sql(sql_str)

    def delete_memory(self, date, text):
        sql_str = "DELETE FROM memories WHERE date = '%s' AND text = '%s'" % (date, text)
        self.run_sql(sql_str)

    def get_memories_matching_search(self, term):
        sql_str = "SELECT * FROM memories WHERE INSTR(text, '%s')" % term
        return self.fetch_sql(sql_str)
