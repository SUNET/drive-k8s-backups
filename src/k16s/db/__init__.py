import mysql.connector

from k16s import Agent


class DB():
    def __init__(self, agent: Agent):
        self.agent = agent
        db_cred = agent.db_creds()
        if not db_cred:
            raise Exception("No database credentials found")

        self.conn = mysql.connector.connect(
            host=db_cred['host'],
            user=db_cred['user'],
            password=db_cred['password'],
            database=db_cred['database']
        )
        self.cursor = self.conn.cursor()
